"""Rainbow basketball and satellites in the tunnel and rotator."""
import math
from build_sequence import Code
ENTRY=0x7800

SPIN_FRAMES=16


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

def tunnel_offsets():
    return [(round(5*math.sin(math.tau*i/32)),round(2*math.sin(2*math.tau*i/32))) for i in range(32)]

def helper():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # Match the translated Act 5 clock; other scenes retain real music time.
    a(0x20,0x7480)
    # Tunnel: gentle two-axis motion; rotator: full left/right sweep.
    a(0xad,0x83ed);c.emit(0x29,32);c.branch(0xd0,'centered')
    a(0xad,0x83ed);c.emit(0x29,31);a(0x8d,0x83e8)
    a(0xad,0x0dd4);c.emit(0x29,2,0x0a,0x0a,0x0a,0x0a);a(0x0d,0x83e8);c.emit(0xaa)
    c.jump(0xbd,'sweep');a(0x8d,0x83e8)
    c.jump(0xbd,'sweep_y');a(0x8d,0x83e9);c.jump(0x4c,'offset_ready')
    c.label('centered');a(0xad,0x83ed);c.emit(0x29,31,0xaa)
    c.jump(0xbd,'tunnel_x');a(0x8d,0x83e8);c.jump(0xbd,'tunnel_y');a(0x8d,0x83e9)
    c.label('offset_ready')
    # Trevor borrows this exact renderer with a translated centre. HPOS
    # registers are write-only: apply the offset before publishing, never
    # read them back (GTIA reads return collision latches instead).
    a(0xad,0x83ed);c.emit(0xc9,96);c.branch(0xd0,'wait')
    a(0xad,0x83ea);a(0x8d,0x83e8)
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
    a(0xad,0x0dd3);c.emit(0x29,0x70,0x0a,0xaa)
    c.emit(0xa9,40,0x18);a(0x6d,0x83e9);c.emit(0xa8)
    c.label('blit');c.jump(0x8e,'spin_index')
    for half in range(2):
        c.label('panel_left' if half==0 else 'panel_right');c.jump(0xbd,f'plane{half}')
        a(0x99,0xa00+half*128)
        c.emit(0x49,255,0x48,0x8a,0x29,31,0xaa,0x68)
        c.jump(0x3d,f'outline{half}')
        a(0x99,0xb00+half*128)
        c.jump(0xae,'spin_index')
    c.emit(0xe8,0xc8,0x8a,0x29,31);c.branch(0xd0,'blit')
    # Two symmetric stars: each uses a pair of adjacent missiles.
    a(0xad,0x0dd3);c.emit(0x4a,0x4a,0x4a,0x29,31,0xaa)
    for i in range(4):
        c.jump(0xbd,f'orbit_x{i//2}');c.emit(0x18);a(0x6d,0x83e8)
        if i%2:c.emit(0x18,0x69,4)
        a(0x8d,0xd004+i)
        c.jump(0xbd,f'orbit_y{i//2}');c.emit(0x18);a(0x6d,0x83e9);c.emit(0xa8)
        tips=(1,1,3,1,1) if i%2==0 else (2,2,3,2,2)
        for dy,bits in enumerate(tips):
            a(0xb9,0x980+dy);c.emit(0x09,bits<<(i*2));a(0x99,0x980+dy)
    for i in range(4):
        c.emit(0xa9,112+(i%2)*16,0x18);a(0x6d,0x83e8);a(0x8d,0xd000+i)
        c.emit(0xa9,1);a(0x8d,0xd008+i)
    # Four saturated body/panel inks with a bright rim and white-hot satellites.
    for addr,val in ((0xd019,0x0e),(0xd407,8),(0xd01b,0x11),(0xd01d,3),(0xd400,0x2e),(0xd00c,0x55)):
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
    c.label('sweep');c.emit(*(v&255 for v in rotator_offsets()))
    c.label('sweep_y');c.emit(*(v&255 for v in rotator_vertical_offsets()))
    c.label('tunnel_x');c.emit(*(x&255 for x,y in tunnel_offsets()))
    c.label('tunnel_y');c.emit(*(y&255 for x,y in tunnel_offsets()))
    # Align the two 512-byte panel tables to pages; outline lookup uses
    # a compact row index, independent of phase. No new expansion bank.
    c.label('spin_index');c.emit(0)
    for half in range(2):
        c.labels[('panel_left' if half==0 else 'panel_right')+'_hi']=c.labels['panel_left' if half==0 else 'panel_right']+2
    c.label('spin_page');c.emit(0)  # Patched to the first panel table page.
    for half,outline in enumerate(silhouette()):
        c.label(f'outline{half}');c.emit(*outline)
    for i in range(2):
        rx,ry=((25,14) if i==0 else (40,23))
        phase=0 if i==0 else 8
        c.label(f'orbit_x{i}');c.emit(*(124+round(rx*math.cos((j+phase)*math.tau/32)) for j in range(32)))
        c.label(f'orbit_y{i}');c.emit(*(55+round(ry*math.sin((j+phase)*math.tau/32)) for j in range(32)))
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
