"""Ease the final PMG orbits toward a new shape at each terminal line."""
import math
from build_sequence import Code

ENTRY=0x66a0
VALUES_X=0x69b8
VALUES_Y=0x69bc
AMOUNT,LAST,VALID,TARGET=0x69c0,0x69c1,0x69c2,0x69c3
PHASE_SHIFT=3  # Advance the visible angle every two PAL frames.
# A clear morph between tall and wide ellipses. Adjacent shapes differ
# by three source pixels, preserving smooth movement while making the
# change visible over the boy's head.
ORBIT_SHAPES=tuple((9+3*i, 30-3*i, 0) for i in range(8))


def events():
    import outro_text as text
    import terminal_typing
    schedule=terminal_typing.schedule()
    return tuple(schedule[i*text.HISTORY_ROWS+row]
                 for i,page in enumerate(text.pages()) for row in range(len(page)))


def target_for(index):
    return (index*3)&7


def position(phase,amount,plane=0):
    from final_boy import HEAD_X,HEAD_Y
    angle=((phase+plane*4)&15)*math.tau/16
    rx,ry,tilt=ORBIT_SHAPES[amount]
    tilt=math.radians(tilt)
    ex=rx*math.cos(angle);ey=ry*math.sin(angle)
    xoff=ex*math.cos(tilt)-ey*math.sin(tilt)
    yoff=ex*math.sin(tilt)+ey*math.cos(tilt)
    x=HEAD_X+round(xoff)-4+48
    y=round((HEAD_Y+yoff-7+17)/2)+16
    return x,y


def animated_position(phase, amount, plane=0):
    """Position at one of 32 angular steps using the 16-point orbit table."""
    index, halfway = divmod(phase, 2)
    start = position(index, amount, plane)
    if not halfway:
        return start
    end = position(index+1, amount, plane)
    return tuple((a+b)//2 for a,b in zip(start,end))


def helper():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # Find the most recent actual line start, independent of callback cadence.
    c.emit(0xa2,len(events())-1)
    c.label('find');a(0xad,0x83e3);c.jump(0xdd,'hi');c.branch(0x90,'previous');c.branch(0xd0,'found')
    a(0xad,0x83e2);c.jump(0xdd,'lo');c.branch(0xb0,'found')
    c.label('previous');c.emit(0xca);c.branch(0x10,'find');c.emit(0xe8)
    c.label('found')
    # One unit per 8 player ticks; repeated callbacks at the same time do not
    # accelerate the morph. First entry initializes without stale scene state.
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a);a(0x8d,0x0dd9)
    a(0xad,0x83e3);c.emit(0x0a,0x0a,0x0a,0x0a,0x0a);a(0x0d,0x0dd9)
    a(0x8d,0x0dd9)
    a(0xad,VALID);c.branch(0xd0,'initialized')
    c.emit(0x8a,0x18,0x69,1);a(0x8d,VALID)
    c.emit(0x8a);a(0x8d,0x0dd8);c.emit(0x0a,0x18);a(0x6d,0x0dd8);c.emit(0x29,7)
    a(0x8d,TARGET);a(0x8d,AMOUNT);a(0xad,0x0dd9);a(0x8d,LAST);c.jump(0x4c,'positions')
    c.label('initialized');c.emit(0x8a,0x18,0x69,1);a(0xcd,VALID);c.branch(0xf0,'same_line')
    a(0x8d,VALID);c.emit(0x8a);a(0x8d,0x0dd8);c.emit(0x0a,0x18);a(0x6d,0x0dd8);c.emit(0x29,7)
    a(0xcd,AMOUNT);c.branch(0xd0,'different_amount');c.emit(0x49,7)
    c.label('different_amount');a(0xcd,TARGET);c.branch(0xd0,'new_target')
    c.emit(0x18,0x69,1,0x29,7);a(0xcd,AMOUNT);c.branch(0xd0,'new_target')
    c.emit(0x18,0x69,1,0x29,7)
    c.label('new_target');a(0x8d,TARGET)
    c.label('same_line');a(0xad,0x0dd9);a(0xcd,LAST);c.branch(0xf0,'positions');a(0x8d,LAST)
    a(0xad,AMOUNT);a(0xcd,TARGET);c.branch(0xf0,'positions');c.branch(0x90,'increase')
    a(0xce,AMOUNT);c.jump(0x4c,'positions')
    c.label('increase');a(0xee,AMOUNT)
    # Keep the two-frame update cadence. Every other step is the midpoint
    # between adjacent table entries, including the wrap at the end of a turn.
    c.label('positions');a(0xad,AMOUNT);c.emit(0x0a,0x0a,0x0a,0x0a);a(0x8d,0x0dd9)
    a(0xad,0x24a7);c.emit(*([0x4a]*PHASE_SHIFT));a(0x8d,0x0dd8)
    c.emit(0x4a);a(0x8d,0x83ff)  # Original 16-step index for the colour tables.
    c.emit(0xa0,0)
    c.label('plane');c.emit(0x98,0x0a,0x0a,0x18);a(0x6d,0x83ff)
    c.emit(0x29,15);a(0x0d,0x0dd9);c.emit(0xaa)
    c.jump(0xbd,'xs');a(0x99,VALUES_X)
    c.jump(0xbd,'ys');a(0x99,VALUES_Y)
    a(0xad,0x0dd8);c.emit(0x4a);c.branch(0x90,'next_plane')
    c.emit(0x8a,0x18,0x69,1,0x29,15);a(0x0d,0x0dd9);c.emit(0xaa)
    for table,values in (('xs',VALUES_X),('ys',VALUES_Y)):
        c.jump(0xbd,table);c.emit(0x18);a(0x79,values);c.emit(0x4a);a(0x99,values)
    c.label('next_plane');c.emit(0xc8,0xc0,4);c.branch(0xd0,'plane')
    c.emit(0x60)
    for name,values in (('lo',[t&255 for t in events()]),('hi',[t>>8 for t in events()]),
                        ('xs',[position(p,a)[0] for a in range(8) for p in range(16)]),
                        ('ys',[position(p,a)[1] for a in range(8) for p in range(16)])):
        c.label(name);c.emit(*values)
    code=bytes(c.finish());assert ENTRY+len(code)<=VALUES_X,len(code)
    return code


def install(bank):
    out=bytearray(bank);data=helper();offset=ENTRY-0x4000
    assert not any(out[offset:offset+len(data)])
    assert not any(out[VALUES_X-0x4000:0x69c4-0x4000])
    out[offset:offset+len(data)]=data
    return bytes(out)
