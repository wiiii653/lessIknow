"""Long-form speed/reverse choreography for the post-Trevor rotator montage."""
from build_sequence import Code
from music_timing import tick_at_bar
ENTRY=0xec20
TIMELINE_ENTRY=ENTRY+8
SIZE=384
BANK_ENTRY=0x6e20
SHIFT=4000
MONTAGE_START=tick_at_bar(88)-SHIFT
START=tick_at_bar(98)
CYCLE_START=tick_at_bar(102)
from outro_text import START as END
DESC=0x0dda
VLO,VHI=0x0dd3,0x0dd4
QSTART,ELAPSED=0x0ddb,0x0ddc
ACTLO,ACTHI=0x0dd5,0x0dd6
MODE=0x0dd7

# Two-bar passes let the tunnel finish an arc before changing direction.
# The first half of each eight-segment cycle accelerates forward, then runs
# back through the same space. Organic and spiral textures each hold eight bars.
# The v215 montage advances at the normal frame cadence. Keep that steadier
# pace, with four-bar reverse passages through each current tunnel texture.
PATTERN=(0x00,0x00,0x80,0x80,0x10,0x10,0x90,0x90)

def cuts():
    # Finish one calm organic revolution before the long-form choreography.
    result=[(START,0x10)]
    for index,bar in enumerate(range(102,134,2)):
        tick=tick_at_bar(bar)
        result.append((tick,PATTERN[index%len(PATTERN)]))
    return tuple((tick,mode) for tick,mode in result if tick<END)

def timeline():
    """Attach a phase origin to every pass so reversals never jump frames."""
    result=[]
    for index,(tick,mode) in enumerate(cuts()):
        period=12 if mode&0x10 else 16
        qstart=(tick>>4)&255
        if index==0 or (mode&0x10)!=(result[-1][1]&0x10):
            base=0
        else:
            _,previous_mode,previous_q,previous_base=result[-1]
            distance=(qstart-previous_q)&255
            speed=2 if previous_mode&0x40 else 1
            direction=-1 if previous_mode&0x80 else 1
            base=(previous_base+direction*speed*distance)%period
        result.append((tick,mode,qstart,base))
    return tuple(result)

def frame_at(tick):
    # Match the legacy clock: bit 10, not bit 9, selects the motif.
    clock=tick+SHIFT if MONTAGE_START<=tick<END else tick
    original=((clock>>4)&31)|((clock>>5)&32)
    if tick<START:return original
    if not original&32:
        return 48|(original&15) if tick<CYCLE_START else original
    _,mode,qstart,base=next(item for item in reversed(timeline()) if tick>=item[0])
    period=12 if mode&0x10 else 16
    elapsed=((tick>>4)-qstart)&255
    speed=2 if mode&0x40 else 1
    direction=-1 if mode&0x80 else 1
    phase=(base+direction*speed*elapsed)%period
    return (48 if tick<CYCLE_START or mode&0x10 else 32)+phase

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
    # Leave all earlier scenes' own selected frame untouched.
    a(0xad,0x83e2);a(0x8d,VLO);a(0x8d,ACTLO)
    a(0xad,0x83e3);a(0x8d,VHI);a(0x8d,ACTHI)
    # Translate the original clock for the montage's base motif selection.
    a(0xad,0x83e3);c.emit(0xc9,MONTAGE_START>>8);c.branch(0x90,'clock_ready')
    c.branch(0xd0,'shift_clock');a(0xad,0x83e2);c.emit(0xc9,MONTAGE_START&255);c.branch(0x90,'clock_ready')
    c.label('shift_clock');c.emit(0x18);a(0xad,VLO);c.emit(0x69,SHIFT&255);a(0x8d,VLO)
    a(0xad,VHI);c.emit(0x69,SHIFT>>8);a(0x8d,VHI)
    c.label('clock_ready')
    a(0xad,VHI);c.emit(0x29,1,0x0a,0x0a,0x0a,0x0a);a(0x8d,0x83ed)
    a(0xad,VLO);c.emit(0x4a,0x4a,0x4a,0x4a);a(0x0d,0x83ed);a(0x8d,0x83ed)
    a(0xad,VHI);c.emit(0x29,4,0x0a,0x0a,0x0a);a(0x0d,0x83ed);a(0x8d,0x83ed)
    a(0xad,0x83e3);c.emit(0xc9,START>>8);c.branch(0xb0,'check_start_low');c.jump(0x4c,'done')
    c.label('check_start_low');c.branch(0xd0,'apply_timeline')
    a(0xad,0x83e2);c.emit(0xc9,START&255);c.branch(0xb0,'apply_timeline');c.jump(0x4c,'done')
    c.label('apply_timeline')
    a(0xad,0x83ed);c.emit(0x29,32);c.branch(0xd0,'has_tunnel');c.jump(0x4c,'done')
    c.label('has_tunnel')
    c.emit(0xa2,len(cuts())-1)
    c.label('find');a(0xad,ACTHI);c.jump(0xdd,'hi');c.branch(0x90,'previous');c.branch(0xd0,'selected')
    a(0xad,ACTLO);c.jump(0xdd,'lo');c.branch(0xb0,'selected')
    c.label('previous');c.emit(0xca);c.branch(0x10,'find')
    c.label('selected');c.jump(0xbd,'mode');a(0x8d,DESC)
    c.jump(0xbd,'qstart');a(0x8d,QSTART)
    # Quantize the live clock to the 16-tick image cadence and subtract the
    # selected pass origin. A pass is under 256 frames, so its low byte suffices.
    a(0xad,ACTLO);c.emit(0x4a,0x4a,0x4a,0x4a);a(0x8d,ELAPSED)
    a(0xad,ACTHI);c.emit(0x29,15,0x0a,0x0a,0x0a,0x0a);a(0x0d,ELAPSED)
    c.emit(0x38);a(0xed,QSTART);a(0x8d,ELAPSED)
    a(0xad,DESC);c.emit(0x29,16);c.branch(0xd0,'organic_phase');c.jump(0x4c,'spiral_phase')
    # Organic art has twelve stored rotations. Reduce elapsed and speed before
    # applying direction, then wrap within those twelve real frames.
    c.label('organic_phase')
    a(0xad,ELAPSED);c.label('organic_reduce');c.emit(0xc9,12);c.branch(0x90,'organic_speed')
    c.emit(0x38,0xe9,12);c.jump(0x4c,'organic_reduce')
    c.label('organic_speed');a(0x8d,ELAPSED);a(0xad,DESC);c.emit(0x29,64);c.branch(0xf0,'organic_reverse')
    a(0xad,ELAPSED);c.emit(0x0a);c.label('organic_double_reduce');c.emit(0xc9,12);c.branch(0x90,'organic_double_done')
    c.emit(0x38,0xe9,12);c.jump(0x4c,'organic_double_reduce')
    c.label('organic_double_done');a(0x8d,ELAPSED)
    c.label('organic_reverse');a(0xad,DESC);c.emit(0x29,128);c.branch(0xf0,'organic_add')
    a(0xad,ELAPSED);c.branch(0xf0,'organic_add');c.emit(0xa9,12,0x38);a(0xed,ELAPSED);a(0x8d,ELAPSED)
    c.label('organic_add');a(0xad,ELAPSED);c.emit(0x18);c.jump(0x7d,'base')
    c.emit(0xc9,12);c.branch(0x90,'organic_ready');c.emit(0x38,0xe9,12)
    c.label('organic_ready');c.emit(0x18,0x69,48);a(0x8d,0x83ed);c.jump(0x4c,'done')
    # Spiral has sixteen rotations, so wrapping and reverse are a short mask.
    c.label('spiral_phase');a(0xad,ELAPSED);c.emit(0x29,15);a(0x8d,ELAPSED)
    a(0xad,DESC);c.emit(0x29,64);c.branch(0xf0,'spiral_reverse')
    a(0xad,ELAPSED);c.emit(0x0a,0x29,15);a(0x8d,ELAPSED)
    c.label('spiral_reverse');a(0xad,DESC);c.emit(0x29,128);c.branch(0xf0,'spiral_add')
    a(0xad,ELAPSED);c.emit(0x49,15,0x18,0x69,1,0x29,15);a(0x8d,ELAPSED)
    c.label('spiral_add');a(0xad,ELAPSED);c.emit(0x18);c.jump(0x7d,'base');c.emit(0x29,15,0x18,0x69,32);a(0x8d,0x83ed)
    c.label('done');a(0xad,0x83ed);c.emit(0x60)
    tl=timeline()
    for name,values in (('lo',[t&255 for t,m in cuts()]),('hi',[t>>8 for t,m in cuts()]),
                        ('mode',[m for t,m in cuts()]),('qstart',[q for t,m,q,b in tl]),
                        ('base',[b for t,m,q,b in tl])):
        c.label(name);c.emit(*values)
    data=bytes(c.finish());assert BANK_ENTRY+len(data)<=0x7250,len(data)
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
    import girl_eyes
    eye=girl_eyes.helper();offset=girl_eyes.BANK_ENTRY-0x4000
    assert not any(out[offset:offset+len(eye)])
    out[offset:offset+len(eye)]=eye
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
