"""Bank-eight portrait renderer; music owns offsets below $0B10."""
from pathlib import Path
from build_sequence import Code
from music_timing import tick_at_bar
START, END = tick_at_bar(40), tick_at_bar(56)
CUTS = tuple(tick_at_bar(40 + 4*i) for i in range(4))
ENTRY, DATA, HEIGHT = 0x4b10, 0x4fc0, 52

def portraits():
    rgb=Path('build/crush-portraits.rgb').read_bytes()
    palette=((0,0,0),(255,50,160),(0,220,255),(255,190,150))
    assert len(rgb)==160*104*3
    pixels=bytes(min(range(4),key=lambda j:sum((rgb[i+c]-palette[j][c])**2 for c in range(3))) for i in range(0,len(rgb),3))
    return [bytes(pixels[(r*52+y)*160+col*80+x] for y in range(52) for x in range(80)) for r in range(2) for col in range(2)]

def packed():
    return b''.join(bytes(sum(p[y*80+x+k]<<(6-2*k) for k in range(4)) for y in range(52) for x in range(0,80,4)) for p in portraits())

def helper(eyes=None, effects_address=0):
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # Four views, one every four bars. X is the portrait index.
    c.emit(0xa2,3)
    c.label('find')
    a(0xad,0x83e3);c.jump(0xdd,'cut_hi');c.branch(0x90,'previous');c.branch(0xd0,'found')
    a(0xad,0x83e2);c.jump(0xdd,'cut_lo');c.branch(0xb0,'found')
    c.label('previous');c.emit(0xca);c.branch(0x10,'find')
    c.label('found');a(0x8e,0x83ff);c.emit(0x8a,0x09,0x40);a(0xcd,0x83fa);c.branch(0xd0,'changed');c.jump(0x4c,'patch_wait')
    c.label('changed');a(0x8d,0x83fa)
    c.emit(0xa9,255);a(0x8d,0x83eb)
    c.jump(0xbd,'source_lo');c.jump(0x8d,'src1lo');c.jump(0x8d,'src2lo')
    c.jump(0xbd,'source_hi');c.jump(0x8d,'src1hi');c.jump(0x8d,'src2hi')
    a(0xad,0x83e6);c.emit(0x29,4,0x0a,0x0a,0x0a,0x49,0xb0);a(0x8d,0x83fe)
    c.jump(0x8d,'dst1hi');c.jump(0x8d,'dst2hi')
    c.emit(0xa9,0);c.jump(0x8d,'dst1lo');c.emit(0xa9,1);c.jump(0x8d,'dst2lo')
    c.emit(0xa0,HEIGHT)
    c.label('copyrow');c.emit(0xa2,20);a(0x8e,0x83fd)
    c.label('pixel')
    c.label('src1');c.emit(0xad,0,0);c.emit(0x4a,0x4a,0x4a,0x4a,0xaa);c.jump(0xbd,'expand')
    c.label('dst1');c.emit(0x8d,0,0)
    c.label('src2');c.emit(0xad,0,0);c.emit(0x29,15,0xaa);c.jump(0xbd,'expand')
    c.label('dst2');c.emit(0x8d,0,0)
    for label in ('src1','src2'):
        c.jump(0xee,label+'lo');c.branch(0xd0,label+'ok');c.jump(0xee,label+'hi');c.label(label+'ok')
    for label in ('dst1','dst2'):
        c.emit(0x18);c.jump(0xad,label+'lo');c.emit(0x69,2);c.jump(0x8d,label+'lo');c.branch(0x90,label+'ok');c.jump(0xee,label+'hi');c.label(label+'ok')
    a(0xce,0x83fd);c.branch(0xd0,'pixel');c.emit(0x88);c.branch(0xd0,'copyrow')
    # Inactive display list: portrait lines are repeated to fill 192 scanlines.
    a(0xad,0x83e6);c.jump(0x8d,'dl1hi');c.jump(0x8d,'dl2hi')
    c.emit(0xa9,3);c.jump(0x8d,'dl1lo');c.emit(0xa9,4);c.jump(0x8d,'dl2lo');c.emit(0xa0,0)
    c.label('rows');c.jump(0xb9,'row_lo');c.label('dl1');c.emit(0x8d,0,0)
    c.jump(0xb9,'row_hi');c.emit(0x18);a(0x6d,0x83fe);c.label('dl2');c.emit(0x8d,0,0)
    for label in ('dl1','dl2'):
        c.emit(0x18);c.jump(0xad,label+'lo');c.emit(0x69,3);c.jump(0x8d,label+'lo');c.branch(0x90,label+'ok');c.jump(0xee,label+'hi');c.label(label+'ok')
    c.emit(0xc8,0xc0,192);c.branch(0xd0,'rows')
    a(0x20,effects_address)
    c.label('swapwait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'swapwait')
    c.emit(0xa9,0);a(0x8d,0xd402);a(0xad,0x83e6);a(0x8d,0xd403);c.emit(0x49,4);a(0x8d,0x83e6)
    c.emit(0xa9,255);a(0x8d,0x83f8);a(0x8d,0x83f9)
    c.jump(0x4c,'wait')
    c.label('patch_wait');a(0x20,effects_address)
    c.label('wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'wait')
    for addr,val in ((0xd01d,0),(0xd01b,1),(0xd400,0x22),(0xd01a,0),(0xd016,0x48),(0xd017,0x9a),(0xd018,0x2c)):
        c.emit(0xa9,val);a(0x8d,addr)
    a(0xae,0x83ff)
    for i in range(2):
        c.jump(0xbd,f'palette{i}');a(0x8d,0xd016+i)
    # Fresh masks use the same double-line PMG buffer as the dance accents.
    c.emit(0xa9,0,0xa2,0)
    c.label('clearpmg')
    for base in (0x0a00,0x0b00,0x0980):a(0x9d,base)
    c.emit(0xe8);c.branch(0xd0,'clearpmg')
    a(0xae,0x83ff)
    for index in range(2):
        c.jump(0xbd,f'eye_y{index}');c.emit(0xa8,0xa9,0xff)
        for base in (0xa00+index*128,):
            a(0x99,base);a(0x99,base+2)
        c.emit(0xa9,0x7e);a(0x99,0xb00+index*128+1)
    # Hair strand: a small golden lock sways one logical pixel each 32 ticks.
    c.jump(0xbd,'hair_y');c.emit(0xa8,0xa9,3)
    a(0x99,0x0980);a(0x99,0x0981);a(0x99,0x0982)
    a(0xad,0x83e2);c.emit(0x29,32,0x4a,0x4a,0x4a,0x4a,0x4a,0x18);c.jump(0x7d,'hair_x');a(0x8d,0xd004)
    for addr,val in ((0xd012,0x2c),(0xd013,0x2c),(0xd014,0),(0xd015,0),(0xd407,8),(0xd008,0),(0xd009,0),(0xd00a,0),(0xd00b,0),(0xd00c,0)):
        c.emit(0xa9,val);a(0x8d,addr)
    # Eyes close for 16 music ticks once per 256 ticks.
    a(0xad,0x83e2);c.emit(0xc9,240);c.branch(0xb0,'blink')
    c.emit(0xa9,0)
    for addr in range(0xd000,0xd004):a(0x8d,addr)
    c.jump(0x4c,'pmgon')
    c.label('blink')
    for i in range(2):
        c.jump(0xbd,f'eye_x{i}');a(0x8d,0xd000+i);a(0x8d,0xd002+i)
    c.label('pmgon')
    for addr,val in ((0xd01d,3),(0xd400,0x2e)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    for label in ('src1','src2','dst1','dst2','dl1','dl2'):
        c.labels[label+'lo']=c.labels[label]+1;c.labels[label+'hi']=c.labels[label]+2
    c.label('expand');c.emit(*(sum(((n>>(2-2*k))&3)<<(6-2*(2*k+d)) for k in range(2) for d in range(2)) for n in range(16)))
    c.label('cut_lo');c.emit(*(t&255 for t in CUTS));c.label('cut_hi');c.emit(*(t>>8 for t in CUTS))
    c.label('source_lo');c.emit(*((DATA+i*1040)&255 for i in range(4)));c.label('source_hi');c.emit(*((DATA+i*1040)>>8 for i in range(4)))
    c.label('row_lo');c.emit(*((y*HEIGHT//192*40)&255 for y in range(192)))
    c.label('row_hi');c.emit(*((y*HEIGHT//192*40)>>8 for y in range(192)))
    # Coordinates in 160x192 logical pixels, then converted to PMG registers.
    eye_positions=eyes or [((70,76),(89,76)),((51,72),(64,67)),((66,69),(82,63)),((68,66),(86,66))]
    for i in range(2):
        c.label(f'eye_x{i}');c.emit(*(pair[i][0]+48 for pair in eye_positions))
        c.label(f'eye_y{i}');c.emit(*((pair[i][1]+17)//2 for pair in eye_positions))
    c.label('hair_x');c.emit(*(x+48 for x in (54,33,33,43)))
    c.label('hair_y');c.emit(*(y for y in (58,63,66,63)))
    from pompom_effects import PALETTES
    for i in range(2):
        c.label(f'palette{i}');c.emit(*(p[i] for p in PALETTES))
    result=c.finish()
    assert ENTRY+len(result)<=0x4f00,(len(result),DATA-ENTRY)
    return result


def cleanup(origin=0x4f00):
    """Restore dance PMG after leaving portraits, including SELECT restart."""
    c=Code(origin)
    c.emit(0xa9,0,0xa2,0)
    c.label('clear')
    for base in (0x0980,0x0a00,0x0b00):c.emit(0x9d,base&255,base>>8)
    c.emit(0xe8);c.branch(0xd0,'clear')
    c.emit(0xa2,6)
    c.label('stars');c.jump(0xbd,'shape')
    for base in (0x0a0e,0x0a8a,0x0b0f,0x0b8b):c.emit(0x9d,base&255,base>>8)
    c.emit(0xca);c.branch(0x10,'stars')
    for i,row in enumerate((14,10,15,11)):
        for y in range(row-3,row):
            c.emit(0xad,(0x980+y)&255,9,0x09,3<<(2*i),0x8d,(0x980+y)&255,9)
    c.emit(0x60)
    c.label('shape');c.emit(0x10,0x10,0x38,0xfe,0x38,0x10,0x10)
    data=c.finish();assert len(data)<=0xc0
    return data
