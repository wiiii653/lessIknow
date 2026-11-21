"""Double-buffered PMG fireworks in unused tails of plasma banks 40/41.

Complete fireworks are drawn in front of plasma, letters and the crane.
No silhouette/text clipping is applied to their radial burst and falling trails.
"""
import math
from build_sequence import Code

ENTRY=0x6c00
PUBLISH=0x7000
DATA=0x7400
META=0x7280
CENTRES=((22,44),(56,72),(106,56),(138,36))
LAUNCH_Y=190
FIREWORK_CUES = (768, 1216, 1408, 1856, 2048)
LEFTS=tuple(x-14 for x,y in CENTRES)
HUES=(0x2e,0x4e,0x6e,0x8e,0xae,0xce,0xee,0x1e,
      0x3e,0x5e,0x7e,0x9e,0xbe,0xde,0xfe,0x2e)


def occupied(mask,x,y):
    if not (0<=x<160 and 0<=y<192):return False
    nibble_x=x//2;byte=mask[(y//3)*40+nibble_x//2]
    return bool((byte>>4) if nibble_x%2==0 else (byte&15))


def launch_y(age, plane):
    """Fine four-tick trajectory: visible lower edge to the explosion apex."""
    apex=CENTRES[plane][1]
    return round(apex+(LAUNCH_Y-apex)*(1-age/16)**1.25)


def anchors(step):
    result=[]
    for plane in range(4):
        age=(step+plane*16)&63
        if age<16:
            result.append((launch_y(age,plane)+8)//2-4)
        else:
            result.append((CENTRES[plane][1]+8)//2-16)
    return tuple(result)+(0,)


def anchor_data():
    # Players move at four times the shape rate; upper-sky missiles stay put.
    return bytes(anchors(step)[plane] for plane in range(4) for step in range(64))+b'\0'


def missile_position(phase,plane):
    age=(phase+plane*4)&15
    if age<4:return CENTRES[plane][0]
    radius=min(27,(age-4)*3)
    return CENTRES[plane][0]+(-1 if plane%2==0 else 1)*radius


def graphics(mask):
    del mask  # Foreground fireworks deliberately cross letters and the crane.
    result=bytearray()
    for plane in range(5):
        for phase in range(16):
            out=bytearray(32 if plane<4 else 64)
            if plane<4:
                age=(phase+plane*4)&15
                if age<4:
                    # Bright rocket nose and a broken exhaust below it. The
                    # moving anchor carries this shape up the entire screen.
                    for dy,bits in ((4,0x18),(5,0x18),(7,0x08),(8,0x10),
                                    (10,0x08),(12,0x10),(15,0x08)):
                        out[dy]=bits
                elif age==4:
                    for y in range(12,21):
                        out[y]=0xff if y==16 else 0x7e if abs(y-16)<=1 else 0x3c if abs(y-16)<=2 else 0x18
                else:
                    radius=min(13,(age-4)*2.6)
                    fall=max(0,age-10)**2*.18
                    for ray in range(12):
                        if age>=12 and (ray+plane)%3==0:continue
                        if age>=14 and (ray+plane)%2==0:continue
                        theta=ray*math.tau/12+plane*.21
                        for tail in range(3 if age<11 else 2 if age<13 else 1):
                            r=max(0,radius-tail*1.9)
                            xx=round(3.5+3.4*r/13*math.cos(theta))
                            yy=round(16+r*.74*math.sin(theta)+fall)
                            if 0<=xx<8 and 0<=yy<32:out[yy]|=0x80>>xx
            else:
                # Detached fragments extend the bursts sideways beyond the
                # player bodies. Their 64-row plane spans the upper sky.
                for i in range(4):
                    age=(phase+i*4)&15
                    if age<4:continue
                    radius=min(27,(age-4)*3)
                    fall=max(0,age-9)**2*.24
                    y=round((CENTRES[i][1]+8)/2-radius*.3+fall)
                    for dy,bits in ((0,3),(2,1),(5,2),(8,1)):
                        if 0<=y+dy<64:out[y+dy]|=bits<<(2*i)
            result.extend(out)
    assert len(result)==3072
    return bytes(result)


def install(bank,mask):
    out=bytearray(bank);code=helper()
    assert ENTRY+len(code)<=META
    meta=anchor_data()
    assert META+len(meta)<=DATA
    for offset,payload in ((ENTRY-0x4000,code),(DATA-0x4000,graphics(mask)),(META-0x4000,meta)):
        assert out[offset:offset+len(payload)]==bytes(len(payload)),hex(offset)
        out[offset:offset+len(payload)]=payload
    return bytes(out)


def helper():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # Prepare the alternate PMG buffer while the last complete burst stays on.
    a(0xad,0xd407);c.emit(0x29,0x80,0x49,0x80);a(0x8d,0x83e8);c.jump(0x8d,'back_bit')
    for i,high in enumerate((9,10,10,11,11)):
        c.emit(0xa9,high);a(0x0d,0x83e8);c.jump(0x8d,f'clear{i}_hi')
    c.emit(0xa9,0,0xa2,127)
    c.label('clear')
    for i,addr in enumerate((0x980,0xa00,0xa80,0xb00,0xb80)):
        c.label(f'clear{i}');a(0x9d,addr)
    c.emit(0xca);c.branch(0x10,'clear')
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x29,63);c.jump(0x8d,'vertical_index')
    c.emit(0x4a,0x4a,0xaa);c.jump(0x8d,'frame_index')
    c.jump(0xbd,'source_lo');c.jump(0x8d,'read_lo');c.jump(0xbd,'source_hi');c.jump(0x8d,'read_hi')
    for plane in range(5):
        if plane:
            c.jump(0xad,'read_hi');c.emit(0x18,0x69,2);c.jump(0x8d,'read_hi')
        if plane==4:
            a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x29,15,0xaa)
            c.jump(0xbd,'missile_source_lo');c.jump(0x8d,'read_lo')
            c.jump(0xbd,'missile_source_hi');c.jump(0x8d,'read_hi')
        cue = FIREWORK_CUES[plane]
        a(0xad,0x83e3); c.emit(0xc9,cue>>8); c.branch(0x90,f'not_visible{plane}')
        if cue & 255:
            c.branch(0xd0,f'visible{plane}')
            a(0xad,0x83e2); c.emit(0xc9,cue&255); c.branch(0x90,f'not_visible{plane}')
            c.label(f'visible{plane}')
        c.emit(0xa9,(10 if plane<2 else 11 if plane<4 else 9));a(0x0d,0x83e8);c.jump(0x8d,f'write{plane}_hi')
        if plane<4:
            c.jump(0xae,'vertical_index');a(0xbc,META+plane*64)
        else:a(0xac,META+256)
        c.emit(0xa2,0)
        c.label(f'copy{plane}');c.jump(0x20,'read');c.emit(0xc0,128);c.branch(0xb0,f'skip{plane}')
        c.label(f'write{plane}');a(0x99,0xa00+(plane%2)*128 if plane<4 else 0x980)
        c.label(f'skip{plane}');c.emit(0xc8,0xe8,0xe0,64 if plane==4 else 32);c.branch(0xd0,f'copy{plane}')
        c.label(f'not_visible{plane}')
    c.emit(0x60)
    assert c.origin+len(c.data)<=PUBLISH
    c.emit(*bytes(PUBLISH-c.origin-len(c.data)))
    c.label('wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'wait');c.emit(0xc9,128);c.branch(0xb0,'wait')
    c.jump(0xad,'back_bit');c.emit(0x09,8);a(0x8d,0xd407)
    # PMG fade follows the same per-card fade envelope as the plasma.
    a(0xad,0x83e0);c.branch(0xd0,'title_fade')
    a(0xad,0x83fd);c.emit(0x4a,0xc9,7);c.branch(0x90,'luminance');c.emit(0xa9,7);c.jump(0x4c,'luminance')
    c.label('title_fade');a(0xad,0x83fd);c.emit(0x4a,0xc9,39);c.branch(0x90,'full_light')
    c.emit(0x49,255,0x18,0x69,47);c.jump(0x4c,'luminance')
    c.label('full_light');c.emit(0xa9,7)
    c.label('luminance');c.emit(0x0a,0x29,14);a(0x8d,0x83e9)
    # Rainbow changes twice as fast as the shape sequence, including in
    # the burst/fragment stage rather than assigning each rocket one colour.
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x29,15,0xaa)
    for i in range(4):
        c.jump(0xbd,f'hues{i}');c.emit(0x29,0xf0);a(0x0d,0x83e9);a(0x8d,0xd012+i)
    c.jump(0xae,'frame_index')
    for i in range(4):
        c.emit(0xa9,LEFTS[i]+48);a(0x8d,0xd000+i)
        c.jump(0xbd,f'missile_x{i}');a(0x8d,0xd004+i)
        c.emit(0xa9,3);a(0x8d,0xd008+i)
    for addr,val in ((0xd00c,0x55),(0xd01b,0xc1),(0xd400,0x2e)):
        c.emit(0xa9,val);a(0x8d,addr)
    a(0xad,0x83e9);c.branch(0xf0,'hidden');c.emit(0xa9,3)
    c.label('hidden');a(0x8d,0xd01d);c.emit(0x60)
    c.label('read');c.emit(0xbd,0,0);c.emit(0x60)
    c.label('back_bit');c.emit(0)
    c.label('vertical_index');c.emit(0)
    c.label('frame_index');c.emit(0)
    c.labels['read_lo']=c.labels['read']+1;c.labels['read_hi']=c.labels['read']+2
    for i in range(5):
        c.labels[f'clear{i}_hi']=c.labels[f'clear{i}']+2
        c.labels[f'write{i}_hi']=c.labels[f'write{i}']+2
    c.label('source_lo');c.emit(*((DATA+i*32)&255 for i in range(16)))
    c.label('source_hi');c.emit(*((DATA+i*32)>>8 for i in range(16)))
    c.label('missile_source_lo');c.emit(*((DATA+2048+i*64)&255 for i in range(16)))
    c.label('missile_source_hi');c.emit(*((DATA+2048+i*64)>>8 for i in range(16)))
    for i in range(4):
        c.label(f'hues{i}');c.emit(*(HUES[(phase+i*4)&15] for phase in range(16)))
    for i in range(4):
        c.label(f'missile_x{i}');c.emit(*((missile_position(phase,i)+48)&255 for phase in range(16)))
    return c.finish()
