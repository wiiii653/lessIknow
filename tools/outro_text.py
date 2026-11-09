"""Finale text, unpacked into the retired second bitmap buffer on entry."""
from build_sequence import Code
from music_timing import tick_at_bar

ENTRY = 0xC000
RESET_ENTRY = 0xC340
START, END = tick_at_bar(144)-2000, tick_at_bar(158)
TEXT_POINTERS = 0xC400
FONT = 0xC800
TEXT_LOW = 0xC48A
TEXT_HIGH = 0xCC00
TEXT_END = 0xCF00
STATE_FLAG = 0x0DD0
STATE_START = 0x0DD1
STATE_PHASE = 0x0DD2
TMP_LO = 0x0DD3
TMP_HI = 0x0DD4
TMP_INDENT = 0x0DD5
TMP_ROW = 0x0DD6
HISTORY_ROWS = 6
TEXT_ROWS = HISTORY_ROWS + 1
BITMAP_SKIP = (TEXT_ROWS-5)*8
BITMAP_ROWS = 192-BITMAP_SKIP
BITMAP_DL = 1+TEXT_ROWS*3
FOOTER_DL = BITMAP_DL+BITMAP_ROWS*3
PALETTE_VCOUNT = (1+TEXT_ROWS*8+7)//2
PROMPT = b'>'

CREDITS = (
    ("SYS.OPEN CREDITS [OK]", "THE LESS I KNOW THE BETTER", "AN ATARI XE 1 MB DEMO", "BY OGNJEN",
     "MADE WITH OPENAI CODEX", "HUMAN VISION / LLM CODE"),
    ("SYS.OPEN AUDIO.LOG [OK]", "SONG / TAME IMPALA", "THE LESS I KNOW THE BETTER",
     "POKEY / OGNJEN / CODEX", "MIDI / MIDISHOW 200337"),
    ("UPLINK SV2026 [CONNECTED]", "MADE FOR", "SILLY VENTURE 2026",
     "AI TOOLS / ATARI SOUL"),
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
    "VIRUS / FOORMAN / MAQ",
    "ATARIONLINE.PL / PTODT",
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
    '+':('00000','00100','00100','11111','00100','00100','00000'),
}


def all_lines():
    lines = tuple(line for page in CREDITS for line in page) + GREETZ
    if len(lines) > 38 or any(len(line) > 36 for line in lines):
        raise ValueError('outro text exceeds its compact line layout')
    if len(GREETZ) > 23:
        raise ValueError('greetz needs more than the reserved scroll window')
    return lines


# Three-pixel-wide glyphs: ANTIC 4 supplies independently coloured letters
# over true COLBK black, unlike the shared-hue ANTIC 2 high-resolution mode.
TERMINAL_FONT = {
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
}

def font_data():
    font=bytearray(1024)
    for char in set(''.join(all_lines())+'>'):
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
    return bytes(font)


def line_data():
    lines = all_lines()
    ptrs = bytearray()
    records = bytearray()
    addresses = []
    pos = TEXT_POINTERS + 2 * len(lines)
    high = False
    for line in lines:
        if not high and pos + 44 > 0xC800:
            high = True
            pos = TEXT_HIGH
        addresses.append(pos)
        encoded = line.upper().encode('ascii')
        records.extend((PROMPT if line else b' ') + encoded.ljust(40-len(PROMPT), b' ') + b' ' * 4)
        pos += 44
    ptrs.extend(address & 255 for address in addresses)
    ptrs.extend(address >> 8 for address in addresses)
    # Two pointer tables are followed by 44-byte records.
    first_count = sum(address < 0xC800 for address in addresses)
    first = records[:first_count * 44]
    second = records[first_count * 44:]
    return bytes(ptrs), bytes(first), bytes(second)


def helper():
    c = Code(ENTRY)
    def a(op, address): c.emit(op, address & 255, address >> 8)
    c.label('active')
    # Text replaces only black upper bitmap rows; artwork stays at the same Y.
    a(0xAD, STATE_FLAG); c.branch(0xF0, 'init_text');c.jump(0x4C,'text_ready')
    c.label('init_text')
    c.emit(0xA9, 1); a(0x8D, STATE_FLAG)
    for page, length in ((0,256),(1,256),(2,BITMAP_ROWS*3-512)):
        c.emit(0xA2,0);c.label(f'copy{page}')
        a(0xBD,0xB802+BITMAP_SKIP*3+page*256)
        a(0x9D,0xBC00+BITMAP_DL+page*256)
        c.emit(0xE8,0xE0,length&255);c.branch(0xD0,f'copy{page}')
    for base in (0xBC00,):
        c.emit(0xA9,0x80);a(0x8D,base)
        for row in range(TEXT_ROWS):
            c.emit(0xA9,0xC4 if row==TEXT_ROWS-1 else 0x44);a(0x8D,base+1+row*3)
        for row,cmd in ((69-BITMAP_SKIP,0x4E),(147-BITMAP_SKIP,0x4E),
                        (77-TEXT_ROWS*8,0xCE),(155-TEXT_ROWS*8,0xCE)):
            c.emit(0xA9,cmd);a(0x8D,base+BITMAP_DL+row*3)
        for offset,value in enumerate((0x90,0x41,base&255,base>>8)):
            c.emit(0xA9,value);a(0x8D,base+FOOTER_DL+offset)
    c.emit(0xA9,0xC8);a(0x8D,0xD409)
    c.label('text_ready')
    c.label('choose')
    c.emit(0xA9,0);a(0x8D,0xBC02);c.emit(0xA9,0xC8);a(0x8D,0xBC03)
    c.emit(0xA9,32);a(0x8D,FONT+38);a(0xAD,0x83E2);c.emit(0x29,0xFC);c.branch(0xD0,'status_clean')
    c.emit(0xA9,47);a(0x8D,FONT+38);c.label('status_clean')
    a(0xAD,0x83E4);c.branch(0xD0,'final_blank')
    a(0xAD,0x83E3);c.emit(0xC9,END>>8);c.branch(0x90,'cards');c.branch(0xD0,'final_blank')
    a(0xAD,0x83E2);c.emit(0xC9,END&255);c.branch(0x90,'cards')
    c.label('final_blank')
    blank=_line_addresses()[all_lines().index('')]
    c.emit(0xA9,blank&255);a(0x8D,0xBC02);c.emit(0xA9,blank>>8);a(0x8D,0xBC03)
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
    c.emit(0xA9,0);a(0x8D,TMP_INDENT)
    c.emit(0xA2, 0)
    c.label('row')
    c.emit(0x8A); a(0x8D,TMP_ROW)
    a(0xAD, TMP_ROW); c.emit(0x18); a(0x6D, STATE_START); c.emit(0xA8)
    c.jump(0xB9, 'line_lo'); c.emit(0x18); a(0x6D, TMP_INDENT); a(0x8D, TMP_LO)
    c.jump(0xB9, 'line_hi'); c.emit(0x69, 0); a(0x8D, TMP_HI)
    a(0x20,0xEB44)
    a(0xAD, TMP_ROW); c.emit(0x0A, 0x18); a(0x6D, TMP_ROW); c.emit(0xA8)
    a(0xAD, TMP_LO); a(0x99, 0xBC05)
    a(0xAD, TMP_HI); a(0x99, 0xBC06)
    c.emit(0xE8, 0xE0, HISTORY_ROWS); c.branch(0xD0, 'row')
    c.label('done')
    a(0xAD,STATE_FLAG);c.emit(0xC9,1);c.branch(0xD0,'published')
    c.label('publish_wait');a(0xAD,0xD40B);c.emit(0xC9,124);c.branch(0x90,'publish_wait');c.emit(0xC9,128);c.branch(0xB0,'publish_wait')
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
    c.emit(0xA9,0x84);a(0x8D,0xD403)
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
    count = len(all_lines())
    result=[];pos=TEXT_POINTERS+count*2;high=False
    for _ in all_lines():
        if not high and pos+44>0xC800:
            high=True;pos=TEXT_HIGH
        result.append(pos);pos+=44
    return result


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
    ptrs, low_records, high_records = line_data()
    # Two pointer tables and line records are packed into the existing
    # retired second framebuffer, loaded only on finale entry.
    table_and_low = bytes(len(ptrs)) + low_records
    return [(ENTRY, helper()), 
            (TEXT_POINTERS, table_and_low), (TEXT_HIGH, high_records),
            (FONT, font_data())]
