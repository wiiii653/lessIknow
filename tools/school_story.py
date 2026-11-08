"""School encounter artwork and music-clock staging."""

from pathlib import Path

from build_sequence import PALETTE
from gym_practice import PRACTICE_TICK, PRACTICE_SCENE
from music_timing import tick_at_bar

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
# The first placement is twice full height: the bottom crops at the waist.
GIRL_PLACEMENTS = ((0, 0, 96, 128), (44, 11, 36, 48),
                   (62, 22, 24, 32), (76, 36, 12, 16))
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


def boy_poses():
    """Forward gaze, turn, then puckered lips while she approaches the doorway."""
    from arena_art import portrait
    turned=portrait(load_rgb('build/school.rgb'))
    poses=[]
    for name in ('build/school-neutral.rgb',None,'build/school-front.rgb'):
        canvas=bytearray(turned)
        if name:
            source=portrait(load_rgb(name))
            for y in range(64):
                canvas[y*160+104:(y+1)*160]=source[y*160+104:(y+1)*160]
        if name=='build/school-front.rgb':
            # Remove the old source image's whistle rays outside the face.
            from arena_art import background
            bg=background()
            for y in range(31,43):
                for x in range(104,116):canvas[y*160+x]=bg[y*200+x]
            # A clean, deliberately drawn puckered mouth survives 160x64.
            lips=(".##.","#...",".##.","#...",".##.")
            for y,row in enumerate(lips):
                for x,cell in enumerate(row):canvas[(33+y)*160+119+x]=0 if cell=='#' else 3
        poses.append(expand(canvas))
    return tuple(poses)


def story_frames():
    from arena_art import logo, FUJI_ORIGIN
    neutral,turned,whistle=boy_poses()
    rgba=Path('build/north-girl.rgba').read_bytes()
    if len(rgba)!=48*64*4:
        raise ValueError('girl sprite must be 48x64 RGBA')
    girl=bytearray(color(rgba[i:i+3]) for i in range(0,len(rgba),4))
    mask=bytearray(rgba[i+3]>=128 for i in range(0,len(rgba),4))
    for y in range(14,24):
        for x in range(14,33):girl[y*48+x]=2
    logo(girl,48,*FUJI_ORIGIN)
    # First two encounter views face forward. He turns as she passes in
    # the foreground, then whistles as she recedes toward the doorway.
    frames = [turned, neutral]
    for index, (left, top, width, height) in enumerate(GIRL_PLACEMENTS):
        canvas = bytearray(whistle if index in (1,2) else turned)
        for y in range(height):
            source_y = y * 64 // height
            for x in range(width):
                source_x = x * 48 // width
                source = source_y * 48 + source_x
                target_x, target_y = left + x, top + y
                if 0 <= target_x < 104 and 0 <= target_y < 64 and mask[source]:
                    for dy in range(3):
                        canvas[(target_y*3+dy)*160+target_x] = girl[source]
        frames.append(bytes(canvas))
    return frames


def girl_front_pixels():
    return expand(load_rgb("build/school-girl-side-v033.rgb"))
