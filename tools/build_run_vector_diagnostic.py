#!/usr/bin/env python3
"""Minimal test: does the loader execute the $02E0 RUN vector?

INIT writes "INIT OK" to row 0 and returns. RUN writes "RUN OK" to row 2 and
halts. Both use the same five-row ANTIC-2 screen in the free $2B00-$2EFF gap.
If only "INIT OK" is visible, this loader does not honour RUNAD for our XEX.
"""
from pathlib import Path

from build_sequence import Code
from build_visual_prototype import xex_segment

OUTPUT = Path('releases/avg-run-vector-diagnostic-001.xex')

SCREEN = 0x2B00
DLIST = 0x2C00
INIT_TEXT = 0x2C20
RUN_TEXT = 0x2C48
INIT_CODE = 0x2CC0
RUN_CODE = 0x2D40


def display_list():
    rows = bytearray((0x70, 0x70, 0x70))
    for row in range(5):
        rows.extend((0x42, (SCREEN + row * 40) & 255,
                     (SCREEN + row * 40) >> 8))
    rows.extend((0x41, DLIST & 255, DLIST >> 8))
    return bytes(rows)


def enc(text):
    return bytes((ord(ch) - 32) & 0x7F for ch in text[:40].ljust(40))


def display_setup(c):
    def store(address, value):
        c.emit(0xA9, value, 0x8D, address & 255, address >> 8)

    for address, value in ((0x022F, 0x22), (0x0230, DLIST & 255),
                           (0x0231, DLIST >> 8), (0x02F4, 0xE0),
                           (0x02C5, 0x0E), (0x02C6, 0x00),
                           (0xD402, DLIST & 255), (0xD403, DLIST >> 8),
                           (0xD409, 0xE0), (0xD017, 0x0E),
                           (0xD018, 0xE0), (0xD400, 0x22)):
        store(address, value)


def row_copy(c, tag, source, row):
    target = SCREEN + row * 40
    c.emit(0xA0, 0)
    c.label(tag)
    c.emit(0xB9, source & 255, source >> 8, 0x99, target & 255, target >> 8)
    c.emit(0xC8, 0xC0, 40)
    c.branch(0xD0, tag)


def init_code(origin):
    c = Code(origin)
    row_copy(c, 'init_row', INIT_TEXT, 0)
    display_setup(c)
    c.emit(0x60)
    return bytes(c.finish())


def run_code(origin):
    c = Code(origin)
    row_copy(c, 'run_row', RUN_TEXT, 2)
    display_setup(c)
    c.label('halt')
    c.jump(0x4C, 'halt')
    return bytes(c.finish())


def main():
    init = init_code(INIT_CODE)
    run = run_code(RUN_CODE)
    assert INIT_CODE + len(init) <= RUN_CODE
    out = bytearray(b'\xff\xff')
    out.extend(xex_segment(DLIST, display_list()))
    out.extend(xex_segment(INIT_TEXT, enc('INIT OK')))
    out.extend(xex_segment(RUN_TEXT, enc('RUN OK - RUNAD WORKS')))
    out.extend(xex_segment(INIT_CODE, init))
    out.extend(xex_segment(RUN_CODE, run))
    out.extend(xex_segment(0x02E2, INIT_CODE.to_bytes(2, 'little')))
    out.extend(xex_segment(0x02E0, RUN_CODE.to_bytes(2, 'little')))
    with OUTPUT.open('xb') as stream:
        stream.write(out)


if __name__ == '__main__':
    main()
