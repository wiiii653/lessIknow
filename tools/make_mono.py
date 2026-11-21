#!/usr/bin/env python3
"""Convert a stereo XEX for one POKEY, with a fold-down for audited releases."""
import argparse
import hashlib
from pathlib import Path

from build_sequence import Code
from extract_music import segments
from build_visual_prototype import xex_segment

RIGHT_WRITES = (0x217b, 0x2186, 0x225c, 0x2265, 0x226e, 0x2277,
                0x2280, 0x2289, 0x22bd, 0x22f1, 0x231a, 0x231d,
                0x2320, 0x2c39, 0x2c3f, 0x2c45, 0x2c4b, 0x2c51,
                0x2c57, 0x2c5d, 0x2c63, 0x2c69)
MERGE_SOURCES = {
    '0da2f621e0ff4b35f6f284fbbf14f6fa1f99d053e635898eacac0f62eeb37d5b',  # 064
    '2369853082b52dc69ebb03d88101722e3246f9a1a669c8d48a3bbde40a8f6fdd',  # 066
}

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


def folded_writer():
    """Fold the v035 pairs within the existing writer at $2C00–$2C80."""
    code = Code(0x2c00)
    left, right = 0x2900, 0x2909
    scratch = 0x2923

    def absolute(op, addr):
        code.emit(op, addr & 255, addr >> 8)

    # Voices 1+2 are joined for both source basses. Use the left pitch to
    # remove the stereo detune and round the merged level to a POKEY nibble.
    for reg in (8, 0, 2, 1):
        absolute(0xad, left + reg)
        absolute(0x8d, 0xd200 + reg)
    absolute(0xad, right + 3)
    code.emit(0x29, 15)
    absolute(0x8d, scratch)
    absolute(0xad, left + 3)
    code.emit(0x29, 15, 0xd8, 0x38)  # AND, CLD, SEC (round sum up before shift)
    absolute(0x6d, scratch)
    code.emit(0x4a, 0x09, 0xa0)
    absolute(0x8d, 0xd203)

    # One oscillator for each remaining pair. Preserve the louder voice's
    # pitch and distortion together, with a stable left tie break.
    code.emit(0xa2, 4)
    code.label('voice')
    absolute(0xbd, left + 1)
    code.emit(0x29, 15)
    absolute(0x8d, scratch)
    absolute(0xbd, right + 1)
    code.emit(0x29, 15)
    absolute(0xcd, scratch)
    code.branch(0x90, 'left')
    code.branch(0xf0, 'left')
    absolute(0xbd, right)
    absolute(0x9d, 0xd200)
    absolute(0xbd, right + 1)
    code.jump(0x4c, 'control')
    code.label('left')
    absolute(0xbd, left)
    absolute(0x9d, 0xd200)
    absolute(0xbd, left + 1)
    code.label('control')
    absolute(0x9d, 0xd201)
    code.emit(0xe8, 0xe8, 0xe0, 8)
    code.branch(0xd0, 'voice')

    # Keep the original visual meters and the original song tick handler.
    for reg, addr in ((3, 0x24b6), (5, 0x24b8), (7, 0x24ba)):
        absolute(0xad, left + reg)
        absolute(0x8d, addr)
    absolute(0x4c, 0x22f4)
    writer = bytes(code.finish())
    if len(writer) > 129:
        raise ValueError('folded writer exceeds $2C00–$2C80')
    return writer.ljust(129, b'\xea')


def merge(data):
    # The fold relies on the audited v035 channel layout and score.
    if hashlib.sha256(data).hexdigest() not in MERGE_SOURCES:
        raise ValueError('merged mono requires stereo release 064 or 066')
    out = bytearray(b'\xff\xff')
    for start, end, payload in segments(mono(data)):
        if (start, end) == (0x2c00, 0x2c80):
            payload = folded_writer()
        out.extend(xex_segment(start, payload))
    return bytes(out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--merge', action='store_true', help='fold both stereo sides of release 064 or 066')
    args = parser.parse_args()
    result = (merge if args.merge else mono)(args.source.read_bytes())
    with args.output.open('xb') as output:
        output.write(result)
