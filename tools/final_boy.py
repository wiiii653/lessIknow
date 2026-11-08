"""Final shot: defeated boy, alternating orbiting stars/melody, black ending."""
import math
from collections import deque
from functools import lru_cache
from pathlib import Path
from build_sequence import Code
from engine_effects import cached_display_list
from music_timing import tick_at_bar
from whistle_pmg import SHAPES as WHISTLE_SHAPES

STAR_SHAPE=(0,0,0x10,0x54,0x38,0xfe,0x38,0x54,0x10,0,0,0)
NOTE_SHAPES=tuple(glyph[::2] for glyph in WHISTLE_SHAPES)
GLYPH_ROWS=12

def notes_active(tick):
    return bool((tick >> 8) & 1)

START,END=tick_at_bar(144),tick_at_bar(160)
FADE_START=END-128
ENTRY=0x5cd0
ORBIT_DATA=0x69c4  # 60-byte gap after the Trevor controller
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
            if y in (5,9,60) or (y>=9 and (x+y//3)%24==0):p[y*160+x]=2
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
    return HEAD_X+round(22*math.cos(t))-4,round((HEAD_Y+20*math.sin(t)-7+17)/2)


def fade_level(tick):
    return 12 if tick<FADE_START else max(0,12-2*((tick-FADE_START)//16))


def helper(copy_address):
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    c.emit(0xa9,0);a(0x8d,0x83e5)
    a(0xad,0x83fa);c.emit(0xc9,0x7e);c.branch(0xd0,'bitmap_changed');c.jump(0x4c,'prepare')
    c.label('bitmap_changed');c.emit(0xa9,0x7e);a(0x8d,0x83fa)
    c.emit(0xa9,FRAME_KEY);a(0x8d,0x83ed)
    a(0xad,0x83e6);c.emit(0x29,4,0x0a,0x0a,0x0a,0x49,0xb0);a(0x8d,0x83fe)
    a(0x20,copy_address);c.emit(0xa9,1);a(0x8d,0x83e5)
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
    c.label('swap')
    c.label('prepare')
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x29,15);a(0x8d,0x83ff)
    # Double-buffer every glyph; keep the previous orbit visible until publication.
    a(0xad,0xd407);c.emit(0x29,0x80,0x49,0x80);a(0x8d,0x83e8)
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
        a(0xae,0x83ff);c.jump(0xbd,f'star_y{plane}');c.emit(0x38,0xe9,2,0xa8)
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
    c.label('held');a(0xad,0x83e8);c.emit(0x09,8);a(0x8d,0xd407)
    for plane in range(4):
        a(0xae,0x83ff);c.jump(0xbd,f'star_x{plane}');a(0x8d,0xd000+plane)
        c.jump(0xbd,'star_hues'+str(plane));a(0x0d,0x83ec);a(0x8d,0xd012+plane)
        c.emit(0xa9,0);a(0x8d,0xd004+plane);a(0x8d,0xd008+plane)
    for addr,val in ((0xd01b,1),(0xd400,0x2e),(0xd01a,0),(0xd00c,0)):
        c.emit(0xa9,val);a(0x8d,addr)
    a(0xad,0x83ec);c.branch(0xf0,'dark_pixels')
    for addr,hue in ((0xd016,0x40),(0xd017,0x90),(0xd018,0x20)):
        a(0xad,0x83ec);c.emit(0x09,hue);a(0x8d,addr)
    c.emit(0xa9,2);a(0x8d,0xd01d);c.emit(0x60)
    c.label('dark_pixels');c.emit(0xa9,0)
    for addr in (0xd016,0xd017,0xd018,0xd01d):a(0x8d,addr)
    c.emit(0x60)
    for label in ('dl1','dl2'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    for i in range(5):c.labels[f'clear{i}_hi']=c.labels[f'clear{i}']+2
    for i in range(4):c.labels[f'put{i}_hi']=c.labels[f'put{i}']+2
    c.labels['star_x0']=ORBIT_DATA
    c.labels['star_y0']=ORBIT_DATA+16
    for plane in range(1,4):
        c.label(f'star_x{plane}');c.emit(*(star_position(phase,plane)[0]+48 for phase in range(16)))
        c.label(f'star_y{plane}');c.emit(*(star_position(phase,plane)[1] for phase in range(16)))
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
    out=bytearray(bank);code=helper(copy_address);offset=ENTRY-0x4000
    assert out[offset:offset+len(code)]==bytes(len(code))
    out[offset:offset+len(code)]=code
    orbit=bytes(star_position(phase,0)[0]+48 for phase in range(16))
    orbit+=bytes(star_position(phase,0)[1] for phase in range(16))
    for plane in range(4):
        for shift in (0,8):
            orbit+=bytes(((SHAPE_DATA>>shift)&255,((SHAPE_DATA+12+plane*12)>>shift)&255))
    offset=ORBIT_DATA-0x4000
    assert out[offset:offset+len(orbit)]==bytes(len(orbit))
    out[offset:offset+len(orbit)]=orbit
    shapes=bytes(STAR_SHAPE)+b''.join(bytes(g) for g in NOTE_SHAPES)
    shapes+=bytes(max(0,12-2*i) for i in range(16))
    shapes+=bytes((0x20,0x90,0x40,0)[i%4] for i in range(19))
    offset=SHAPE_DATA-0x4000
    assert out[offset:offset+len(shapes)]==bytes(len(shapes))
    out[offset:offset+len(shapes)]=shapes
    return bytes(out)


def install_bitmap(bank,index):
    if index!=BITMAP_BANK:return bank
    out=bytearray(bank);data=packed();offset=BITMAP_SOURCE-0x4000
    assert out[offset:offset+len(data)]==bytes(len(data))
    out[offset:offset+len(data)]=data
    return bytes(out)
