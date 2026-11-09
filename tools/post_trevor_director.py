"""Beat cuts and speed/reverse fills for the post-Trevor tunnel windows."""
from build_sequence import Code
from music_timing import tick_at_bar
ENTRY=0xec20
SIZE=384
START=((tick_at_bar(112)+1023)//1024)*1024
from outro_text import START as END
DESC=0x0dda

def cuts():
    pattern=(0x00,0x90,0x40,0x10,0x80,0x50,0x00,0xd0)
    result=[]
    for bar in range(112,144,4):
        for half,mode in enumerate(pattern):
            tick=tick_at_bar(bar*2+half,2)
            if not result:tick=START
            result.append((tick,mode))
        result.append((tick_at_bar(bar*4+15,4),0x10))
    return tuple((tick,mode) for tick,mode in result if tick<END)

def frame_at(tick):
    # Match the legacy clock: bit 10, not bit 9, selects the motif.
    original=((tick>>4)&31)|((tick>>5)&32)
    if tick<START or not original&32:return original
    mode=next(mode for start,mode in reversed(cuts()) if tick>=start)
    phase=(tick>>4)&15
    if mode&128:phase^=15
    if mode&64:phase=(phase*2)&15
    return 32|(mode&16)|phase

def helper():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    a(0xad,0x83e3);c.emit(0x29,1,0x0a,0x0a,0x0a,0x0a);a(0x8d,0x83ed)
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a);a(0x0d,0x83ed);a(0x8d,0x83ed)
    a(0xad,0x83e3);c.emit(0x29,4,0x0a,0x0a,0x0a);a(0x0d,0x83ed);a(0x8d,0x83ed)
    a(0xad,0x83e3);c.emit(0xc9,START>>8);c.branch(0x90,'done')
    a(0xad,0x83ed);c.emit(0x29,32);c.branch(0xf0,'done')
    c.emit(0xa2,len(cuts())-1)
    c.label('find');a(0xad,0x83e3);c.jump(0xdd,'hi');c.branch(0x90,'previous');c.branch(0xd0,'selected')
    a(0xad,0x83e2);c.jump(0xdd,'lo');c.branch(0xb0,'selected')
    c.label('previous');c.emit(0xca);c.branch(0x10,'find')
    c.label('selected');c.jump(0xbd,'mode');a(0x8d,DESC)
    a(0xad,0x83ed);c.emit(0x29,15);a(0x2c,DESC);c.branch(0x10,'forward');c.emit(0x49,15)
    c.label('forward');c.branch(0x50,'normal');c.emit(0x0a,0x29,15)
    c.label('normal');c.emit(0x48);a(0xad,DESC);c.emit(0x29,16,0x09,32);a(0x8d,DESC)
    c.emit(0x68);a(0x0d,DESC);a(0x8d,0x83ed)
    c.label('done');a(0xad,0x83ed);c.emit(0x60)
    for name,values in (('lo',[t&255 for t,m in cuts()]),('hi',[t>>8 for t,m in cuts()]),('mode',[m for t,m in cuts()])):
        c.label(name);c.emit(*values)
    data=bytes(c.finish());assert len(data)<=SIZE,len(data)
    return data
