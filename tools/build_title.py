#!/usr/bin/env python3
"""Render the opening title with a small, repository-owned bitmap font."""

from pathlib import Path


GLYPHS = {
    'A': ('01110', '10001', '10001', '11111', '10001', '10001', '10001'),
    'M': ('10001', '11011', '10101', '10101', '10001', '10001', '10001'),
    'P': ('11110', '10001', '10001', '11110', '10000', '10000', '10000'),
    'T': ('11111', '00100', '00100', '00100', '00100', '00100', '00100'),
    'H': ('10001', '10001', '10001', '11111', '10001', '10001', '10001'),
    'E': ('11111', '10000', '10000', '11110', '10000', '10000', '11111'),
    'L': ('10000', '10000', '10000', '10000', '10000', '10000', '11111'),
    'S': ('01111', '10000', '10000', '01110', '00001', '00001', '11110'),
    'I': ('11111', '00100', '00100', '00100', '00100', '00100', '11111'),
    'K': ('10001', '10010', '10100', '11000', '10100', '10010', '10001'),
    'N': ('10001', '11001', '11001', '10101', '10011', '10011', '10001'),
    'O': ('01110', '10001', '10001', '10001', '10001', '10001', '01110'),
    'W': ('10001', '10001', '10001', '10101', '10101', '11011', '10001'),
    'B': ('11110', '10001', '10001', '11110', '10001', '10001', '11110'),
    'R': ('11110', '10001', '10001', '11110', '10100', '10010', '10001'),
    ',': ('00000', '00000', '00000', '00000', '00000', '00110', '00100'),
    '.': ('00000', '00000', '00000', '00000', '00000', '00110', '00110'),
    ' ': ('00000',) * 7,
}
ROWS = (('THE LESS', 3, 19), ('I KNOW', 3, 75), ('THE BETTER', 2, 131))


def render(rows=ROWS):
    pixels = bytearray(160 * 192)
    for text, scale_x, top in rows:
        width = (len(text) * 6 - 1) * scale_x
        left = (160 - width) // 2
        for index, char in enumerate(text):
            for gy, row in enumerate(GLYPHS[char]):
                for gx, bit in enumerate(row):
                    if bit != '1':
                        continue
                    for dy in range(6):
                        for dx in range(scale_x):
                            x = left + index * 6 * scale_x + gx * scale_x + dx
                            y = top + gy * 6 + dy
                            # Two color bands within each letter animate via
                            # the hardware palette, without redrawing pixels.
                            pixels[y * 160 + x] = 220 if (gy + dy // 3) % 3 else 100
    return pixels


def main():
    pixels = render()
    output = Path('build')
    output.mkdir(exist_ok=True)
    (output / 'title.gray').write_bytes(pixels)
    (output / 'title.pgm').write_bytes(b'P5\n160 192\n255\n' + pixels)
    print('Rendered title: THE LESS / I KNOW / THE BETTER')


if __name__ == '__main__':
    main()
