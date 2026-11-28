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

def sample_windows(info):
    def window(start, span=300):
        return range(start, start+span, 4)

    return {
        'intro': window(0, 100),
        'title': window(info['title_tick']),
        'school': window(info['school_tick'], 100),
        'pan': window(info['school_portrait_tick']),
        'practice': window(info['practice_tick']),
        'side_dancer': window(info['ribbon_side_start']),
        'early_tunnel': window(info['kaleido_tick']),
        'ribbon_trio': window(info['crush_tick']),
        'tunnel_cutaway': window(info['hero_cutaway_start']),
        'hero': window(info['hero_start']),
        'trevor': window(info['trevor_hit']),
        'post_trevor_montage': window(info['trevor_end']),
        'late_montage': window(info['post_trevor_cuts'][-4][0]),
        'credits': window(info['final_boy_start']),
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
    for name, ticks in sample_windows(json.loads(sequence.METADATA.read_text())).items():
        cpu = None
        costs = []
        for tick in ticks:
            before = cpu.processorCycles if cpu else 0
            cpu = sequence.execute(tick, cpu, publish_side=False)
            costs.append(cpu.processorCycles - before)
            sequence.publish_side_ribbons(cpu)
        result[name] = {
            'first_tick': ticks[0], 'last_tick': ticks[-1],
            'samples': len(costs), 'min': min(costs),
            'median': statistics.median(costs), 'max': max(costs),
            'over_pal_frame': sum(c > 35568 for c in costs), 'costs': costs,
        }
        print(name, {k: v for k, v in result[name].items() if k != 'costs'}, flush=True)
    args.output.write_text(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
