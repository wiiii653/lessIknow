"""Full-screen animated GTIA 11 plasma with hue-only lettering.

Sixteen 80x64 plasma frames, six cumulative text masks and spatial
dissolve and lettering-transition masks occupy nine expansion banks. The CPU combines one frame with a mask into an inactive
unbanked framebuffer; ANTIC repeats each line three times.
"""
import math
from build_sequence import Code, TITLE_TICK
from school_portrait_bank import bank_value
from music_timing import tick_at_beat

SIZE = 1792
STATE = 0x83e0
FRAME_BYTES = 2560
FIRST_BANK = 40
MASK_BANK = 44
FADE_BANK = 45
TRANSITION_BANK = 47
TRANSITION_START = TITLE_TICK - 128
BAYER_4 = (0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5)

# Compact slab-serif capitals, hand-drawn for the 80x64 GTIA grid. These
# blocky forms echo the multicoloured, extruded title in the reference image.
TITLE_GLYPHS = {
    'A': ('01110','11011','11011','11111','11011','11011','11011'),
    'B': ('11110','11011','11011','11110','11011','11011','11110'),
    'E': ('11111','11000','11000','11110','11000','11000','11111'),
    'H': ('11011','11011','11011','11111','11011','11011','11011'),
    'I': ('11111','01110','01110','01110','01110','01110','11111'),
    'K': ('11011','11011','11110','11100','11110','11011','11011'),
    'L': ('11000','11000','11000','11000','11000','11000','11111'),
    'M': ('11011','11111','11111','11011','11011','11011','11011'),
    'N': ('10001','11001','11101','10101','10111','10011','10001'),
    'O': ('01110','11011','11011','11011','11011','11011','01110'),
    'P': ('11110','11011','11011','11110','11000','11000','11000'),
    'R': ('11110','11011','11011','11110','11100','11110','11011'),
    'S': ('01111','11000','11000','01110','00011','00011','11110'),
    'T': ('11111','11111','01110','01110','01110','01110','01110'),
    'W': ('11011','11011','11011','11011','11111','11111','01010'),
    ' ': ('00000',)*7,
}


def dither_hue(value, x, y):
    """Quantize the plasma field to hues 2..7 with a fixed ordered raster.

    The centered threshold mixes adjacent hues only near their boundaries.
    Keeping the raster fixed in screen space avoids random frame flicker and
    leaves bit 3 available for the existing hue-only lettering mask.
    """
    level = (value + 2.55) * 6 / 5.1
    threshold = (BAYER_4[(y & 3) * 4 + (x & 3)] + .5) / 16 - .5
    return 2 + int(min(5, max(0, level + threshold)))


# Stable, saturated face colours; the offset shadow uses neutral hue zero.
LETTER_HUES = (9, 11, 13, 10, 12, 14, 15, 9)

# All coordinates below are source GTIA pixels (80x64). A source row is
# displayed three times. Keep the title and its extrusion above the skyline.
CARDS = ((('TAME', 2, 0, None), ('IMPALA', 2, 48, None)),
         (('I KNOW', 2, 33, None), ('THE BETTER', 1, 66, None),
          ('THE LESS', 1, 0, None)))
CARD_Y_SCALE = (2,1)
ZURAW_LEFT, ZURAW_TOP = 22, 35
ZURAW_WIDTH, ZURAW_HEIGHT = 36, 29


def zuraw_artwork():
    """Hand-drawn Motlawa facade: round brick towers and projecting timber.

    Shape reference: National Maritime Museum / Visit Gdansk. Contrast comes
    from black keylines, cyan brickwork, warm tiles and golden timber edges.
    Source pixels are wider than tall in the corrected Atari preview.
    """
    p=[[None]*40 for _ in range(32)]
    def dot(x,y,ink):
        if 0<=x<40 and 0<=y<32:p[y][x]=ink
    def line(x0,y0,x1,y1,ink):
        n=max(abs(x1-x0),abs(y1-y0),1)
        for i in range(n+1):dot(round(x0+(x1-x0)*i/n),round(y0+(y1-y0)*i/n),ink)
    def polygon(points,ink,outline=0):
        for y in range(32):
            for x in range(40):
                inside=False;px,py=x+.5,y+.5
                for (ax,ay),(bx,by) in zip(points,points[1:]+points[:1]):
                    if (ay>py)!=(by>py) and px<(bx-ax)*(py-ay)/(by-ay)+ax:inside=not inside
                if inside:dot(x,y,ink)
        for a,b in zip(points,points[1:]+points[:1]):line(*a,*b,outline)
    # Continuous rear gatehouse wall: the towers attach to the timber core,
    # with no slit of moving plasma between the left tower and the crane.
    polygon([(13,14),(31,14),(31,30),(13,30)],8)
    # Rounded, shaded masonry cylinders under steep red tiled roofs.
    for left,right,top in ((1,18,15),(28,38,16)):
        polygon([(left+1,top),(right-1,top),(right,top+2),(right,30),
                 (left,30),(left,top+2)],9)
        line(left+1,top+2,left+1,29,10)
        line(right-1,top+2,right-1,29,8)
        for y in range(top+3,30,3):
            for x in range(left+3,right-1):
                if (x+y//3)%4!=0:dot(x,y,10)
        for x,y in ((left+4,top+3),(right-4,top+10),(left+4,top+12)):
            line(x,y,x,y+2,0);dot(x+1,y+1,1)
    polygon([(0,16),(9,8),(19,16)],3)
    polygon([(27,17),(32,10),(39,17)],3)
    for x in range(2,19,3):line(9,9,x,15,2)
    for x in range(28,39,3):line(32,11,x,16,2)
    line(1,16,18,16,9);line(28,17,38,17,9)
    # Tall roof with the protruding gable clearly above the two towers.
    polygon([(14,10),(18,4),(25,1),(31,7),(28,10)],3)
    for x in (17,20,23):line(24,2,x,9,2)
    line(14,10,18,4,9)
    polygon([(18,10),(21,7),(29,8),(28,24),(19,25)],0)
    line(19,11,19,24,1);line(21,10,21,23,1);line(27,10,27,23,1)
    for y in (12,17,22):line(21,y,27,y,1)
    # Upper loading hood and lower flared housing: the historic crane's
    # recognisable two projections, rather than an industrial jib/gantry.
    polygon([(21,7),(25,4),(30,8),(30,10),(20,10)],0)
    line(21,7,25,4,9);line(26,5,29,8,1)
    line(24,8,26,8,15);line(25,10,25,24,0)
    polygon([(20,24),(28,24),(31,28),(28,29),(17,29)],0)
    line(20,24,18,28,1);line(28,24,30,28,1)
    line(20,28,28,28,1)
    # Open water gate, hoisting rope, quay and slim cool edge.
    polygon([(18,29),(27,29),(27,31),(18,31)],0)
    line(23,29,23,30,15)
    line(0,31,39,31,9)
    line(25,0,25,1,1);dot(26,0,1)
    # Slightly smaller, categorical pixel resampling; preserve roof peak and quay.
    return tuple(tuple(p[round(y*31/(ZURAW_HEIGHT-1))][round(x*39/(ZURAW_WIDTH-1))]
                       for x in range(ZURAW_WIDTH)) for y in range(ZURAW_HEIGHT))


ZURAW = zuraw_artwork()


def zuraw_hue(x,y):
    if ZURAW_TOP<=y<64 and ZURAW_LEFT<=x<ZURAW_LEFT+ZURAW_WIDTH:
        return ZURAW[y-ZURAW_TOP][x-ZURAW_LEFT]
    return None


def skyline_hue(x,y):
    """Return the static night skyline hue, or None for unobstructed sky."""
    crane=zuraw_hue(x,y)
    if crane is not None:return crane
    if y>=54:
        roof=(57,55,58,56,58,57,55,57,54,58)[x//8]
        if y>=roof:
            return 10 if y>roof and x%8 in (2,5) and y%3==0 else 0
    return None


def letter_ink(code, phase=0):
    return LETTER_HUES[(code + phase) & 7] if code & 8 else 0


def compose_byte(background, mask, phase=0):
    result=0
    for shift in (4,0):
        code=(mask >> shift) & 15
        hue=letter_ink(code, phase) if code else (background >> shift) & 15
        result |= hue << shift
    return result


def artwork():
    frames = []
    for phase in range(16):
        t = phase * math.tau / 16
        image = bytearray()
        for y in range(64):
            for x in range(0, 80, 2):
                pixels = []
                for xx in (x, x + 1):
                    # Overlapping moving radial waves produce rounded islands
                    # which merge and split, rather than scrolling stripes.
                    x1 = 24 + 14 * math.sin(t)
                    y1 = 26 + 11 * math.cos(t)
                    x2 = 54 + 15 * math.cos(t)
                    y2 = 35 + 10 * math.sin(t)
                    d1 = math.hypot((xx-x1)*.72, y-y1)
                    d2 = math.hypot((xx-x2)*.72, y-y2)
                    value = math.sin(d1*.19 - t) + math.cos(d2*.18 + t) + .55*math.sin(xx*.09 + y*.11 + t)
                    hue=dither_hue(value, xx, y)
                    # Half-screen historic crane below the compact lettering.
                    # Composited text always wins over these background pixels.
                    city=skyline_hue(xx,y)
                    if city is not None:hue=city
                    pixels.append(hue)
                image.append((pixels[0] << 4) | pixels[1])
        frames.append(bytes(image))
    # Every plasma bank has the same four colour lookup tables in its tail;
    # composition can read them without switching away from the current frame.
    color_tables = bytes((letter_ink(value >> 4, phase) << 4 if value >> 4 else 0) |
                         (letter_ink(value & 15, phase) if value & 15 else 0)
                         for phase in range(4) for value in range(256))
    banks = [(b''.join(frames[n:n+4]) + color_tables).ljust(16384, b'\0')
             for n in range(0, 16, 4)]
    masks = []
    # Large two-line artist card; taller, centred song-title lettering.
    for card,rows in enumerate(CARDS):
        sy=CARD_Y_SCALE[card]
        for stage in (1, 2, 3):
            mask = bytearray(FRAME_BYTES)
            for text, sx, top, fixed_left in rows[:stage]:
                advance = 7 if fixed_left is not None else 5 * sx + 3
                left = fixed_left if fixed_left is not None else (80 - (len(text) * advance - 3)) // 2
                letters = []
                for i, char in enumerate(text):
                    pixels = set()
                    for gy, line in enumerate(TITLE_GLYPHS[char]):
                        for gx, bit in enumerate(line):
                            if bit == '1':
                                for dy in range(sy):
                                    for dx in range(sx):
                                        pixels.add((left + i*advance + gx*sx + dx,
                                                    top//3 + gy*sy + dy))
                    letters.append((i, pixels))

                def ink(x, y, hue_mask):
                    if 0 <= x < 80 and 0 <= y < 64:
                        offset = y*40 + x//2
                        if x & 1:
                            mask[offset] = (mask[offset] & 0xf0) | hue_mask
                        else:
                            mask[offset] = (mask[offset] & 0x0f) | (hue_mask << 4)

                # Offset extrusion separates the letters from the plasma.
                for i, pixels in letters:
                    shadow = 1
                    for x, y in pixels:
                        for dx, dy in ((1, 1), (2, 1), (2, 2)):
                            ink(x+dx, y+dy, shadow)
                for i, pixels in letters:
                    face = 8 | ((i * 3) & 7)
                    for x, y in pixels:
                        ink(x, y, face)
            masks.append(bytes(mask))
    fade_frames = []
    for level in range(1, 7):
        frame = bytearray()
        for y in range(64):
            for x in range(0, 80, 2):
                bits = []
                for xx in (x, x+1):
                    # Broad, irregular islands recede instead of a straight wipe.
                    field = (math.sin(xx*.11 + y*.08) + math.cos(y*.19 - xx*.045)
                             + .5*math.sin(xx*.23 - y*.13))
                    raster = BAYER_4[(y % 4)*4 + xx % 4] / 16
                    rank = max(0, min(7, int(((field + 2.5) / 5 * .65 + raster * .35) * 8)))
                    bits.append(15 if rank < level else 0)
                frame.append((bits[0] << 4) | bits[1])
        fade_frames.append(bytes(frame))
    fade_banks = [b''.join(fade_frames[n:n+4]).ljust(16384, b'\0') for n in (0, 4)]
    # Pixel-ordered transition from the full artist to the first title line.
    transition_frames = []
    for step in range(8):
        old, new = masks[1], masks[3]
        frame = bytearray(FRAME_BYTES)
        for y in range(64):
            for x in range(80):
                offset = y * 40 + x // 2
                nibble = 0xf0 if x % 2 == 0 else 0x0f
                source = new if BAYER_4[(y % 4)*4 + x % 4] // 2 <= step else old
                frame[offset] |= source[offset] & nibble
        transition_frames.append(bytes(frame))
    # Each word/line first resolves through a half-density ordered raster.
    # The four extra masks fit in the unused tails of the transition banks.
    reveal_frames = []
    for old, new in ((bytes(FRAME_BYTES), masks[0]), (masks[0], masks[1]),
                     (masks[3], masks[4]), (masks[4], masks[5])):
        frame = bytearray(FRAME_BYTES)
        for y in range(64):
            for x in range(80):
                offset = y*40 + x//2
                nibble = 0xf0 if x % 2 == 0 else 0x0f
                source = new if BAYER_4[(y % 4)*4 + x % 4] < 8 else old
                frame[offset] |= source[offset] & nibble
        reveal_frames.append(bytes(frame))
    transition_banks = [
        (b''.join(transition_frames[n:n+4]) + b''.join(reveal_frames[n//2:n//2+2])).ljust(16384, b'\0')
        for n in (0, 4)
    ]
    return banks + [b''.join(masks).ljust(16384, b'\0')] + fade_banks + transition_banks


def build(origin, blank):
    del blank
    c = Code(origin)
    def a(op, addr): c.emit(op, addr & 255, addr >> 8)
    c.label('prepare')
    a(0xad, STATE); c.emit(0xc9, 2); c.branch(0x90, 'intro')
    c.emit(0xa9, 0, 0x60)
    c.label('intro')
    # Relative time remains stable while the music tick is paused.
    a(0xad, STATE); c.branch(0xf0, 'artist')
    c.emit(0x38); a(0xad, STATE+2); c.emit(0xe9, TITLE_TICK & 255); a(0x8d, STATE+8)
    a(0xad, STATE+3); c.emit(0xe9, TITLE_TICK >> 8); a(0x8d, STATE+9); c.jump(0x4c, 'elapsed')
    c.label('artist')
    a(0xad, STATE+2); a(0x8d, STATE+8); a(0xad, STATE+3); a(0x8d, STATE+9)
    c.label('elapsed')
    c.emit(0xa9, 0); a(0x8d, STATE+1)
    # cache key: scene plus elapsed / 32 (47 phases per card).
    a(0xad, STATE+9); c.emit(0x0a, 0x0a, 0x0a); a(0x8d, STATE+29)
    a(0xad, STATE+8); c.emit(0x4a,0x4a,0x4a,0x4a,0x4a); a(0x0d, STATE+29); a(0x8d, STATE+29)
    # Fade only at the opening and after the final title, never at the cut.
    a(0xad, STATE); c.branch(0xd0, 'second_fade')
    a(0xad, STATE+29); c.emit(0xc9, 7); c.branch(0x90, 'save_fade')
    c.emit(0xa9, 7); c.jump(0x4c, 'save_fade')
    c.label('second_fade'); a(0xad, STATE+29); c.emit(0xc9, 39)
    c.branch(0xb0, 'save_fade'); c.emit(0xa9, 7)
    c.label('save_fade'); c.jump(0x8d, 'fade_phase')
    # Find the current musical beat using the same integer timing map as
    # the rest of the demo; a changed phase invalidates the render cache.
    c.emit(0xa2, 31)
    c.label('find_beat')
    a(0xad, STATE+3); c.jump(0xdd, 'beat_hi'); c.branch(0x90, 'previous_beat')
    c.branch(0xd0, 'beat_found')
    a(0xad, STATE+2); c.jump(0xdd, 'beat_lo'); c.branch(0xb0, 'beat_found')
    c.label('previous_beat'); c.emit(0xca); c.branch(0x10, 'find_beat')
    c.emit(0xa2, 0)
    c.label('beat_found'); c.emit(0x8a, 0x29, 3); c.jump(0x8d, 'color_phase')
    c.emit(0x0a, 0x09, 0x40); a(0x0d, STATE); a(0x8d, STATE+23)
    c.emit(0xa9, 1, 0x60)

    c.label('invalidate')
    a(0xad, STATE); c.emit(0xc9, 2); c.branch(0x90, 'invalidate_done')
    c.emit(0xa9, 0xff); c.jump(0x8d, 'mask_key')
    c.label('invalidate_done'); c.emit(0x60)

    c.label('draw')
    # Invalidate the dance/practice buffer cache, since both buffers are reused.
    c.emit(0xa9, 0xff); a(0x8d, STATE+24); a(0x8d, STATE+25)
    a(0xad, 0xd301); c.emit(0x48)
    # Across the card boundary, replace letter pixels in an ordered raster
    # while leaving the background phase and luminance continuous.
    c.emit(0x38); a(0xad, STATE+2); c.emit(0xe9, TRANSITION_START & 255); a(0x8d, STATE+11)
    a(0xad, STATE+3); c.emit(0xe9, TRANSITION_START >> 8)
    c.branch(0xd0, 'normal_stage')
    a(0xad, STATE+11); c.emit(0x4a,0x4a,0x4a,0x4a,0x4a,0x18,0x69,7)
    a(0x8d, STATE+10); c.jump(0x4c, 'mask_key_ready')
    c.label('normal_stage')
    a(0xad, STATE+9); c.emit(0xc9, 4); c.branch(0x90, 'stage_ok'); c.emit(0xa9, 3)
    c.label('stage_ok'); a(0x8d, STATE+10)
    a(0xad, STATE); c.branch(0xf0, 'maybe_reveal')
    a(0xad, STATE+10); c.branch(0xd0, 'title_nonzero'); c.emit(0xa9, 1)
    c.label('title_nonzero'); c.emit(0x18,0x69,3); a(0x8d, STATE+10)
    c.label('maybe_reveal'); a(0xad, STATE+8); c.emit(0xc9,64); c.branch(0xb0,'mask_key_ready')
    a(0xae, STATE+10); c.jump(0xbd,'reveal_key'); c.branch(0xf0,'mask_key_ready')
    a(0x8d, STATE+10)
    c.label('mask_key_ready'); a(0xad, STATE+10); c.jump(0xcd, 'mask_key')
    c.branch(0xd0, 'mask_changed'); c.jump(0x4c, 'mask_done')
    c.label('mask_changed'); c.jump(0x8d, 'mask_key'); a(0xad, STATE+10); c.branch(0xf0, 'clear_mask')
    c.emit(0xc9, 15); c.branch(0xb0, 'reveal_mask')
    c.emit(0xc9, 7); c.branch(0xb0, 'transition_mask')
    a(0xad, bank_value(MASK_BANK)); a(0x8d, 0xd301)
    a(0xad, STATE+10); c.emit(0x38,0xe9,1,0xaa)
    c.jump(0xbd, 'mask_high'); c.jump(0x4c, 'mask_source_selected')
    c.label('transition_mask')
    a(0xad, STATE+10); c.emit(0x38,0xe9,7,0x48,0x4a,0x4a,0xaa)
    a(0xbd, bank_value(TRANSITION_BANK)); a(0x8d,0xd301)
    c.emit(0x68,0x29,3,0xaa); c.jump(0xbd,'frame_high')
    c.jump(0x4c, 'mask_source_selected')
    c.label('reveal_mask')
    a(0xad, STATE+10); c.emit(0x38,0xe9,15,0x48,0x4a,0xaa)
    a(0xbd, bank_value(TRANSITION_BANK)); a(0x8d,0xd301)
    c.emit(0x68,0x29,1,0xaa); c.jump(0xbd,'reveal_high')
    c.label('mask_source_selected'); c.jump(0x8d, 'mask_source_high')
    c.emit(0xa2, 0, 0xa0, 10)
    c.label('mask_copy')
    c.label('mask_source'); c.emit(0xbd,0,0x40)
    c.label('mask_dest'); c.emit(0x9d,0,0xa0,0xe8); c.branch(0xd0,'mask_copy')
    c.jump(0xee,'mask_source_high'); c.jump(0xee,'mask_dest_high'); c.emit(0x88); c.branch(0xd0,'mask_copy')
    c.emit(0xa9, 0xa0); c.jump(0x8d,'mask_dest_high'); c.jump(0x4c,'mask_done')
    c.label('clear_mask'); c.emit(0xa9,0,0xa2,0)
    c.label('clear_loop')
    for page in range(10): a(0x9d,0xa000+page*256)
    c.emit(0xe8); c.branch(0xd0,'clear_loop')
    c.label('mask_done')
    # Select one of sixteen 2560-byte frames across four bank windows.
    a(0xad,STATE+3); c.emit(0x29,1,0x0a,0x0a,0x0a); a(0x8d,STATE+12)
    a(0xad,STATE+2); c.emit(0x4a,0x4a,0x4a,0x4a,0x4a); a(0x0d,STATE+12)
    c.emit(0x29,15,0x48,0x4a,0x4a,0xaa)
    a(0xbd,bank_value(FIRST_BANK)); a(0x8d,0xd301)
    c.emit(0x68,0x29,3,0xaa); c.jump(0xbd,'frame_high'); a(0x8d,STATE+12)
    # The inactive display list determines which framebuffer can be written.
    a(0xad,STATE+6); c.emit(0x29,4,0x4a,0x4a,0x49,1,0xaa,0x48)
    c.emit(0x0a,0x0a,0x0a,0x0a,0x0a,0x18,0x69,0x90); a(0x8d,STATE+13)
    # Patch high bytes of the ten page operations, then composite 2560 bytes.
    for page in range(10):
        a(0xad,STATE+12); c.emit(0x18,0x69,page); c.jump(0x8d,f'src_hi{page}')
        a(0xad,STATE+13); c.emit(0x18,0x69,page); c.jump(0x8d,f'dst_hi{page}')
    c.jump(0xad,'color_phase'); c.emit(0x18,0x69,0x68)
    for page in range(10): c.jump(0x8d,f'color_hi{page}')
    c.emit(0xa2,0)
    c.label('compose')
    for page in range(10):
        a(0xbd,0xa000+page*256);c.emit(0xa8)
        c.jump(0xb9,'letter_keep')
        c.label(f'src{page}'); c.emit(0x3d,0,0x40)
        c.label(f'color{page}'); c.emit(0x19,0,0x68)
        c.labels[f'color_hi{page}']=c.labels[f'color{page}']+2
        c.label(f'dst{page}'); c.emit(0x9d,0,0x90)
        c.labels[f'src_hi{page}']=c.labels[f'src{page}']+2
        c.labels[f'dst_hi{page}']=c.labels[f'dst{page}']+2
    c.emit(0xe8);c.branch(0xf0,'composed');c.jump(0x4c,'compose')
    c.label('composed')
    # During both fades, AND a spatial dissolve mask over the composited
    # image. The brightness ramp also reaches black at either boundary.
    c.jump(0xad, 'fade_phase'); c.emit(0xc9, 7); c.branch(0x90, 'fade_level')
    c.emit(0xc9, 39); c.branch(0xb0, 'fade_out'); c.jump(0x4c, 'fade_done')
    c.label('fade_out')
    c.emit(0x49, 0xff, 0x18, 0x69, 47)  # level = 46 - phase
    c.label('fade_level'); c.emit(0xc9, 1); c.branch(0xb0, 'fade_nonzero'); c.jump(0x4c, 'fade_done')
    c.label('fade_nonzero'); c.emit(0xc9, 7); c.branch(0x90, 'fade_start'); c.jump(0x4c, 'fade_done')
    c.label('fade_start')
    c.emit(0x38,0xe9,1,0x48,0x4a,0x4a,0xaa)
    a(0xbd,bank_value(FADE_BANK)); a(0x8d,0xd301)
    c.emit(0x68,0x29,3,0xaa); c.jump(0xbd,'frame_high'); a(0x8d,STATE+12)
    for page in range(10):
        a(0xad,STATE+12); c.emit(0x18,0x69,page); c.jump(0x8d,f'fade_hi{page}')
        a(0xad,STATE+13); c.emit(0x18,0x69,page); c.jump(0x8d,f'fade_read_hi{page}'); c.jump(0x8d,f'fade_dst_hi{page}')
    c.emit(0xa2,0)
    c.label('fade_loop')
    for page in range(10):
        c.label(f'fade_read{page}'); c.emit(0xbd,0,0x90)
        c.label(f'fade{page}'); c.emit(0x3d,0,0x40)
        c.label(f'fade_dst{page}'); c.emit(0x9d,0,0x90)
        c.labels[f'fade_read_hi{page}']=c.labels[f'fade_read{page}']+2
        c.labels[f'fade_hi{page}']=c.labels[f'fade{page}']+2
        c.labels[f'fade_dst_hi{page}']=c.labels[f'fade_dst{page}']+2
    c.emit(0xe8); c.branch(0xd0,'fade_loop')
    c.label('fade_done')
    c.emit(0x68,0x18,0x69,2,0xaa,0x68); a(0x8d,0xd301); c.emit(0x60)
    c.labels['mask_source_high']=c.labels['mask_source']+2
    c.labels['mask_dest_high']=c.labels['mask_dest']+2
    c.label('color_phase'); c.emit(0)
    c.label('beat_lo'); c.emit(*(tick_at_beat(i) & 255 for i in range(32)))
    c.label('beat_hi'); c.emit(*(tick_at_beat(i) >> 8 for i in range(32)))
    c.label('mask_key'); c.emit(0xff)
    c.label('fade_phase'); c.emit(0)
    c.label('reveal_key'); c.emit(0,15,16,0,0,17,18)
    c.label('reveal_high'); c.emit(0x68,0x72)
    c.label('mask_high'); c.emit(0x40,0x4a,0x54,0x5e,0x68,0x72)
    c.label('frame_high'); c.emit(0x40,0x4a,0x54,0x5e)

    c.label('color')
    # Entire picture rises from black and falls back before the scene cut.
    c.jump(0xae,'fade_phase'); c.jump(0xbd,'brightness'); a(0x8d,0xd01a); c.emit(0x60)
    c.label('brightness')
    c.emit(*([0,2,4,6,6,6,6] + [6]*32 + [6,6,6,4,4,2,0,0]))
    c.label('letter_keep')
    c.emit(*( (0 if value>>4 else 0xf0) | (0 if value&15 else 15) for value in range(256)))
    data=c.finish()
    if len(data)>SIZE: raise ValueError(f'plasma helper exceeds reservation: {len(data)}')
    return data,c.labels
