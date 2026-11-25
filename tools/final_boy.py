"""Final shot: defeated boy, alternating orbiting stars/melody, black ending."""
import math
from collections import deque
from functools import lru_cache
from pathlib import Path
from build_sequence import Code
from engine_effects import PMBASE_SHADOW, cached_display_list
from music_timing import tick_at_bar
from whistle_pmg import SHAPES as WHISTLE_SHAPES
from outro_loader import ENTRY as OUTRO_ENTRY, FLAG as OUTRO_FLAG, PRELOAD as OUTRO_PRELOAD
from outro_text import START

STAR_SHAPE=(0,0,0x10,0x54,0x38,0xfe,0x38,0x54,0x10,0,0,0)
NOTE_SHAPES=tuple(glyph[::2] for glyph in WHISTLE_SHAPES)
GLYPH_ROWS=12

def notes_active(tick):
    return bool((tick >> 8) & 1)

END=tick_at_bar(139)
FADE_START=END-128
ENTRY=0x5cd0
ORBIT_DATA=0x69c4  # 60-byte gap after the Trevor controller
ENTRY_BLANK = 0xFE88
ENTRY_VISIBLE = 0xFEB0
PORTRAIT_LUMA = 0x83ef
MARK_ANIMATE = 0xECE4
CARD_UPDATE = 0xED35
CARD_PAGES_ENTRY = 0x4A00
MARK_BANK = 20
MARK_FRAMES = 0x6800
MARK_FRAMES_PER_BANK = 8
SHAPE_DATA=0x7fa0  # 96 unused bytes after the launch wind masks
BITMAP_BANK=39
BITMAP_SOURCE=0x4a00
FRAME_KEY=36  # unbanked ribbon-copy trampoline's dedicated final-shot route
HEAD_X,HEAD_Y=34,74


@lru_cache(maxsize=1)
def artwork():
    rgb=Path('build/boy-floor-v145.rgb').read_bytes()
    assert len(rgb)==144*56*3
    black=bytearray(max(rgb[i:i+3])<45 for i in range(0,len(rgb),3))
    outside=bytearray(144*56);queue=deque()
    for pos in list(range(144))+list(range(55*144,56*144))+[y*144 for y in range(56)]+[y*144+143 for y in range(56)]:
        if black[pos] and not outside[pos]:outside[pos]=1;queue.append(pos)
    while queue:
        pos=queue.popleft();y,x=divmod(pos,144)
        for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=xx<144 and 0<=yy<56:
                n=yy*144+xx
                if black[n] and not outside[n]:outside[n]=1;queue.append(n)
    p=bytearray(160*64)
    for y in range(64):
        for x in range(160):
            if y==60 or (y>=9 and (x+y//3)%24==0):p[y*160+x]=2
            elif y>=9 and y%12==0:p[y*160+x]=1
    points={}
    for y in range(56):
        for x in range(144):
            if outside[y*144+x]:continue
            i=(y*144+x)*3;r,g,b=rgb[i:i+3]
            ink=0 if max(r,g,b)<45 else 1 if r>g*1.15 and b>g*1.15 else 2 if b>r*1.15 or g>r*1.15 else 3
            points[x+8,y+6]=ink
    for x,y in points:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)):
            xx,yy=x+dx,y+dy
            if 0<=xx<160 and 0<=yy<64 and (xx,yy) not in points:p[yy*160+xx]=0
    for (x,y),ink in points.items():p[y*160+x]=ink
    return bytes(p)


def packed():
    p=artwork()
    return bytes(sum(p[i+k]<<(6-2*k) for k in range(4)) for i in range(0,len(p),4))


def star_position(phase,plane):
    t=((phase+plane*4)&15)*math.tau/16
    return HEAD_X+round(22*math.cos(t))-4,round((HEAD_Y+20*math.sin(t)-7+17)/2)+16


def fade_level(tick):
    return 12 if tick<FADE_START else max(0,12-2*((tick-FADE_START)//16))


def helper(copy_address):
    import final_orbits
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    c.emit(0xa9,0);a(0x8d,0x83e5)
    a(0xad,0x83fa);c.emit(0xc9,0x7e);c.branch(0xd0,'bitmap_changed');c.jump(0x4c,'prepare')
    c.label('bitmap_changed');a(0x20,ENTRY_BLANK);c.emit(0xa9,0x7e);a(0x8d,0x83fa)
    c.emit(0xa9,FRAME_KEY);a(0x8d,0x83ed)
    a(0x8d,0x0dfe);a(0x8d,0x0dff)
    c.emit(0xa9,0);a(0x8d,OUTRO_FLAG);a(0x8d,0xd01d)
    c.emit(0xa9,0x90);a(0x8d,0x83fe)
    a(0x20,copy_address)
    cached_display_list(c,7)
    a(0xad,0x83e6);c.jump(0x8d,'dl1_hi');c.jump(0x8d,'dl2_hi')
    c.emit(0xa9,3);c.jump(0x8d,'dl1_lo');c.emit(0xa9,4);c.jump(0x8d,'dl2_lo')
    c.emit(0xa9,0);a(0x8d,0x83ea);a(0xad,0x83fe);a(0x8d,0x83eb)
    c.emit(0xa0,0,0xa2,3)
    c.label('rows');a(0xad,0x83ea);c.label('dl1');c.emit(0x8d,0,0)
    a(0xad,0x83eb);c.label('dl2');c.emit(0x8d,0,0)
    for label in ('dl1','dl2'):
        c.jump(0xad,label+'_lo');c.emit(0x18,0x69,3);c.jump(0x8d,label+'_lo');c.branch(0x90,label+'_ready');c.jump(0xee,label+'_hi');c.label(label+'_ready')
    c.emit(0xca);c.branch(0xd0,'next_line');c.emit(0xa2,3)
    a(0xad,0x83ea);c.emit(0x18,0x69,40);a(0x8d,0x83ea);c.branch(0x90,'next_line');a(0xee,0x83eb)
    c.label('next_line');c.emit(0xc8,0xc0,192);c.branch(0xd0,'rows')
    # Unpack the terminal while the outgoing frame is still blanked.
    a(0x20,OUTRO_PRELOAD)
    c.label('swap')
    c.label('prepare')
    a(0x20,final_orbits.ENTRY)
    # Double-buffer every glyph; keep the previous orbit visible until publication.
    a(0xad,0x83e8);c.emit(0x29,0x80,0x49,0x80);a(0x8d,0x83e8)
    for i,high in enumerate((9,10,10,11,11)):
        c.emit(0xa9,high);a(0x0d,0x83e8);c.jump(0x8d,f'clear{i}_hi')
    for i,high in enumerate((10,10,11,11)):
        c.emit(0xa9,high);a(0x0d,0x83e8);c.jump(0x8d,f'put{i}_hi')
    c.emit(0xa9,0,0xa2,127)
    c.label('clear')
    for i,addr in enumerate((0x980,0xa00,0xa80,0xb00,0xb80)):
        c.label(f'clear{i}');a(0x9d,addr)
    c.emit(0xca);c.branch(0x10,'clear')
    for plane in range(4):
        a(0xad,final_orbits.VALUES_Y+plane);c.emit(0x38,0xe9,21,0xa8)
        a(0xad,0x83e3);c.emit(0x29,1,0xaa)
        c.jump(0xbd,f'select_lo{plane}');c.jump(0x8d,f'shape{plane}_lo')
        c.jump(0xbd,f'select_hi{plane}');c.jump(0x8d,f'shape{plane}_hi')
        c.emit(0xa2,0)
        c.label(f'star{plane}');c.label(f'shape{plane}');c.jump(0xbd,'star_shape');c.label(f'put{plane}');a(0x99,0xa00+plane*128)
        c.emit(0xc8,0xe8,0xe0,GLYPH_ROWS);c.branch(0xd0,f'star{plane}')
    # Fade stays zero after the music ends, including later callbacks.
    a(0xad,0x83e4);c.branch(0xd0,'black')
    a(0xad,0x83e3);c.emit(0xc9,END>>8);c.branch(0x90,'before_end');c.branch(0xd0,'black')
    a(0xad,0x83e2);c.emit(0xc9,END&255);c.branch(0xb0,'black')
    c.label('before_end')
    a(0xad,0x83e2);c.emit(0x38,0xe9,FADE_START&255);a(0x8d,0x83ea)
    a(0xad,0x83e3);c.emit(0xe9,FADE_START>>8);c.branch(0x90,'full_light')
    a(0xad,0x83ea);c.emit(0x4a,0x4a,0x4a,0x4a,0xaa);c.jump(0xbd,'fade');c.jump(0x4c,'light_ready')
    c.label('full_light');c.emit(0xa9,12);c.jump(0x4c,'light_ready')
    c.label('black');c.emit(0xa9,0)
    c.label('light_ready');a(0x8d,0x83ec)
    c.label('wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'wait');c.emit(0xc9,128);c.branch(0xb0,'wait')
    a(0xad,0x83e5);c.branch(0xf0,'held')
    c.emit(0xa9,0);a(0x8d,0xd402);a(0xad,0x83e6);a(0x8d,0xd403);c.emit(0x49,4);a(0x8d,0x83e6)
    c.label('held')
    a(0xad,0x83ec);c.branch(0xf0,'portrait_light_ready')
    c.emit(0x4a,0x69,4,0x29,0xfe)
    c.label('portrait_light_ready');a(0x8d,PORTRAIT_LUMA)
    a(0xad,0x83e8);c.emit(0x09,8);a(0x8d,PMBASE_SHADOW);a(0x8d,0xd407)
    for plane in range(4):
        a(0xad,final_orbits.VALUES_X+plane);a(0x8d,0xd000+plane)
        a(0xae,0x83ff)
        c.jump(0xbd,'star_hues'+str(plane));a(0x0d,0x83ec);a(0x8d,0xd012+plane)
        c.emit(0xa9,0);a(0x8d,0xd004+plane);a(0x8d,0xd008+plane)
    for addr,val in ((0xd01b,1),(0xd400,0x2e),(0xd01a,0),(0xd00c,0)):
        c.emit(0xa9,val);a(0x8d,addr)
    a(0xad,OUTRO_FLAG);c.branch(0xf0,'load_terminal')
    a(0xad,0x83ec);c.branch(0xf0,'dark_pixels')
    a(0x20,ENTRY_VISIBLE);a(0x4c,OUTRO_ENTRY)
    c.label('dark_pixels');c.emit(0xa9,0)
    for addr in (0xd016,0xd017,0xd018,0xd01d):a(0x8d,addr)
    c.label('load_terminal');a(0x4c,OUTRO_ENTRY)
    for label in ('dl1','dl2'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    for i in range(5):c.labels[f'clear{i}_hi']=c.labels[f'clear{i}']+2
    for i in range(4):c.labels[f'put{i}_hi']=c.labels[f'put{i}']+2
    for plane in range(4):
        c.labels[f'shape{plane}_lo']=c.labels[f'shape{plane}']+1
        c.labels[f'shape{plane}_hi']=c.labels[f'shape{plane}']+2
        for part,shift in (('lo',0),('hi',8)):
            c.labels[f'select_{part}{plane}']=ORBIT_DATA+32+plane*4+(2 if shift else 0)
    c.labels['star_shape']=SHAPE_DATA
    c.labels['fade']=SHAPE_DATA+60
    for plane in range(4):c.labels[f'star_hues{plane}']=SHAPE_DATA+76+plane
    code=bytes(c.finish())
    assert ENTRY+len(code)<=0x6000,len(code)
    return code


def install_control(bank,copy_address):
    import final_orbits
    out=bytearray(bank);code=helper(copy_address);offset=ENTRY-0x4000
    assert out[offset:offset+len(code)]==bytes(len(code))
    out[offset:offset+len(code)]=code
    import outro_text
    card=card_helper();offset=outro_text.FINAL_CARD_ENTRY-0x4000
    assert offset+len(card)<=0x2000 and not any(out[offset:offset+len(card)])
    out[offset:offset+len(card)]=card
    for address, payload in ((outro_text.FINAL_CARD_SOURCE, outro_text.final_card_display_list()),
                             *final_mark_inserts()):
        offset=address-0x4000
        assert not any(out[offset:offset+len(payload)]), hex(address)
        out[offset:offset+len(payload)]=payload
    orbit=bytes(32)  # Reserved for the orbit midpoint routine.
    for plane in range(4):
        for shift in (0,8):
            orbit+=bytes(((SHAPE_DATA>>shift)&255,((SHAPE_DATA+12+plane*12)>>shift)&255))
    offset=ORBIT_DATA-0x4000
    assert out[offset:offset+len(orbit)]==bytes(len(orbit))
    out[offset:offset+len(orbit)]=orbit
    shapes=bytes(STAR_SHAPE)+b''.join(bytes(g) for g in NOTE_SHAPES)
    shapes+=bytes(max(0,12-2*i) for i in range(16))
    # Nineteen vivid GTIA hues give each plane a phase-offset rainbow sweep.
    rainbow=(0x0f,0x2f,0x4f,0x6f,0x8f,0xaf,0xcf,0xef,
             0x1f,0x3f,0x5f,0x7f,0x9f,0xbf,0xdf,0xff,
             0x1e,0x5e,0x9e)
    shapes+=bytes(rainbow)
    offset=SHAPE_DATA-0x4000
    assert out[offset:offset+len(shapes)]==bytes(len(shapes))
    out[offset:offset+len(shapes)]=shapes
    return final_orbits.install(out)


def final_mark_inserts():
    import outro_text as t

    tiles, glyphs = t.final_mark()
    first, tail = glyphs[:144], glyphs[144:]
    font_dest = t.FONT + t.FINAL_MARK_FIRST_GLYPH * 8
    copy = Code(t.FINAL_MARK_FONT_COPY)
    parts = ((t.FINAL_MARK_GLYPHS,first),(t.FINAL_MARK_GLYPHS_TAIL,tail))
    for i, (src, data) in enumerate(parts):
        if data:
            copy.emit(0xa2,len(data));copy.label(f'glyphs{i}')
            copy.emit(0xbd,(src-1)&255,(src-1)>>8,0x9d,(font_dest-1)&255,(font_dest-1)>>8,0xca)
            copy.branch(0xd0,f'glyphs{i}')
        font_dest += len(data)
    copy.emit(0x4c,t.FINAL_MARK_DRAW&255,t.FINAL_MARK_DRAW>>8)

    draw = Code(t.FINAL_MARK_DRAW)
    draw.emit(0xa9,32,0xa2,t.FINAL_MARK_ROWS*40);draw.label('clear')
    dest = t.FINAL_MARK_SCREEN - 1
    draw.emit(0x9d,dest&255,dest>>8,0xca);draw.branch(0xd0,'clear')
    draw.emit(0xa2,t.FINAL_MARK_WIDTH-1);draw.label('tiles')
    for row in range(t.FINAL_MARK_ROWS):
        src = t.FINAL_MARK_TILES + row*t.FINAL_MARK_WIDTH
        dest = t.FINAL_MARK_SCREEN + row*40 + (40-t.FINAL_MARK_WIDTH)//2
        draw.emit(0xbd,src&255,src>>8,0x9d,dest&255,dest>>8)
    draw.emit(0xca);draw.branch(0x10,'tiles');draw.emit(0x60)

    draw_code, copy_code = bytes(draw.finish()), bytes(copy.finish())
    assert len(tail)<=t.FINAL_MARK_TILES-t.FINAL_MARK_GLYPHS_TAIL
    assert t.FINAL_MARK_TILES+len(tiles)<=ENTRY
    assert t.FINAL_MARK_DRAW+len(draw_code)<=0x69b8
    assert t.FINAL_MARK_FONT_COPY+len(copy_code)<=0x6000
    return (*parts,(t.FINAL_MARK_TILES,tiles),(t.FINAL_MARK_DRAW,draw_code),
            (t.FINAL_MARK_FONT_COPY,copy_code))


def card_helper():
    import outro_text as t
    from outro_palette import CARD_CLOCK_PENDING, CARD_FADE, CARD_FONT_ENTRY
    c=Code(t.FINAL_CARD_ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    a(0xad,0x83e4);c.branch(0xd0,'card')
    a(0xad,0x83e3);c.emit(0xc9,END>>8);c.branch(0x90,'normal');c.branch(0xd0,'card')
    a(0xad,0x83e2);c.emit(0xc9,END&255);c.branch(0xb0,'card')
    c.label('normal');a(0x4c,t.ENTRY)
    c.label('card');a(0xad,t.STATE_FLAG);c.emit(0xc9,3);c.branch(0xf0,'color')
    a(0x20,CARD_FONT_ENTRY)
    a(0x20,t.FINAL_MARK_FONT_COPY)
    c.emit(0xa2,len(t.final_card_display_list())-1);c.label('copy')
    a(0xbd,t.FINAL_CARD_SOURCE);a(0x9d,t.FINAL_CARD_DL);c.emit(0xca);c.branch(0x10,'copy')
    c.label('wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'wait');c.emit(0xc9,128);c.branch(0xb0,'wait')
    for address,value in ((CARD_FADE,CARD_CLOCK_PENDING),(0xd409,t.FONT>>8),(0xd402,t.FINAL_CARD_DL&255),(0xd403,t.FINAL_CARD_DL>>8),(t.STATE_FLAG,3)):
        c.emit(0xa9,value);a(0x8d,address)
    c.label('color');a(0x4c,CARD_UPDATE)
    result=bytes(c.finish());assert t.FINAL_CARD_ENTRY+len(result)<=t.FINAL_MARK_FONT_COPY,len(result)
    return result


def install_bitmap(bank,index):
    if index!=BITMAP_BANK:return bank
    out=bytearray(bank);data=packed();offset=BITMAP_SOURCE-0x4000
    assert out[offset:offset+len(data)]==bytes(len(data))
    out[offset:offset+len(data)]=data
    return bytes(out)

def install_mark_frames(bank, index):
    from outro_text import FINAL_MARK_PHASES, final_mark

    first = (index - MARK_BANK) * MARK_FRAMES_PER_BANK
    if not 0<=first<FINAL_MARK_PHASES:
        return bank
    frames = b''.join(final_mark(phase)[1].ljust(256, b'\0')
                      for phase in range(first,first+MARK_FRAMES_PER_BANK))
    offset = MARK_FRAMES - 0x4000
    assert offset + len(frames) <= len(bank)
    assert not any(bank[offset:offset + len(frames)])
    return bank[:offset] + frames + bank[offset + len(frames):]


def mark_animator():
    from outro_text import FONT, FINAL_MARK_FIRST_GLYPH, FINAL_MARK_ROWS, FINAL_MARK_WIDTH
    from school_portrait_bank import bank_value

    c = Code(MARK_ANIMATE)
    def a(op, addr):
        c.emit(op, addr & 255, addr >> 8)

    for address, value in ((0xd016,0x0e),(0xd017,0x9a),(0xd018,0x2c)):
        c.emit(0xa9,value);a(0x8d,address)
    # The interrupt count keeps moving after the last music packet.
    a(0xad,0x24aa);c.emit(0x4a,0x4a,0x29,31)
    c.label('previous');c.emit(0xc9,0xff);c.branch(0xf0,'done')
    c.jump(0x8d,'previous_phase')
    c.emit(0xaa,0x29,7,0x09,MARK_FRAMES >> 8);c.jump(0x8d,'frame_page')
    c.emit(0x8a,0x4a,0x4a,0x4a,0xaa)
    # Even at VCOUNT 143, more than 60 PAL scanlines remain before
    # ANTIC fetches the mark. Allow for the stereo decoder's longer ticks.
    c.label('blank');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'blank')
    c.emit(0xc9,144);c.branch(0xb0,'blank')
    a(0xad,0xd301);c.emit(0x48)
    a(0xbd,bank_value(MARK_BANK));a(0x8d,0xd301)
    c.emit(0xa2, FINAL_MARK_ROWS * FINAL_MARK_WIDTH * 8 - 1)
    c.label('copy');a(0xbd,MARK_FRAMES)
    a(0x9d,FONT+FINAL_MARK_FIRST_GLYPH*8)
    c.emit(0xca)
    c.emit(0xe0,0xff);c.branch(0xd0,'copy')
    c.emit(0x68);a(0x8d,0xd301)
    c.label('done');c.emit(0x60)
    c.labels['frame_page']=c.labels['copy']+2
    c.labels['previous_phase']=c.labels['previous']+1
    return bytes(c.finish())


def entry_blank():
    """Hide the outgoing bitmap while its RAM is reused by the terminal."""
    c = Code(ENTRY_BLANK)
    c.label('wait')
    c.emit(0xad,0x0b,0xd4,0xc9,124);c.branch(0x90,'wait')
    c.emit(0xc9,128);c.branch(0xb0,'wait')
    c.emit(0xa9,0)
    for address in (0xd016,0xd017,0xd018,0xd019,0xd01a,0xd01d):
        c.emit(0x8d,address&255,address>>8)
    c.emit(0x60)
    return bytes(c.finish())

def entry_visible():
    c = Code(ENTRY_VISIBLE)
    c.emit(0xad,PORTRAIT_LUMA&255,PORTRAIT_LUMA>>8,0xaa)
    for addr, hue in ((0xd016,0x40),(0xd017,0x90),(0xd018,0x20)):
        c.emit(0x8a,0x09,hue,0x8d,addr&255,addr>>8)
    c.emit(0xa9,2,0x8d,0x1d,0xd0,0x60)
    return bytes(c.finish())

def card_update():
    from school_portrait_bank import bank_value

    # Call the animation and then the text logic in bank 0.
    c = Code(CARD_UPDATE)
    for opcode,address in ((0x20,MARK_ANIMATE),(0xad,0xd301)):
        c.emit(opcode,address&255,address>>8)
    c.emit(0x48,0xad,bank_value(0)&255,bank_value(0)>>8,0x8d,1,0xd3)
    c.emit(0x20,CARD_PAGES_ENTRY&255,CARD_PAGES_ENTRY>>8,0x68,0x8d,1,0xd3,0x60)
    return bytes(c.finish())


def install_card_pages(bank):
    from outro_text import FINAL_CARD_PAGES, FINAL_CARD_TEXT, FINAL_CARD_TEXT_ROWS
    from outro_palette import CARD_FADE

    c = Code(CARD_PAGES_ENTRY)
    def a(op,addr):
        c.emit(op,addr&255,addr>>8)

    c.label('clock');a(0xae,0x24ab);a(0xac,0x24aa);a(0xec,0x24ab)
    c.branch(0xd0,'clock')
    a(0xad,CARD_FADE);c.branch(0x10,'elapsed')
    c.jump(0x8e,'start_hi');c.jump(0x8c,'start_lo')
    c.emit(0xa9,255);c.jump(0x8d,'previous');c.jump(0x8d,'page')
    c.label('elapsed');c.emit(0x98,0x38);c.jump(0xed,'start_lo')
    c.jump(0x8d,'low');c.emit(0x8a);c.jump(0xed,'start_hi')
    # A page takes four high-byte steps. Rebase at the end of the carousel,
    # preserving the remainder even when the NMI counter wraps.
    cycle_high = len(FINAL_CARD_PAGES)*4
    c.label('wrap');c.emit(0xc9,cycle_high);c.branch(0x90,'within_cycle')
    c.emit(0xe9,cycle_high,0x48)
    c.jump(0xad,'start_hi');c.emit(0x18,0x69,cycle_high);c.jump(0x8d,'start_hi')
    c.emit(0x68);c.jump(0x4c,'wrap')
    c.label('within_cycle');c.emit(0xaa,0x4a,0x4a);c.jump(0x8d,'next_page')
    c.jump(0xad,'low');c.emit(0x4a,0x4a,0x4a,0x4a)
    c.jump(0x1d,'quarters')
    c.jump(0xcd,'previous');c.branch(0xd0,'ready');c.emit(0x60)
    c.label('ready');c.jump(0x8d,'previous')
    c.emit(0x29,63,0xaa);c.jump(0xbd,'fade');c.emit(0x48)
    c.jump(0xae,'next_page')
    c.label('blank');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'blank')
    c.emit(0xc9,144);c.branch(0xb0,'blank')
    c.emit(0x8a);c.jump(0xcd,'page');c.branch(0xf0,'publish')
    c.jump(0x8d,'page')
    c.emit(0xa9,0);a(0x8d,CARD_FADE)
    for op,label in ((0xbd,'text_lo'),(0xbd,'text_hi')):
        c.jump(op,label);c.jump(0x8d,'read_lo' if label.endswith('lo') else 'read_hi')
    c.emit(0xa0,FINAL_CARD_TEXT_ROWS*40-1)
    c.label('read');a(0xb9,0)
    a(0x99,FINAL_CARD_TEXT);c.emit(0x88);c.branch(0x10,'read')
    c.label('publish');c.emit(0x68);a(0x8d,CARD_FADE);c.emit(0x60)

    c.labels['read_lo']=c.labels['read']+1;c.labels['read_hi']=c.labels['read']+2
    for label,value in (('start_hi',0),('start_lo',0),('low',0),
                        ('previous',255),('page',255),('next_page',0)):
        c.label(label);c.emit(value)
    c.label('quarters');c.emit(*(i*16&255 for i in range(cycle_high)))
    c.label('fade');c.emit(*[min(i,63-i,7)*2 for i in range(64)])
    c.label('text_lo');c.emit(*bytes(len(FINAL_CARD_PAGES)))
    c.label('text_hi');c.emit(*bytes(len(FINAL_CARD_PAGES)))
    data = c.finish()
    for index,page in enumerate(FINAL_CARD_PAGES):
        assert len(page)==FINAL_CARD_TEXT_ROWS
        address = CARD_PAGES_ENTRY+len(data)
        data[c.labels['text_lo']-CARD_PAGES_ENTRY+index] = address&255
        data[c.labels['text_hi']-CARD_PAGES_ENTRY+index] = address>>8
        for line in page:
            assert len(line)<=40 and all(32<=ord(char)<96 for char in line)
            data.extend(line.center(40).encode('ascii'))
    offset=CARD_PAGES_ENTRY-0x4000
    assert offset+len(data)<=0x1a00
    assert not any(bank[offset:offset+len(data)])
    return bank[:offset]+data+bank[offset+len(data):]
