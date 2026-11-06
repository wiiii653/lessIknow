"""Rainbow basketball and satellites in the tunnel and rotator."""
import math
from build_sequence import Code
ENTRY=0x7800

def masks():
    frames=[]
    for phase in range(8):
        theta=phase*math.tau/8
        planes=[bytearray(32) for _ in range(4)]
        # Breathing silhouette gives the rotating ball a depth cue.
        radius=0.78+0.16*math.cos(theta)
        for y in range(32):
            v=(y-15.5)/16
            for x in range(16):
                u=(x-7.5)/8
                if u*u+v*v>radius*radius:continue
                # The curved basketball seam is also the boundary between
                # the two colored panels; the cross seam exchanges colors.
                divider=0.42*math.sin(theta+v*1.5)
                panel=u>=divider
                if abs(v-0.34*math.sin(theta)*u)<0.055:
                    panel=not panel
                plane=x//8+(2 if panel else 0)
                planes[plane][y] |= 1<<(7-x%8)
        frames.append(planes)
    return frames

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
    # Tunnel: gentle two-axis motion; rotator: full left/right sweep.
    a(0xad,0x83ed);c.emit(0x29,32);c.branch(0xd0,'centered')
    a(0xad,0x83ed);c.emit(0x29,31);a(0x8d,0x83e8)
    a(0xad,0x83e3);c.emit(0x29,2,0x0a,0x0a,0x0a,0x0a);a(0x0d,0x83e8);c.emit(0xaa)
    c.jump(0xbd,'sweep');a(0x8d,0x83e8)
    c.jump(0xbd,'sweep_y');a(0x8d,0x83e9);c.jump(0x4c,'offset_ready')
    c.label('centered');a(0xad,0x83ed);c.emit(0x29,31,0xaa)
    c.jump(0xbd,'tunnel_x');a(0x8d,0x83e8);c.jump(0xbd,'tunnel_y');a(0x8d,0x83e9)
    c.label('offset_ready')
    c.label('wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'wait')
    c.emit(0xa9,0,0xa2,0)
    c.label('clear')
    for base in (0x980,0xa00,0xb00):a(0x9d,base)
    c.emit(0xe8);c.branch(0xd0,'clear')
    # 8 rotations; split planes into 256-byte tables, indexed by phase*32.
    a(0xad,0x83e2);c.emit(0x29,0xe0,0xaa,0xa9,40,0x18);a(0x6d,0x83e9);c.emit(0xa8)
    c.label('blit')
    for plane in range(4):c.jump(0xbd,f'plane{plane}');a(0x99,0xa00+plane*128)
    c.emit(0xe8,0xc8,0x8a,0x29,31);c.branch(0xd0,'blit')
    # Four sparks circle the ball with short radial tails.
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x29,31,0xaa)
    for i in range(4):
        c.jump(0xbd,f'orbit_x{i}');c.emit(0x18);a(0x6d,0x83e8);a(0x8d,0xd004+i)
        c.jump(0xbd,f'orbit_y{i}');c.emit(0x18);a(0x6d,0x83e9);c.emit(0xa8)
        for dy in (0,1,2,4,6):
            a(0xb9,0x980+dy);c.emit(0x09,3<<(i*2));a(0x99,0x980+dy)
    for i in range(4):
        c.emit(0xa9,112+(i%2)*16,0x18);a(0x6d,0x83e8);a(0x8d,0xd000+i)
        c.emit(0xa9,1);a(0x8d,0xd008+i)
    # Two rainbow panels, larger fifth-player satellites.
    for addr,val in ((0xd019,0x0e),(0xd407,8),(0xd01b,0x11),(0xd01d,3),(0xd400,0x2e),(0xd00c,0xff)):
        c.emit(0xa9,val);a(0x8d,addr)
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x4a,0xaa)
    for label,addresses in (('rainbow_left',(0xd012,0xd013)),('rainbow_right',(0xd014,0xd015)),('rainbow_sparks',(0xd019,))):
        c.jump(0xbd,label)
        for address in addresses:a(0x8d,address)
    c.emit(0x60)
    hues=(0x40,0x60,0x80,0xa0,0xc0,0xe0,0x20,0x30)
    for label,offset,luma in (('rainbow_left',0,14),('rainbow_right',3,12),('rainbow_sparks',5,14)):
        c.label(label);c.emit(*(hues[(i+offset)%8]|luma for i in range(8)))
    c.label('sweep');c.emit(*(v&255 for v in rotator_offsets()))
    c.label('sweep_y');c.emit(*(v&255 for v in rotator_vertical_offsets()))
    c.label('tunnel_x');c.emit(*(x&255 for x,y in tunnel_offsets()))
    c.label('tunnel_y');c.emit(*(y&255 for x,y in tunnel_offsets()))
    frames=masks()
    for plane in range(4):
        c.label(f'plane{plane}');c.emit(*(value for f in frames for value in f[plane]))
    for i in range(4):
        c.label(f'orbit_x{i}');c.emit(*(128+round((23+3*math.sin(j*math.tau/32))*math.cos((j+i*8)*math.tau/32)) for j in range(32)))
        c.label(f'orbit_y{i}');c.emit(*(55+round(24*math.sin((j+i*8)*math.tau/32)) for j in range(32)))
    code=c.finish();assert len(code)<=2048,len(code)
    return code
