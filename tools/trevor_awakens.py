"""Act 4: dark gym reveal, then PMG zoom, mirror poses and orbital accents."""
import math
from pathlib import Path
from build_sequence import Code
START,HIT,END=23936,26928,32912
ENTRY=0x6000
BANK_VALUE=0x24b5
COLORS=((0,0,0),(255,50,160),(116,0,144),(255,190,206))

def indices(path):
    rgb=Path(path).read_bytes()
    return bytes(min(range(4),key=lambda j:sum((rgb[i+k]-COLORS[j][k])**2 for k in range(3))) for i in range(0,len(rgb),3))

def backgrounds():
    return [indices(f'build/trevor-panel-{i}.rgb') for i in range(2)]

def pmg_frames():
    # Native PMG silhouette: enlarge face/shoulders so features survive 16 columns.
    rows=("     VVVVVV     ","    VVVVVVVV    ","   VVPPPPPPVV   ",
          "   VPF.FF.FPV   ","   VPFFFFFFPV   ","   VPFF..FFPV   ",
          "   VVPFFFFPVV   ","  VVVVPPPPVVVV  "," VVVVVVVVVVVVVV ",
          "VVVVVPPPPPPVVVVV","VVVVPPPPPPPPVVVV","VVVPPPPPPPPPPVVV",
          "VVVVPFFPPFFPVVVV","VVV VFFFFFFV VVV","VVV VFFFFFFV VVV",
          "VVV VVFFFFVV VVV","VVV VVVVVVVV VVV","PPP VVVVVVVV PPP",
          "PPP VVVVVVVV PPP","    VVV  VVV    ","    VVV  VVV    ",
          "    VVV  VVV    ","   PPPP  PPPP   ","   PPPP  PPPP   ")
    assert all(len(row)==16 for row in rows)
    colors={' ':0,'.':0,'V':2,'P':1,'F':3}
    base=bytes(colors[c] for row in rows for c in row)
    raised=bytearray(base)
    for y in range(9,19):
        for x in range(13,16):raised[y*16+x]=0
    for y in range(8,16):
        for x in range(13,16):raised[y*16+x]=1 if y<11 else 2
    poses=[base,bytes(raised)]
    poses += [bytes(p[y*16+15-x] for y in range(24) for x in range(16)) for p in poses[:]]
    result=[]
    for scale in (1,2,4):
        for pose in poses:
            planes=bytearray(512)
            for y in range(24):
                for x in range(16):
                    color=pose[y*16+x]
                    if not color:continue
                    if 4<=x<12 and color in (1,3):
                        plane=2 if color==3 else 3;bit=7-(x-4)
                    else:plane=x//8;bit=7-x%8
                    for dy in range(scale):planes[plane*128+y*scale+dy] |= 1<<bit
            result.append(bytes(planes))
    return result

def helper():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    c.emit(0xa9,16);a(0x8d,0x83e0)
    # Classify the quiet/loud half and set a unique bitmap cache key.
    a(0xad,0x83e3);c.emit(0xc9,HIT>>8);c.branch(0x90,'quiet');c.branch(0xd0,'loud')
    a(0xad,0x83e2);c.emit(0xc9,HIT&255);c.branch(0xb0,'loud')
    c.label('quiet');c.emit(0xa9,0);c.jump(0x4c,'background')
    c.label('loud');c.emit(0xa9,1)
    c.label('background');a(0x8d,0x83ec);c.emit(0xaa,0x09,0x60);a(0xcd,0x83fa);c.branch(0xd0,'changed');c.jump(0x4c,'wait')
    c.label('changed');a(0x8d,0x83fa)
    c.emit(0xa9,0);c.jump(0x8d,'read_lo');c.jump(0x8d,'write_lo')
    c.emit(0x8a,0x0a,0x0a,0x18,0x69,0x40);c.emit(0x18,0x69,0) # 0 or 1 becomes $40/$44, corrected by lookup below.
    c.jump(0xbd,'bg_hi');c.jump(0x8d,'read_hi')
    a(0xad,0x83e6);c.emit(0x29,4,0x0a,0x0a,0x0a,0x49,0xb0);a(0x8d,0x83fe);c.jump(0x8d,'write_hi')
    c.emit(0xa2,10,0xa0,0)
    c.label('copy');c.label('read');c.emit(0xb9,0,0);c.label('write');c.emit(0x99,0,0,0xc8);c.branch(0xd0,'copy')
    c.jump(0xee,'read_hi');c.jump(0xee,'write_hi');c.emit(0xca);c.branch(0xd0,'copy')
    a(0xad,0x83e6);c.jump(0x8d,'dl1_hi');c.jump(0x8d,'dl2_hi')
    c.emit(0xa9,3);c.jump(0x8d,'dl1_lo');c.emit(0xa9,4);c.jump(0x8d,'dl2_lo');c.emit(0xa0,0)
    c.label('rows');c.jump(0xb9,'row_lo');c.label('dl1');c.emit(0x8d,0,0)
    c.jump(0xb9,'row_hi');c.emit(0x18);a(0x6d,0x83fe);c.label('dl2');c.emit(0x8d,0,0)
    for label in ('dl1','dl2'):
        c.emit(0x18);c.jump(0xad,label+'_lo');c.emit(0x69,3);c.jump(0x8d,label+'_lo');c.branch(0x90,label+'ok');c.jump(0xee,label+'_hi');c.label(label+'ok')
    c.emit(0xc8,0xc0,192);c.branch(0xd0,'rows')
    c.label('swap');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'swap')
    c.emit(0xa9,0);a(0x8d,0xd402);a(0xad,0x83e6);a(0x8d,0xd403);c.emit(0x49,4);a(0x8d,0x83e6)
    c.emit(0xa9,255);a(0x8d,0x83f8);a(0x8d,0x83f9)
    c.label('wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'wait')
    # Elapsed quiet time in 256-tick units, also determines fade and scale.
    a(0xad,0x83e2);c.emit(0x38,0xe9,START&255);a(0xad,0x83e3);c.emit(0xe9,START>>8);a(0x8d,0x83ea)
    a(0xad,0x83ec);c.branch(0xd0,'active_motion')
    a(0xad,0x83ea);c.emit(0xc9,4,0xa9,0);c.branch(0x90,'quiet_stage')
    a(0xad,0x83ea);c.emit(0xc9,8,0xa9,1);c.branch(0x90,'quiet_stage');c.emit(0xa9,2)
    c.label('quiet_stage');a(0x8d,0x83ed)
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x4a,0x4a,0x4a,0x29,1);a(0x8d,0x83eb)
    a(0xad,0x83e3);c.emit(0x29,31,0xaa);c.jump(0xbd,'quiet_sine');c.jump(0x4c,'motion_ready')
    c.label('active_motion')
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x4a,0x4a,0x29,3,0xaa);c.jump(0xbd,'zoom');a(0x8d,0x83ed)
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x4a,0x29,3);a(0x8d,0x83eb)
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x29,31,0xaa);c.jump(0xbd,'sine')
    c.label('motion_ready');a(0x8d,0x83e8)
    a(0xae,0x83ed);c.jump(0xbd,'top');a(0x8d,0x83e9)
    c.jump(0xbd,'size');
    for addr in range(0xd008,0xd00c):a(0x8d,addr)
    c.jump(0xbd,'halfwidth');a(0x8d,0x83fd)
    a(0xad,0x83e8);c.emit(0x38);a(0xed,0x83fd);c.emit(0x18,0x69,48);a(0x8d,0xd000)
    c.emit(0x18);a(0x6d,0x83fd);a(0x8d,0xd001)
    a(0xad,0x83fd);c.emit(0x4a);a(0x8d,0x83fd)
    a(0xad,0x83e8);c.emit(0x38);a(0xed,0x83fd);c.emit(0x18,0x69,48);a(0x8d,0xd002);a(0x8d,0xd003)
    a(0xad,0x83ed);c.emit(0x0a,0x0a,0x18);a(0x6d,0x83eb);c.emit(0xaa)
    for i in range(4):
        c.jump(0xbd,f'pm_lo{i}');c.jump(0x8d,f'pm{i}_lo');c.jump(0xbd,f'pm_hi{i}');c.jump(0x8d,f'pm{i}_hi')
    c.emit(0xa9,0,0xa2,0)
    c.label('clear')
    for base in (0x980,0xa00,0xb00):a(0x9d,base)
    c.emit(0xe8);c.branch(0xd0,'clear')
    a(0xae,0x83ed);c.jump(0xbd,'height');a(0x8d,0x83fd);a(0xac,0x83e9);c.emit(0xa2,0)
    c.label('blit')
    for i in range(4):c.label(f'pm{i}');c.emit(0xbd,0,0);a(0x99,0xa00+i*128)
    c.emit(0xe8,0xc8);a(0xec,0x83fd);c.branch(0x90,'blit')
    # One rotating missile spark per quadrant, following a 32-step orbit.
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x29,31,0xaa)
    for i in range(4):
        c.jump(0xbd,f'orbit_x{i}');c.emit(0x18);a(0x6d,0x83e8);c.emit(0x18,0x69,48);a(0x8d,0xd004+i)
        c.jump(0xbd,f'orbit_y{i}');c.emit(0xa8,0xa9,3<<(2*i));a(0x19,0x980);a(0x99,0x980)
    # Quiet fade uses low luminance; loud colors cycle with the music clock.
    a(0xad,0x83ec);c.branch(0xd0,'bright')
    a(0xae,0x83ea);c.jump(0xbd,'fade');c.emit(0x09,0x60);a(0x8d,0xd012);a(0x8d,0xd013);a(0x8d,0xd017)
    c.emit(0x49,0x20);a(0x8d,0xd015);a(0x8d,0xd016)
    c.emit(0x49,0x60);a(0x8d,0xd014);a(0x8d,0xd018);c.jump(0x4c,'colors_done')
    c.label('bright');a(0xad,0x83e2);c.emit(0x29,0xf0,0x09,10);a(0x8d,0xd012);a(0x8d,0xd013);a(0x8d,0xd017)
    c.emit(0x18,0x69,0x40);a(0x8d,0xd015);a(0x8d,0xd016)
    c.emit(0xa9,0x2e);a(0x8d,0xd014);a(0x8d,0xd018)
    c.label('colors_done')
    for addr,val in ((0xd01a,0),(0xd407,8),(0xd01b,1),(0xd01d,3),(0xd400,0x2e),(0xd00c,0x55)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    for label in ('read','write','dl1','dl2',*(f'pm{i}' for i in range(4))):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    c.label('bg_hi');c.emit(0x40,0x4a) # Two 2560-byte backdrops.
    c.label('row_lo');c.emit(*((y//3*40)&255 for y in range(192)))
    c.label('row_hi');c.emit(*((y//3*40)>>8 for y in range(192)))
    c.label('zoom');c.emit(1,2,2,1)
    c.label('size');c.emit(0,1,3)
    c.label('height');c.emit(24,48,96)
    c.label('top');c.emit(44,32,8)
    c.label('halfwidth');c.emit(8,16,32)
    c.label('fade');c.emit(*(min(8,2+(i//3)*2) for i in range(16)))
    c.label('sine');c.emit(*(80+round(16*math.sin(i*math.pi/16)) for i in range(32)))
    c.label('quiet_sine');c.emit(*(80+round(4*math.sin(i*math.pi/16)) for i in range(32)))
    addresses=[0x5400+i*512 if i<6 else 0x6c00+(i-6)*512 for i in range(12)]
    for plane in range(4):
        c.label(f'pm_lo{plane}');c.emit(*((addr+plane*128)&255 for addr in addresses))
        c.label(f'pm_hi{plane}');c.emit(*((addr+plane*128)>>8 for addr in addresses))
    for i in range(4):
        angle=i*math.pi/2
        c.label(f'orbit_x{i}');c.emit(*(round(50*math.cos(j*math.pi/16+angle))&255 for j in range(32)))
        c.label(f'orbit_y{i}');c.emit(*((96+round(70*math.sin(j*math.pi/16+angle))+17)//2 for j in range(32)))
    code=c.finish();assert ENTRY+len(code)<=0x6c00,len(code)
    return code

def bank():
    out=bytearray(16384)
    for i,p in enumerate(backgrounds()):
        b=bytes(sum(p[y*160+x+k]<<(6-2*k) for k in range(4)) for y in range(64) for x in range(0,160,4))
        out[i*2560:(i+1)*2560]=b
    for i,data in enumerate(pmg_frames()):
        address=0x5400+i*512 if i<6 else 0x6c00+(i-6)*512
        out[address-0x4000:address-0x4000+512]=data
    code=helper();out[ENTRY-0x4000:ENTRY-0x4000+len(code)]=code
    from tunnel_ball import helper as tunnel_helper
    tunnel=tunnel_helper();out[0x3800:0x3800+len(tunnel)]=tunnel
    return bytes(out)
