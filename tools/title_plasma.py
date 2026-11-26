"""Full-screen animated GTIA 11 plasma with hue-only lettering.

The 6502 synthesizes an 80x64 wave field in the inactive framebuffer,
adds the static skyline, then composites the lettering and dissolve masks.
ANTIC repeats each source line three times.
"""
import math
from pathlib import Path
from PIL import Image
from build_sequence import Code, TITLE_TICK
from school_portrait_bank import bank_value
from music_timing import tick_at_beat
import title_water

SIZE = 2272
STATE = 0x83e0
FRAME_BYTES = 2560
LETTER_PAGES = 5
PLASMA_STEP_TICKS = 16
FIRST_BANK = 40
PLASMA_ENTRY = 0x4000
WAVE_TABLES = 0x4500
VERTICAL_WAVE = 0x4d00
SKYLINE_DATA = 0x4e00
SKYLINE_FIRST_PAGE = 5
SKYLINE_PAGES = 5
FADE_RANKS = 0x5500
FADE_LOOKUP = 0x5f00
FADE_ENTRY = 0x6500
# Whole pages after the arena helpers and in two unused side-actor gaps.
MASK_PAGE_SLOTS = (*((bank, 0x73, 0x80) for bank in range(20, 24)),
                   (36, 0x50, 0x54), (37, 0x50, 0x54))
TRANSITION_START = TITLE_TICK
CITY_REVEAL_START = 1024
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


def city_picture():
    """Convert the supplied Atari picture to the title's 80 by 64 grid."""
    path = Path(__file__).resolve().parents[1] / 'assets/art/source/title_city_reference.png'
    # The input is 160x103 display pixels. GTIA pixels are two display pixels
    # wide and each source row is displayed three times: 34 rows preserve its
    # height to within one display pixel, anchored to the bottom of the frame.
    picture = Image.open(path).convert('RGB').crop((1, 0, 159, 103))
    picture = picture.resize((80, 34), Image.Resampling.NEAREST)
    colors = {(13,58,115): None, (134,178,234): 9, (155,84,70): 3,
              (60,60,60): 1, (4,4,4): 0, (0,0,0): 0,
              (8,5,5): 0, (255,255,0): None}
    return tuple(colors[pixel] for pixel in picture.getdata())


CITY_PICTURE = city_picture()


def skyline_hue(x,y):
    """Return a city hue; the dark blue key exposes the animated plasma."""
    return CITY_PICTURE[(y-30)*80+x] if y >= 30 else None


def letter_ink(code, phase=0):
    return LETTER_HUES[(code + phase) & 7] if code & 8 else 0


def compose_byte(background, mask, phase=0):
    result=0
    for shift in (4,0):
        code=(mask >> shift) & 15
        hue=letter_ink(code, phase) if code else (background >> shift) & 15
        result |= hue << shift
    return result


def plasma_tables():
    """Packed horizontal waves for each quantized vertical intensity."""
    return tuple(bytes(
        (dither_hue(horizontal(x) + (band-3.5)*.20, x, 0) << 4) |
        dither_hue(horizontal(x+1) + (band-3.5)*.20, x+1, 0)
        for x in range(0,512,2))
        for band in range(8))


def horizontal(x):
    return 1.05*math.sin(x*math.tau/256*3) + .72*math.cos(x*math.tau/256*5)


def vertical_wave():
    return bytes(round(127.5 + 127.5*math.sin(i*math.tau/256)) for i in range(256))


def skyline_masks():
    keep = bytearray(FRAME_BYTES)
    ink = bytearray(FRAME_BYTES)
    for y in range(64):
        for x in range(80):
            hue = skyline_hue(x,y)
            i = y*40 + x//2
            shift = 0 if x&1 else 4
            if hue is None:
                keep[i] |= 15 << shift
            else:
                ink[i] |= hue << shift
    start = SKYLINE_FIRST_PAGE*256
    assert all(byte == 255 for byte in keep[:start])
    assert not any(ink[:start])
    return bytes(keep[start:]), bytes(ink[start:])


def city_reveal_level(tick):
    return max(0, min(8, (tick - CITY_REVEAL_START) // 32 + 1))


def procedural_frame(phase, tick=None):
    """Reference for the 6502's two-dimensional wave and skyline compositor."""
    tables, vertical = plasma_tables(), vertical_wave()
    time = (phase & 127)*2
    image = bytearray()
    for row in range(64):
        shift = (vertical[(3*row + time)&255]//4 + row + time)&255
        table = tables[vertical[(4*row - time)&255]//32]
        image.extend(table[(shift+column)&255] for column in range(39,-1,-1))
    keep, ink = skyline_masks()
    ranks = fade_ranks()[SKYLINE_FIRST_PAGE*256:]
    level = 8 if tick is None else city_reveal_level(tick)
    for i,(mask,hue,rank) in enumerate(zip(keep,ink,ranks), SKYLINE_FIRST_PAGE*256):
        if rank >> 4 < level:
            image[i] = (image[i]&mask) | hue
    return bytes(image)


def plasma_renderer():
    """Draw into the selected inactive buffer while title bank 40 is mapped."""
    c = Code(PLASMA_ENTRY)
    def a(op, address):
        c.emit(op,address&255,address>>8)

    # STATE+12 holds the wave phase. STATE+13 is framebuffer high.
    a(0xad,STATE+13); c.jump(0x8d,'dest_hi')
    keep, ink = skyline_masks()
    # Reveal packed GTIA byte pairs in the same island order as the plasma fade.
    ranks = tuple(rank >> 4 for rank in fade_ranks()[SKYLINE_FIRST_PAGE*256:])
    skyline = bytearray()
    groups = []
    for page in range(SKYLINE_PAGES):
        start = page*256
        masks = keep[start:start+256]
        for partial in (False,True):
            offsets = bytes(sorted((i for i,mask in enumerate(masks)
                            if (0 < mask < 255 if partial else mask == 0)),
                            key=lambda i: ranks[start+i]))
            if not offsets:
                continue
            width = len(offsets)
            base = SKYLINE_DATA+len(skyline)
            skyline.extend(offsets)
            skyline.extend(ink[start+i] for i in offsets)
            if partial:
                skyline.extend(masks[i] for i in offsets)
            counts = bytes(sum(ranks[start+i] < level for i in offsets)
                           for level in range(9))
            count_address = SKYLINE_DATA + len(skyline)
            skyline.extend(counts)
            groups.append((page,partial,width,base,count_address))
    for index,(page,partial,_,_,_) in enumerate(groups):
        a(0xad,STATE+13); c.emit(0x18,0x69,SKYLINE_FIRST_PAGE+page)
        if partial:
            c.jump(0x8d,f'city_read_hi{index}')
        c.jump(0x8d,f'city_write_hi{index}')
    c.emit(0xa9,0); c.jump(0x8d,'dest_lo'); c.jump(0x8d,'row')
    c.label('next_row')
    c.label('row_load'); c.emit(0xa9,0,0x0a,0x18); c.jump(0x6d,'row')
    c.emit(0x18); a(0x6d,STATE+12); c.emit(0xaa)
    a(0xbd,VERTICAL_WAVE); c.emit(0x4a,0x4a,0x18); c.jump(0x6d,'row')
    c.emit(0x18); a(0x6d,STATE+12); c.emit(0x48)
    c.jump(0xad,'row'); c.emit(0x0a,0x0a,0x38); a(0xed,STATE+12); c.emit(0xaa)
    a(0xbd,VERTICAL_WAVE); c.emit(0x4a,0x4a,0x4a,0x4a,0x4a,0x18,0x69,WAVE_TABLES>>8)
    for column in range(8):
        c.jump(0x8d,f'wave_hi{column}')
    c.label('dest_hi_load'); c.emit(0xa9,0)
    for column in range(8):
        c.jump(0x8d,f'row_dest_hi{column}')
    c.label('dest_lo_load'); c.emit(0xa9,0)
    for column in range(8):
        c.jump(0x8d,f'row_dest_lo{column}')
    c.emit(0x68,0xaa,0xa0,39)
    c.label('pixel')
    for column in range(8):
        c.label(f'wave{column}'); a(0xbd,WAVE_TABLES)
        c.label(f'row_dest{column}'); a(0x99,0x9000)
        c.emit(0xe8,0x88)
        c.labels[f'wave_hi{column}'] = c.labels[f'wave{column}']+2
        c.labels[f'row_dest_lo{column}'] = c.labels[f'row_dest{column}']+1
        c.labels[f'row_dest_hi{column}'] = c.labels[f'row_dest{column}']+2
    c.branch(0x10,'pixel')
    c.jump(0xad,'dest_lo'); c.emit(0x18,0x69,40); c.jump(0x8d,'dest_lo')
    c.branch(0x90,'row_advance'); c.jump(0xee,'dest_hi')
    c.label('row_advance'); c.jump(0xee,'row'); c.jump(0xad,'row')
    c.emit(0xc9,64); c.branch(0xf0,'skyline'); c.jump(0x4c,'next_row')

    c.label('skyline')
    a(0x20, title_water.ENTRY)
    a(0xad,STATE+3); c.emit(0xc9,CITY_REVEAL_START>>8)
    c.branch(0x90,'city_none'); c.branch(0xd0,'city_full')
    a(0xad,STATE+2); c.emit(0x4a,0x4a,0x4a,0x4a,0x4a,0x18,0x69,1)
    c.jump(0x4c,'city_level')
    c.label('city_none'); c.emit(0xa9,0); c.jump(0x4c,'city_level')
    c.label('city_full'); c.emit(0xa9,8)
    c.label('city_level'); c.jump(0x8d,'city_rank')
    for index,(_,partial,width,base,count_address) in enumerate(groups):
        c.jump(0xae,'city_rank'); a(0xbd,count_address); c.branch(0xf0,f'city_done{index}')
        c.emit(0xa8,0x88)
        c.label(f'city{index}'); a(0xbe,base)
        if partial:
            c.label(f'city_read{index}'); a(0xbd,0x9000)
            a(0x39,base+2*width); a(0x19,base+width)
            c.labels[f'city_read_hi{index}'] = c.labels[f'city_read{index}']+2
        else:
            a(0xb9,base+width)
        c.label(f'city_write{index}'); a(0x9d,0x9000)
        c.labels[f'city_write_hi{index}'] = c.labels[f'city_write{index}']+2
        c.emit(0x88,0xc0,255); c.branch(0xd0,f'city{index}')
        c.label(f'city_done{index}')
    # Every plasma phase uses the same LMS addresses in a given buffer.
    # Rebuild only when a different renderer has used the inactive list.
    from engine_effects import cached_display_list
    cached_display_list(c,8)
    c.emit(0xa0,0)
    for block,count in enumerate((21,21,22)):
        offset = 3+block*21*9
        for line in range(3):
            for part in ('lo','hi'):
                address = offset+3*line+(part=='hi')
                label = f'lms_{block}_{part}{line}'
                a(0xad,STATE+6); c.emit(0x18,0x69,address>>8)
                c.jump(0x8d,label+'_hi')
        c.emit(0xa2,0)
        c.label(f'lms_loop{block}')
        for part in ('lo','hi'):
            c.jump(0xb9,'lms_'+part)
            if part=='hi':
                a(0x0d,STATE+13)
            for line in range(3):
                address = offset+3*line+(part=='hi')
                label = f'lms_{block}_{part}{line}'
                c.label(label); a(0x9d,0x8000|(address&255))
                c.labels[label+'_hi'] = c.labels[label]+2
        c.emit(0x8a,0x18,0x69,9,0xaa,0xc8,0xc0,block*21+count)
        c.branch(0xd0,f'lms_loop{block}')
    c.label('swap'); c.emit(0x60)
    # The music NMI uses STATE+14 to save PORTB. Keep the rank bank-local.
    c.label('city_rank'); c.emit(0)
    c.label('lms_lo'); c.emit(*(row*40&255 for row in range(64)))
    c.label('lms_hi'); c.emit(*(row*40>>8 for row in range(64)))
    for name,label in (('row','row_load'),('dest_lo','dest_lo_load'),('dest_hi','dest_hi_load')):
        c.labels[name] = c.labels[label]+1
    return bytes(c.finish()), bytes(skyline)


def fade_ranks():
    ranks = []
    for y in range(64):
        for x in range(80):
            # Fixed, irregular islands keep the dissolve stable across phases.
            field = (math.sin(x*.11 + y*.08) + math.cos(y*.19 - x*.045)
                     + .5*math.sin(x*.23 - y*.13))
            raster = BAYER_4[(y%4)*4 + x%4] / 16
            ranks.append(max(0,min(7,int(((field+2.5)/5*.65 + raster*.35)*8))))
    return bytes((hi << 4) | lo for hi,lo in zip(ranks[::2],ranks[1::2]))


def fade_lookup(level):
    return bytes((0xf0 if rank >> 4 < level else 0) |
                 (0x0f if (rank & 15) < level else 0)
                 for rank in range(256))


def fade_mask(level):
    return fade_ranks().translate(fade_lookup(level))


def fade_bank():
    c = Code(FADE_ENTRY)
    def a(op,address):
        c.emit(op,address&255,address>>8)

    # A is the current dissolve level (1–6). Compute the lookup page once.
    c.emit(0x18,0x69,(FADE_LOOKUP>>8)-1)
    for page in range(10):
        c.jump(0x8d,f'lookup_hi{page}')
        a(0xad,STATE+13); c.emit(0x18,0x69,page)
        c.jump(0x8d,f'read_hi{page}')
        c.jump(0x8d,f'write_hi{page}')
        c.jump(0xad,f'lookup_hi{page}')
    c.emit(0xa2,0)
    c.label('pixels')
    for page in range(10):
        a(0xbc,FADE_RANKS+page*256)
        c.label(f'lookup{page}'); a(0xb9,FADE_LOOKUP)
        c.label(f'read{page}'); a(0x3d,0x9000)
        c.label(f'write{page}'); a(0x9d,0x9000)
        for name in ('lookup','read','write'):
            c.labels[f'{name}_hi{page}'] = c.labels[f'{name}{page}']+2
    c.emit(0xe8); c.branch(0xd0,'pixels'); c.emit(0x60)
    ranks = fade_ranks()
    lookup = b''.join(fade_lookup(level) for level in range(1,7))
    assert FADE_RANKS+len(ranks)==FADE_LOOKUP
    assert FADE_LOOKUP+len(lookup)==FADE_ENTRY
    return ranks + lookup + bytes(c.finish())


def artwork():
    # Bank 40 holds the procedural renderer and the only skyline copy.
    # Banks 41–43 retain their selectors and later banana-cache ownership.
    colors = bytes((letter_ink(value >> 4, phase) << 4 if value >> 4 else 0) |
                   (letter_ink(value & 15, phase) if value & 15 else 0)
                   for phase in range(4) for value in range(256))
    renderer, skyline = plasma_renderer()
    bank = bytearray(16384)
    end = 0
    for address,data in ((PLASMA_ENTRY,renderer),(title_water.TEMPLATES,title_water.templates()),
                         (WAVE_TABLES,b''.join(plasma_tables())),
                         (VERTICAL_WAVE,vertical_wave()),(SKYLINE_DATA,skyline),
                         (title_water.FOOTER_ENTRY,title_water.footer()),
                         (title_water.TABLES,title_water.tables()),
                         (FADE_RANKS,fade_bank()),
                         (title_water.ENTRY,title_water.renderer(CITY_REVEAL_START)),
                         (0x6800,colors)):
        offset = address-0x4000
        assert offset>=end
        end = offset+len(data)
        bank[offset:end] = data
    assert end == 0x2c00  # Firework code starts at $6C00.
    banks = [bytes(bank)] + [bytes(16384)]*3
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
    fade_banks = [bytes(16384)] * 2
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
    # Runtime only copies and composites the upper five pages.
    for mask in masks + transition_frames + reveal_frames:
        assert not any(mask[LETTER_PAGES*256:])
    return banks + [b''.join(masks).ljust(16384, b'\0')] + fade_banks + transition_banks


def mask_pages():
    """Share identical title mask pages across permanent bank slots."""
    banks = artwork()
    frames = [bytes(FRAME_BYTES)]
    frames += [banks[4][i*FRAME_BYTES:(i+1)*FRAME_BYTES] for i in range(6)]
    for bank in banks[7:9]:
        frames += [bank[i*FRAME_BYTES:(i+1)*FRAME_BYTES] for i in range(4)]
    for bank in banks[7:9]:
        frames += [bank[i*FRAME_BYTES:(i+1)*FRAME_BYTES] for i in (4, 5)]
    slots = iter((bank, page) for bank, start, end in MASK_PAGE_SLOTS
                 for page in range(start, end))
    locations, descriptors = {}, []
    for frame in frames:
        for offset in range(0, LETTER_PAGES * 256, 256):
            data = frame[offset:offset+256]
            if data not in locations:
                location = next(slots, None)
                if location is None:
                    raise ValueError('title mask pages exceed permanent bank slots')
                locations[data] = location
            descriptors.append(locations[data])
    return locations, descriptors


def install_mask_pages(bank, index, locations):
    out = bytearray(bank)
    for data, (owner, page) in locations.items():
        if owner == index:
            offset = (page - 0x40) * 256
            assert not any(out[offset:offset+256]), (index, page)
            out[offset:offset+256] = data
    return bytes(out)


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
    # Fade levels use 32 ticks. The plasma cache uses 16 ticks.
    a(0xad, STATE+9); c.emit(0x0a, 0x0a, 0x0a, 0x0a); a(0x8d, STATE+29)
    a(0xad, STATE+8); c.emit(0x4a,0x4a,0x4a,0x4a); a(0x0d, STATE+29); a(0x8d, STATE+29)
    # Fade only at the opening and after the final title, never at the cut.
    c.emit(0x4a); a(0xac, STATE); c.branch(0xd0, 'second_fade')
    c.emit(0xc9, 7); c.branch(0x90, 'save_fade')
    c.emit(0xa9, 7); c.jump(0x4c, 'save_fade')
    c.label('second_fade'); c.emit(0xc9, 39)
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
    # A development seek out of captions must restore both normal DLISTs
    # before earlier scene builders reuse their LMS operands.
    a(0xad,STATE);c.emit(0xc9,17);c.branch(0xd0,'outro_seek_done')
    a(0xad,0x0dd0);c.branch(0xf0,'outro_seek_done')
    from outro_text import BITMAP_JVB_HIGH, RESET_ENTRY, START as OUTRO_START
    a(0xad,STATE+3);c.emit(0xc9,OUTRO_START>>8);c.branch(0x90,'outro_seek_reset');c.branch(0xd0,'outro_seek_done')
    a(0xad,STATE+2);c.emit(0xc9,OUTRO_START&255);c.branch(0xb0,'outro_seek_done')
    c.label('outro_seek_reset');a(0x20,RESET_ENTRY)
    # The credits restore copies one saved list into both bitmap pages.
    # Each page needs its own JVB target to hold its picture until the swap.
    for page in (0x80,0x84):
        c.emit(0xa9,page);a(0x8d,(page<<8)+BITMAP_JVB_HIGH)
    c.label('outro_seek_done')
    a(0xad, STATE); c.emit(0xc9, 2); c.branch(0xb0, 'invalidate_mask')
    a(0x4c, title_water.RETIRE_ENTRY)
    c.label('invalidate_mask')
    c.emit(0xa9, 0xff); c.jump(0x8d, 'mask_key')
    c.emit(0x60)
    c.label('mask_key'); c.emit(0xff)

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
    a(0xad, STATE); c.branch(0xd0, 'song_title')
    # The artist lines begin at ticks 512 and 768.
    a(0xad, STATE+10); c.emit(0xc9, 2); c.branch(0xb0, 'artist_stage')
    c.emit(0xa9, 1)
    c.label('artist_stage'); c.emit(0x38,0xe9,1); a(0x8d, STATE+10)
    c.jump(0x4c, 'maybe_reveal')
    c.label('song_title')
    a(0xad, STATE+10); c.branch(0xd0, 'title_nonzero'); c.emit(0xa9, 1)
    c.label('title_nonzero'); c.emit(0x18,0x69,3); a(0x8d, STATE+10)
    c.label('maybe_reveal'); a(0xad, STATE+9); c.emit(0xc9,4); c.branch(0xb0,'mask_key_ready')
    a(0xad, STATE+8); c.emit(0xc9,64); c.branch(0xb0,'mask_key_ready')
    a(0xae, STATE+10); c.jump(0xbd,'reveal_key'); c.branch(0xf0,'mask_key_ready')
    a(0x8d, STATE+10)
    c.label('mask_key_ready'); a(0xad, STATE+10); c.jump(0xcd, 'mask_key')
    c.branch(0xd0, 'mask_changed'); c.jump(0x4c, 'mask_done')
    c.label('mask_changed'); c.jump(0x8d, 'mask_key')
    # Y points to the frame's first descriptor. X copies one whole page.
    c.emit(0x0a, 0x0a, 0x18); a(0x6d, STATE+10); c.emit(0xa8)
    c.emit(0xa9, 0xa0); c.jump(0x8d, 'mask_dest_high')
    c.label('mask_page')
    c.jump(0xb9, 'mask_bank_indices'); c.emit(0xaa)
    a(0xbd, bank_value(3)); a(0x8d, 0xd301)
    c.jump(0xb9, 'mask_pages'); c.jump(0x8d, 'mask_source_high')
    c.emit(0xa2, 0)
    c.label('mask_copy')
    c.label('mask_source'); a(0xbd, 0x4000)
    c.label('mask_dest'); a(0x9d, 0xa000)
    c.emit(0xe8); c.branch(0xd0, 'mask_copy')
    c.emit(0xc8); c.jump(0xee, 'mask_dest_high'); c.jump(0xad, 'mask_dest_high')
    c.emit(0xc9, 0xa0+LETTER_PAGES); c.branch(0xd0, 'mask_page')
    c.label('mask_done')
    # Use the same music-clock phase and render directly into the back buffer.
    a(0xad,STATE+2); c.emit(0x4a,0x4a,0x4a,0x29,0x1e); a(0x8d,STATE+12)
    a(0xad,STATE+3); c.emit(0x29,7,0x0a,0x0a,0x0a,0x0a,0x0a); a(0x0d,STATE+12); a(0x8d,STATE+12)
    a(0xad,bank_value(FIRST_BANK)); a(0x8d,0xd301)
    # The inactive display list determines which framebuffer can be written.
    a(0xad,STATE+6); c.emit(0x29,4,0x4a,0x4a,0x49,1,0xaa,0x48)
    c.emit(0x0a,0x0a,0x0a,0x0a,0x0a,0x18,0x69,0x90); a(0x8d,STATE+13)
    c.jump(0xad, 'fade_phase'); a(0x8d,STATE+11)
    a(0x20,PLASMA_ENTRY)
    c.jump(0xad,'mask_key'); c.branch(0xd0,'letter_setup'); c.jump(0x4c,'composed')
    c.label('letter_setup')
    # Patch the ten page operations, then composite lettering in place.
    for page in range(LETTER_PAGES):
        a(0xad,STATE+13); c.emit(0x18,0x69,page); c.jump(0x8d,f'src_hi{page}'); c.jump(0x8d,f'dst_hi{page}')
    c.jump(0xad,'color_phase'); c.emit(0x18,0x69,0x68)
    for page in range(LETTER_PAGES): c.jump(0x8d,f'color_hi{page}')
    c.emit(0xa2,0)
    c.label('compose')
    for page in range(LETTER_PAGES):
        a(0xbd,0xa000+page*256);c.branch(0xf0,f'letter_done{page}');c.emit(0xa8)
        c.jump(0xb9,'letter_keep')
        c.label(f'src{page}'); c.emit(0x3d,0,0x40)
        c.label(f'color{page}'); c.emit(0x19,0,0x68)
        c.labels[f'color_hi{page}']=c.labels[f'color{page}']+2
        c.label(f'dst{page}'); c.emit(0x9d,0,0x90)
        c.label(f'letter_done{page}')
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
    a(0x20,FADE_ENTRY)
    c.label('fade_done')
    c.emit(0x68,0x18,0x69,2,0xaa,0x68); a(0x8d,0xd301); c.emit(0x60)
    c.labels['mask_source_high']=c.labels['mask_source']+2
    c.labels['mask_dest_high']=c.labels['mask_dest']+2
    c.label('color_phase'); c.emit(0)
    c.label('beat_lo'); c.emit(*(tick_at_beat(i) & 255 for i in range(32)))
    c.label('beat_hi'); c.emit(*(tick_at_beat(i) >> 8 for i in range(32)))
    c.label('fade_phase'); c.emit(0)
    c.label('reveal_key'); c.emit(0,15,16,0,0,17,18)
    _, descriptors = mask_pages()
    c.label('mask_bank_indices')
    c.emit(*(bank-3 for bank, _ in descriptors))
    c.label('mask_pages'); c.emit(*(page for _, page in descriptors))

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
