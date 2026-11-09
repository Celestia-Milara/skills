"""Exercise real TLC and installed Windows statechart entries without model calls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from install import HOST_ROOTS, install


ROOT = Path(__file__).resolve().parents[1]


def wait_for(predicate, seconds=15):
    deadline = time.monotonic() + seconds
    while not predicate():
        if time.monotonic() >= deadline:
            raise TimeoutError('Statechart acceptance condition did not arrive')
        time.sleep(.025)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--tlc', required=True, type=Path)
    parser.add_argument('--java')
    args = parser.parse_args()
    if os.name != 'nt':
        parser.error('This acceptance runner requires Windows')
    base = args.output.resolve()
    base.mkdir(parents=True, exist_ok=False)
    summary = {'cases': [], 'model_calls': 0}
    env = {**os.environ, 'TLA2TOOLS': str(args.tlc.resolve())}
    if args.java:
        env['JAVA'] = args.java
    corpus = ROOT / 'pstack/skills/statechart/scripts/test/corpus'

    def run(name, command, expected, out=None):
        result = subprocess.run(command, env=env, capture_output=True, timeout=90)
        (base / (name + '.stdout')).write_bytes(result.stdout)
        (base / (name + '.stderr')).write_bytes(result.stderr)
        if result.returncode != expected:
            raise AssertionError(f'{name}: expected {expected}, got {result.returncode}: {result.stderr.decode("utf-8", "replace")}')
        receipt = json.loads((base / (name + '-evidence/receipt.json')).read_text()) if (base / (name + '-evidence/receipt.json')).exists() else None
        if receipt and (not receipt['cleanup']['confirmed'] or not receipt['finalized']):
            raise AssertionError(f'{name}: cleanup not confirmed')
        summary['cases'].append({'name': name, 'exit': result.returncode, 'receipt': receipt,
                                 'output_exists': out.exists() if out else None})
        print(name, 'PASS', flush=True)
        return result

    installed = []
    for host, storage in [('codex', 'copy'), ('claude-code', 'copy'), ('pi', 'copy'), ('codex', 'junction')]:
        label = host + '-' + storage
        home = base / label
        record = install(host, None, scope='user', home=str(home), storage=storage,
                         store=str(base / 'store') if storage == 'junction' else None)
        host_root = home / ('.codex' if host == 'codex' else HOST_ROOTS[host])
        command = [sys.executable, '-B', str(host_root / 'pstack/adapters/platforms/runtime.py'),
                   'run', '--skills-root', str(host_root / 'skills'), 'statechart']
        installed.append((host_root, command))
        for fixture, expected in [('Login', 0), ('MediaPlayer', 1)]:
            name = label + '-' + fixture
            out = base / (name + '-output')
            run(name, [*command, str(corpus / fixture / (fixture + '.tla')),
                       '--view', str(corpus / fixture / 'view.mjs'), '--out', str(out),
                       '--evidence', str(base / (name + '-evidence')), '--timeout-seconds', '60'], expected, out)
            for file in ['report.md', 'chart.mmd']:
                if (out / file).read_text(encoding='utf-8') != (corpus / fixture / file).read_text(encoding='utf-8'):
                    raise AssertionError(f'{name}: {file} differs from the committed upstream expected result')
            for file in out.glob('tlc*.out'):
                text = file.read_bytes()
                if b'\r' in text or b'Picked up JAVA_TOOL_OPTIONS' in text:
                    raise AssertionError(f'{name}: TLC output contains platform-injected text or CR')
    host_root, command = installed[0]
    unicode_out = base / '\u8def\u5f84 & \u7a7a\u683c' / 'out'
    env['PYTHONIOENCODING'] = 'ascii'
    result = run('unicode-output', [*command, str(corpus / 'MediaPlayer/MediaPlayer.tla'),
                                   '--view', str(corpus / 'MediaPlayer/view.mjs'), '--out', str(unicode_out),
                                   '--evidence', str(base / 'unicode-output-evidence')], 1, unicode_out)
    if str(unicode_out) not in result.stdout.decode('utf-8'):
        raise AssertionError('Unicode output path was not reported as UTF-8')
    env.pop('PYTHONIOENCODING')
    bad = base / 'Bad.tla'
    bad.write_text('---- MODULE Bad ----\nINVALID INPUT\n====\n')
    bad.with_suffix('.cfg').write_text('INIT Init\nNEXT Next\n')
    out = base / 'bad-output'
    run('invalid-spec', [*command, str(bad), '--out', str(out), '--evidence', str(base / 'invalid-spec-evidence')], 2, out)
    if out.exists():
        raise AssertionError('Invalid input published output')
    endless = base / 'Endless.tla'
    endless.write_text('---- MODULE Endless ----\nEXTENDS Naturals\nVARIABLE x\nInit == x = 0\nNext == x\' = x + 1\n====\n')
    endless.with_suffix('.cfg').write_text('INIT Init\nNEXT Next\nCHECK_DEADLOCK FALSE\n')
    out = base / 'timeout-output'
    run('timeout', [*command, str(endless), '--out', str(out), '--evidence', str(base / 'timeout-evidence'), '--timeout-seconds', '3'], 2, out)
    if out.exists():
        raise AssertionError('Timed-out check published output')
    evidence = base / 'parent-death-evidence'
    with (base / 'parent-death.stdout').open('wb') as stdout, (base / 'parent-death.stderr').open('wb') as stderr:
        process = subprocess.Popen([*command, str(endless), '--out', str(base / 'parent-death-output'),
                                    '--evidence', str(evidence)], env=env, stdout=stdout, stderr=stderr)
        try:
            wait_for(lambda: (evidence / 'startup.json').exists())
            time.sleep(.8)
            process.kill()
            process.wait(timeout=10)
            def finalized():
                try:
                    return json.loads((evidence / 'receipt.json').read_text()).get('finalized')
                except (OSError, ValueError):
                    return False
            wait_for(finalized)
            receipt = json.loads((evidence / 'receipt.json').read_text())
            if receipt['status'] != 'parent-eof' or not receipt['cleanup']['confirmed'] or (base / 'parent-death-output').exists():
                raise AssertionError('Launcher death did not abandon the contained check')
            wait_for(lambda: not list(base.glob('.parent-death-output.statechart-*')))
            summary['cases'].append({'name': 'parent-death', 'receipt': receipt, 'output_exists': False})
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=10)
    source_paths = ['adapters/platforms/statechart.py', 'adapters/platforms/statechart_java.mjs', 'adapters/platforms/windows_job.py',
                    'adapters/platforms/runtime.py', 'adapters/platforms/manifest.json']
    summary['source_sha256'] = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in source_paths}
    summary['upstream_files'] = len(json.loads((ROOT / 'source-lock.json').read_text())['upstream']['files'])
    (base / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print('PASS:', len(summary['cases']), 'cases; no model calls or active installations changed')


if __name__ == '__main__':
    main()
