"""Append one timestamped decision to the pstack TSV log."""
import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path


def cell(value):
    value = value.replace('\t', ' ').replace('\r', ' ').replace('\n', ' ')
    return "'" + value if value.startswith(('=', '+', '-', '@')) else value


def append(path, phase, decision, why, evidence, result):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        if stream.tell() == 0:
            writer.writerow(['ts', 'phase', 'decision', 'why', 'evidence', 'result'])
        writer.writerow([datetime.now(timezone.utc).isoformat(), *map(cell, [phase, decision, why, evidence, result])])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['logfile', 'phase', 'decision', 'why', 'evidence', 'result']:
        parser.add_argument(name)
    args = parser.parse_args()
    append(args.logfile, args.phase, args.decision, args.why, args.evidence, args.result)


if __name__ == '__main__':
    main()
