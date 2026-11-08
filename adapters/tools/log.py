"""Append one timestamped decision to the pstack TSV log."""
from datetime import datetime, timezone
from pathlib import Path
import sys


def cell(value):
    value = value.replace('\t', ' ').replace('\r', ' ').replace('\n', ' ')
    return "'" + value if value.startswith(('=', '+', '-', '@')) else value


def append(path, phase, decision, why, evidence, result):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8', newline='') as stream:
        if stream.tell() == 0:
            stream.write('ts\tphase\tdecision\twhy\tevidence\tresult\n')
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        stream.write('\t'.join([timestamp, *map(cell, [phase, decision, why, evidence, result])]) + '\n')


def main():
    values = sys.argv[1:]
    if len(values) != 6:
        print('usage: log.py <logfile> <phase> <decision> <why> <evidence> <result>', file=sys.stderr)
        return 1
    append(*values)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
