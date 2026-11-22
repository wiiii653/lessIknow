"""School encounter artwork and music-clock staging."""

from pathlib import Path

from gym_practice import PRACTICE_TICK, PRACTICE_SCENE
from music_timing import tick_at_bar
from scene_palettes import ART_PALETTE

# The opening scene keeps its established camera framing and timing.
GIRL_PORTRAIT_SCENE = 14
SCHOOL_PORTRAIT_TICK = tick_at_bar(19, 2)
SCHOOL_PORTRAIT_END = tick_at_bar(11)
WHISTLE_START = tick_at_bar(13)  # after the foreground pass
WHISTLE_END = tick_at_bar(15)  # arrival at the doorway
SCHOOL_PHASES = ((tick_at_bar(8), 8), (SCHOOL_PORTRAIT_TICK, GIRL_PORTRAIT_SCENE),
                 (SCHOOL_PORTRAIT_END, 8), (tick_at_bar(12), 9),
                 (tick_at_bar(13), 10), (tick_at_bar(14), 11),
                 (tick_at_bar(15), 12), (PRACTICE_TICK, PRACTICE_SCENE))
# (left, top, width, height), in the 160x64 school artwork's coordinates.
# The foreground crops at the waist. The distant poses place the soles
# along the sloping pavement and end at the doorway sill.
GIRL_PLACEMENTS = ((0, 0, 96, 128), (43, 19, 33, 44),
                   (60, 28, 21, 28), (75, 38, 12, 16))
# Bright running stitches (#) and a few darker thread ends (+).
JACKET_BADGE = (
    "#....# .#........#+ #....# ####..",
    ".#..#. .#+......#.. .#..#. #.....",
    "..##.. .#......#... ..##.. ###...",
    "..##.. .#.....##### ..##.. #.....",
    ".#..#. .#+......#.. .#..#. #.....",
    "#....# .####...#... #....# ####..",
    "+..... ..+.+..+.... .....+ .....+",
)
JACKET_THREAD_INKS = {"#": 3, "+": 1}
JACKET_BADGE_ORIGIN = (30, 33)
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
    return min(range(4), key=lambda i: sum((rgb[c] - ART_PALETTE[i][c]) ** 2 for c in range(3)))


def load_rgb(path):
    data = Path(path).read_bytes()
    if len(data) != 160 * 64 * 3:
        raise ValueError('school artwork must be 160x64 RGB')
    return bytearray(color(data[i:i + 3]) for i in range(0, len(data), 3))


def expand(pixels):
    return bytes(pixels[(y // 3) * 160 + x] for y in range(192) for x in range(160))


def boy_poses():
    """Forward gaze, turn, then puckered lips while she approaches the doorway."""
    from arena_art import portrait
    turned=portrait(load_rgb('build/school.rgb'))
    poses=[]
    for name in ('build/school-neutral.rgb',None,'build/school-front.rgb'):
        canvas=bytearray(turned)
        if name:
            source=portrait(load_rgb(name),'neutral' if name=='build/school-neutral.rgb' else 'whistle')
            for y in range(64):
                canvas[y*160+104:(y+1)*160]=source[y*160+104:(y+1)*160]
        if name=='build/school-front.rgb':
            # Remove the old source image's whistle rays outside the face.
            from arena_art import background,inside,PORTRAIT_OUTLINES
            bg=background()
            for y in range(31,43):
                for x in range(104,116):
                    if not inside(x+.5,y+.5,PORTRAIT_OUTLINES['whistle']):
                        canvas[y*160+x]=bg[y*200+x]
            # A clean, deliberately drawn puckered mouth survives 160x64.
            lips=(".##.","#...",".##.","#...",".##.")
            for y,row in enumerate(lips):
                for x,cell in enumerate(row):canvas[(33+y)*160+119+x]=0 if cell=='#' else 3
        poses.append(expand(canvas))
    return tuple(poses)


def load_girl(path, width, height):
    rgba = Path(path).read_bytes()
    if len(rgba) != width * height * 4:
        raise ValueError(f'{path} must contain {width}x{height} RGBA')
    girl = bytearray(color(rgba[i:i + 3]) for i in range(0, len(rgba), 4))
    mask = bytes(rgba[i + 3] >= 128 for i in range(0, len(rgba), 4))
    return girl, mask


def party_girl():
    """The untouched v330 back sprite, including the party jacket badge."""
    from arena_art import FUJI_ORIGIN, logo

    girl, mask = load_girl('build/north-girl.rgba', 48, 64)
    for y in range(14, 24):
        girl[y * 48 + 14:y * 48 + 33] = b'\x02' * 19
    logo(girl, 48, *FUJI_ORIGIN)
    return bytes(girl), mask


def foreground_girl():
    """Sample the original party drawing on the encounter's 160x64 grid."""
    width, height = GIRL_PLACEMENTS[0][2:]
    girl, mask = load_girl('build/north-girl-close.rgba', width, height)
    # Clear the source lettering while retaining the folds and outline.
    # Leave the jacket's folds and outline at their sampled resolution.
    for y in range(32, 41):
        for x in range(30, 64):
            at = y * width + x
            if mask[at] and girl[at] == 3:
                girl[at] = 2
    left, top = JACKET_BADGE_ORIGIN
    for y, row in enumerate(JACKET_BADGE, top):
        for x, ink in enumerate(row, left):
            if ink in JACKET_THREAD_INKS:
                girl[y * width + x] = JACKET_THREAD_INKS[ink]
    return girl, mask


def story_frames():
    neutral, turned, whistle = boy_poses()
    close_art = foreground_girl()
    distant_inks, distant_mask = party_girl()
    distant_inks = bytearray(distant_inks)
    # Use the same blue ink as the earlier side view. Retain the black
    # silhouette and leave dark folds at the waist and hem.
    for y in range(31, 38):
        middle = y * 48
        for x in range(15, 34):
            at = middle + x
            if all(distant_mask[at+step] and distant_inks[at+step] in (0, 2)
                   for step in (-1, 0, 1)) and x not in (19, 29):
                distant_inks[at] = 2
    # At this scale only the separator is legible.
    for y in range(15, 24):
        distant_inks[y * 48 + 17:y * 48 + 30] = b'\x02' * 13
    for x, y in ((24, 16), (23, 17), (22, 18), (23, 18), (24, 18),
                 (23, 19), (22, 20), (21, 21)):
        distant_inks[y * 48 + x] = 3
    distant_art = distant_inks, distant_mask
    # First two encounter views face forward. He turns as she passes in
    # the foreground, then whistles as she recedes toward the doorway.
    frames = [turned, neutral]
    for index, (left, top, width, height) in enumerate(GIRL_PLACEMENTS):
        canvas = bytearray(whistle if index in (1,2) else turned)
        girl, mask = close_art if index == 0 else distant_art
        source_width, source_height = (width, height) if index == 0 else (48, 64)
        for y in range(min(height,64-top)):
            source_row = ((2*y+1) * source_height // (2*height)) * source_width
            for x in range(width):
                source = source_row + (2*x+1) * source_width // (2*width)
                target_x, target_y = left + x, top + y
                if 0 <= target_x < 104 and 0 <= target_y < 64 and mask[source]:
                    for dy in range(3):
                        canvas[(target_y*3+dy)*160+target_x] = girl[source]
        frames.append(bytes(canvas))
    return frames


def girl_front_pixels():
    return expand(load_rgb("build/school-girl-side-v033.rgb"))
