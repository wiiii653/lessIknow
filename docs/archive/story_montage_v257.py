"""Brief comic story cutaways within the established post-Trevor montage."""
from functools import lru_cache
from build_sequence import Code

ENTRY=0x7600
GATE=0x7700
# Original planned story beats translated along with the v248 montage.
# Alternate the story still with the existing moving effect every 256 ticks.
WINDOWS=((37884,39379,56),(40875,42371,57),(42371,43867,58),(46858,49850,59))

def selected(tick):
    if (tick>>8)&1:return None
    return next((frame for start,end,frame in WINDOWS if start<=tick<end),None)

@lru_cache(maxsize=1)
def frames():
    """Four ANTIC-E compositions made from the existing character art."""
    from trevor_polished import frames as trevor_frames
    from basketball_hero import frames as hero_frames
    from school_story import girl_front_pixels, boy_poses
    trevor=trevor_frames()[2]; hero=hero_frames()[0]
    girl=girl_front_pixels(); boy=boy_poses()[1]

    def canvas():return bytearray(160*96)
    def rect(dst,x,y,w,h,color):
        for yy in range(max(0,y),min(96,y+h)):
            for xx in range(max(0,x),min(160,x+w)):dst[yy*160+xx]=color
    def blit(dst,src,sw,sh,crop,box,mirror=False):
        sx,sy,cw,ch=crop;dx,dy,dw,dh=box
        for yy in range(dh):
            for xx in range(dw):
                tx=dw-1-xx if mirror else xx
                xx_src=sx+tx*cw//dw;yy_src=sy+yy*ch//dh
                if 0<=dx+xx<160 and 0<=dy+yy<96:
                    dst[(dy+yy)*160+dx+xx]=src[yy_src*sw+xx_src]
    # One readable face fills the shot; avoid repeated checkerboard portraits.
    a=canvas()
    blit(a,trevor,160,64,(48,0,80,50),(0,0,160,96))
    # The three characters in adjacent panels retain their established designs.
    b=canvas()
    for x in (1,54,107):rect(b,x,3,52,90,3)
    blit(b,trevor,160,64,(57,0,48,38),(3,5,48,86))
    blit(b,girl,160,192,(18,0,40,78),(56,5,48,86))
    blit(b,boy,160,192,(105,0,55,132),(109,5,48,86))
    # Opposed Trevor and basketball hero, separated by a comic lightning seam.
    c=canvas();rect(c,0,0,160,96,3)
    blit(c,trevor,160,64,(35,0,95,64),(2,2,77,92))
    blit(c,hero,160,56,(20,0,75,56),(81,2,77,92),mirror=True)
    for y in range(5,91):
        x=79+(4 if (y//12)&1 else -4)
        for dx in (-1,0,1):c[y*160+x+dx]=0
    # Enlarged Trevor foreshadows the established defeated-boy outro.
    d=canvas();blit(d,trevor,160,64,(37,0,91,64),(0,0,160,96))
    return tuple(map(bytes,(a,b,c,d)))

def helper():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    c.emit(0xa2,len(WINDOWS)-1)
    c.label('find');a(0xad,0x83e3);c.jump(0xdd,'start_hi');c.branch(0x90,'previous');c.branch(0xd0,'lower_ok')
    a(0xad,0x83e2);c.jump(0xdd,'start_lo');c.branch(0x90,'previous')
    c.label('lower_ok');a(0xad,0x83e3);c.jump(0xdd,'end_hi');c.branch(0x90,'inside');c.branch(0xd0,'none')
    a(0xad,0x83e2);c.jump(0xdd,'end_lo');c.branch(0xb0,'none')
    c.label('inside');a(0xad,0x83e3);c.emit(0x29,1);c.branch(0xd0,'none')
    c.emit(0x8a,0x18,0x69,56,0x38,0x60)
    c.label('previous');c.emit(0xca);c.branch(0x10,'find')
    c.label('none');c.emit(0x18,0x60)
    for name,values in (('start_lo',[s&255 for s,e,f in WINDOWS]),('start_hi',[s>>8 for s,e,f in WINDOWS]),
                        ('end_lo',[e&255 for s,e,f in WINDOWS]),('end_hi',[e>>8 for s,e,f in WINDOWS])):
        c.label(name);c.emit(*values)
    data=bytes(c.finish());assert ENTRY+len(data)<=GATE
    return data

def gate():
    """Keep the tunnel ball off the portraits and publish palette safely."""
    c=Code(GATE)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    a(0xad,0x83ed);c.emit(0xc9,56);c.branch(0x90,'ball');c.emit(0xc9,60);c.branch(0xb0,'ball')
    c.label('wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'wait');c.emit(0xc9,128);c.branch(0xb0,'wait')
    for addr,val in ((0xd01d,0),(0xd016,0x48),(0xd017,0x68),(0xd018,0x2c)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    c.label('ball');a(0x4c,0x7800)
    data=bytes(c.finish());assert GATE+len(data)<=0x7800
    return data
