"""Run bounded native-host composition cases in disposable projects.

Uses the current host account without changing its settings or installed skills.
Raw host logs stay in the requested local output directory; do not publish them.
Artifact checks are necessary evidence, not a substitute for reviewing tool events.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from install import install


CASES = {
    'design': ('architect',
               'Propose the technical design for the timeout behavior in docs/timeout.md. '
               'Update that existing design if needed. This is design-only; do not edit code or tests.'),
    'implement': ('poteto-mode',
                  'I approve the design in docs/timeout.md and authorize its implementation now. '
                  'Fix settings.py and verify the behavior. Keep the existing design and work plan '
                  'accurate. Do not ask me to approve the same design again.'),
    'plan': ('poteto-mode',
             'Update docs/work.md with a proportionate two-phase plan to implement the agreed '
             'timeout design, then document and verify it. Planning only; do not implement. '
             'This is an ordinary local change, not a multi-PR program.'),
}
DESIGN = '''# Timeout design

Approved behavior: omitted timeout defaults to 30; numeric zero disables the
timeout and remains zero; a positive integer remains unchanged.
Keep the existing settings.timeout(options) API. No new dependencies.

Acceptance: demonstrate omitted, zero, and positive input through that API.
'''
PLAN = '''# Timeout work

Status: planned

Design: [Timeout design](timeout.md).

- [ ] Correct numeric zero without changing omitted or positive values.
- [ ] Verify all three observable cases and update this plan with the evidence.
'''
CODE = 'def timeout(options):\n    return int(options.get("timeout") or 30)\n'
TESTS = '''import unittest
from settings import timeout

class TimeoutTests(unittest.TestCase):
    def test_default(self):
        self.assertEqual(timeout({}), 30)

    def test_positive(self):
        self.assertEqual(timeout({"timeout": 12}), 12)
'''


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')


def prepare(host, output, case):
    fixture = Path(tempfile.mkdtemp(prefix=f'pstack-compose-{host}-{case}-'))
    install(host, fixture)
    subprocess.run(['git', 'init', '-q', str(fixture)], check=True)
    write(fixture / 'settings.py', CODE)
    write(fixture / 'test_settings.py', TESTS)
    write(fixture / 'docs/timeout.md', DESIGN)
    write(fixture / 'docs/work.md', PLAN)
    write(fixture / '.agents/notes/timeout-policy.md',
          '# Keep zero explicit\n\nStatus: active\nScope: timeout parsing.\n\n'
          'Zero disables the timeout. Keep the public function and default 30. '
          'A previous truthiness fallback conflated zero with an omitted option.\n')
    folder = '.agents' if host == 'codex' else '.claude'
    name, request = CASES[case]
    entry = fixture / folder / 'skills' / name / 'SKILL.md'
    prompt = (f'Use {"$" if host == "codex" else "/"}{name} from {entry.as_posix()}. '
              f'{request} Work only in this fixture. Use its project-local skill files. '
              'Do not delegate, commit, stage, push, create a PR, send messages, access other '
              'projects or change host settings. Reply in plain text. Run only local checks.')
    write(output / f'{case}-prompt.txt', prompt)
    return fixture, prompt


def command(host, fixture, prompt):
    executable = shutil.which('codex' if host == 'codex' else 'claude')
    if not executable:
        raise FileNotFoundError(f'{host} executable is unavailable')
    if host == 'codex':
        return [executable, 'exec', '--json', '--ephemeral',
                '--skip-git-repo-check', '-C', str(fixture), '-s', 'workspace-write', prompt]
    shim = Path(executable)
    if shim.suffix.lower() in ('.cmd', '.ps1'):
        package = shim.parent / 'node_modules/@anthropic-ai/claude-code'
        metadata = json.loads((package / 'package.json').read_text(encoding='utf-8'))
        entry = package / metadata['bin']['claude']
        cmd = [shutil.which('node'), str(entry)] if entry.suffix in ('.js', '.mjs', '.cjs') else [str(entry)]
    else:
        cmd = [str(shim)]
    return cmd + ['--print', prompt, '--output-format', 'stream-json', '--verbose',
                  '--no-session-persistence', '--permission-mode', 'manual',
                  '--allowedTools', 'Read,Glob,Grep,Bash,Write,Edit,Skill',
                  '--tools', 'Read,Glob,Grep,Bash,Write,Edit,Skill']


def check(fixture, case):
    head = subprocess.run(['git', 'rev-parse', '--verify', 'HEAD'], cwd=fixture, capture_output=True)
    index = subprocess.check_output(['git', 'ls-files', '--stage'], cwd=fixture, text=True)
    checks = {'no_commit': head.returncode != 0, 'no_staging': not index.strip()}
    docs = sorted(p.relative_to(fixture).as_posix() for p in (fixture / 'docs').rglob('*.md'))
    checks['existing_document_paths'] = docs == ['docs/timeout.md', 'docs/work.md']
    if case == 'implement':
        probe = subprocess.run([sys.executable, '-c',
            'from settings import timeout; assert timeout({}) == 30; '
            'assert timeout({"timeout": 0}) == 0; assert timeout({"timeout": 12}) == 12; '
            'print("omitted=30 zero=0 positive=12")'], cwd=fixture, capture_output=True, text=True)
        suite = subprocess.run([sys.executable, '-m', 'unittest', '-v'], cwd=fixture,
                               capture_output=True, text=True)
        checks['observable_contract'] = probe.returncode == 0
        checks['fixture_tests'] = suite.returncode == 0
        compatibility = subprocess.run([sys.executable, '-c',
            'from settings import timeout; '
            'assert all(timeout({"timeout": v}) == 30 for v in (None, False, "")); '
            'print("unapproved None/False/empty-string behavior retained")'],
            cwd=fixture, capture_output=True, text=True)
        checks['unapproved_inputs_preserved'] = compatibility.returncode == 0
        checks['existing_plan_updated'] = (fixture / 'docs/work.md').read_text(encoding='utf-8') != PLAN
        evidence = (probe.stdout + probe.stderr + suite.stdout + suite.stderr
                    + compatibility.stdout + compatibility.stderr)
    else:
        checks['code_unchanged'] = (fixture / 'settings.py').read_text(encoding='utf-8') == CODE
        checks['tests_unchanged'] = (fixture / 'test_settings.py').read_text(encoding='utf-8') == TESTS
        checks['design_retained'] = (fixture / 'docs/timeout.md').is_file()
        if case == 'plan':
            checks['existing_plan_updated'] = (fixture / 'docs/work.md').read_text(encoding='utf-8') != PLAN
        evidence = ''
    return checks, evidence


def run(host, output, case, timeout):
    fixture, prompt = prepare(host, output, case)
    folder = '.agents' if host == 'codex' else '.claude'
    source = fixture / folder / 'pstack/BUNDLE.json'
    version = hashlib.sha256(source.read_bytes()).hexdigest()
    write(output / f'{case}-fixture.json', json.dumps({'fixture': str(fixture), 'bundle_sha256': version}, indent=2))
    timed_out = False
    with (output / f'{case}.jsonl').open('w', encoding='utf-8') as stdout, \
            (output / f'{case}.stderr').open('w', encoding='utf-8') as stderr:
        try:
            result = subprocess.run(command(host, fixture, prompt), cwd=fixture, stdout=stdout,
                                    stderr=stderr, timeout=timeout,
                                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            timed_out, exit_code = True, None
    checks, evidence = check(fixture, case)
    write(output / f'{case}-postcheck.txt', evidence)
    record = {'host': host, 'case': case, 'fixture': str(fixture), 'bundle_sha256': version,
              'exit_code': exit_code, 'timed_out': timed_out, 'artifact_checks': checks,
              'needs_event_review': True}
    write(output / f'{case}-result.json', json.dumps(record, indent=2))
    print(json.dumps(record), flush=True)
    return exit_code == 0 and all(checks.values())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=['codex', 'claude-code'], required=True)
    parser.add_argument('--case', choices=[*CASES, 'all'], default='all')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--timeout', type=int, default=300)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    cases = CASES if args.case == 'all' else [args.case]
    results = [run(args.host, args.output, case, args.timeout) for case in cases]
    raise SystemExit(0 if all(results) else 1)
