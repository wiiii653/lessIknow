"""Side-profile tracking shot and three-shot ribbon performance.

36 ANTIC-E 160x64 frames, five 64-byte PMG streams per ribbon phase.
Both bitmap and PMG are prepared in inactive unbanked buffers.
"""
import math
from collections import deque
from functools import lru_cache
from pathlib import Path
from build_sequence import Code
from engine_effects import cached_display_list, clear_pmg, DL_KEYS
from music_timing import tick_at_bar, tick_at_beat

ENTRY = 0x5400
RIBBONS = 0x6a00
META = 0x7e00
WIND = 0x7f20
FIRST_BANK = 8  # original player bank table: six formerly-pompom banks
FRAME_COUNT = 36
FRAMES_PER_BANK = 6
SIDE_COMPOSITOR = 0x0e00
SIDE_BANK = 24  # extra loader indices 24–31, $4A00–$51FF
SIDE_START, SIDE_END = tick_at_bar(24),tick_at_bar(32)
START, END = tick_at_bar(40), tick_at_bar(56)
CUTS = (START, tick_at_bar(44), tick_at_bar(48))
STEPS = tuple(tick_at_beat(40*8+i, 2) for i in range(128))
LAUNCH_PREP = STEPS[118]
LAUNCH_START = STEPS[119]
OVERHEAD_START = STEPS[120]
FIREWORK_START = LAUNCH_START
FIREWORK_CENTRES = ((18,42),(18,132),(142,54),(142,147))
FIREWORK_ROWS = tuple((y+17)//2-8 for x,y in FIREWORK_CENTRES)
SIDE_STEPS = tuple(tick_at_beat(24*8+i,2) for i in range(64))
ALL_STEPS = SIDE_STEPS + STEPS
PALETTE = (0, 0x48, 0x9a, 0x2e)
RAINBOW = (0x2e,0x3c,0x4e,0x5c,0x6e,0x7c,0x8e,0x9c,
           0xae,0xbc,0xce,0xdc,0xee,0xfc,0x1e,0x2c)


def rainbow_palette(tick, band, airflow=False):
    phase=((tick & 255)>>4)+band*3
    inks=tuple(RAINBOW[(phase+offset)&15] for offset in (0,4,8,12,2))
    return ((0x0e,inks[1],inks[2],0x9e) if airflow else inks[:4])+(inks[4]|14,)


def emit_rainbow(c):
    """Reentrant unbanked NMI/foreground helper; private stack scratch only.

    Music DLIs keep their original spacing; colours change AFTER the music
    decoder. The four calls per frame divide ribbons into broad rainbow bands.
    """
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    c.label('ribbon_palette')
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x48)
    a(0xad,0xd40b);c.emit(0x29,0x60,0x4a,0xba)
    a(0x1d,0x0101);c.emit(0xaa,0x68)
    for i,addr in enumerate((0xd012,0xd013,0xd014,0xd015,0xd019)):
        c.jump(0xbd,f'ribbon_ink{i}');a(0x8d,addr)
    a(0xad,0x83ed);c.emit(0xc9,12);c.branch(0x90,'wind_colours_done')
    c.emit(0xc9,16);c.branch(0xb0,'wind_colours_done')
    c.emit(0xa9,0x0e);a(0x8d,0xd012);c.emit(0xa9,0x9e);a(0x8d,0xd015)
    c.label('wind_colours_done')
    c.emit(0x60)
    for i in range(5):
        c.label(f'ribbon_ink{i}')
        c.emit(*(rainbow_palette(phase*16,band)[i] for band in range(4) for phase in range(16)))
# Hand locations in source cells, left and right in screen space.
HANDS = (((.12,.34),(.70,.05)), ((.12,.55),(.17,.61)),
         ((.12,.27),(.88,.27)), ((.12,.52),(.76,.12)),
         ((.20,.25),(.26,.33)), ((.22,.63),(.75,.64)),
         ((.20,.02),(.74,.02)), ((.20,.03),(.78,.03)))
SIDE_HANDS = (((.18,.36),(.70,.05)),((.20,.47),(.64,.09)),
              ((.23,.57),(.52,.13)),((.20,.62),(.73,.43)),
              ((.16,.34),(.80,.52)),((.20,.30),(.80,.41)),
              ((.25,.14),(.80,.40)),((.39,.04),(.66,.63)))


def frame_for_step(step):
    if step < 32:
        return (0,32,1,33,3,2,32,0)[step & 7]
    if step < 64:
        return (4,5,34,6,7,6,34,5)[step & 7]
    if step < 118:
        # Dance fills the recovered time. The actual throw below runs once.
        return (8,9,35,10,8,10,35,9)[step&7]
    return (11,12,13,14,15,15,15,15,15,15)[step-118]


def frame_at(tick):
    if SIDE_START<=tick<SIDE_END:return 16+((tick>>4)&15)
    from ribbon_inbetweens import midpoint_at,quarter_at
    step=max(i for i,t in enumerate(STEPS) if t <= tick)
    quarter=quarter_at(tick,step)
    if quarter is not None:return 45+quarter
    mid=midpoint_at(tick,step)
    return 37+mid if mid is not None else frame_for_step(step)


@lru_cache(maxsize=4)
def source(side=False,overhead=False,mid=False):
    data=Path('build/ribbon-inbetweens-v173.rgb' if mid==3 else 'build/ribbon-inbetweens-v171.rgb' if mid==2 else 'build/ribbon-inbetweens-v166.rgb' if mid else 'build/ribbon-overhead-v145.rgb' if overhead else 'build/ribbon-side-v142.rgb' if side else 'build/ribbon-dancer-v136.rgb').read_bytes()
    assert len(data)==(1329*1329 if mid else 1774*887)*3
    return data


@lru_cache(maxsize=40)
def sprite(pose,side=False,overhead=False,mid=False):
    data=source(side,overhead,mid)
    width,height,cols,rows=(1329,1329,3,3) if mid else (1774,887,4,2)
    col,row=pose%cols,pose//cols
    x0,x1=round(col*width/cols),round((col+1)*width/cols)
    y0,y1=round(row*height/rows),round((row+1)*height/rows)
    w,h=x1-x0,y1-y0
    rgb=b''.join(data[((y0+y)*width+x0)*3:((y0+y)*width+x1)*3] for y in range(h))
    black=bytearray(max(rgb[i:i+3])<45 for i in range(0,len(rgb),3))
    outside=bytearray(w*h);queue=deque()
    for pos in list(range(w))+list(range((h-1)*w,h*w))+[y*w for y in range(h)]+[y*w+w-1 for y in range(h)]:
        if black[pos] and not outside[pos]:outside[pos]=1;queue.append(pos)
    while queue:
        pos=queue.popleft();y,x=divmod(pos,w)
        for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=xx<w and 0<=yy<h:
                n=yy*w+xx
                if black[n] and not outside[n]:outside[n]=1;queue.append(n)
    return rgb,outside,w,h


def actor(canvas, pose, center, baseline, scale, mirror=False,side=False,mask=None,mid=False):
    """Sample the fixed-scale source sheet, preserving black facial details."""
    data,outside,w,h=sprite(pose,side,mid=mid)
    sx,sy=scale*1.5,scale
    points={}
    for y in range(64):
        oy=round((y-baseline)/sy+402)
        if not 0<=oy<h: continue
        for x in range(160):
            ox=round((x-center)/sx+222)
            if mirror:ox=443-ox
            if not 0<=ox<w or outside[oy*w+ox]:continue
            n=(oy*w+ox)*3;r,g,b=data[n:n+3]
            if max(r,g,b)<45:ink=0
            elif r>g*1.15 and b>g*1.15: ink=1
            elif b>r*1.15 or g>r*1.15: ink=2
            else:ink=3
            points[x,y]=ink
    # A black keyline keeps legs and skirt distinct from the floor/wall.
    for x,y in points:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)):
            xx,yy=x+dx,y+dy
            if 0<=xx<160 and 0<=yy<64 and (xx,yy) not in points:
                canvas[yy*160+xx]=0
                if mask is not None:mask[yy*160+xx]=1
    for (x,y),ink in points.items():
        canvas[y*160+x]=ink
        if mask is not None:mask[y*160+x]=1
    hands=[]
    if mid:
        from ribbon_inbetweens import HANDS as MID_HANDS
    for hx,hy in (MID_HANDS if mid else SIDE_HANDS if side else HANDS)[pose]:
        ox=hx*443
        if mirror:ox=443-ox
        hands.append((round(center+(ox-222)*sx),round(baseline+(hy*443-402)*sy)))
    return hands


def gym(close=False):
    p=bytearray(160*64)
    def line(x0,y0,x1,y1,c):
        n=max(abs(x1-x0),abs(y1-y0),1)
        for i in range(n+1):
            x=round(x0+(x1-x0)*i/n);y=round(y0+(y1-y0)*i/n)
            if 0<=x<160 and 0<=y<64:p[y*160+x]=c
    for x in (4,32,128,156):
        line(x,2,x,39,2)
    for y in (4,19,35):
        line(4,y,48,y,2);line(112,y,155,y,2)
    line(0,40,159,40,1);line(0,42,159,42,2)
    for x in (-40,0,40,80,120,160,200):line(80,40,x,63,2)
    for y in (48,58):line(0,y,159,y,2)
    # Basketball backboard and restrained light rails establish the same gym.
    for a,b,c,d in ((69,5,91,5),(69,5,69,13),(91,5,91,13),(69,13,91,13),
                    (76,9,84,9),(76,9,76,14),(84,9,84,14),(74,15,86,15)):
        line(a,b,c,d,1 if d>=14 else 2)
    return p


def side_gym(phase):
    """Side tracking shot: the wall moves LEFT as she backsteps RIGHT."""
    p=bytearray(160*64)
    for y in range(64):
        for x in range(160):
            u=(x+phase*4)%64
            if y<42:
                if (u in (2,3,27,28,51,52) and 4<=y<=35) or (y in (4,19,35) and 2<=u<=52):p[y*160+x]=2
                if y in (38,39):p[y*160+x]=1
                if 22<=y<=32 and u in (57,58):p[y*160+x]=1
            else:
                if y in (44,54,62) or (x+phase*2)%16==0:p[y*160+x]=2
    return p


def overhead_actor(canvas,pose,cx,cy,scale):
    data,outside,w,h=sprite(pose,overhead=True)
    points={}
    for y in range(64):
        oy=round((y-cy)/scale+220)
        if not 0<=oy<h:continue
        for x in range(160):
            ox=round((x-cx)/(scale*1.3)+222)
            if not 0<=ox<w or outside[oy*w+ox]:continue
            n=(oy*w+ox)*3;r,g,b=data[n:n+3]
            ink=0 if max(r,g,b)<45 else 1 if r>g*1.15 and b>g*1.15 else 2 if b>r*1.15 or g>r*1.15 else 3
            points[x,y]=ink
    for x,y in points:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)):
            xx,yy=x+dx,y+dy
            if 0<=xx<160 and 0<=yy<64 and (xx,yy) not in points:canvas[yy*160+xx]=0
    for (x,y),ink in points.items():canvas[y*160+x]=ink
    hands=(((.35,.42),(.65,.43)),((.23,.52),(.78,.50)),((.18,.49),(.85,.51)),
           ((.13,.46),(.90,.48)),((.13,.43),(.87,.43)),((.17,.43),(.82,.43)),
           ((.17,.55),(.85,.58)),((.19,.52),(.88,.56)))[pose]
    return [(round(cx+(hx*443-222)*scale*1.3),round(cy+(hy*443-220)*scale)) for hx,hy in hands]


def overhead_artwork(frame):
    launch=1 if frame==13 else frame-11
    depth=launch/4;p=bytearray(160*64)
    # Quiet black ground: no plank grid, court rectangle or centre markings.
    # The receding bases retain the overhead depth cue without line clutter.
    pose=4 if frame==13 else frame-8
    small=.065*(1-depth*.65)
    left=overhead_actor(p,0,round(51+depth*17),round(45-depth*7),small)
    right=overhead_actor(p,1,round(109-depth*17),round(45-depth*7),small)
    scale=(.105,.11,.115,.12,.155,.195,.24,.285)[pose]
    hero=overhead_actor(p,pose,80,32,scale)
    return bytes(p),[hero[0],hero[1],left[0],right[1]]


@lru_cache(maxsize=FRAME_COUNT)
def artwork(frame):
    if frame>=37:
        from ribbon_inbetweens import artwork as midpoint_artwork
        return midpoint_artwork(frame-37)
    if 13<=frame<16:return overhead_artwork(frame)
    if 16<=frame<32:
        phase=frame-16;pose=(phase//2)&7
        p=side_gym(phase)
        hands=actor(p,pose,99,61,.125,side=True)
        left=hands[0]
        return bytes(p),[left,(left[0]-20,left[1]+8),(left[0]-40,left[1]),hands[1]]
    p=bytearray(160*64) if frame==12 else gym(frame in range(4,8));anchors=[]
    if frame<4 or frame in (32,33):
        pose={0:0,1:1,2:2,3:3,32:4,33:5}[frame]
        left=actor(p,pose,32,57,.09)
        right=actor(p,pose,128,57,.09,True)
        hero=actor(p,pose,80,61,.125)
        anchors=[hero[0],hero[1],left[0],right[1]]
    elif frame<8 or frame==34:
        pose=(0,4,3,2)[frame-4] if frame<8 else 1
        hero=actor(p,pose,80,67,.16)
        anchors=[hero[0],hero[1],hero[0],hero[1]]
    else:
        # The third shot shows the bases, a shared crouch, then the flyer.
        pose=(2,0,3,5,6,6,7,7)[frame-8] if frame<16 else 4
        if frame<12 or frame==35:
            left=actor(p,pose,42,61,.10)
            right=actor(p,pose,118,61,.10,True)
            hero=actor(p,pose,80,55,.11)
        else:
            left=actor(p,6,57,62,.065)
            right=actor(p,6,103,62,.065,True)
            # Continuous ascent across four distinct stored flight stages.
            hero=actor(p,pose,80,36,.10)
        anchors=[hero[0],hero[1],left[0],right[1]]
    return bytes(p),anchors


def packed_frame(frame):
    p=side_gym(frame-16) if 16<=frame<32 else artwork(frame)[0]
    return bytes(sum(p[i+k]<<(6-2*k) for k in range(4)) for i in range(0,len(p),4))


def side_step(tick):
    return min(22,max(0,(tick-SIDE_START)//128))


def scene_artwork(tick):
    frame=frame_at(tick)
    if not SIDE_START<=tick<SIDE_END:return artwork(frame)
    p=side_gym(frame-16)
    hands=actor(p,(frame-16)//2,40+4*side_step(tick),61,.125,side=True)
    left=hands[0]
    return bytes(p),[left,(left[0]-20,left[1]+8),(left[0]-40,left[1]),hands[1]]


def side_actor_data(pose):
    p=bytearray(160*64);mask=bytearray(160*64)
    actor(p,pose,40,61,.125,side=True,mask=mask)
    # Crop includes black keylines: x=4..71, y=8..63, 17 packed bytes/row.
    assert all(not v or (4<=i%160<72 and i//160>=8) for i,v in enumerate(mask))
    pixels=bytearray();keep=bytearray()
    for y in range(8,64):
        for x in range(4,72,4):
            pixels.append(sum(p[y*160+x+k]<<(6-2*k) for k in range(4)))
            keep.append(sum((0 if mask[y*160+x+k] else 3)<<(6-2*k) for k in range(4)))
    assert len(pixels)==len(keep)==952
    return bytes(pixels)+bytes(72)+bytes(keep)+bytes(72)


def install_side_actor(bank,index):
    if not SIDE_BANK<=index<SIDE_BANK+8:return bank
    out=bytearray(bank);data=side_actor_data(index-SIDE_BANK)
    assert out[0xa00:0x1200]==bytes(2048)
    out[0xa00:0x1200]=data
    return bytes(out)


def install_runtime(runtime):
    """Unbanked masked overlay; music NMI may restore banks at any instruction."""
    c=Code(SIDE_COMPOSITOR)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    from ribbon_inbetweens import COPY
    c.emit(0x48);a(0xad,0x83e5);c.branch(0x10,'normal_frame');c.emit(0x68);a(0x4c,COPY)
    c.label('normal_frame');c.emit(0x68)
    a(0x20,0x0c00)  # existing background copy, A=source page, X=2
    a(0xad,0x83ed);c.emit(0xc9,16);c.branch(0x90,'done');c.emit(0xc9,32);c.branch(0xb0,'done')
    c.emit(0x38,0xe9,16,0x4a,0xaa);a(0xbd,0x08c0+SIDE_BANK);a(0x8d,0xd301)
    c.emit(0xa9,0)
    for label in ('pixel_lo','mask_lo'):c.jump(0x8d,label)
    c.emit(0xa9,0x4a);c.jump(0x8d,'pixel_hi');c.emit(0xa9,0x4e);c.jump(0x8d,'mask_hi')
    a(0xad,0x83fc);c.emit(0x18,0x69,0x41)
    for label in ('read_lo','write_lo'):c.jump(0x8d,label)
    a(0xad,0x83fe);c.emit(0x18,0x69,1)
    for label in ('read_hi','write_hi'):c.jump(0x8d,label)
    c.emit(0xa2,56)
    c.label('row');c.emit(0xa0,16)
    c.label('byte');c.label('read');c.emit(0xb9,0,0x90)
    c.label('mask');c.emit(0x39,0,0x4e)
    c.label('pixel');c.emit(0x19,0,0x4a)
    c.label('write');c.emit(0x99,0,0x90)
    c.emit(0x88);c.branch(0x10,'byte')
    c.jump(0xad,'pixel_lo');c.emit(0x18,0x69,17)
    for label in ('pixel_lo','mask_lo'):c.jump(0x8d,label)
    c.branch(0x90,'source_ready')
    for label in ('pixel_hi','mask_hi'):c.jump(0xee,label)
    c.label('source_ready');c.jump(0xad,'read_lo');c.emit(0x18,0x69,40)
    for label in ('read_lo','write_lo'):c.jump(0x8d,label)
    c.branch(0x90,'target_ready')
    for label in ('read_hi','write_hi'):c.jump(0xee,label)
    c.label('target_ready');c.emit(0xca);c.branch(0xd0,'row')
    c.label('done');c.emit(0x60)
    for label in ('pixel','mask','read','write'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    data=c.finish();assert len(data)<=256
    out=bytearray(runtime);offset=SIDE_COMPOSITOR-0x0c00
    assert out[offset:offset+len(data)]==bytes(len(data))
    out[offset:offset+len(data)]=data
    from ribbon_inbetweens import install_runtime as install_midpoint_runtime
    return install_midpoint_runtime(out)


def ribbon_streams():
    """16 continuously varying shapes; four broad ribbons plus fine missiles."""
    result=bytearray()
    for plane in range(5):
        for phase in range(16):
            out=bytearray(64);angle=phase*math.tau/16+plane*.8
            if plane<4:
                # A waving loop rooted at local (3.5,32), followed by a tail.
                points=[]
                for i in range(161):
                    t=i/160
                    xx=3.5+3.2*math.sin(t*math.tau+angle)*math.sin(math.pi*t)
                    yy=32+28*math.sin(t*math.tau)
                    points.append((round(xx),round(yy)))
                # Rasterize every segment, not just curve samples. At the
                # steepest points neighbouring samples differ by two rows.
                for (x0,y0),(x1,y1) in zip(points,points[1:]):
                    steps=max(abs(x1-x0),abs(y1-y0),1)
                    for j in range(steps+1):
                        x=round(x0+(x1-x0)*j/steps)
                        y=round(y0+(y1-y0)*j/steps)
                        if 0<=x<8 and 0<=y<64:out[y]|=0x80>>x
            else:
                for i in range(4):
                    age=(phase+i*4)&15
                    y=32-round(2.8*age-.05*age*age)
                    # Bright two-pixel head and a thinning falling trail.
                    for dy,bits in enumerate((1,3,2,1)):
                        if age>11 and dy>1:continue
                        if 0<=y+dy<64:out[y+dy]|=bits<<(i*2)
            result.extend(out)
    assert len(result)==5120
    return bytes(result)


def firework_shapes():
    """Eight compact rocket / radial burst / falling ember silhouettes."""
    frames=[]
    for phase in range(8):
        out=bytearray(16)
        if phase<2:
            y=12-phase*5
            out[y]=0x10;out[y+1]=0x10;out[y+3]=0x08
        else:
            radius=(1.8,3.8,5.8,7.2,7.8,8.5)[phase-2]
            for ray in range(10):
                theta=ray*math.tau/10
                for tail in range(2 if phase<6 else 1):
                    r=max(0,radius-tail*1.6)
                    x=round(3.5+3.2*r/8.5*math.cos(theta))
                    y=round(6+r*.75*math.sin(theta)+max(0,phase-4)*.65)
                    if 0<=x<8 and 0<=y<16:out[y]|=0x80>>x
        frames.extend(out)
    return bytes(frames)


def wind_shapes():
    """Narrow air streaks sweep down against the upward motion of the flyer."""
    frames=[]
    for phase in range(8):
        out=bytearray(16)
        for x,offset in ((2,0),(5,10)):
            head=(phase*3+offset)%24
            for tail in range(9):
                y=head-tail
                if 0<=y<16:out[y]|=0x80>>(x+(1 if tail>5 else 0))
        frames.extend(out)
    return bytes(frames)


def metadata():
    blob=bytearray()
    for player in range(4):
        blob.extend(FIREWORK_CENTRES[player][0]+40 if 12<=f<16 else
                    max(0,min(255,artwork(f)[1][player][0]+48-14)) for f in range(FRAME_COUNT))
    for player in range(4):
        blob.extend(((artwork(f)[1][player][1]*3+17)//2-32)&255 for f in range(FRAME_COUNT))
    assert len(blob)==8*FRAME_COUNT
    return blob


def frame_bank(index):
    assert 0<=index<6
    return b''.join(packed_frame(index*6+i) for i in range(6))+bytes(1024)


def install_control(bank, copy_address, palette_address):
    out=bytearray(bank);code=helper(copy_address,palette_address)
    assert len(code)<=0xc00
    for offset,data in ((0x1400,code),(RIBBONS-0x4000,ribbon_streams()),(META-0x4000,metadata()),(WIND-0x4000,wind_shapes())):
        assert out[offset:offset+len(data)]==bytes(len(data)),hex(offset)
        out[offset:offset+len(data)]=data
    return bytes(out)


def helper(copy_address, palette_address=0):
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # Descending half-beat table preserves exact player-clock synchronization.
    c.emit(0xa2,len(ALL_STEPS)-1)
    c.label('find');a(0xad,0x83e3);c.jump(0xdd,'step_hi');c.branch(0x90,'previous');c.branch(0xd0,'found')
    a(0xad,0x83e2);c.jump(0xdd,'step_lo');c.branch(0xb0,'found')
    c.label('previous');c.emit(0xca,0xe0,0xff);c.branch(0xd0,'find')
    c.label('found');c.emit(0xe0,64);c.branch(0xb0,'front_shot')
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x29,15,0x18,0x69,16);c.jump(0x4c,'selected_frame')
    c.label('front_shot');c.jump(0xbd,'frames')
    c.label('selected_frame');a(0x8d,0x83ed)
    from ribbon_inbetweens import SELECT
    a(0x20,SELECT)
    c.emit(0xa9,0);a(0x8d,0x83fc);a(0x8d,0x83fd)
    a(0xad,0x83ed);c.emit(0xc9,16);c.branch(0x90,'position_ready');c.emit(0xc9,32);c.branch(0xb0,'position_ready')
    a(0xad,0x83e2);c.emit(0x38,0xe9,SIDE_START&255);a(0x8d,0x83e9)
    a(0xad,0x83e3);c.emit(0xe9,SIDE_START>>8,0x0a);a(0x8d,0x83fc)
    a(0xad,0x83e9);c.emit(0x0a);a(0xad,0x83fc);c.emit(0x69,0,0xc9,23);c.branch(0x90,'position_clamped');c.emit(0xa9,22)
    c.label('position_clamped');a(0x8d,0x83fc);c.emit(0x0a,0x0a,0x38,0xe9,59);a(0x8d,0x83fd)
    c.label('position_ready')
    c.emit(0xa9,0);a(0x8d,0x83eb)
    a(0xad,0x83fc);c.label('position_cache');c.emit(0xc9,255);c.branch(0xd0,'changed')
    # Other scenes can share the small frame key; the active layout must
    # also belong to ribbons before a held-frame cache hit is valid.
    a(0xad,0x83e6);c.emit(0x29,4,0x4a,0x4a,0x49,1,0xaa)
    a(0xbd,DL_KEYS);c.emit(0xc9,7);c.branch(0xd0,'changed')
    a(0xad,0x83ed);c.emit(0x09,0x40);a(0x0d,0x83e5)
    a(0xcd,0x83fa);c.branch(0xd0,'changed');c.jump(0x4c,'prepare_pmg')
    c.label('changed');a(0xad,0x83fc);c.jump(0x8d,'position_cache_value');a(0xad,0x83ed);c.emit(0x09,0x40);a(0x0d,0x83e5);a(0x8d,0x83fa);c.emit(0xa9,1);a(0x8d,0x83eb)
    a(0xad,0x83e6);c.emit(0x29,4,0x0a,0x0a,0x0a,0x49,0xb0);a(0x8d,0x83fe)
    a(0x20,copy_address)
    # Inactive bitmap DL, 64 source rows tripled to 192 display lines.
    cached_display_list(c,7)
    a(0xad,0x83e6);c.jump(0x8d,'dl1_hi');c.jump(0x8d,'dl2_hi')
    c.emit(0xa9,3);c.jump(0x8d,'dl1_lo');c.emit(0xa9,4);c.jump(0x8d,'dl2_lo');c.emit(0xa0,0)
    c.label('rows');c.jump(0xb9,'row_lo');c.label('dl1');c.emit(0x8d,0,0)
    c.jump(0xb9,'row_hi');c.emit(0x18);a(0x6d,0x83fe);c.label('dl2');c.emit(0x8d,0,0)
    for label in ('dl1','dl2'):
        c.emit(0x18);c.jump(0xad,label+'_lo');c.emit(0x69,3);c.jump(0x8d,label+'_lo');c.branch(0x90,label+'ok');c.jump(0xee,label+'_hi');c.label(label+'ok')
    c.emit(0xc8,0xc0,192);c.branch(0xd0,'rows')
    c.label('swap')
    c.label('prepare_pmg')
    # Back PMG base is $08 or $88. The unused prefix may hold static rows.
    a(0xad,0xd407);c.emit(0x29,0x80,0x49,0x80);a(0x8d,0x83e8)
    c.emit(0xa9,0xa,0x0d,0xe8,0x83)
    for label,delta in (('clear0',0),('clear1',0),('clear2',1),('clear3',1)):
        if delta and label=='clear2':c.emit(0x18,0x69,1)
        c.jump(0x8d,label+'_hi')
    # Missile plane starts one page below the players.
    c.emit(0x38,0xe9,2);c.jump(0x8d,'clear4_hi')
    c.emit(0xa9,0,0xa2,127)
    c.label('clear_pmg')
    for i,addr in enumerate((0xa00,0xa80,0xb00,0xb80,0x980)):
        c.label(f'clear{i}');a(0x9d,addr)
    c.emit(0xca);c.branch(0x10,'clear_pmg')
    c.emit(0xa9,3);a(0x8d,0x83e7)
    a(0xad,0x83ed);c.emit(0xc9,12);c.branch(0x90,'normal_ribbons');c.emit(0xc9,16);c.branch(0xb0,'normal_ribbons')
    c.label('overhead_pmg');c.emit(0xa9,1);a(0x8d,0x83e7)
    c.jump(0x20,'launch_fireworks');c.jump(0x4c,'wait')
    c.label('normal_ribbons')
    # Copy five separately positioned 64-byte streams into inactive PMG RAM.
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x29,15,0xaa)
    c.jump(0xbd,'phase_lo');c.jump(0x8d,'get_lo');c.jump(0xbd,'phase_hi');c.jump(0x8d,'get_hi')
    for plane in range(5):
        if plane:
            c.jump(0xad,'get_hi');c.emit(0x18,0x69,4);c.jump(0x8d,'get_hi')
        a(0xae,0x83ed);a(0xbd,META+4*FRAME_COUNT+(plane if plane<4 else 0)*FRAME_COUNT);c.emit(0xa8)
        c.emit(0xa9,(0xa if plane<2 else 0xb if plane<4 else 9));a(0x0d,0x83e8);c.jump(0x8d,f'put{plane}_hi')
        c.emit(0xa2,0)
        c.label(f'blit{plane}');c.jump(0x20,'get');c.emit(0xc0,128);c.branch(0xb0,f'skip{plane}')
        c.label(f'put{plane}');a(0x99,0xa00+(plane%2)*128 if plane<4 else 0x980)
        c.label(f'skip{plane}');c.emit(0xc8,0xe8,0xe0,64);c.branch(0xd0,f'blit{plane}')
    # Atomic presentation: wait with OLD PMG enabled, then update DL/PMG/regs.
    c.label('wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'wait');c.emit(0xc9,128);c.branch(0xb0,'wait')
    a(0xad,0x83eb);c.branch(0xf0,'held')
    c.emit(0xa9,0);a(0x8d,0xd402);a(0xad,0x83e6);a(0x8d,0xd403);c.emit(0x49,4);a(0x8d,0x83e6)
    c.label('held')
    a(0xad,0x83e8);c.emit(0x09,8);a(0x8d,0xd407)
    for plane in range(4):
        a(0xae,0x83ed)
        a(0xbd,META+plane*FRAME_COUNT);c.emit(0x18);a(0x6d,0x83fd);a(0x8d,0xd000+plane)
        a(0x8d,0x83e9)
        a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x29,15,0xaa)
        c.jump(0xbd,f'spark_x{plane}');c.emit(0x18);a(0x6d,0x83e9);a(0x8d,0xd004+plane)
        a(0xad,0x83e7);a(0x8d,0xd008+plane)
    a(0xad,0x83e7);c.emit(0x4a);c.branch(0xf0,'missile_size_ready');c.emit(0xa9,0x55)
    c.label('missile_size_ready');a(0x8d,0xd00c)
    for addr,val in ((0xd01b,0x11),(0xd01d,3),(0xd400,0x2e),
                     (0xd01a,0),(0xd016,0x48),(0xd017,0x9a),(0xd018,0x2c)):
        c.emit(0xa9,val);a(0x8d,addr)
    a(0x20,palette_address)
    c.emit(0x60)
    c.label('get');c.emit(0xbd,0,0);c.emit(0x60)
    # The overhead preparation is free of ribbons. On launch, use compact
    # bursts in side columns, leaving the central face/body unobstructed.
    c.label('launch_fireworks')
    a(0xad,0x83e3);c.emit(0xc9,FIREWORK_START>>8);c.branch(0xb0,'fw_high_ready');c.emit(0x60)
    c.label('fw_high_ready');c.branch(0xd0,'fw_active')
    a(0xad,0x83e2);c.emit(0xc9,FIREWORK_START&255);c.branch(0xb0,'fw_active');c.emit(0x60)
    c.label('fw_active');a(0xad,0x83e8);c.emit(0x09,9)
    c.jump(0x8d,'fw_spark_read_hi');c.jump(0x8d,'fw_spark_write_hi')
    a(0xad,0x83e2);c.emit(0x38,0xe9,FIREWORK_START&255,0x29,0x70,0xaa)
    for plane in range(4):
        c.emit(0xa0,FIREWORK_ROWS[plane])
        a(0xad,0x83e8);c.emit(0x09,10 if plane<2 else 11);c.jump(0x8d,f'fw_put{plane}_hi')
        c.label(f'fw_blit{plane}')
        if plane in (0,3):a(0xbd,WIND)
        else:c.jump(0xbd,'fw_shapes')
        c.label(f'fw_put{plane}');a(0x99,0xa00+plane*128)
        c.emit(0xc8,0xe8,0x8a,0x29,15);c.branch(0xd0,f'fw_blit{plane}')
        c.emit(0xa9,3<<(2*plane));c.jump(0x20,'fw_spark')
        c.emit(0x8a,0x18,0x69,16,0x29,0x7f,0xaa)
    c.emit(0x60)
    c.label('fw_spark');c.jump(0x8d,'fw_mask_value');c.emit(0x8a,0x48)
    c.emit(0x98,0x38,0xe9,12);a(0x8d,0x83e9)
    a(0xad,0x83e2);c.emit(0x29,12,0x18);a(0x6d,0x83e9);c.emit(0xa8,0xa2,4)
    c.label('fw_trail');c.label('fw_spark_read');a(0xb9,0x980)
    c.label('fw_mask');c.emit(0x09,0)
    c.label('fw_spark_write');a(0x99,0x980);c.emit(0xc8,0xca);c.branch(0xd0,'fw_trail')
    c.emit(0x68,0xaa,0x60)
    for i in range(4):c.labels[f'fw_put{i}_hi']=c.labels[f'fw_put{i}']+2
    c.labels['fw_spark_read_hi']=c.labels['fw_spark_read']+2
    c.labels['fw_spark_write_hi']=c.labels['fw_spark_write']+2
    c.labels['fw_mask_value']=c.labels['fw_mask']+1
    c.label('fw_shapes');c.emit(*firework_shapes())
    for label in ('dl1','dl2','get'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    for i in range(5):
        c.labels[f'clear{i}_hi']=c.labels[f'clear{i}']+2
        c.labels[f'put{i}_hi']=c.labels[f'put{i}']+2
    c.label('phase_lo');c.emit(*((RIBBONS+i*64)&255 for i in range(16)))
    c.label('phase_hi');c.emit(*((RIBBONS+i*64)>>8 for i in range(16)))
    for i in range(4):
        c.label(f'spark_x{i}')
        c.emit(*((14+round((i-1.5)*((phase+i*4)&15)*.55))&255 for phase in range(16)))
    c.label('step_lo');c.emit(*(t&255 for t in ALL_STEPS))
    c.label('step_hi');c.emit(*(t>>8 for t in ALL_STEPS))
    c.label('frames');c.emit(*(tuple([16]*64)+tuple(frame_for_step(i) for i in range(128))))
    c.label('row_lo');c.emit(*((y//3*40)&255 for y in range(192)))
    c.label('row_hi');c.emit(*((y//3*40)>>8 for y in range(192)))
    c.labels['position_cache_value']=c.labels['position_cache']+1
    return c.finish()
