"""Finale text, unpacked into the retired second bitmap buffer on entry."""
from build_sequence import Code
from music_timing import tick_at_bar

ENTRY = 0xC000
RESET_ENTRY = 0xC340
START, END = tick_at_bar(112), tick_at_bar(137)
TEXT_POINTERS = 0xC400
FONT = 0xC800
COLOR_FONT = 0xB400
COLOR_FONT_SOURCE = 0x5A00
COLOR_FONT_LOAD = 0xFECE
TEXT_HIGH = 0xCC00
TEXT_END = 0xCF00
STATE_FLAG = 0x0DD0
STATE_START = 0x0DD1
STATE_PHASE = 0x0DD2
TMP_LO = 0x0DD3
TMP_HI = 0x0DD4
TMP_ROW = 0x0DD6
HISTORY_ROWS = 6
TEXT_ROWS = HISTORY_ROWS + 1
TEXT_RASTERS = TEXT_ROWS*8
# Eight blank lines trigger the color DLI. Two more let it align before text.
TEXT_LEAD = (0xf0, 0x10)
TEXT_LEAD_RASTERS = 10
TEXT_DLI_VCOUNT = 8
BODY_DLI_VCOUNT = (8+TEXT_LEAD_RASTERS+TEXT_RASTERS)//2
TEXT_DL = 1+len(TEXT_LEAD)
BITMAP_SKIP = TEXT_LEAD_RASTERS+(TEXT_ROWS-5)*8
BITMAP_ROWS = 192-BITMAP_SKIP
BITMAP_DL = TEXT_DL+TEXT_ROWS*3
FOOTER_DL = BITMAP_DL+BITMAP_ROWS*3
# Ordinary bitmap lists have two leading bytes, 192 LMS entries and an
# eight-byte footer ending in the JVB target's high byte.
BITMAP_JVB_HIGH = 2 + 192 * 3 + 7
PROMPT = b'>'
FINAL_CARD_ENTRY = 0x5F90
FINAL_CARD_DL = 0xBE80
FINAL_CARD_SOURCE = 0x5C60   # control bank, before the final-orbit data
FINAL_MARK_GLYPHS = 0x6904   # control bank, before orbit state at $69B8
FINAL_MARK_GLYPHS_TAIL = 0x5C88
FINAL_MARK_TILES = 0x5CB0
FINAL_MARK_DRAW = 0x6994
FINAL_MARK_FONT_COPY = 0x5FE7
FINAL_MARK_PHASES = 32
FINAL_MARK_WIDTH = 7
FINAL_MARK_ROWS = 3
FINAL_MARK_FIRST_GLYPH = 96
FINAL_MARK_SCREEN = 0xBF00   # retired finale framebuffer
FINAL_CARD_PAGES = (
    ('A\\SLOP BY OGNJEN 2026', 'SILLY VENTURE WE', ''),
    ('STEREO MUSIC PLAYER / 2 POKEYS', 'CREATED AS A SEPARATE PROJECT',
     '4 POKEY UPDATES PER PAL FRAME'),
    ('OPENING EFFECTS', 'PROCEDURAL PLASMA / CITY REVEAL', 'TITLE REVEAL / PMG FIREWORKS'),
    ('LOADER / TEXT EFFECTS', 'ANIMATED STAR / LOADING DOTS', 'RAINBOW DLI GLITCH / TEXT FADES'),
    ('SCENE DIRECTOR', 'MUSIC TICKS CUE EACH SCENE', 'ANTIC MODES / BANKED 1 MB RAM'),
)
FINAL_CARD_TEXT = 0xBF80
FINAL_CARD_TEXT_ROWS = 3
CREDITS = (
    ("SYS.OPEN CREDITS [OK]", "THE LESS I KNOW THE BETTER",
     "A\\SLOP BY OGNJEN / ATARI XE 1 MB", "I STARTED VIBECODING IN JULY 2026",
     "THIS IS MY FIRST WORK FOR ATARI", "MADE WITH OPENAI CODEX"),
    ("SYS.OPEN AUDIO.LOG [OK]", "SONG / TAME IMPALA", "THE LESS I KNOW THE BETTER",
     "POKEY / OGNJEN / CODEX", "MIDI / MIDISHOW 200337"),
    ("UPLINK SV2026 [CONNECTED]", "MADE FOR", "SILLY VENTURE 2026",
     "AI TOOLS / ATARI SOUL", "HUMAN VISION / LLM CODE"),
)
GREETZ = (
    "GREETINGS TO ALL MY CHOOMS!",
    "ESPECIALLY MY SON VICVIP AND HIS",
    "MUM, MY MUM AND DAD,",
    "AND THE REST OF MY FAMILY.",
    "",
    'I TOLD MUM: "IT\'S AN ATARI DEMO."',
    'SHE SAID: "I CAN HEAR THAT!"',
    "SHE'D HEARD AN ATARI XE",
    "ABOUT 30 YEARS AGO.",
    "",
    "TO MY FRIENDS AND NEIGHBOURS -",
    "SPECIAL THANKS TO D3CKER,",
    "WHO INTRODUCED ME TO AI AGENTS,",
    "AND BLASPH, WHO GAVE ME THE IDEA:",
    "TAME IMPALA ON THE ATARI!",
    "",
    "VIRUS / FOORMAN / MAQ / KEY-G",
    "FALCON / ATARIONLINE.PL / PTODT",
    "ATARIMUZEUM.PL",
    "",
    "ALL THE GUESTS AT SILLY VENTURE,",
    "THE WHOLE SILLY VENTURE CREW,",
    "AND EVERYONE WATCHING -",
    "EACH OF YOU, PERSONALLY!",
)

# Compact 5x7 capitals, digits and the punctuation used by the credits.
GLYPHS = {
    '>':('10000','01000','00100','00010','00100','01000','10000'),
    'A':('01110','10001','10001','11111','10001','10001','10001'),
    'B':('11110','10001','10001','11110','10001','10001','11110'),
    'C':('01111','10000','10000','10000','10000','10000','01111'),
    'D':('11110','10001','10001','10001','10001','10001','11110'),
    'E':('11111','10000','10000','11110','10000','10000','11111'),
    'F':('11111','10000','10000','11110','10000','10000','10000'),
    'G':('01111','10000','10000','10111','10001','10001','01111'),
    'H':('10001','10001','10001','11111','10001','10001','10001'),
    'I':('11111','00100','00100','00100','00100','00100','11111'),
    'J':('00111','00010','00010','00010','10010','10010','01100'),
    'K':('10001','10010','10100','11000','10100','10010','10001'),
    'L':('10000','10000','10000','10000','10000','10000','11111'),
    'M':('10001','11011','10101','10101','10001','10001','10001'),
    'N':('10001','11001','11001','10101','10011','10011','10001'),
    'O':('01110','10001','10001','10001','10001','10001','01110'),
    'P':('11110','10001','10001','11110','10000','10000','10000'),
    'Q':('01110','10001','10001','10001','10101','10010','01101'),
    'R':('11110','10001','10001','11110','10100','10010','10001'),
    'S':('01111','10000','10000','01110','00001','00001','11110'),
    'T':('11111','00100','00100','00100','00100','00100','00100'),
    'U':('10001','10001','10001','10001','10001','10001','01110'),
    'V':('10001','10001','10001','10001','10001','01010','00100'),
    'W':('10001','10001','10001','10101','10101','11011','10001'),
    'X':('10001','10001','01010','00100','01010','10001','10001'),
    'Y':('10001','10001','01010','00100','00100','00100','00100'),
    'Z':('11111','00001','00010','00100','01000','10000','11111'),
    '0':('01110','10001','10011','10101','11001','10001','01110'),
    '1':('00100','01100','00100','00100','00100','00100','01110'),
    '2':('01110','10001','00001','00010','00100','01000','11111'),
    '3':('11110','00001','00001','01110','00001','00001','11110'),
    '4':('00010','00110','01010','10010','11111','00010','00010'),
    '5':('11111','10000','10000','11110','00001','00001','11110'),
    '6':('01110','10000','10000','11110','10001','10001','01110'),
    '7':('11111','00001','00010','00100','01000','01000','01000'),
    '8':('01110','10001','10001','01110','10001','10001','01110'),
    '9':('01110','10001','10001','01111','00001','00001','01110'),
    ' ':('00000',)*7, '!':('00100','00100','00100','00100','00100','00000','00100'),
    '"':('01010','01010','01010','00000','00000','00000','00000'),
    '#':('01010','11111','01010','01010','11111','01010','00000'),
    "'":('00100','00100','00010','00000','00000','00000','00000'),
    ',':('00000','00000','00000','00000','00110','00100','01000'),
    '.':('00000','00000','00000','00000','00000','00110','00110'),
    ':':('00000','00110','00110','00000','00110','00110','00000'),
    '-':('00000','00000','00000','11111','00000','00000','00000'),
    '/':('00001','00010','00010','00100','01000','01000','10000'),
    '\\':('10000','01000','01000','00100','00010','00010','00001'),
    '+':('00000','00100','00100','11111','00100','00100','00000'),
}


def all_lines():
    lines = tuple(dict.fromkeys(tuple(line for page in CREDITS for line in page) + GREETZ))
    if len(lines) > 38 or any(len(line) > 36 for line in lines):
        raise ValueError('outro text exceeds its compact line layout')
    if len(GREETZ) > 24:
        raise ValueError('greetz needs more than the reserved scroll window')
    return lines


# Three-pixel-wide glyphs: ANTIC 4 supplies independently coloured letters
# over true COLBK black, unlike the shared-hue ANTIC 2 high-resolution mode.
TERMINAL_FONT = {
    "4": "101 101 101 111 001 001 001",
'[':"111 100 100 100 100 100 111",
']':"111 001 001 001 001 001 111",
'>':"100 010 001 001 001 010 100",
'A':"010 101 101 111 101 101 101",'B':"110 101 101 110 101 101 110",
'C':"011 100 100 100 100 100 011",'D':"110 101 101 101 101 101 110",
'E':"111 100 100 110 100 100 111",'F':"111 100 100 110 100 100 100",
'G':"011 100 100 101 101 101 011",'H':"101 101 101 111 101 101 101",
'I':"111 010 010 010 010 010 111",'J':"001 001 001 001 101 101 010",
'K':"101 101 110 100 110 101 101",'L':"100 100 100 100 100 100 111",
'M':"101 111 111 101 101 101 101",'N':"101 101 111 111 111 101 101",
'O':"010 101 101 101 101 101 010",'P':"110 101 101 110 100 100 100",
'Q':"010 101 101 101 111 011 001",'R':"110 101 101 110 101 101 101",
'S':"011 100 100 010 001 001 110",'T':"111 010 010 010 010 010 010",
'U':"101 101 101 101 101 101 111",'V':"101 101 101 101 101 101 010",
'W':"101 101 101 111 111 111 101",'X':"101 101 010 010 010 101 101",
'Y':"101 101 101 010 010 010 010",'Z':"111 001 001 010 100 100 111",
'7':"111 001 001 010 010 100 100",
}

def final_mark(phase=0):
    """Tile the faceted star and its two broken orbits into ANTIC 5 glyphs."""
    import math
    from arena_art import inside

    width, height = FINAL_MARK_WIDTH*4, FINAL_MARK_ROWS*8
    art = bytearray(width * height)

    turn = math.tau * phase / FINAL_MARK_PHASES
    width_scale = 1.00 + 0.14 * math.cos(turn)
    ridge = 3.2 * math.sin(turn)

    def facet(ink, *points):
        points = tuple(((19 + (x-19)*width_scale + (y-16)*ridge/10)*.7, y*.75)
                       for x, y in points)
        for y in range(height):
            for x in range(width):
                if inside(x + .5, y + .5, points):
                    art[y * width + x] = ink

    glints = []
    for angle in range(360):
        theta = math.radians(angle)
        for tilt, ink, gaps in ((-.36, 2, (32, 212)), (.36, 3, (150, 330))):
            offset = math.degrees(turn) * (1 if tilt > 0 else -1)
            if any(abs((angle - gap - offset + 180) % 360 - 180) < 18 for gap in gaps):
                continue
            u, v = 18.5 * math.cos(theta), 7.4 * math.sin(theta)
            tilt += 0.16 * math.sin(turn + tilt)
            x = round((19.5 + u * math.cos(tilt) - v * math.sin(tilt))*.7)
            y = round((15.5 + u * math.sin(tilt) + v * math.cos(tilt))*.75)
            art[y * width + x] = ink
            if angle == round(gaps[0] + offset + 36) % 360:
                glints.append((x,y))

    # Split the light into a bright ridge, a blue plane and a gold plane.
    facet(0, (20, 0), (25, 10), (32, 16), (25, 21), (20, 32),
          (15, 21), (8, 16), (15, 10))
    facet(1, (20, 2), (23, 12), (29, 16), (22, 17), (20, 30),
          (17, 20), (11, 16), (17, 12))
    facet(2, (20, 2), (23, 12), (29, 16), (21, 14))
    facet(3, (29, 16), (22, 17), (20, 30), (20, 18))
    facet(2, (11, 16), (17, 20), (20, 30), (18, 18))
    for x, y in glints:
        for dx,dy in ((0,0),(-1,0),(1,0),(0,-1),(0,1)):
            if 0<=x+dx<width and 0<=y+dy<height:
                art[(y+dy)*width+x+dx] = 1

    used = set(map(ord, ''.join(all_lines()) + '>'))
    assert used.isdisjoint(range(FINAL_MARK_FIRST_GLYPH, 128))
    glyphs = bytearray()
    screen = bytearray()
    for top in range(0, height, 8):
        row = bytearray()
        for left in range(0, width, 4):
            tile = bytes(sum(art[y * width + left + x] << (6 - x * 2)
                             for x in range(4)) for y in range(top, top + 8))
            screen.append(FINAL_MARK_FIRST_GLYPH + len(glyphs)//8)
            glyphs.extend(tile)
    assert len(glyphs) <= (128-FINAL_MARK_FIRST_GLYPH)*8
    assert len(screen) == FINAL_MARK_WIDTH * FINAL_MARK_ROWS
    return bytes(screen), bytes(glyphs)


def font_data(card=False):
    font=bytearray(1024)
    card_lines = ''.join(line for page in FINAL_CARD_PAGES for line in page)
    for char in set(''.join(all_lines())+card_lines+'>'):
        rows=TERMINAL_FONT[char].split() if char in TERMINAL_FONT else tuple(''.join(row[i] for i in (0,2,4)) for row in GLYPHS[char])
        font[ord(char)*8:ord(char)*8+8]=bytes(sum((int(bit)<<(6-2*i)) for i,bit in enumerate(row)) for row in rows)+b'\0'
    font[:40]=b'[XE-OS] LINK:ONLINE // SV2026 [OK]'.ljust(40,b' ')
    # Unused control glyphs hold timing/length tables, loaded on entry.
    # The retired UI bytes are available for compressed staging instead.
    lines=display_lines()
    from terminal_typing import TIMES,LENGTHS,schedule
    ticks=schedule();timing=bytes(t&255 for t in ticks)+bytes(t>>8 for t in ticks)
    lengths=bytes(len(line)+len(PROMPT) if line else 0 for line in lines)
    assert TIMES+len(timing)<=LENGTHS
    assert LENGTHS+len(lengths)<=FONT+32*8
    font[TIMES-FONT:TIMES-FONT+len(timing)]=timing
    font[LENGTHS-FONT:LENGTHS-FONT+len(lengths)]=lengths
    font[95*8:96*8]=bytes([0]*6+[0x54,0])  # blinking baseline underscore
    if card:
        font[0x100:0x300] = bytes(value*3 for value in font[0x100:0x300])
    return bytes(font)


def color_font():
    from outro_palette import GLYPH_INKS
    assert all(32<=ord(char)<96 for char in ''.join(all_lines())+'>_')
    source = font_data()
    return bytes(source[glyph+max(0,row-1)]*pen
                 for glyph in range(0x100,0x300,8)
                 for row,pen in enumerate(GLYPH_INKS))


def install_color_font(bank):
    offset = COLOR_FONT_SOURCE - 0x4000
    data = color_font()
    assert not any(bank[offset:offset+len(data)])
    return bank[:offset]+data+bank[offset+len(data):]


def color_font_loader():
    # The compressed payload has been decoded. Its staging pages now hold
    # the terminal font while the final card keeps the original at $C800.
    c = Code(COLOR_FONT_LOAD)
    def a(op,address):
        c.emit(op,address&255,address>>8)

    from school_portrait_bank import BANK_VALUE
    a(0xAD,0xD301);c.emit(0x48);a(0xAD,BANK_VALUE);a(0x8D,0xD301)
    c.emit(0xA2,0);c.label('copy_font')
    for page in range(2):
        a(0xBD,COLOR_FONT_SOURCE+page*256);a(0x9D,COLOR_FONT+0x100+page*256)
    c.emit(0xE8);c.branch(0xD0,'copy_font')
    c.emit(0x68);a(0x8D,0xD301)
    c.emit(0x60)
    return bytes(c.finish())


def line_records():
    """Pack typed lines at their natural length and keep direct ANTIC rows padded."""
    address = TEXT_POINTERS
    for line in all_lines():
        encoded = line.upper().encode('ascii')
        if line:
            record = PROMPT + encoded
        else:
            record = b' ' * 40
        if address < FONT and address + len(record) > FONT:
            address = TEXT_HIGH
        if address + len(record) > TEXT_END:
            raise ValueError('outro text exceeds the reserved record space')
        yield address, record
        address += len(record)


def helper():
    c = Code(ENTRY)
    def a(op, address): c.emit(op, address & 255, address >> 8)
    c.label('active')
    # Text replaces only black upper bitmap rows; artwork stays at the same Y.
    a(0xAD, STATE_FLAG); c.branch(0xF0, 'init_text');c.jump(0x4C,'text_ready')
    c.label('init_text')
    c.emit(0xA9, 1); a(0x8D, STATE_FLAG)
    from terminal_typing import CACHE_ENTRY, CACHED_LINES, ENTRY as typing_entry, cache_helper
    c.emit(0xa9,0xff,0xa2,HISTORY_ROWS-1)
    c.label('invalidate_rows');a(0x9d,CACHED_LINES);c.emit(0xca);c.branch(0x10,'invalidate_rows')
    for offset in range(0,BITMAP_ROWS*3,256):
        length = min(256,BITMAP_ROWS*3-offset)
        c.emit(0xA2,0);c.label(f'copy{offset}')
        a(0xBD,0xB802+BITMAP_SKIP*3+offset)
        a(0x9D,0xBC00+BITMAP_DL+offset)
        c.emit(0xE8,0xE0,length&255);c.branch(0xD0,f'copy{offset}')
    base = 0xBC00
    for offset,value in enumerate((0x80,*TEXT_LEAD)):
        c.emit(0xA9,value);a(0x8D,base+offset)
    for row in range(TEXT_ROWS):
        # Each row's last raster sets the next palette or restores the bitmap.
        c.emit(0xA9,0xC4);a(0x8D,base+TEXT_DL+row*3)
    for row,cmd in ((69-BITMAP_SKIP,0x4E),(147-BITMAP_SKIP,0x4E),
                    (77-TEXT_LEAD_RASTERS-TEXT_RASTERS,0xCE),
                    (155-TEXT_LEAD_RASTERS-TEXT_RASTERS,0xCE)):
        c.emit(0xA9,cmd);a(0x8D,base+BITMAP_DL+row*3)
    for offset,value in enumerate((0x90,0x41,base&255,base>>8)):
        c.emit(0xA9,value);a(0x8D,base+FOOTER_DL+offset)
    a(0x20,COLOR_FONT_LOAD)
    c.label('text_ready')
    c.label('choose')
    c.emit(0xA9,0);a(0x8D,0xBC00+TEXT_DL+1);c.emit(0xA9,0xC8);a(0x8D,0xBC00+TEXT_DL+2)
    a(0xAD,0x83E4);c.branch(0xD0,'final_blank')
    a(0xAD,0x83E3);c.emit(0xC9,END>>8);c.branch(0x90,'cards');c.branch(0xD0,'final_blank')
    a(0xAD,0x83E2);c.emit(0xC9,END&255);c.branch(0x90,'cards')
    c.label('final_blank')
    blank=_line_addresses()[all_lines().index('')]
    c.emit(0xA9,blank&255);a(0x8D,0xBC00+TEXT_DL+1);c.emit(0xA9,blank>>8);a(0x8D,0xBC00+TEXT_DL+2)
    c.emit(0xA9,len(pages())*HISTORY_ROWS);a(0x8D,STATE_START);c.jump(0x4C,'update')
    c.label('cards')
    # Write a whole page quickly, then hold it until the next page starts.
    c.emit(0xA2,len(pages())-1)
    c.label('find_page');a(0xAD,0x83E3);c.jump(0xDD,'page_hi');c.branch(0x90,'previous_page');c.branch(0xD0,'page_found')
    a(0xAD,0x83E2);c.jump(0xDD,'page_lo');c.branch(0xB0,'page_found')
    c.label('previous_page');c.emit(0xCA);c.branch(0x10,'find_page');c.emit(0xA2,0)
    c.label('page_found');c.jump(0xBD,'page_offset');a(0x8D,STATE_START)
    c.label('update')
    # A real prompt stays in one column; only the cursor advances.
    c.emit(0xA2, 0)
    c.label('row')
    c.emit(0x8A); a(0x8D,TMP_ROW)
    a(0xAD, TMP_ROW); c.emit(0x18); a(0x6D, STATE_START); c.emit(0xA8)
    c.jump(0xB9, 'line_lo'); a(0x8D, TMP_LO)
    c.jump(0xB9, 'line_hi'); a(0x8D, TMP_HI)
    a(0x20,typing_entry)
    a(0xAD, TMP_ROW); c.emit(0x0A, 0x18); a(0x6D, TMP_ROW); c.emit(0xA8)
    a(0xAD, TMP_LO); a(0x99, 0xBC00+TEXT_DL+4)
    c.emit(0xa9,0xbf); a(0x99, 0xBC00+TEXT_DL+5)
    c.emit(0xE8, 0xE0, HISTORY_ROWS); c.branch(0xD0, 'row')
    c.label('done')
    a(0xAD,STATE_FLAG);c.emit(0xC9,1);c.branch(0xD0,'published')
    c.label('publish_wait');a(0xAD,0xD40B);c.emit(0xC9,124);c.branch(0x90,'publish_wait');c.emit(0xC9,128);c.branch(0xB0,'publish_wait')
    from final_boy import ENTRY_VISIBLE
    a(0x20,ENTRY_VISIBLE)
    c.emit(0xA9,COLOR_FONT>>8);a(0x8D,0xD409)
    c.emit(0xA9,0);a(0x8D,0xD402);c.emit(0xA9,0xBC);a(0x8D,0xD403)
    c.emit(0xA9,2);a(0x8D,STATE_FLAG)
    c.label('published');c.emit(0x60)
    c.label('wave'); c.emit(2,3,3,4,4,4,3,3,2,1,1,0,0,0,1,1)
    c.label('line_lo'); c.emit(*(a & 255 for a in display_addresses()))
    c.label('line_hi'); c.emit(*(a >> 8 for a in display_addresses()))
    c.label('flag'); c.emit(0)
    c.label('page_lo');c.emit(*(t&255 for t in page_starts()))
    c.label('page_hi');c.emit(*(t>>8 for t in page_starts()))
    c.label('page_offset');c.emit(*(i*HISTORY_ROWS for i in range(len(pages()))))
    assert c.origin+len(c.data)<=CACHE_ENTRY
    c.emit(*bytes(CACHE_ENTRY-c.origin-len(c.data)),*cache_helper())
    if c.origin+len(c.data)>RESET_ENTRY:raise ValueError('text helper exceeds reset boundary')
    c.emit(*bytes(RESET_ENTRY-c.origin-len(c.data)))
    a(0xAD, STATE_FLAG); c.branch(0xF0, 'ended')
    c.emit(0xA2,0)
    c.label('restore')
    for page in range(3):
        if page==2:c.emit(0xE0,74);c.branch(0xB0,'restore_next')
        a(0xBD,0xB800+page*256)
        a(0x9D,0x8400+page*256)
    c.label('restore_next')
    c.emit(0xE8);c.branch(0xD0,'restore')
    c.label('restore_wait');a(0xAD,0xD40B);c.emit(0xC9,124);c.branch(0x90,'restore_wait');c.emit(0xC9,128);c.branch(0xB0,'restore_wait')
    c.emit(0xA9,0);a(0x8D,0xD402)
    c.emit(0xA9,0x84);a(0x8D,0xD403)
    c.emit(0xA9,0x80);a(0x8D,0x83E6)
    c.emit(0xA2,0);c.label('restore_other')
    for page in range(3):
        if page==2:c.emit(0xE0,74);c.branch(0xB0,'restore_other_next')
        a(0xBD,0xB800+page*256);a(0x9D,0x8000+page*256)
    c.label('restore_other_next')
    c.emit(0xE8);c.branch(0xD0,'restore_other')
    c.emit(0xA9,0);a(0x8D,STATE_FLAG)
    c.emit(0xA9,0xFF)
    for address in (0x83F8,0x83F9,0x0DFE,0x0DFF):a(0x8D,address)
    c.label('ended');c.emit(0x60)
    result = c.finish()
    if len(result) > 0x400:
        raise ValueError(f'outro controller exceeds 1024-byte code slot: {len(result)}')
    return bytes(result)


def _line_addresses():
    return [address for address, _ in line_records()]


def final_card_display_list():
    # The last row of the mark ends on line 78 and clocks music once.
    data=[0x80]+[0x70]*3+[0x50,0x45,FINAL_MARK_SCREEN&255,FINAL_MARK_SCREEN>>8,
                          0x05,0x85,0x70,0x70,0xf0]
    for row in range(FINAL_CARD_TEXT_ROWS):
        address=FINAL_CARD_TEXT+row*40
        data.extend((0x44,address&255,address>>8))
        data.append(0xf0)
    data.extend([0xd0]+[0x70]*9+[0xd0,0x41,FINAL_CARD_DL&255,FINAL_CARD_DL>>8])
    return bytes(data)


def display_addresses():
    addresses=dict(zip(all_lines(),_line_addresses()))
    return [addresses[line] for line in display_lines()]


def display_lines():
    return tuple(line for page in pages() for line in (*page,*(['']*(HISTORY_ROWS-len(page)))))+('',)*HISTORY_ROWS


def pages():
    result=list(CREDITS);paragraph=[]
    for line in (*GREETZ,''):
        if line:paragraph.append(line)
        elif paragraph:
            result.append(tuple(paragraph));paragraph=[]
    assert all(0<len(page)<=HISTORY_ROWS for page in result)
    return tuple(result)


def page_starts():
    credits_end=START+len(CREDITS)*1000
    greetings=len(pages())-len(CREDITS)
    assert credits_end<END and greetings>0
    return tuple(START+i*1000 for i in range(len(CREDITS)))+tuple(
        credits_end+(END-credits_end)*i//greetings for i in range(greetings))


def inserts():
    return [(ENTRY, helper()), (FONT, font_data(card=True)), *line_records()]
