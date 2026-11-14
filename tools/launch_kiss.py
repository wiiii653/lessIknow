"""One wink/kiss and a shaded PMG heart approaching the overhead camera.

The entire heart lives in one previously empty 1 KiB ribbon-bank tail.
Only the inactive PMG buffer is touched; a small unbanked bank trampoline
returns to the ribbon controller before presentation.
"""
import math
from build_sequence import Code
from music_timing import tick_at_beat

PREPARE, COMMIT = 0x0f00, 0x0f04
ENTRY, LIMIT = 0x7c00, 0x8000
TAIL_INDEX = 2  # ribbon compositions 12–17, original player bank table 10
START = tick_at_beat(40*8+122,2)
PHASE, DOUBLE = 0x0ddb, 0x0ddc
# Saturated magenta-pink with a light glint and a deeper edge.
COLORS = (0x56,0x58,0x5c,0x54)
MOUTH = (82,67)


def phase_at(tick):
    return min(7,max(0,(tick-START)//32))


def geometry(phase):
    # Gentle depth yaw and a travelling specular ridge accompany expansion.
    # Keep the large sixth beat at double width; the old quadruple-width
    # register stretched the heart sideways while its height stayed doubled.
    size=0 if phase<4 else 1
    scale_x=1 if size==0 else 2
    scale_y=1 if size==0 else 2
    # Two expansions and contractions give the flying heart a heartbeat.
    width=(4,7,12,10,17,22,17,30)[phase]
    height=(8,14,24,20,34,44,34,60)[phase]
    cx=MOUTH[0]+(0,2,5,9,15,22,37,37)[phase]
    cy=MOUTH[1]-(0,1,3,6,10,15,27,27)[phase]
    return cx-8*scale_x,(cy+17)//2-8*scale_y,size,width,height


def face(canvas,frame):
    """Refine only the face inside the existing head/hair silhouette."""
    if frame not in (14,15):return
    cx,cy,rx,ry=(80,16,8,8) if frame==14 else (81,17,11,10)
    def put(x,y,ink):canvas[y*160+x]=ink
    for y in range(cy-ry,cy+ry+1):
        for x in range(cx-rx,cx+rx+1):
            q=((x-cx)/rx)**2+((y-cy)/ry)**2
            if q<=1:put(x,y,0 if q>.84 and y>cy+3 else 3)
    eyes=14 if frame==14 else 13
    for x0 in (cx-6,cx+3):
        for x in range(x0,x0+4):put(x,eyes-2,0)
    if frame==14:
        for x,y in ((74,14),(75,15),(76,15),(77,14),(73,13)):put(x,y,0)
    else:
        for x,y in ((75,13),(76,13),(77,13),(76,14)):put(x,y,0)
        put(76,13,2)
    for x,y in ((cx+3,eyes),(cx+4,eyes),(cx+5,eyes),(cx+4,eyes+1)):put(x,y,0)
    put(cx+4,eyes,2)
    put(cx,eyes+3,1)
    if frame==14:
        for x,y in ((78,20),(79,21),(80,21),(81,21),(82,20)):put(x,y,1)
    else:
        # Pursed lips, with a single dark centre at the emission point.
        for x,y in ((80,21),(81,20),(82,20),(83,21),(81,22),(82,22)):put(x,y,1)
        put(81,21,0);put(82,21,1)
        put(74,19,1);put(88,19,1)


def masks(phase):
    """Shaded heart followed by two expanding, multicolour particle bursts."""
    if phase >= 7:
        planes = [bytearray(16) for _ in range(4)]
        # Each particle travels radially away from the centre between phases.
        rays = ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1),
                (-2,-1),(2,-1),(-2,1),(2,1))
        for i,(dx,dy) in enumerate(rays):
            distance = 2 if phase == 6 else 3
            x = max(0,min(15,round(7.5 + dx * distance)))
            y = max(0,min(15,round(7.5 + dy * distance)))
            # Players 0/2 occupy the left half; 1/3 the right half.
            plane = (i % 2) * 2 + (x >= 8)
            planes[plane][y] |= 0x80 >> (x % 8)
        return tuple(bytes(p) for p in planes)
    _,_,size,width,height=geometry(phase)
    scale=1 if size==0 else 2
    yaw=math.sin((phase-2)*.52)*.18
    planes=[bytearray(16) for _ in range(4)]
    for y in range(16):
        yy=(7.5-y)*4*scale/height*1.35
        for x in range(16):
            xx=(x-7.5)*2*scale/width*1.2
            u=(xx+yaw*yy)/(.9+abs(yaw))
            def heart(u,v):
                # Deepen the upper cleft so the silhouette survives 16 columns.
                return ((u*u+v*v-1)**3-u*u*v**3<=0 and
                        not (v>.5 and abs(u)<.55*(v-.5)))
            front=heart(u,yy)
            back=phase>=2 and heart(u-.22,yy+.07)
            if not (front or back):continue
            if x<8:
                glint=((u+.45)/.18)**2+((yy-.65)/.3)**2<1
                plane=2 if glint else 0
            else:
                bright=front and (u+.12+yaw)**2+(yy-.16)**2<1.15
                plane=1 if bright else 3
            planes[plane][y]|=0x80>>(x&7)
    return tuple(bytes(p) for p in planes)


def trampoline():
    c=Code(PREPARE)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    c.emit(0xa2,0);c.branch(0xf0,'common')
    assert c.origin+len(c.data)==COMMIT
    c.emit(0xa2,1)
    c.label('common');a(0xad,0x83ed);c.emit(0xc9,15);c.branch(0xd0,'done')
    a(0xad,0xd301);c.emit(0x48)
    a(0xad,0x26fc+8+TAIL_INDEX);a(0x8d,0xd301);a(0x20,ENTRY)
    c.emit(0x68);a(0x8d,0xd301)
    c.label('done');c.emit(0x60)
    code=bytes(c.finish());assert len(code)<=64
    return code


def install_runtime(runtime):
    out=bytearray(runtime);offset=PREPARE-0xc00;code=trampoline()
    assert out[offset:offset+len(code)]==bytes(len(code))
    out[offset:offset+len(code)]=code
    return bytes(out)


def helper():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    c.emit(0x8a,0x48)
    a(0xad,0x83e2);c.emit(0x38,0xe9,START&255);a(0x8d,PHASE)
    a(0xad,0x83e3);c.emit(0xe9,START>>8);c.branch(0xd0,'last')
    a(0xad,PHASE);c.emit(0x4a,0x4a,0x4a,0x4a,0x4a);c.jump(0x4c,'phase_ready')
    c.label('last');c.emit(0xa9,7)
    c.label('phase_ready');a(0x8d,PHASE);c.emit(0xaa,0x68);c.branch(0xf0,'prepare');c.jump(0x4c,'commit')
    c.label('prepare');a(0xad,PHASE);c.emit(0x0a,0x0a,0x0a,0x0a,0x0a);a(0x8d,DOUBLE)
    # Erase inherited wind/bursts only in the inactive four player planes.
    for plane in range(4):
        a(0xad,0x83e8);c.emit(0x09,10 if plane<2 else 11);c.jump(0x8d,f'clear{plane}_hi')
    c.emit(0xa2,127,0xa9,0)
    c.label('clear')
    for plane in range(4):c.label(f'clear{plane}');a(0x9d,0xa00+plane*128)
    c.emit(0xca);c.branch(0x10,'clear')
    for plane in range(4):
        a(0xae,PHASE)
        for part in ('lo','hi'):
            c.jump(0xbd,f'mask{plane}_{part}');c.jump(0x8d,f'read{plane}_{part}')
        c.jump(0xbc,'ys')
        a(0xad,0x83e8);c.emit(0x09,10 if plane<2 else 11)
        for stem in ('put','duplicate'):c.jump(0x8d,f'{stem}{plane}_hi')
        c.emit(0xa2,0)
        c.label(f'blit{plane}');c.label(f'read{plane}');c.emit(0xbd,0,0)
        c.label(f'put{plane}');a(0x99,0xa00+plane*128);c.emit(0xc8)
        a(0x2c,DOUBLE);c.branch(0x10,f'single{plane}')
        c.label(f'duplicate{plane}');a(0x99,0xa00+plane*128);c.emit(0xc8)
        c.label(f'single{plane}');c.emit(0xe8,0xe0,16);c.branch(0xd0,f'blit{plane}')
    c.emit(0x60)
    c.label('commit');a(0xae,PHASE)
    for plane in range(4):
        c.jump(0xbd,'xs');c.emit(0x18,0x69,48+(8 if plane&1 else 0))
        # A doubled player is 16 color clocks wide, instead of eight.
        if plane&1:
            a(0x2c,DOUBLE);c.branch(0x10,f'normal_x{plane}');c.emit(0x18,0x69,8)
            c.label(f'normal_x{plane}')
        a(0x8d,0xd000+plane)
        c.jump(0xbd,'sizes');a(0x8d,0xd008+plane)
    c.emit(0x60)
    for plane in range(4):
        for stem in ('clear','put','duplicate','read'):
            c.labels[f'{stem}{plane}_hi']=c.labels[f'{stem}{plane}']+2
        c.labels[f'read{plane}_lo']=c.labels[f'read{plane}']+1
    for name,values in (('xs',[geometry(p)[0] for p in range(8)]),
                        ('ys',[geometry(p)[1] for p in range(8)]),
                        ('sizes',[geometry(p)[2] for p in range(8)])):
        c.label(name);c.emit(*values)
    for plane in range(4):
        for part,shift in (('lo',0),('hi',8)):
            c.label(f'mask{plane}_{part}')
            for phase in range(8):
                # Code resolves absolute label operands; tables are patched below.
                c.emit(0)
    for phase in range(8):
        for plane,data in enumerate(masks(phase)):
            c.label(f'shape{phase}_{plane}');c.emit(*data)
    result=bytearray(c.finish())
    for plane in range(4):
        for part,shift in (('lo',0),('hi',8)):
            start=c.labels[f'mask{plane}_{part}']-ENTRY
            for phase in range(8):result[start+phase]=(c.labels[f'shape{phase}_{plane}']>>shift)&255
    assert len(result)<=LIMIT-ENTRY,len(result)
    return bytes(result)


def install_tail(bank,index):
    if index!=TAIL_INDEX:return bank
    out=bytearray(bank);data=helper()
    assert out[ENTRY-0x4000:]==bytes(1024)
    out[ENTRY-0x4000:ENTRY-0x4000+len(data)]=data
    return bytes(out)
