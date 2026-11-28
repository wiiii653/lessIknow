"""Rainbow basketball and satellites in the tunnel and rotator."""
import math
from engine_effects import PMBASE_SHADOW
from build_sequence import Code
ENTRY=0x7800

SPIN_FRAMES=16
EYE_X, EYE_Y = 0x7550, 0x7650
ORBIT_TABLES = 0x76d0
EYE_POSITION = 0x77d0
DRIFT_X, DRIFT_Y = 0x5b00, 0x5b80
SCENE_POSITION = 0x5c00
SPIRAL_DRIFT_PERIOD = 16 * 4
ORGANIC_DRIFT_PERIOD = 12 * 4
DRIFT_PADDING = 2 * 3  # Three PAL subphases at up to double speed.


def motion_tables():
    """Sample each centre path and satellite orbit once per PAL frame."""
    spiral = tunnel_offsets(SPIRAL_DRIFT_PERIOD)
    organic = tunnel_offsets(ORGANIC_DRIFT_PERIOD)
    # The organic key indices start at 64. Pad both ends so signed
    # subphases wrap through the same loop without a modulo operation.
    drift = spiral + organic[-DRIFT_PADDING:] + organic + organic[:DRIFT_PADDING]
    assert DRIFT_X + len(drift) <= DRIFT_Y
    assert DRIFT_Y + len(drift) <= SCENE_POSITION
    tables = [
        (EYE_X, bytes(round(40*math.sin(math.tau*i/256)) & 255 for i in range(256))),
        (EYE_Y, bytes(round(8*math.sin(math.tau*i/128)) & 255 for i in range(128))),
        (DRIFT_X, bytes(x & 255 for x, _ in drift)),
        (DRIFT_Y, bytes(y & 255 for _, y in drift)),
    ]
    satellites = bytearray()
    for rx, ry, phase in ((25, 14, 0), (40, 23, 16)):
        satellites.extend(124+round(rx*math.cos((i+phase)*math.tau/64)) for i in range(64))
        satellites.extend(55+round(ry*math.sin((i+phase)*math.tau/64)) for i in range(64))
    tables.append((ORBIT_TABLES, bytes(satellites)))

    # Convert the translated tick to an eight-bit frame index.
    c = Code(EYE_POSITION)
    c.emit(0xad,0xd3,0x0d,0x8d,0xe8,0x83,0xad,0xd4,0x0d,
           0x4a,0x6e,0xe8,0x83,0x4a,0x6e,0xe8,0x83,0xae,0xe8,0x83)
    c.emit(0x4c,0,0)  # Patched to the shared sweep lookup below.
    eye_jump = len(c.data)-2
    assert c.origin+len(c.data) <= ENTRY

    d = Code(SCENE_POSITION)
    # Start from the director's current four-frame key and add the
    # subphase in the same direction and at the same speed as the art.
    d.emit(0xad,0xe2,0x83,0x4a,0x4a,0x29,3,0xaa)
    d.emit(0xad,0xda,0x0d,0x29,0x40,0xf0,0x02,0x8a,0x0a)
    d.branch(0xd0,'rate_ready')
    d.emit(0x8a)
    d.label('rate_ready')
    d.emit(0x2c,0xda,0x0d)
    d.branch(0x10,'direction_ready')
    d.emit(0x49,255,0x18,0x69,1)
    d.label('direction_ready')
    d.emit(0x8d,0xe8,0x83,0xad,0xed,0x83,0x29,31,0x0a,0x0a)
    d.emit(0x18,0x6d,0xe8,0x83,0xaa)
    d.emit(0xad,0xed,0x83,0x29,32)
    d.branch(0xd0,'drift')
    d.emit(0xad,0xd4,0x0d,0x29,2)
    d.branch(0xf0,'sweep')
    d.emit(0x8a,0x18,0x69,128,0xaa)
    d.label('sweep')
    d.emit(0xbd,EYE_X&255,EYE_X>>8,0x8d,0xe8,0x83,0x8a,0x29,127,0xaa)
    d.emit(0xbd,EYE_Y&255,EYE_Y>>8,0x8d,0xe9,0x83,0x60)
    d.label('drift')
    d.emit(0xad,0xed,0x83,0x29,16)
    d.branch(0xf0,'spiral_drift')
    d.emit(0x8a,0x18,0x69,DRIFT_PADDING)
    d.branch(0xd0,'drift_lookup')
    d.label('spiral_drift')
    d.emit(0x8a,0x29,SPIRAL_DRIFT_PERIOD-1)
    d.label('drift_lookup')
    d.emit(0xaa,0xbd,DRIFT_X&255,DRIFT_X>>8,0x8d,0xe8,0x83)
    d.emit(0xbd,DRIFT_Y&255,DRIFT_Y>>8,0x8d,0xe9,0x83,0x60)
    c.data[eye_jump:eye_jump+2] = d.labels['sweep'].to_bytes(2, 'little')
    tables.append((EYE_POSITION, bytes(c.finish())))
    tables.append((SCENE_POSITION, bytes(d.finish())))
    return tables


def masks():
    """Opaque sphere: tilted great-circle seams, rotating panels and glint.

    Each physical half has a body ink and a bright panel/seam ink. Geometry
    never cuts holes: the complementary planes share one fixed silhouette.
    """
    frames=[]
    for phase in range(SPIN_FRAMES):
        theta=phase*math.tau/SPIN_FRAMES
        planes=[bytearray(32) for _ in range(4)]
        for y in range(32):
            v=(y-15.5)/15.75
            for x in range(16):
                u=(x-7.5)/7.75;r2=u*u+v*v
                if r2>1:continue
                z=math.sqrt(1-r2)
                # Tilt the spinning sphere so the equator is a visible arc.
                sy=v*math.cos(.38)-z*math.sin(.38)
                sz=v*math.sin(.38)+z*math.cos(.38)
                sx=u*math.cos(theta)-sz*math.sin(theta)
                depth=u*math.sin(theta)+sz*math.cos(theta)
                diagonal=(sx+sy)*.707
                panel=(sx>0) ^ (sy>0) ^ (depth>0) ^ (diagonal>0)
                seam=min(abs(sx),abs(sy),abs(depth),abs(diagonal))<.065
                rim=r2>.80
                glint=((u+.32)/.20)**2+((v+.40)/.12)**2<1
                logo=depth>.65 and ((sx-.22)/.24)**2+((sy+.12)/.22)**2<1
                bright=rim or glint or (panel ^ seam ^ logo)
                plane=x//8+(2 if bright else 0)
                planes[plane][y]|=0x80>>(x%8)
        frames.append(planes)
    return frames


def silhouette():
    frame=masks()[0]
    return [bytes(a|b for a,b in zip(frame[i],frame[i+2])) for i in range(2)]


def rotator_offsets():
    return [round(40*math.sin(math.tau*i/64)) for i in range(64)]

def rotator_vertical_offsets():
    # The trajectory is invisible: only the ball traces the sideways figure 8.
    return [round(8*math.sin(2*math.tau*i/64)) for i in range(64)]

def tunnel_offsets(period):
    return [(round(5*math.sin(math.tau*i/period)),
             round(2*math.sin(2*math.tau*i/period))) for i in range(period)]

def helper():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # The director owns the PMG while it draws BUM/BAM over banana frames.
    a(0xad,0x0dd2);c.branch(0xf0,'ball_clock');c.emit(0x60)
    c.label('ball_clock')
    # Match the translated Act 5 clock; other scenes retain real music time.
    a(0x20,0x7480)
    # Eye frames occupy 60–63; give their ball a clock-driven figure eight.
    # Other tunnel frames keep their gentle centred drift.
    a(0xad,0x83ed);c.emit(0x29,0xfc,0xc9,60);c.branch(0xf0,'eye_path')
    a(0x20,SCENE_POSITION);c.jump(0x4c,'offset_ready')
    c.label('eye_path');a(0x20,EYE_POSITION);c.jump(0x4c,'offset_ready')
    c.label('offset_ready')
    # Trevor borrows this exact renderer with a translated centre. HPOS
    # registers are write-only: apply the offset before publishing, never
    # read them back (GTIA reads return collision latches instead).
    a(0xad,0x83ed);c.emit(0xc9,96);c.branch(0xd0,'wait')
    a(0xad,0x83ea);a(0x8d,0x83e8)
    c.emit(0xa9,0);a(0x8d,0x83e9)
    c.label('wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'wait')
    # Admit only the start of bottom blanking (lines 248–255). If late,
    # retain the previous ball and wait for the NEXT safe window. The full
    # clear/blit must finish before the first satellite on the next frame.
    c.emit(0xc9,128);c.branch(0xb0,'wait')
    c.emit(0xa9,0,0xa2,127)
    c.label('clear')
    for base in (0x980,0xa00,0xa80,0xb00,0xb80):a(0x9d,base)
    c.emit(0xca);c.branch(0x10,'clear')
    # Sixteen rotations, 512 bytes per half. Select the upper/lower page
    # without changing the bank; complement against the opaque outline.
    a(0xad,0x0dd3);c.emit(0x29,0x80,0x0a,0xa9,0)
    c.emit(0x69,0)
    c.jump(0x6d,'spin_page');c.jump(0x8d,'panel_left_hi')
    c.emit(0x18,0x69,2);c.jump(0x8d,'panel_right_hi')
    # Fill in the three PAL frames between each pair of stored rotations.
    # Take whole rows from the next mask in a staggered pattern so both
    # inks always agree and the silhouette remains opaque.
    a(0xad,0x0dd3);c.emit(0x4a,0x4a,0x29,3);c.jump(0x8d,'spin_mix')
    c.jump(0xad,'panel_left_hi')
    a(0xae,0x0dd3);c.emit(0xe0,0xf0);c.branch(0x90,'next_page')
    c.emit(0x38,0xe9,2)  # Phase 15 wraps to phase 0 after the index adds 32.
    c.label('next_page');c.jump(0x8d,'next_panel0_hi')
    c.emit(0x18,0x69,2);c.jump(0x8d,'next_panel1_hi')
    a(0xad,0x0dd3);c.emit(0x29,0x70,0x0a,0xaa)
    c.emit(0xa9,40,0x18);a(0x6d,0x83e9);c.emit(0xa8)
    c.label('blit');c.jump(0x8e,'spin_index')
    for half in range(2):
        c.emit(0x8a,0x29,3);c.jump(0xcd,'spin_mix')
        c.branch(0xb0,f'key_panel{half}')
        c.label(f'next_panel{half}');a(0xbd,0x7c20+half*512)
        c.jump(0x4c,f'paint_panel{half}')
        c.label(f'key_panel{half}')
        c.label('panel_left' if half==0 else 'panel_right');c.jump(0xbd,f'plane{half}')
        c.label(f'paint_panel{half}')
        a(0x99,0xa00+half*128)
        c.emit(0x49,255,0x48,0x8a,0x29,31,0xaa,0x68)
        c.jump(0x3d,f'outline{half}')
        a(0x99,0xb00+half*128)
        c.jump(0xae,'spin_index')
    c.emit(0xe8,0xc8,0x8a,0x29,31);c.branch(0xd0,'blit')
    # Two symmetric stars: each uses a pair of adjacent missiles.
    a(0xad,0x0dd3);c.emit(0x4a,0x4a,0x29,63,0xaa)
    for i in range(4):
        a(0xbd,ORBIT_TABLES+(i//2)*128);c.emit(0x18);a(0x6d,0x83e8)
        if i%2:c.emit(0x18,0x69,4)
        a(0x8d,0xd004+i)
        a(0xbd,ORBIT_TABLES+(i//2)*128+64);c.emit(0x18);a(0x6d,0x83e9);c.emit(0xa8)
        tips=(1,1,3,1,1) if i%2==0 else (2,2,3,2,2)
        for dy,bits in enumerate(tips):
            a(0xb9,0x980+dy);c.emit(0x09,bits<<(i*2));a(0x99,0x980+dy)
    for i in range(4):
        c.emit(0xa9,112+(i%2)*16,0x18);a(0x6d,0x83e8);a(0x8d,0xd000+i)
        c.emit(0xa9,1);a(0x8d,0xd008+i)
    # Four saturated body/panel inks with a bright rim and white-hot satellites.
    for addr,val in ((0xd019,0x0e),(PMBASE_SHADOW,8),(0xd407,8),(0xd01b,0x11),(0xd01d,3),(0xd400,0x2e),(0xd00c,0x55)):
        c.emit(0xa9,val);a(0x8d,addr)
    a(0xad,0x0dd3);c.emit(0x4a,0x4a,0x4a,0x4a,0x29,7,0xaa)
    for label,addresses in (('rainbow_p0',(0xd012,)),('rainbow_p1',(0xd013,)),('rainbow_p2',(0xd014,)),('rainbow_p3',(0xd015,)),('rainbow_sparks',(0xd019,))):
        c.jump(0xbd,label)
        for address in addresses:a(0x8d,address)
    c.emit(0x60)
    hues=(0x40,0x60,0x80,0xa0,0xc0,0xe0,0x20,0x30)
    # Neighboring players use related hues so their fixed hardware boundary
    # reads as shading; the stronger division remains on the curved seam.
    for label,offset,luma in (('rainbow_p0',0,8),('rainbow_p1',1,10),('rainbow_p2',4,14),('rainbow_p3',5,12),('rainbow_sparks',2,14)):
        c.label(label);c.emit(*(hues[(i+offset)%8]|luma for i in range(8)))
    # Align the two 512-byte panel tables to pages; outline lookup uses
    # a compact row index, independent of phase. No new expansion bank.
    c.label('spin_index');c.emit(0)
    c.label('spin_mix');c.emit(0)
    for half in range(2):
        c.labels[('panel_left' if half==0 else 'panel_right')+'_hi']=c.labels['panel_left' if half==0 else 'panel_right']+2
        c.labels[f'next_panel{half}_hi']=c.labels[f'next_panel{half}']+2
    c.label('spin_page');c.emit(0)  # Patched to the first panel table page.
    for half,outline in enumerate(silhouette()):
        c.label(f'outline{half}');c.emit(*outline)
    # Place masks at a fixed page boundary, leaving the small preceding gap
    # for code/tables rather than increasing the 2 KiB reservation.
    assert c.origin+len(c.data)<=0x7c00, len(c.data)
    c.emit(*bytes(0x7c00-c.origin-len(c.data)))
    c.data[c.labels['spin_page']-c.origin]=0x7c
    frames=masks()
    for half in range(2):
        c.label(f'plane{half}');c.emit(*(v for frame in frames for v in frame[half]))
    code=c.finish();assert len(code)<=2048,len(code)
    return code


def rebound_helper():
    """Translate the complete existing ball/orbits towards the nearest edge.

    Caller supplies hand (2 right, 4 left) and age since leaving the impact.
    The original PMG routine owns mask/colour/size updates and safe blanking.
    """
    c=Code(0x4000)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    a(0xad,0x83ed);c.emit(0x48,0xa9,96);a(0x8d,0x83ed)
    a(0xad,0x83eb);c.emit(0x18,0x69,32);a(0x8d,0x83ea)
    a(0xad,0x83e7);c.emit(0xc9,4);c.branch(0xd0,'right')
    a(0xad,0x83ea);c.emit(0x49,255,0x18,0x69,1);a(0x8d,0x83ea)
    c.label('right');a(0x20,ENTRY)
    c.emit(0x68);a(0x8d,0x83ed);c.emit(0x60)
    return c.finish()
