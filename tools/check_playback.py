#!/usr/bin/env python3
"""Compare stereo POKEY recordings with the original player or a saved demo."""

import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path.home() / '.atari800.cfg')
    parser.add_argument('--seconds', type=int, default=10,
                        help='host seconds to record each turbo emulator run')
    parser.add_argument('--demo', type=Path, default=Path('build/visual-prototype-dev.xex'))
    parser.add_argument('--reference', type=Path, default=Path('less-i-know-release-v035.xex'),
                        help='original player, or an archived demo for regression checks')
    parser.add_argument('--minimum-seconds', type=float, default=305,
                        help='minimum aligned emulated duration (default: full original track)')
    args = parser.parse_args()
    env = dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy')
    with tempfile.TemporaryDirectory(prefix='tliktb-playback-') as directory:
        root = Path(directory)
        config = root / 'atari800.cfg'
        lines = args.config.read_text().splitlines()
        lines = [line for line in lines if not line.startswith('STEREO_POKEY=')]
        config.write_text('\n'.join(lines) + '\nSTEREO_POKEY=1\n')
        recordings = []
        for index, xex in enumerate((args.reference, args.demo)):
            recording = root / f'{index}.dat'
            command = ['timeout', str(args.seconds) + 's', 'atari800',
                       '-config', str(config), '-no-autosave-config', '-1088xe',
                       '-pal', '-nobasic', '-xl-rev', 'altirra', '-turbo', '-nosound',
                       '-pokeyrec', '-pokeyrec-stereo', '-pokeyrec-interval', '78',
                       '-pokeyrec-file', str(recording), '-run', str(xex)]
            result = subprocess.run(command, env=env, capture_output=True)
            if result.returncode not in (0, 124):
                raise SystemExit(result.stderr.decode(errors='replace'))
            recordings.append(recording.read_bytes())
        # Asset INITs add startup silence. Align once at the first nonzero
        # complete stereo sample; never realign or drop ticks during music.
        aligned = []
        for recording in recordings:
            start = next((i for i in range(0, len(recording) - 17, 18)
                          if any(recording[i:i + 18])), None)
            if start is None:
                raise SystemExit('No music detected in recording')
            aligned.append(recording[start:])
        a, b = aligned
        common = min(len(a), len(b))
        # Raw recording: 9 registers per POKEY, two chips, 4 samples/PAL frame.
        seconds = common / (18 * 4 * 49.86)
        if seconds < args.minimum_seconds:
            raise SystemExit(f'Only {seconds:.1f}s emulated; increase --seconds')
        if a[:common] != b[:common]:
            offset = next(i for i in range(common) if a[i] != b[i])
            raise SystemExit(f'POKEY mismatch at recording byte {offset}')
        print(f'PASS: {common:,} identical stereo POKEY bytes, '
              f'approximately {seconds:.1f}s emulated, '
              f'reference: {args.reference}.')


if __name__ == '__main__':
    main()
