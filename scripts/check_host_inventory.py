"""Ask an installed host for its actual skill/command inventory without a model call."""
import argparse
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import time


def inventory(host, project, plugin=None):
    executable = shutil.which('codex' if host == 'codex' else 'claude')
    if not executable:
        raise FileNotFoundError(f'{host} executable is unavailable')
    # Resolve the package's declared executable instead of composing shell code.
    if host == 'claude-code' and Path(executable).suffix.lower() in ('.cmd', '.ps1'):
        package = Path(executable).parent / 'node_modules/@anthropic-ai/claude-code'
        manifest = json.loads((package / 'package.json').read_text(encoding='utf-8'))
        entry = package / manifest['bin']['claude']
        command = [shutil.which('node'), str(entry)] if entry.suffix in ('.js', '.cjs', '.mjs') else [str(entry)]
    else:
        command = [executable]
    if host == 'codex':
        command += ['app-server', '--stdio']
    else:
        command += ['--print', '--input-format', 'stream-json', '--output-format', 'stream-json', '--verbose', '--no-session-persistence']
        if plugin:
            command += ['--plugin-dir', str(Path(plugin).resolve())]
    events = queue.Queue()
    stderr_lines = []
    process = subprocess.Popen(command, cwd=project, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    def reader(stream, target):
        for line in stream:
            target(line)
    threading.Thread(target=reader, args=(process.stdout, events.put), daemon=True).start()
    threading.Thread(target=reader, args=(process.stderr, stderr_lines.append), daemon=True).start()
    def send(value):
        process.stdin.write(json.dumps(value) + '\n')
        process.stdin.flush()
    def receive(predicate):
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            try:
                line = events.get(timeout=1)
            except queue.Empty:
                if process.poll() is not None:
                    break
                continue
            try:
                item = json.loads(line)
            except ValueError:
                continue
            if predicate(item):
                return item
        detail = ''.join(stderr_lines)[-1200:]
        raise RuntimeError(f'{host} inventory timed out or exited ({process.poll()}): {detail}')
    try:
        if host == 'codex':
            send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name': 'pstack-inventory', 'version': '1'}, 'capabilities': {'experimentalApi': True}}})
            initialized = receive(lambda item: item.get('id') == 1)
            if 'error' in initialized:
                raise RuntimeError(initialized['error'])
            send({'method': 'initialized'})
            send({'id': 2, 'method': 'skills/list', 'params': {'cwds': [str(Path(project).resolve())], 'forceReload': True}})
            return receive(lambda item: item.get('id') == 2)
        send({'type': 'control_request', 'request_id': 'inventory', 'request': {'subtype': 'initialize'}})
        result = receive(lambda item: item.get('type') == 'control_response' and item.get('response', {}).get('request_id') == 'inventory')
        response = result.get('response', {}).get('response', {})
        result.get('response', {})['response'] = {k: response[k] for k in ('commands', 'agents', 'models', 'claude_code_version') if k in response}
        return result
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=['codex', 'claude-code'], required=True)
    parser.add_argument('--project', required=True)
    parser.add_argument('--plugin')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = inventory(args.host, args.project, args.plugin)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    if args.host == 'codex':
        entries = result.get('result', {}).get('data', [])
        local = [skill for item in entries for skill in item.get('skills', []) if str(Path(args.project).resolve()).casefold() in skill.get('path', '').casefold()]
        errors = [error for item in entries for error in item.get('errors', [])]
        all_skills = [skill for item in entries for skill in item.get('skills', [])]
        marker = Path.home() / '.codex/pstack/.library-install.json'
        expected = set(json.loads(marker.read_text()).get('skills', {})) if marker.is_file() else set()
        user_skills = [skill for skill in all_skills if skill['name'] in expected and skill.get('scope') == 'user']
        print(json.dumps({'project_skills': len(local), 'managed_user_skills': len(user_skills), 'names': sorted(s['name'] for s in local), 'errors': errors}, indent=2))
    else:
        response = result.get('response', {})
        body = response.get('response', {})
        print(json.dumps({'subtype': response.get('subtype'),
                          'commands': [c['name'] for c in body.get('commands', [])],
                          'agents': [a['name'] for a in body.get('agents', [])]}, indent=2))


if __name__ == '__main__':
    main()
