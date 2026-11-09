"""Run the unchanged statechart worker inside a native Windows Job."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import queue
import re
import shutil
import subprocess
import sys
import threading
import uuid


HERE = Path(__file__).resolve().parent
TLC_SHA256 = '936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88'


def dependencies(java=None, tlc=None, node=None):
    from runtime import statechart_dependencies
    node, java, tlc = statechart_dependencies(java, tlc, node)
    if not java or not node or not tlc.is_file():
        raise ValueError('Statechart requires Node 22.18-22.x or 23.6+, Java 11+ and TLC 1.7.4. '
                         'Set JAVA/TLA2TOOLS or pass --java/--tlc. Nothing was installed.')
    if hashlib.sha256(tlc.read_bytes()).hexdigest() != TLC_SHA256:
        raise ValueError('TLC jar differs from pinned TLC 1.7.4')
    env = {'JAVA': str(Path(java).resolve()), 'TLA2TOOLS': str(tlc.resolve())}
    for command, label in [([node, '--version'], 'Node'), ([java, '-Dline.separator=\n', '-version'], 'Java')]:
        probe = subprocess.run(command, capture_output=True, timeout=15, env={**os.environ, **env},
                               creationflags=subprocess.CREATE_NO_WINDOW)
        if probe.returncode:
            raise ValueError(f'{label} cannot run: {probe.stderr.decode("utf-8", "replace").strip()}')
        text = (probe.stdout + probe.stderr).decode('utf-8', 'replace')
        version = re.search(r'^v(\d+)\.(\d+)', text) if label == 'Node' else re.search(r'^(?:openjdk|java) version "(\d+)(?:\.(\d+))?', text, re.M)
        supported = False
        if version:
            major, minor = int(version[1]), int(version[2] or 0)
            supported = ((major == 22 and minor >= 18) or (major, minor) >= (23, 6)) if label == 'Node' else major >= 11
        if not supported:
            raise ValueError(f'Unsupported {label} version: {text}')
        if label == 'Java' and b'\r\n' in probe.stdout + probe.stderr:
            raise ValueError('Java did not honor LF output; remove conflicting JVM line.separator options')
    return str(Path(node).resolve()), env


def private_worker(skills_root):
    from runtime import BUNDLE, validate
    record = validate()
    root = Path(skills_root).resolve()
    if (root == (BUNDLE / 'skills').resolve() or root == (BUNDLE / 'pstack/skills').resolve()
            or any((root.parent / marker).is_file() for marker in ['BUNDLE.json', 'plugin.json', '.cursor-plugin/plugin.json'])):
        raise ValueError('Use private host entries, not the public resource bundle')
    for relative, expected in record['tools']['statechart']['sources'].items():
        file = root / relative.removeprefix('skills/')
        if not file.resolve().is_relative_to(root) or hashlib.sha256(file.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Private statechart source differs from pinned mapping: {relative}')
    return root / 'statechart/scripts/worker.ts'


def output_path(out):
    out = Path(out)
    if os.path.lexists(out) and not out.exists():
        raise ValueError(f'{out} is a broken link; use a new or empty output folder')
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError(f'{out} is not an empty folder; the command wrote nothing')
    return out.resolve()


def directory_identity(path):
    if not os.path.lexists(path):
        return None
    info = path.lstat()
    if getattr(info, 'st_file_attributes', 0) & 0x400:
        raise FileExistsError(f'Output became a reparse point during the check: {path}')
    return info.st_dev, info.st_ino


def publish(done, dest, expected=None):
    if directory_identity(dest) != expected:
        raise FileExistsError(f'Output changed during the check; preserved {dest}')
    removed = False
    if dest.exists():
        dest.rmdir()
        removed = True
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        os.rename(done, dest)
    except OSError:
        if removed:
            dest.mkdir(exist_ok=True)
        raise


def forward(file, stream):
    if file.is_file():
        stream.flush()
        with file.open('rb') as source:
            shutil.copyfileobj(source, stream.buffer)
        stream.flush()


def run(args):
    if os.name != 'nt':
        raise ValueError('This adapter requires Windows; use the official POSIX entry on other platforms')
    spec = Path(args.spec).resolve()
    config = Path(args.config).resolve() if args.config else spec.with_suffix('.cfg')
    if not config.is_file():
        raise ValueError(f'Cannot find the TLC config {config}. Pass --config FILE.')
    if not spec.is_file():
        raise ValueError(f'Cannot find the TLA+ spec {spec}')
    dest = output_path(args.out or spec.with_suffix('').with_name(spec.stem + '-chart'))
    original_output = directory_identity(dest)
    evidence = Path(args.evidence).resolve() if args.evidence else None
    if evidence and (evidence.is_relative_to(dest) or dest.is_relative_to(evidence)):
        raise ValueError('--evidence must be a new directory outside the output folder')
    worker = private_worker(args.skills_root)
    node, env = dependencies(args.java, args.tlc, args.node)
    base = dest.parent
    while not base.exists():
        base = base.parent
    owned = base / ('.' + dest.name + '.statechart-' + uuid.uuid4().hex)
    owned.mkdir()
    stage, temp = owned / 'stage', owned / 'temp'
    stage.mkdir()
    temp.mkdir()
    evidence = evidence or owned / 'evidence'
    try:
        evidence.mkdir(parents=True, exist_ok=False)
    except OSError:
        shutil.rmtree(owned)
        raise
    request = dict(schema=1, runId=uuid.uuid4().hex, cwd=os.getcwd(), evidenceDir=str(evidence),
                   argv=[node, '--disable-warning=ExperimentalWarning', '--import',
                         (HERE / 'statechart_java.mjs').as_uri(), str(worker), str(stage), str(spec), str(config),
                         *([str(Path(args.view).resolve())] if args.view else [])],
                   env={**env, 'TMPDIR': str(temp), 'TMP': str(temp), 'TEMP': str(temp)},
                   cleanupDirs=[str(stage), str(temp)], timeoutMs=args.timeout_seconds * 1000,
                   prepareCleanupDirs=[str(temp)], stageDir=str(stage),
                   abandonDir=str(owned))
    receipt_file = evidence / 'receipt.json'
    proc = None
    code = 2
    interrupted = False
    published = False
    try:
        proc = subprocess.Popen([sys.executable, '-I', '-B', str(HERE / 'windows_job.py')],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
        proc.stdin.write((json.dumps(request) + '\n').encode())
        proc.stdin.flush()
        received = queue.Queue()
        threading.Thread(target=lambda: received.put(proc.stdout.readline(65537)), daemon=True).start()
        while True:
            try:
                raw = received.get(timeout=.1)
                break
            except queue.Empty:
                pass
        if len(raw) > 65536:
            raise ValueError('Windows Job returned an oversized receipt')
        if not raw:
            raise ValueError('Windows Job did not confirm completion: ' + proc.stderr.read().decode('utf-8', 'replace'))
        receipt = json.loads(raw)
        if receipt.get('schema') != 1 or receipt.get('runId') != request['runId'] or not receipt.get('cleanup', {}).get('confirmed') or receipt['cleanup'].get('activeProcesses') != 0:
            raise ValueError('Windows Job did not confirm process-tree cleanup')
        forward(evidence / 'worker.stdout', sys.stdout)
        forward(evidence / 'worker.stderr', sys.stderr)
        done = stage / 'done'
        if receipt['status'] == 'exited' and receipt['exitCode'] in (0, 1) and receipt.get('prepared') and done.is_dir():
            publish(done, dest, original_output)
            published = True
            code = receipt['exitCode']
            sys.stdout.write((dest / 'report.md').read_text(encoding='utf-8'))
            print(f'\nWrote {dest}')
        else:
            print(f"Statechart stopped: {receipt['status']}. {receipt.get('error', receipt.get('pathCleanupErrors', ''))}", file=sys.stderr)
    except KeyboardInterrupt:
        interrupted = True
        code = 130
        print('Interrupted after publishing output.' if published else 'Interrupted the check; no output was published.', file=sys.stderr)
    finally:
        try:
            if proc:
                if proc.poll() is None:
                    try:
                        proc.stdin.write(b'{"op":"cancel"}\n{"op":"finish"}\n')
                        proc.stdin.flush()
                    except (BrokenPipeError, OSError):
                        pass
                _, errors = proc.communicate()
                if proc.returncode != 0 or not receipt_file.is_file() or not json.loads(receipt_file.read_text()).get('finalized'):
                    detail = json.loads(receipt_file.read_text()).get('pathCleanupErrors', []) if receipt_file.is_file() else []
                    raise ValueError(f'Windows Job cleanup failed; inspect {evidence}: {detail} {errors.decode("utf-8", "replace")}')
            shutil.rmtree(owned)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            if not published:
                raise
            print(f'Output is complete; retained temporary files at {owned}: {error}', file=sys.stderr)
    return 130 if interrupted else code


def main(argv=None):
    for stream in [sys.stdout, sys.stderr]:
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--skills-root', required=True, type=Path)
    parser.add_argument('spec')
    for name in ['config', 'view', 'out', 'java', 'tlc', 'node', 'evidence']:
        parser.add_argument('--' + name)
    parser.add_argument('--timeout-seconds', type=float, default=0)
    args = parser.parse_args(argv)
    try:
        if not math.isfinite(args.timeout_seconds) or args.timeout_seconds < 0:
            raise ValueError('--timeout-seconds must be finite and nonnegative')
        return run(args)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
