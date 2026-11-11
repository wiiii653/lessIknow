#!/usr/bin/env python3
"""Keep the first four POKEY voices and suppress writes to the second chip."""
import argparse
from pathlib import Path

from extract_music import segments
from build_visual_prototype import xex_segment

RIGHT_WRITES = (0x217b, 0x2186, 0x225c, 0x2265, 0x226e, 0x2277,
                0x2280, 0x2289, 0x22bd, 0x22f1, 0x231a, 0x231d,
                0x2320, 0x2c39, 0x2c3f, 0x2c45, 0x2c4b, 0x2c51,
                0x2c57, 0x2c5d, 0x2c63, 0x2c69)

def mono(data):
    remaining = set(RIGHT_WRITES)
    out = bytearray(b'\xff\xff')
    for start, end, source in segments(data):
        payload = bytearray(source)
        for addr in tuple(remaining):
            if start <= addr and addr + 2 <= end:
                i = addr - start
                assert payload[i] in (0x8d, 0x9d, 0x99) and payload[i+2] == 0xd2
                assert 0x10 <= payload[i+1] <= 0x1f
                payload[i:i+3] = b'\xea\xea\xea'
                remaining.remove(addr)
        out.extend(xex_segment(start, payload))
    assert not remaining, remaining
    return bytes(out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('output exists')
    args.output.write_bytes(mono(args.source.read_bytes()))
