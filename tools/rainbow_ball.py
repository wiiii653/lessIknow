"""Four rainbow player bands and four missile spray streams, bank 15."""
import math
from build_sequence import Code
from engine_effects import EFFECT_ORIGIN
ENTRY=0x6000
RESTORE=0x6f00
SHOT_START,SHOT_END=6981,7978

def paths():
    # 997 music ticks, one flight. The final sampled phase is 996 >> 3 = 124.
    return [(round(95+42*(i/124)),
             max(2,round(28+10*(i/124)-32*math.sin(math.pi*i/124))))
            for i in range(125)]


def spin_masks():
    """Eight real shape/color rotations, four players, sixteen double-lines."""
    frames=[]
    outline=(0x18,0x3c,0x7e,0x7e,0xff,0xff,0xff,0xff,
             0xff,0xff,0xff,0xff,0x7e,0x7e,0x3c,0x18)
    for phase in range(8):
        theta=phase*math.pi/4
        planes=[bytearray(16) for _ in range(4)]
        for row,shape in enumerate(outline):
            seam=round(3.5+2.2*math.sin(theta+(row-7.5)*0.13))
            shape &= ~(1<<(7-seam))
            for col in range(8):
                equator=round(7.5+math.sin(theta)*(col-3.5)*0.7)
                if row==equator:shape &= ~(1<<(7-col))
            planes[((row+phase*2)//4)%4][row]=shape
        frames.append(planes)
    return frames

def helper():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    a(0xad,0x83e0);c.emit(0xc9,14);c.branch(0xd0,'not_portrait')
    a(0xad,0x83e3);c.emit(0xc9,14960>>8);c.branch(0x90,'not_portrait');a(0x4c,0x6900)
    c.label('not_portrait');a(0xad,0x83e0);c.emit(0xc9,13);c.branch(0xd0,'inactive')
    # This interval is entirely within high-byte $1B..$1F.
    for threshold,low,high in ((SHOT_START,'inactive','after_start'),(SHOT_END,'active','inactive')):
        a(0xad,0x83e3);c.emit(0xc9,threshold>>8);c.branch(0x90,low);c.branch(0xd0,high)
        a(0xad,0x83e2);c.emit(0xc9,threshold&255);c.branch(0x90,low);c.jump(0x4c,high)
        if high=='after_start':c.label(high)
    c.label('inactive')
    a(0xad,0x83fe);c.emit(0xc9,1);c.branch(0xd0,'ordinary')
    c.emit(0xa9,0);a(0x8d,0x83fe);a(0x20,RESTORE)
    c.label('ordinary');a(0x4c,EFFECT_ORIGIN)
    c.label('active')
    c.emit(0xa9,1);a(0x8d,0x83fe)
    # Use the complete 16-bit elapsed time; low-byte wrap never restarts flight.
    a(0xad,0x83e2);c.emit(0x38,0xe9,SHOT_START&255);a(0x8d,0x83fd)
    a(0xad,0x83e3);c.emit(0xe9,SHOT_START>>8)
    for _ in range(3):c.emit(0x4a);a(0x6e,0x83fd)
    a(0xad,0x83fd);a(0x8d,0x83ff)
    c.emit(0xa9,0,0xa2,0)
    c.label('clear')
    for base in (0x0980,0x0a00,0x0b00):a(0x9d,base)
    c.emit(0xe8);c.branch(0xd0,'clear')
    a(0xae,0x83ff)
    c.jump(0xbd,'ball_x');c.emit(0x18,0x69,48)
    for i in range(4):a(0x8d,0xd000+i)
    c.jump(0xbd,'ball_y');c.emit(0xa8)
    # Rotate both the colored panels and the curved seams around the ball.
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x29,7,0x0a,0x0a,0x0a,0x0a,0xaa)
    c.label('spin_rows')
    for player in range(4):
        c.jump(0xbd,f'spin{player}');a(0x99,0x0a00+128*player)
    c.emit(0xe8,0xc8,0x8a,0x29,15);c.branch(0xd0,'spin_rows')
    a(0xae,0x83ff)
    for i in range(4):
        c.jump(0xbd,f'spray_x{i}');a(0x8d,0xd004+i)
        c.jump(0xbd,f'spray_y{i}');c.emit(0xa8)
        for dy in (0,4,9):
            a(0xb9,0x0980+dy);c.emit(0x09,3<<(i*2));a(0x99,0x0980+dy)
    # Rotate through the Atari hue wheel, offset between the four stripes.
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x29,15,0xaa)
    for i in range(4):
        c.jump(0xbd,f'hues{i}');a(0x8d,0xd012+i)
    for addr,val in ((0xd407,8),(0xd01b,1),(0xd01d,3),(0xd400,0x2e),(0xd00c,0)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0xa9,1,0xa2,3)
    c.label('sizes');a(0x9d,0xd008);c.emit(0xca);c.branch(0x10,'sizes');c.emit(0x60)
    positions=paths()
    c.label('ball_x');c.emit(*(x-8 for x,y in positions))
    c.label('ball_y');c.emit(*((y+17)//2 for x,y in positions))
    frames=spin_masks()
    for player in range(4):
        c.label(f'spin{player}');c.emit(*(value for frame in frames for value in frame[player]))
    for i in range(4):
        dx=(-20,-12,16,24)[i]
        c.label(f'spray_x{i}');c.emit(*(max(50,min(202,x+48+dx+(j%4-2)*2)) for j,(x,y) in enumerate(positions)))
        c.label(f'spray_y{i}');c.emit(*(max(9,min(103,(y+17)//2+((i*3+j)%9)-4)) for j,(x,y) in enumerate(positions)))
        c.label(f'hues{i}');c.emit(*((((j+i*4)%15+1)<<4)|10 for j in range(16)))
    result=c.finish();assert ENTRY+len(result)<RESTORE
    return result
