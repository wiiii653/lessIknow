#!/usr/bin/env python3
"""Standalone result page for the original v035 bank probe.

Contains only the original player's two code/table segments and a small status
page. The original fourteen-selector probe is executed unchanged; the result is
displayed and the machine halts. No graphics bank is loaded or tested, so a
wild bank switch cannot overwrite this page.
"""
from pathlib import Path

from build_sequence import Code
from build_visual_prototype import xex_segment
from extract_music import segments

SOURCE = Path('releases/less-i-know-demo-release-009-stereo.xex')
OUTPUT = Path('releases/avg-first-bank-diagnostic-004.xex')

SCREEN = 0x2B00       # five 40-column rows, $2B00-$2BC7
DLIST = 0x2C00
BANNER = 0x2C20
PASSED = 0x2C48
FAILED = 0x2C70
PASS_CODE = 0x2C98
FAIL_CODE = 0x2D80


def display_list():
    rows = bytearray((0x70, 0x70, 0x70))
    for row in range(5):
        rows.extend((0x42, (SCREEN + row * 40) & 255,
                     (SCREEN + row * 40) >> 8))
    rows.extend((0x41, DLIST & 255, DLIST >> 8))
    return bytes(rows)


def enc(text):
    text = text[:40].ljust(40)
    return bytes((ord(ch) - 32) & 0x7F for ch in text)


def result_page(origin, message):
    """Copy title to row 0 and message to row 2, configure the display, halt."""
    c = Code(origin)
    c.emit(0xA0, 0)
    c.label('title')
    c.emit(0xB9, BANNER & 255, BANNER >> 8, 0x99, SCREEN & 255, SCREEN >> 8)
    c.emit(0xC8, 0xC0, 40)
    c.branch(0xD0, 'title')
    c.emit(0xA0, 0)
    c.label('result')
    c.emit(0xB9, message & 255, message >> 8,
           0x99, (SCREEN + 80) & 255, (SCREEN + 80) >> 8)
    c.emit(0xC8, 0xC0, 40)
    c.branch(0xD0, 'result')

    def store(address, value):
        c.emit(0xA9, value, 0x8D, address & 255, address >> 8)

    # $D018=$E0 selects the ROM font at $E000. The old diagnostic wrote $00
    # (CHBASE page zero), which made every glyph blank.
    for address, value in ((0x022F, 0x22), (0x0230, DLIST & 255),
                           (0x0231, DLIST >> 8), (0x02F4, 0xE0),
                           (0x02C5, 0x0E), (0x02C6, 0x00),
                           (0xD402, DLIST & 255), (0xD403, DLIST >> 8),
                           (0xD409, 0xE0), (0xD017, 0x0E),
                           (0xD018, 0xE0), (0xD400, 0x22)):
        store(address, value)
    c.label('halt')
    c.jump(0x4C, 'halt')
    return bytes(c.finish())


def main():
    entries = list(segments(SOURCE.read_bytes()))
    player = [(a, b, x) for a, b, x in entries
              if (a, b) in ((0x2000, 0x24B2), (0x24BD, 0x28BC))]
    assert len(player) == 2
    pass_code = result_page(PASS_CODE, PASSED)
    fail_code = result_page(FAIL_CODE, FAILED)
    assert PASS_CODE + len(pass_code) <= FAIL_CODE
    assert FAIL_CODE + len(fail_code) <= 0x3000, hex(FAIL_CODE + len(fail_code))
    print(f'pass ${PASS_CODE:04X}+{len(pass_code)}  '
          f'fail ${FAIL_CODE:04X}+{len(fail_code)}')
    out = bytearray(b'\xff\xff')
    out.extend(xex_segment(DLIST, display_list()))
    out.extend(xex_segment(BANNER, enc('ORIGINAL V035 BANK PROBE')))
    out.extend(xex_segment(PASSED, enc('BANK TEST PASSED')))
    out.extend(xex_segment(FAILED, enc('BANK TEST FAILED')))
    out.extend(xex_segment(PASS_CODE, pass_code))
    out.extend(xex_segment(FAIL_CODE, fail_code))
    # Display the banner first, then return to the OS loader so the original
    # $2000 INIT runs. The probe replaces that page with PASS or FAIL. This
    # artifact contains only the original player code/table and no banks.
    banner = Code(0x2E00)
    banner.emit(0xA0, 0)
    banner.label('copy')
    banner.emit(0xB9, BANNER & 255, BANNER >> 8,
                0x99, SCREEN & 255, SCREEN >> 8)
    banner.emit(0xC8, 0xC0, 40)
    banner.branch(0xD0, 'copy')
    for address, value in ((0x022F, 0x22), (0x0230, DLIST & 255),
                           (0x0231, DLIST >> 8), (0x02F4, 0xE0),
                           (0x02C5, 0x0E), (0x02C6, 0x00),
                           (0xD402, DLIST & 255), (0xD403, DLIST >> 8),
                           (0xD409, 0xE0), (0xD017, 0x0E),
                           (0xD018, 0xE0), (0xD400, 0x22)):
        banner.emit(0xA9, value, 0x8D, address & 255, address >> 8)
    banner.emit(0x60)
    banner_code = bytes(banner.finish())
    out.extend(xex_segment(0x2E00, banner_code))
    out.extend(xex_segment(0x02E2, (0x2E00).to_bytes(2, 'little')))
    for start, end, payload in player:
        payload = bytearray(payload)
        if start == 0x2000:
            success = 0x2075 - start
            assert payload[success:success + 3] == bytes.fromhex('20 ca 20')
            payload[success:success + 3] = bytes((0x4C, PASS_CODE & 255,
                                                  PASS_CODE >> 8))
            failure = 0x20BB - start
            assert payload[failure:failure + 3] == bytes.fromhex('4c bb 20')
            payload[failure:failure + 3] = bytes((0x4C, FAIL_CODE & 255,
                                                  FAIL_CODE >> 8))
        out.extend(xex_segment(start, payload))
    with OUTPUT.open('xb') as stream:
        stream.write(out)


if __name__ == '__main__':
    main()
