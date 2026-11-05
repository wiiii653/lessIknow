"""School encounter artwork and music-clock staging."""

from pathlib import Path

from build_sequence import PALETTE
from gym_practice import PRACTICE_TICK, PRACTICE_SCENE
from music_timing import tick_at_bar

# The whole school scene still lasts 15–45 seconds. The girl first appears
# in the left foreground, then recedes toward the school's entrance.
GIRL_PORTRAIT_SCENE = 14
SCHOOL_PORTRAIT_TICK = tick_at_bar(19, 2)
SCHOOL_PORTRAIT_END = tick_at_bar(11)
SCHOOL_PHASES = ((tick_at_bar(8), 8), (SCHOOL_PORTRAIT_TICK, GIRL_PORTRAIT_SCENE),
                 (SCHOOL_PORTRAIT_END, 8), (tick_at_bar(12), 9),
                 (tick_at_bar(13), 10), (tick_at_bar(14), 11),
                 (tick_at_bar(15), 12), (PRACTICE_TICK, PRACTICE_SCENE))
# (left, top, width, height), in the 160x64 school artwork's coordinates.
# The first placement is twice full height: the bottom crops at the waist.
# Foot positions approach the school steps at approximately (66, 46).
GIRL_PLACEMENTS = ((0, 0, 96, 128), (30, 11, 36, 48),
                   (44, 22, 24, 32), (58, 32, 12, 16))
# Compact lettering fits entirely on the teal back panel at source resolution.
NORTH_ORIGIN = (14, 15)
NORTH_ADVANCE = 4
NORTH = {
    'N': ('101', '111', '111', '101'),
    'O': ('111', '101', '101', '111'),
    'R': ('110', '101', '110', '101'),
    'T': ('111', '010', '010', '010'),
    'H': ('101', '111', '101', '101'),
}


def color(rgb):
    return min(range(4), key=lambda i: sum((rgb[c] - PALETTE[i][c]) ** 2 for c in range(3)))


def load_rgb(path):
    data = Path(path).read_bytes()
    if len(data) != 160 * 64 * 3:
        raise ValueError('school artwork must be 160x64 RGB')
    return bytearray(color(data[i:i + 3]) for i in range(0, len(data), 3))


def expand(pixels):
    return bytes(pixels[(y // 3) * 160 + x] for y in range(192) for x in range(160))


def story_frames():
    after = load_rgb('build/school.rgb')
    front_art = load_rgb('build/school-front.rgb')
    front = bytearray(after)
    # Match the court exactly between views; only the portrait changes.
    for y in range(64):
        front[y * 160 + 104:(y + 1) * 160] = front_art[y * 160 + 104:(y + 1) * 160]
    rgba = Path('build/north-girl.rgba').read_bytes()
    if len(rgba) != 48 * 64 * 4:
        raise ValueError('girl sprite must be 48x64 RGBA')
    girl = bytearray(color(rgba[i:i + 3]) for i in range(0, len(rgba), 4))
    mask = bytearray(rgba[i + 3] >= 160 for i in range(0, len(rgba), 4))
    # Hand-set bitmap lettering survives reduction to Atari's logical pixels.
    for y in range(15, 19):
        for x in range(14, 33):
            girl[y * 48 + x] = 2
    for index, letter in enumerate('NORTH'):
        for y, row in enumerate(NORTH[letter]):
            for x, bit in enumerate(row):
                if bit == '1':
                    girl[(NORTH_ORIGIN[1] + y) * 48 + NORTH_ORIGIN[0] + index * NORTH_ADVANCE + x] = 3
    frames = [expand(after), expand(front)]
    for index, (left, top, width, height) in enumerate(GIRL_PLACEMENTS):
        canvas = bytearray(front if index == 0 else after)
        for y in range(height):
            source_y = y * 64 // height
            for x in range(width):
                source_x = x * 48 // width
                source = source_y * 48 + source_x
                target_x, target_y = left + x, top + y
                if 0 <= target_x < 104 and 0 <= target_y < 64 and mask[source]:
                    canvas[target_y * 160 + target_x] = girl[source]
        frames.append(expand(canvas))
    return frames


def girl_front_pixels():
    return expand(load_rgb("build/school-girl-side-v033.rgb"))
