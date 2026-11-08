"""Project installed entries while leaving the official source unchanged."""
import json
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

HOST_ROOTS = {'codex': '.agents', 'claude-code': '.claude', 'pi': '.pi/agent', 'dsh': '.dsh'}
LINK = re.compile(r'\]\(([^\s)]+)\)')

def invocation_metadata(value, explicit):
    policy = re.search(r'^policy:[ \t]*$', value, re.M)
    if policy:
        remainder = value[policy.end():]
        next_key = re.search(r'\n[^\s#][^\n]*:', remainder)
        end = policy.end() + (next_key.start() if next_key else len(remainder))
        block = value[policy.end():end]
        disabled = explicit or bool(re.search(r'^\s+allow_implicit_invocation:\s*false\s*$', block, re.M))
        line = '  allow_implicit_invocation: ' + ('false' if disabled else 'true')
        if re.search(r'^\s+allow_implicit_invocation:[^\n]*', block, re.M):
            block = re.sub(r'^[ \t]+allow_implicit_invocation:[^\n]*', line, block, flags=re.M)
        else:
            block = '\n' + line + block
        return value[:policy.end()] + block + value[end:]
    return value.rstrip() + '\npolicy:\n  allow_implicit_invocation: ' + ('false' if explicit else 'true') + '\n'

def relocate(value, source, target, bundle, host_root, names):
    def rewrite(match):
        href = match[1]
        if urlsplit(href).scheme or href.startswith(('#', '//')):
            return match[0]
        name, separator, fragment = href.partition('#')
        original = (source.parent / unquote(name)).resolve()
        if not original.is_relative_to(bundle.resolve()) or not original.exists():
            return match[0]
        relative = original.relative_to(bundle.resolve())
        if len(relative.parts) >= 2 and relative.parts[0] == 'skills' and relative.parts[1] in names:
            destination = host_root / relative
        else:
            destination = bundle / relative
        href = Path(os.path.relpath(destination, target.parent)).as_posix()
        return '](' + href + (separator + fragment if separator else '') + ')'
    return LINK.sub(rewrite, value)

def entry(value, host, adapter):
    header = re.match(r'^(---\s*\n)(.*?)(\n---)', value, re.S)
    explicit = bool(header and re.search(r'^disable-model-invocation:\s*true\s*$', header[2], re.M))
    if header:
        fields = 'icon|color|paths'
        if host == 'codex':
            fields += '|disable-model-invocation'
        cleaned = re.sub(r'^(?:' + fields + r'):[^\n]*\n?', '', header[2], flags=re.M)
        value = header[1] + cleaned.rstrip() + header[3] + value[header.end():]
    instruction = f'Read [the {host} adapter]({adapter}) before this workflow. It maps tools, models and paths for this installation.'
    value, count = re.subn(r'^(# .*)\n+', lambda m: m[1] + '\n\n' + instruction + '\n\n', value, count=1, flags=re.M)
    if count != 1:
        frontmatter = re.match(r'^---\s*\n.*?\n---', value, re.S)
        if not frontmatter:
            raise ValueError('Skill entrypoint has no frontmatter')
        cut = frontmatter.end()
        value = value[:cut] + '\n\n' + instruction + '\n\n' + value[cut:].lstrip('\n')
    return value, explicit

def project_skill(host, bundle, host_root, name, names):
    target = host_root / 'skills' / name
    adapter = Path(os.path.relpath(bundle / 'adapters' / f'{host}.md', target)).as_posix()
    for path in target.rglob('*.md'):
        original = bundle / 'skills' / name / path.relative_to(target)
        value = relocate(path.read_text(encoding='utf-8'), original, path, bundle, host_root, names)
        if path == target / 'SKILL.md':
            value, explicit = entry(value, host, adapter)
            if host == 'codex':
                metadata = target / 'agents/openai.yaml'
                metadata.parent.mkdir(exist_ok=True)
                original = metadata.read_text(encoding='utf-8') if metadata.exists() else ''
                metadata.write_text(invocation_metadata(original, explicit), encoding='utf-8')
        path.write_text(value, encoding='utf-8', newline='\n')

def project_agent(value, host, final_root, skill_root=None):
    value = re.sub(r'^is_background:[^\n]*\n?', '', value, flags=re.M)
    mode = ((skill_root or final_root / 'pstack/skills') / 'poteto-mode/SKILL.md').as_posix()
    adapter = (final_root / f'pstack/adapters/{host}.md').as_posix()
    instruction = f'Read `{adapter}` before work. For poteto-mode use the parent-provided absolute path, or `{mode}` when none is provided.'
    return re.sub(r'^(# .*)\n+', lambda m: m[1] + '\n\n' + instruction + '\n\n', value, count=1, flags=re.M)
