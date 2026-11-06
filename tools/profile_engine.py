#!/usr/bin/env python3
"""Sample CPU-only callback costs: fixed VCOUNT, no ANTIC DMA or music NMI.

Run from the project root. Each scene starts with a fresh CPU; tick steps do
not model time elapsed during rendering. These numbers are not live FPS.
ATARI_TEST_XEX or --xex selects a build with matching JSON metadata.
"""
import argparse
import json
import os
from pathlib import Path
import statistics
import sys

CASES = {
    'intro': range(0, 100, 4), 'title': range(1496, 1596, 4),
    'school': range(2992, 3092, 4), 'pan': range(3553, 3853, 4),
    'practice': range(6000, 6100, 4), 'dance': range(9216, 9472, 4),
    'mosaic': range(12000, 12300, 4), 'crush': range(18000, 18100, 4),
    'hero': range(21000, 21300, 4), 'trevor': range(27000, 27300, 4),
    'late_mosaic': range(59000, 59300, 4),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--xex', type=Path)
    parser.add_argument('--output', type=Path, default=Path('/tmp/atari-profile.json'))
    args = parser.parse_args()
    if args.xex:
        os.environ['ATARI_TEST_XEX'] = str(args.xex.resolve())
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / 'tests'))
    import test_sequence as sequence

    result = {}
    for name, ticks in CASES.items():
        cpu = None
        costs = []
        for tick in ticks:
            before = cpu.processorCycles if cpu else 0
            cpu = sequence.execute(tick, cpu)
            costs.append(cpu.processorCycles - before)
        result[name] = {
            'samples': len(costs), 'min': min(costs),
            'median': statistics.median(costs), 'max': max(costs),
            'over_pal_frame': sum(c > 35568 for c in costs), 'costs': costs,
        }
        print(name, {k: v for k, v in result[name].items() if k != 'costs'}, flush=True)
    args.output.write_text(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
