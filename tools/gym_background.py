"""School gym in perspective, drawn directly on the 160x192 Atari pixel grid."""

import math
from pathlib import Path
from scene_palettes import ART_PALETTE


def dance_gym_pixels():
    """Four-color gym artwork used by the banked cheer dance."""
    rgb = Path('build/gym-v056.rgb').read_bytes()
    if len(rgb) != 160 * 192 * 3:
        raise ValueError('expected 160x192 RGB dance gym')
    palette = ART_PALETTE
    return bytes(min(range(4), key=lambda j: sum((rgb[i+c]-palette[j][c])**2
                                                for c in range(3)))
                 for i in range(0, len(rgb), 3))


def gym_pixels():
    p = bytearray(160 * 192)

    def rect(x0, y0, x1, y1, ink):
        for y in range(max(0, y0), min(192, y1)):
            left, right = max(0, x0), min(160, x1)
            if left < right:
                p[y * 160 + left:y * 160 + right] = bytes([ink]) * (right - left)

    def line(x0, y0, x1, y1, ink):
        steps = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(steps + 1):
            x = x0 + (x1 - x0) * i // max(1, steps)
            y = y0 + (y1 - y0) * i // max(1, steps)
            if 0 <= x < 160 and 0 <= y < 192:
                p[y * 160 + x] = ink

    # Roof, perspective ceiling beams, recessed far wall.
    rect(0, 0, 160, 13, 0)
    for x in (0, 32, 64, 96, 128, 159):
        line(x, 0, 80 + (x - 80) * 3 // 4, 24, 2)
    rect(0, 12, 160, 15, 2)
    line(0, 14, 20, 30, 3)
    line(159, 14, 140, 30, 3)
    rect(19, 29, 141, 32, 2)
    for x in (19, 45, 114, 139):
        rect(x, 31, x + 2, 93, 2)
    # Tall windows, muntins, illuminated sill and reflected light below.
    for x in (24, 49, 94, 119):
        rect(x, 35, x + 17, 65, 2)
        rect(x + 2, 37, x + 15, 62, 0)
        rect(x + 8, 37, x + 9, 62, 2)
        rect(x + 2, 48, x + 15, 50, 2)
        rect(x - 1, 65, x + 18, 67, 3)
        rect(x + 3, 69, x + 14, 71, 2)
    # Center basketball goal, separate from the roofline.
    rect(78, 15, 82, 34, 3)
    rect(65, 32, 95, 55, 3)
    rect(67, 34, 93, 53, 0)
    rect(75, 42, 85, 52, 3)
    rect(76, 43, 84, 50, 0)
    rect(72, 53, 88, 56, 1)
    for x in (74, 78, 82, 86):
        line(x, 56, 80 + (x - 80) // 2, 66, 3)
    line(76, 61, 84, 61, 3)
    line(78, 66, 82, 66, 3)
    # Wall stripe and double doors at the back of the gym.
    rect(20, 77, 140, 80, 1)
    rect(67, 80, 93, 105, 2)
    rect(69, 82, 91, 104, 0)
    rect(79, 82, 81, 104, 2)
    rect(72, 86, 77, 93, 3)
    rect(83, 86, 88, 93, 3)
    rect(76, 97, 78, 99, 3)
    rect(82, 97, 84, 99, 3)
    # Side-wall sports banners and stepped wooden bleachers.
    for x in (3, 147):
        rect(x, 27, x + 10, 56, 1)
        rect(x + 2, 30, x + 8, 33, 3)
        rect(x + 4, 35, x + 6, 48, 3)
        line(x, 56, x + 5, 61, 1)
        line(x + 9, 56, x + 5, 61, 1)
    for y, width in ((74, 15), (83, 20), (92, 25), (101, 30)):
        rect(0, y, width, y + 4, 3)
        rect(160 - width, y, 160, y + 4, 3)
        rect(0, y + 4, width, y + 8, 0)
        rect(160 - width, y + 4, 160, y + 8, 0)
    # The floor occupies the lower half of the room, under the dancers.
    rect(0, 110, 160, 192, 3)
    line(0, 109, 30, 105, 2)
    line(30, 105, 130, 105, 2)
    line(130, 105, 159, 109, 2)
    # Long parquet joints converge toward the far wall.
    for x in range(-160, 321, 24):
        line(80 + (x - 80) // 4, 110, x, 191, 0)
    for y in (116, 125, 138, 156, 180):
        rect(0, y, 160, y + 1, 0)
    # Court perimeter and center line; ellipse reads correctly with wide pixels.
    line(26, 114, 3, 184, 2)
    line(134, 114, 157, 184, 2)
    line(3, 184, 157, 184, 2)
    line(26, 114, 134, 114, 2)
    line(80, 114, 80, 184, 2)
    for degree in range(360):
        theta = degree * math.pi / 180
        x, y = round(80 + 25 * math.cos(theta)), round(151 + 15 * math.sin(theta))
        p[y * 160 + x] = 2
    # Far key and free-throw semicircle.
    line(66, 114, 60, 134, 1)
    line(94, 114, 100, 134, 1)
    line(60, 134, 100, 134, 1)
    for degree in range(181):
        theta = degree * math.pi / 180
        x, y = round(80 + 20 * math.cos(theta)), round(134 + 8 * math.sin(theta))
        p[y * 160 + x] = 1
    return bytes(p)
