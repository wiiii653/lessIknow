#!/usr/bin/env python3
"""Move the loading screen before the original bank probe and report failure."""
import argparse
from pathlib import Path
from build_avg_diagnostic import status_code
from build_visual_prototype import xex_segment
from extract_music import segments
import loading_screen

def build(data):
    out = bytearray(b'\xff\xff')
    out.extend(loading_screen.segments())
    out.extend(xex_segment(0x0800, status_code(0x0800, 'BANK TEST FAILED')))
    patched = False
    for start, end, data in segments(data):
        payload = bytearray(data)
        if (start, end) == (0x2000, 0x24b2):
            assert payload[7:10] == bytes.fromhex('8d 00 d4')
            assert payload[0xbb:0xbe] == bytes.fromhex('4c bb 20')
            payload[7:10] = bytes.fromhex('ea ea ea')
            payload[0xbb:0xbe] = bytes.fromhex('4c 00 08')
            patched = True
        out.extend(xex_segment(start, payload))
    assert patched
    return bytes(out)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('source', type=Path)
    p.add_argument('output', type=Path)
    a = p.parse_args()
    with a.output.open('xb') as f:
        f.write(build(a.source.read_bytes()))
