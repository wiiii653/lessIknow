"""Notes and treble clefs emitted from the mouth, with missile sparkle tails."""
import math
from build_sequence import Code
from school_story import WHISTLE_START, WHISTLE_END
ENTRY=0x6a00
START=WHISTLE_START
END=WHISTLE_END
LIFE=36
WAVE=36
SHAPES=(
 (0x08,0x0e,0x0b,0x08,0x08,0x08,0x38,0x78,0x70,0,0,0),
 (0x18,0x24,0x24,0x18,0x30,0x58,0x94,0x94,0x78,0x10,0x28,0x18),
 (0x7e,0x42,0x42,0x42,0x42,0x42,0x66,0xee,0xcc,0,0,0),
 (0x10,0x1c,0x16,0x10,0x10,0x10,0x70,0xf0,0xe0,0,0,0))


# Double both axes: 16 logical pixels wide and up to 48 scanlines tall.
SHAPES=tuple(tuple(value for row in glyph for value in (row,row)) for glyph in SHAPES)
GLYPH_ROWS=24

def age_at(phase,plane):
    relative=phase-plane*6
    return relative%WAVE if 0<=relative<2*WAVE else None


def path(age,plane=0):
    t=age/(LIFE-1)
    # Large symbols clear the face rapidly, then fan across the open sky.
    drift=1-(1-t)**1.4
    sway=math.sin(t*math.pi*2)*(3+plane)
    return (101-round((48+plane*10)*drift)+round(sway),
            44-round(40*(.5*t+.5*math.sin(t*math.pi/2))))


def luminance(age):
    # Hold full brilliance; fade only during the final ~0.12 seconds.
    return 14 if age<33 else (12,8,2)[age-33]


def helper():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # Reuse the established alternate PMG buffers ($0980 and $8980).
    a(0xad,0xd407);c.emit(0x29,0x80,0x49,0x80);c.jump(0x8d,'back')
    for i,high in enumerate((9,10,10,11,11)):
        c.emit(0x09,high);c.jump(0x8d,f'clear{i}_hi')
        c.jump(0xad,'back')
    c.emit(0xa9,0,0xa2,127)
    c.label('clear')
    for i,addr in enumerate((0x980,0xa00,0xa80,0xb00,0xb80)):
        c.label(f'clear{i}');a(0x9d,addr)
    c.emit(0xca);c.branch(0x10,'clear')
    a(0xad,0x83e2);c.emit(0x38,0xe9,START&255);a(0x8d,0x83ff)
    a(0xad,0x83e3);c.emit(0xe9,START>>8)
    # Two finite waves finish and fade before the doorway cut.
    for _ in range(3):c.emit(0x4a);a(0x6e,0x83ff)
    for p in range(4):
        c.jump(0xad,'back');c.emit(0x09,10 if p<2 else 11);c.jump(0x8d,f'put{p}_hi')
        c.jump(0xad,'back');c.emit(0x09,9);c.jump(0x8d,f'miss{p}_hi');c.jump(0x8d,f'mread{p}_hi')
        c.emit(0xa9,0);c.jump(0x8d,f'pos{p}');c.jump(0x8d,f'pos{p+4}');c.jump(0x8d,f'color{p}')
        a(0xad,0x83ff);c.emit(0x38,0xe9,p*6);c.branch(0x90,f'hidden{p}')
        c.emit(0xc9,2*WAVE);c.branch(0xb0,f'hidden{p}')
        c.emit(0xc9,WAVE);c.branch(0x90,f'age{p}');c.emit(0xe9,WAVE)
        c.label(f'age{p}');c.emit(0xaa)
        c.jump(0xbd,'luma');c.jump(0x8d,f'color{p}')
        c.jump(0xbd,f'xs{p}');c.jump(0x8d,f'pos{p}');c.emit(0x18,0x69,3);c.jump(0x8d,f'pos{p+4}')
        c.jump(0xbd,f'ys{p}');c.emit(0xa8,0x18,0x69,GLYPH_ROWS);c.jump(0x8d,f'my{p}')
        c.emit(0xa2,0)
        c.label(f'blit{p}');c.jump(0xbd,f'glyph{p}')
        c.label(f'put{p}');a(0x99,0xa00+p*128)
        c.emit(0xe8,0xc8,0xe0,GLYPH_ROWS);c.branch(0xd0,f'blit{p}')
        c.jump(0xac,f'my{p}');c.emit(0xa2,3)
        c.label(f'tail{p}')
        c.label(f'mread{p}');a(0xb9,0x980)
        c.emit(0x09,1<<(p*2))
        c.label(f'miss{p}');a(0x99,0x980)
        c.emit(0xc8,0xc8,0xca);c.branch(0xd0,f'tail{p}')
        c.label(f'hidden{p}')
    # Publish only complete planes in bottom blanking, retaining the old
    # buffer until all notes and tails are ready.
    c.label('wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'wait')
    c.emit(0xc9,128);c.branch(0xb0,'wait')
    c.jump(0xad,'back');c.emit(0x09,8);a(0x8d,0xd407)
    for p in range(8):c.jump(0xad,f'pos{p}');a(0x8d,0xd000+p)
    for p in range(4):
        a(0xad,0x83ff);c.emit(0x18,0x69,p*4,0x29,15,0xaa)
        c.jump(0xbd,'hues');c.jump(0x0d,f'color{p}');a(0x8d,0xd012+p)
        c.emit(0xa9,1);a(0x8d,0xd008+p)
    for addr,val in ((0xd00c,0x55),(0xd01b,1),(0xd01d,3),(0xd400,0x2e)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    c.label('back');c.emit(0)
    for p in range(8):c.label(f'pos{p}');c.emit(0)
    for p in range(4):c.label(f'my{p}');c.emit(0)
    for p in range(4):
        c.label(f'color{p}');c.emit(0)
        c.label(f'xs{p}');c.emit(*(path(i,p)[0]+48 for i in range(LIFE)))
        c.label(f'ys{p}');c.emit(*(path(i,p)[1] for i in range(LIFE)))
    c.label('luma');c.emit(*(luminance(i) for i in range(LIFE)))
    c.label('hues');c.emit(0x00,0x10,0x40,0x00,0x80,0x00,0xc0,0x10,
                             0x00,0x50,0x90,0x00,0xd0,0x20,0x00,0x70)
    for p,glyph in enumerate(SHAPES):c.label(f'glyph{p}');c.emit(*glyph)
    for name in [f'clear{i}' for i in range(5)]+[f'{op}{p}' for op in ('put','miss','mread') for p in range(4)]:
        c.labels[name+'_hi']=c.labels[name]+2
    code=c.finish()
    if ENTRY+len(code)>0x6f00:raise ValueError('whistle PMG overlaps cleanup')
    return code
