"""Beat cuts and speed/reverse fills for the post-Trevor tunnel windows."""
from build_sequence import Code
from music_timing import tick_at_bar
ENTRY=0xec20
SIZE=384
BANK_ENTRY=0x7250
SHIFT=4000
MONTAGE_START=tick_at_bar(88)-SHIFT
START=((tick_at_bar(112)+1023)//1024)*1024-SHIFT
from outro_text import START as END
DESC=0x0dda
VLO,VHI=0x0dd3,0x0dd4

def cuts():
    pattern=(0x00,0x90,0x40,0x10,0x80,0x50,0x00,0xd0)
    result=[]
    for bar in range(112,144,4):
        for half,mode in enumerate(pattern):
            tick=tick_at_bar(bar*2+half,2)-SHIFT
            if not result:tick=START
            result.append((tick,mode))
        result.append((tick_at_bar(bar*4+15,4)-SHIFT,0x10))
    return tuple((tick,mode) for tick,mode in result if tick<END)

def frame_at(tick):
    # Match the legacy clock: bit 10, not bit 9, selects the motif.
    clock=tick+SHIFT if MONTAGE_START<=tick<END else tick
    original=((clock>>4)&31)|((clock>>5)&32)
    if tick<START or not original&32:return original
    mode=next(mode for start,mode in reversed(cuts()) if tick>=start)
    phase=(clock>>4)&15
    if mode&128:phase^=15
    if mode&64:phase=(phase*2)&15
    return 32|(mode&16)|phase

def helper():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # Enter loader bank 2 while preserving the caller's bank across NMIs.
    a(0xad,0xd301);c.emit(0x48);a(0xad,0x24b5);a(0x8d,0xd301)
    a(0x20,BANK_ENTRY);c.emit(0x68);a(0x8d,0xd301);a(0xad,0x83ed);c.emit(0x60)
    return bytes(c.finish())

def bank_helper():
    c=Code(BANK_ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # Use the original montage clock translated onto its new time window.
    a(0xad,0x83e2);a(0x8d,VLO);a(0xad,0x83e3);a(0x8d,VHI)
    a(0xad,0x83e3);c.emit(0xc9,MONTAGE_START>>8);c.branch(0x90,'clock_ready')
    c.branch(0xd0,'shift_clock');a(0xad,0x83e2);c.emit(0xc9,MONTAGE_START&255);c.branch(0x90,'clock_ready')
    c.label('shift_clock');c.emit(0x18);a(0xad,VLO);c.emit(0x69,SHIFT&255);a(0x8d,VLO)
    a(0xad,VHI);c.emit(0x69,SHIFT>>8);a(0x8d,VHI)
    c.label('clock_ready')
    a(0xad,VHI);c.emit(0x29,1,0x0a,0x0a,0x0a,0x0a);a(0x8d,0x83ed)
    a(0xad,VLO);c.emit(0x4a,0x4a,0x4a,0x4a);a(0x0d,0x83ed);a(0x8d,0x83ed)
    a(0xad,VHI);c.emit(0x29,4,0x0a,0x0a,0x0a);a(0x0d,0x83ed);a(0x8d,0x83ed)
    a(0xad,0x83e3);c.emit(0xc9,START>>8);c.branch(0x90,'done');c.branch(0xd0,'after_start')
    a(0xad,0x83e2);c.emit(0xc9,START&255);c.branch(0x90,'done')
    c.label('after_start')
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
    data=bytes(c.finish());assert BANK_ENTRY+len(data)<=0x7800,len(data)
    return data

def install(bank):
    out=bytearray(bank);data=bank_helper();offset=BANK_ENTRY-0x4000
    assert not any(out[offset:offset+len(data)])
    out[offset:offset+len(data)]=data
    variant=variant_helper();offset=0x7400-0x4000
    assert not any(out[offset:offset+len(variant)])
    out[offset:offset+len(variant)]=variant
    clock=ball_clock_helper();offset=0x7480-0x4000
    assert not any(out[offset:offset+len(clock)])
    out[offset:offset+len(clock)]=clock
    return bytes(out)

def variant_helper():
    c=Code(0x7400)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    a(0xad,0x83e2);a(0x8d,VLO);a(0xad,0x83e3);a(0x8d,VHI)
    c.emit(0xc9,MONTAGE_START>>8);c.branch(0x90,'clock')
    c.branch(0xd0,'shift');a(0xad,VLO);c.emit(0xc9,MONTAGE_START&255);c.branch(0x90,'clock')
    c.label('shift');c.emit(0x18);a(0xad,VLO);c.emit(0x69,SHIFT&255);a(0x8d,VLO)
    a(0xad,VHI);c.emit(0x69,SHIFT>>8);a(0x8d,VHI)
    c.label('clock');a(0xad,VHI);c.emit(0xc9,0x80);c.branch(0x90,'global')
    c.emit(0xc9,0x8c);c.branch(0x90,'bunch');c.branch(0xd0,'global')
    a(0xad,VLO);c.emit(0xc9,0x3c);c.branch(0x90,'bunch')
    c.label('global');a(0xad,VHI);c.emit(0x29,8,0x0a,0x0a,0x0a,0x09,0x80,0x60)
    c.label('bunch');c.emit(0xa9,0x80,0x60)
    data=bytes(c.finish());assert 0x7400+len(data)<=0x7800
    return data

def ball_clock_helper():
    c=Code(0x7480)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    a(0xad,0x83e2);a(0x8d,VLO);a(0xad,0x83e3);a(0x8d,VHI)
    a(0xad,0x83e0);c.emit(0xc9,6);c.branch(0xd0,'done')
    a(0xad,VHI);c.emit(0xc9,MONTAGE_START>>8);c.branch(0x90,'done')
    c.branch(0xd0,'shift');a(0xad,VLO);c.emit(0xc9,MONTAGE_START&255);c.branch(0x90,'done')
    c.label('shift');c.emit(0x18);a(0xad,VLO);c.emit(0x69,SHIFT&255);a(0x8d,VLO)
    a(0xad,VHI);c.emit(0x69,SHIFT>>8);a(0x8d,VHI)
    c.label('done');c.emit(0x60)
    data=bytes(c.finish());assert 0x7480+len(data)<=0x7800
    return data
