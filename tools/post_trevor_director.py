"""Beat-aligned choreography for rotators and tunnels throughout the demo."""
from build_sequence import Code
from music_timing import tick_at_bar
from trevor_awakens import END as TREVOR_END
ENTRY=0xec20
TIMELINE_ENTRY=ENTRY+8
SIZE=384
BANK_ENTRY=0x6e20
SHIFT=4000
MONTAGE_START=tick_at_bar(88)-SHIFT
START=TREVOR_END
FIRST_ROTATOR=tick_at_bar(32)
BUM_START=tick_at_bar(104)
CYCLE_START=tick_at_bar(80)
from outro_text import START as END
DESC=0x0dda
VLO,VHI=0x0dd3,0x0dd4
QSTART,ELAPSED=0x0ddb,0x0ddc
ACTLO,ACTHI=0x0dd5,0x0dd6
MODE=0x0dd7

# One-bar passes cover the banana rotator as well as both tunnel textures,
# alternating forward/reverse travel at normal/double speed.
PATTERN=(0x60,0xe0,0x20,0xa0,0x40,0xc0,0x00,0x80,
         0x50,0xd0,0x10,0x90)

def cuts():
    # First rotators, the pre-basketball tunnel, then the post-fight montage.
    result=[(tick_at_bar(bar), (0x20,0x60,0xa0,0xe0)[(bar-32)%4])
            for bar in range(32,40)]
    result.extend(((tick_at_bar(56),0x00),(tick_at_bar(57),0x80),(START,0x20)))
    for index,bar in enumerate(range(80,112)):
        tick=tick_at_bar(bar)
        mode={108:0x60,109:0xe0}.get(bar,PATTERN[index%len(PATTERN)])
        result.append((tick,mode))
    return tuple((tick,mode) for tick,mode in result if tick<END)

def timeline():
    """Attach a phase origin to every pass so reversals never jump frames."""
    result=[]
    for index,(tick,mode) in enumerate(cuts()):
        period=32 if mode&0x20 else 12 if mode&0x10 else 16
        qstart=(tick>>4)&255
        if index==0 or tick==START:
            clock=tick+SHIFT if MONTAGE_START<=tick<END else tick
            original=((clock>>4)&31)|((clock>>5)&32)
            base=original&31
        elif (mode&0x30)!=(result[-1][1]&0x30):
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
    if tick<FIRST_ROTATOR:return original
    _,mode,qstart,base=next(item for item in reversed(timeline()) if tick>=item[0])
    if mode&0x20:
        period=32
    else:period=12 if mode&0x10 else 16
    elapsed=((tick>>4)-qstart)&255
    speed=2 if mode&0x40 else 1
    direction=-1 if mode&0x80 else 1
    phase=(base+direction*speed*elapsed)%period
    return phase if mode&0x20 else (48 if mode&0x10 else 32)+phase

def helper():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # Enter loader bank 2 while preserving the caller's bank across NMIs.
    a(0xad,0xd301);c.emit(0x48);a(0xad,0x24b5);a(0x8d,0xd301)
    a(0x20,BANK_ENTRY);c.emit(0x68);a(0x8d,0xd301)
    # Resolve the eye shot before deciding which effect owns PMG.
    a(0x20,0xec04)
    # On late banana frames, alternate BUM/BAM and puffs on the music beat.
    c.emit(0xa9,0);a(0x8d,0x0dd2)
    a(0xad,0x83e0);c.emit(0xc9,6);c.branch(0xf0,'scene_ready');c.jump(0x4c,'done')
    c.label('scene_ready');a(0xad,0x83e3);c.emit(0xc9,BUM_START>>8);c.branch(0xb0,'time_low');c.jump(0x4c,'done')
    c.label('time_low');c.branch(0xd0,'after_start');a(0xad,0x83e2);c.emit(0xc9,BUM_START&255);c.branch(0xb0,'after_start');c.jump(0x4c,'done')
    c.label('after_start')
    a(0xad,0x83ed);c.emit(0xc9,32);c.branch(0x90,'banana_ready');c.jump(0x4c,'done')
    c.label('banana_ready')
    c.emit(0xa9,1);a(0x8d,0x0dd2)
    # Elapsed ticks from the selected director cut; one word per beat.
    a(0xad,0x83e2);c.emit(0x38);a(0xed,0x0dd8);a(0x8d,0x83ea)
    a(0xad,0x83e3);a(0xed,0x0dd9);a(0x8d,0x83eb)
    c.emit(0xa9,0);a(0x8d,0x83ec)
    c.label('beat_reduce');a(0xad,0x83eb);c.branch(0xd0,'beat_subtract')
    a(0xad,0x83ea);c.emit(0xc9,94);c.branch(0x90,'beat_ready')
    c.label('beat_subtract');a(0xad,0x83ea);c.emit(0x38,0xe9,94);a(0x8d,0x83ea)
    a(0xad,0x83eb);c.emit(0xe9,0);a(0x8d,0x83eb);a(0xee,0x83ec)
    c.jump(0x4c,'beat_reduce')
    c.label('beat_ready');a(0xad,0x83ea);a(0x8d,0x0dd0)
    a(0xad,0x83ec);a(0x4d,MODE);c.emit(0x29,1);a(0x8d,0x0dd1)
    # Keep the outward puffs visible through the entire beat.
    a(0xad,0x83ea);c.emit(0xc9,94);c.branch(0xb0,'impact_hide')
    from trevor_polished import IMPACT_BRIDGE,IMPACT_HIDE_BRIDGE
    c.label('impact_call');a(0xad,0xd301);c.emit(0x48);a(0xad,0x08d8);a(0x8d,0xd301)
    a(0x20,IMPACT_BRIDGE);c.emit(0x68);a(0x8d,0xd301);c.jump(0x4c,'done')
    c.label('impact_hide');a(0xad,0xd301);c.emit(0x48);a(0xad,0x08d8);a(0x8d,0xd301)
    a(0x20,IMPACT_HIDE_BRIDGE);c.emit(0x68);a(0x8d,0xd301)
    c.label('done');a(0xad,0x83ed);c.emit(0x60)
    return bytes(c.finish())

def bank_helper():
    c=Code(BANK_ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # Keep the real and translated music clocks for the selected montage pass.
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
    a(0xad,0x83e3);c.emit(0xc9,FIRST_ROTATOR>>8);c.branch(0xb0,'check_start_low');c.jump(0x4c,'done')
    c.label('check_start_low');c.branch(0xd0,'apply_timeline')
    a(0xad,0x83e2);c.emit(0xc9,FIRST_ROTATOR&255);c.branch(0xb0,'apply_timeline');c.jump(0x4c,'done')
    c.label('apply_timeline')
    # Credits take over the shared $0DD7 scratch byte at END.
    a(0xad,ACTHI);c.emit(0xc9,END>>8);c.branch(0x90,'before_end');c.branch(0xf0,'check_end_low');c.jump(0x4c,'done')
    c.label('check_end_low');a(0xad,ACTLO);c.emit(0xc9,END&255);c.branch(0x90,'before_end');c.jump(0x4c,'done')
    c.label('before_end')
    c.emit(0xa2,len(cuts())-1)
    c.label('find');a(0xad,ACTHI);c.jump(0xdd,'hi');c.branch(0x90,'previous');c.branch(0xd0,'selected')
    a(0xad,ACTLO);c.jump(0xdd,'lo');c.branch(0xb0,'selected')
    c.label('previous');c.emit(0xca);c.branch(0x10,'find')
    c.label('selected');c.jump(0xbd,'mode');a(0x8d,DESC)
    # Expose the selected director cut and its exact start tick to the
    # post-Trevor overlays (e.g. beat-synced BUM/BAM on banana rotations).
    c.emit(0x8e,MODE&255,MODE>>8)
    c.jump(0xbd,'lo');a(0x8d,0x0dd8)
    c.jump(0xbd,'hi');a(0x8d,0x0dd9)
    c.jump(0xbd,'qstart');a(0x8d,QSTART)
    # Quantize the live clock to the 16-tick image cadence and subtract the
    # selected pass origin. A pass is under 256 frames, so its low byte suffices.
    a(0xad,ACTLO);c.emit(0x4a,0x4a,0x4a,0x4a);a(0x8d,ELAPSED)
    a(0xad,ACTHI);c.emit(0x29,15,0x0a,0x0a,0x0a,0x0a);a(0x0d,ELAPSED)
    c.emit(0x38);a(0xed,QSTART);a(0x8d,ELAPSED)
    a(0xad,DESC);c.emit(0x29,32);c.branch(0xd0,'banana_phase')
    a(0xad,DESC);c.emit(0x29,16);c.branch(0xd0,'organic_phase');c.jump(0x4c,'spiral_phase')
    # Banana frames use all 32 orientations and share the same speed/direction
    # controls; unlike tunnel art, they are selected even during their own cycle.
    c.label('banana_phase');a(0xad,ELAPSED);c.emit(0x29,31);a(0x8d,ELAPSED)
    a(0xad,DESC);c.emit(0x29,64);c.branch(0xf0,'banana_reverse')
    a(0xad,ELAPSED);c.emit(0x0a,0x29,31);a(0x8d,ELAPSED)
    c.label('banana_reverse');a(0xad,DESC);c.emit(0x29,128);c.branch(0xf0,'banana_add')
    a(0xad,ELAPSED);c.emit(0x49,31,0x18,0x69,1,0x29,31);a(0x8d,ELAPSED)
    c.label('banana_add');a(0xad,ELAPSED);c.emit(0x18);c.jump(0x7d,'base');c.emit(0x29,31);a(0x8d,0x83ed);c.jump(0x4c,'done')
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
