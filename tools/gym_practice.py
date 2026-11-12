"""Basketball practice and stretching beside the wall bars, 30–45 seconds."""

import math
from gym_background import gym_pixels
from music_timing import tick_at_bar
from scene_palettes import ART_PALETTE

PRACTICE_TICK = tick_at_bar(16)
PRACTICE_SCENE = 13
# The basketball travels from the shooter's hands through an arc to the hoop,
# then drops and bounces on the court before the next shot.
BALL_PATH = tuple((round(57 + 23 * t / 15),
                   round(67 - 12 * t / 15 - 24 * math.sin(math.pi * t / 15)))
                  for t in range(16)) + tuple(
    (80 + t // 3, round(58 + 80 * (t / 9) ** 2) if t < 10 else
     round(138 - 22 * math.sin((t - 9) / 6 * math.pi))) for t in range(16))


PRACTICE_CUTS = (tick_at_bar(16), tick_at_bar(56, 3), tick_at_bar(64, 3))


def practice_pixels():
    from pathlib import Path
    # Three 160x64 shots share a single 8 KiB frame slot.
    palette = ART_PALETTE
    rgb = Path('build/practice-storyboard.rgb').read_bytes()
    if len(rgb) != 160 * 192 * 3:
        raise ValueError('expected 160x192 RGB storyboard')
    pixels=bytearray(min(range(4), key=lambda j: sum((rgb[i+c]-palette[j][c])**2 for c in range(3)))
                 for i in range(0, len(rgb), 3))
    # The illustrated ball is replaced by the moving hardware ball in shot 2.
    for y in range(65,75):
        for x in range(103,118):
            pixels[y*160+x]=0
    return bytes(pixels)


def practice_shot(tick):
    shot = sum(tick >= cut for cut in PRACTICE_CUTS[1:])
    pixels = practice_pixels()
    return bytes(pixels[(shot*64+y//3)*160+x] for y in range(192) for x in range(160))
