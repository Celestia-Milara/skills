"""Ask an installed host for its actual skill/command inventory without a model call."""
import argparse
from collections import Counter
import json
from pathlib import Path
import queue
import subprocess
import threading
import time

from host_process import host_command, managed_process


def inventory(host, project, plugin=None, timeout=45):
    command = host_command(host)
    if host == 'codex':
        command += ['app-server', '--stdio']
    else:
        command += ['--print', '--input-format', 'stream-json', '--output-format', 'stream-json', '--verbose', '--no-session-persistence']
        if plugin:
            command += ['--plugin-dir', str(Path(plugin).resolve())]
    events = queue.Queue()
    stderr_lines = []
    readers = []
    deadline = time.monotonic() + timeout

    def reader(stream, target, eof=False):
        try:
            for line in stream:
                target(line)
        finally:
            if eof:
                events.put(None)

    try:
        with managed_process(command, cwd=project, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             encoding='utf-8', errors='replace') as process:
            for stream, target, eof in ((process.stdout, events.put, True),
                                        (process.stderr, stderr_lines.append, False)):
                thread = threading.Thread(target=reader, args=(stream, target, eof), daemon=True)
                thread.start()
                readers.append(thread)

            def send(value):
                try:
                    process.stdin.write(json.dumps(value) + '\n')
                    process.stdin.flush()
                except (BrokenPipeError, OSError) as error:
                    raise RuntimeError(f'{host} inventory input closed: {error}') from error

            def receive(predicate):
                while True:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        reason = f'timed out after {timeout}s'
                        break
                    try:
                        line = events.get(timeout=remaining)
                    except queue.Empty:
                        reason = f'timed out after {timeout}s'
                        break
                    if line is None:
                        reason = f'closed stdout (exit code {process.poll()})'
                        break
                    try:
                        item = json.loads(line)
                    except ValueError:
                        continue
                    if isinstance(item, dict) and predicate(item):
                        return item
                readers[1].join(timeout=0.1)
                detail = ''.join(stderr_lines)[-1200:]
                raise RuntimeError(f'{host} inventory {reason}: {detail}')

            if host == 'codex':
                send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name': 'pstack-inventory', 'version': '1'}, 'capabilities': {'experimentalApi': True}}})
                initialized = receive(lambda item: item.get('id') == 1)
                if 'error' in initialized:
                    raise RuntimeError(f'{host} initialize failed: {initialized["error"]}')
                send({'method': 'initialized'})
                send({'id': 2, 'method': 'skills/list', 'params': {'cwds': [str(Path(project).resolve())], 'forceReload': True}})
                result = receive(lambda item: item.get('id') == 2)
                if 'error' in result:
                    raise RuntimeError(f'{host} skills/list failed: {result["error"]}')
                if not isinstance(result.get('result'), dict) or not isinstance(result['result'].get('data'), list):
                    raise RuntimeError(f'{host} skills/list returned an invalid result')
                return result
            send({'type': 'control_request', 'request_id': 'inventory', 'request': {'subtype': 'initialize'}})
            result = receive(lambda item: item.get('type') == 'control_response'
                             and isinstance(item.get('response'), dict)
                             and item['response'].get('request_id') == 'inventory')
            envelope = result['response']
            if envelope.get('subtype') == 'error' or envelope.get('error'):
                raise RuntimeError(f'{host} initialize failed: {envelope.get("error", envelope)}')
            response = envelope.get('response')
            if not isinstance(response, dict):
                raise RuntimeError(f'{host} initialize returned an invalid result')
            envelope['response'] = {k: response[k] for k in ('commands', 'agents', 'models', 'claude_code_version') if k in response}
            return result
    finally:
        for thread in readers:
            thread.join(timeout=5)


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
        all_skills = [skill for item in entries for skill in item.get('skills', [])]
        project = Path(args.project).resolve()
        local = [skill for skill in all_skills if skill.get('path')
                 and Path(skill['path']).resolve().is_relative_to(project)]
        errors = [error for item in entries for error in item.get('errors', [])]
        print(json.dumps({'project_skills': len(local), 'names': sorted(s['name'] for s in local),
                          'skills_by_scope': dict(Counter(s.get('scope') for s in all_skills)), 'errors': errors}, indent=2))
        if errors:
            raise SystemExit(1)
    else:
        response = result.get('response', {})
        body = response.get('response', {})
        print(json.dumps({'subtype': response.get('subtype'),
                          'commands': [c['name'] for c in body.get('commands', [])],
                          'agents': [a['name'] for a in body.get('agents', [])]}, indent=2))


if __name__ == '__main__':
    main()
