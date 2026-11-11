#!/usr/bin/env python3
"""Show the v035 first bank-probe result before loading the full demo."""
from pathlib import Path
from build_sequence import Code
from build_visual_prototype import xex_segment
from extract_music import segments
import loading_screen

SOURCE = Path('releases/less-i-know-demo-release-009-stereo.xex')
OUTPUT = Path('releases/avg-first-bank-diagnostic-001.xex')

def status_code(origin, message):
    c = Code(origin)
    # Screen display setup is shared with the real demo.
    c.emit(0x20, 0x80, 0x07, 0xa2, 0)
    c.label('copy')
    c.jump(0xbd, 'message')
    c.emit(0x9d, 0x28, 0x06, 0xe8, 0xe0, 40)
    c.branch(0xd0, 'copy')
    c.label('halt'); c.jump(0x4c, 'halt')
    c.label('message')
    c.emit(*(ord(ch)-32 for ch in message.center(40)))
    return bytes(c.finish())

def main():
    entries = list(segments(SOURCE.read_bytes()))
    out = bytearray(b'\xff\xff')
    out.extend(loading_screen.segments())
    out.extend(xex_segment(0x0800, status_code(0x0800, 'BANK TEST FAILED')))
    out.extend(xex_segment(0x0880, status_code(0x0880, 'BANK TEST PASSED')))
    for start, end, payload in entries[:5]:
        payload = bytearray(payload)
        if start == 0x2000:
            offset = 0x20bb-start
            assert payload[offset:offset+3] == bytes.fromhex('4c bb 20')
            payload[offset:offset+3] = bytes.fromhex('4c 00 08')
        out.extend(xex_segment(start, payload))
    out.extend(xex_segment(0x02e0, bytes.fromhex('80 08')))
    with OUTPUT.open('xb') as f:
        f.write(out)

if __name__ == '__main__':
    main()
