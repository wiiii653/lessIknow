"""Two original balls and their satellites, travelling around Trevor's impacts."""
import math
from build_sequence import Code
from rainbow_ball import spin_masks
from basketball_hero import satellite_orbits
from tunnel_ball import masks as large_masks
from trevor_polished import HITS, impact_anchor, IMPACT_HUES

ENTRY=0x6800
BANK_INDEX=19
# One distinct vector per visible flight, including horizontal and vertical entries.
IN_VECTORS=((-3,0),(3,0),(0,-1),(0,1),(-2,-1),(2,-1),(-2,1),(2,1),(-1,-1),(1,-1),(-1,1),(1,1),(-3,-1))
OUT_VECTORS=((3,1),(-3,1),(3,-1),(-3,-1),(2,1),(-2,1),(2,-1),(-2,-1),(1,1),(-1,1),(1,-1),(-1,-1),(0,1))
assert len(HITS)==len(IN_VECTORS)==len(OUT_VECTORS)


def helper():
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # Locate the last hit or next hit; preserve the full 80-tick BUM/BAM.
    c.emit(0xa2,0)
    c.label('scan');a(0xad,0x83e2);c.emit(0x38);c.jump(0xfd,'hit_lo');a(0x8d,0x83ea)
    a(0xad,0x83e3);c.jump(0xfd,'hit_hi');c.branch(0x90,'future');c.branch(0xd0,'next')
    a(0xad,0x83ea);c.emit(0xc9,80);c.branch(0x90,'next');c.emit(0xc9,136);c.branch(0xb0,'next')
    # A following incoming ball takes priority over the departing effect.
    c.emit(0xe0,len(HITS)-1);c.branch(0xb0,'outgoing_ready');c.emit(0xe8)
    c.jump(0xbd,'hit_lo');c.emit(0x38);a(0xed,0x83e2);c.jump(0x8d,'next_delta')
    c.jump(0xbd,'hit_hi');a(0xed,0x83e3);c.branch(0xd0,'no_overlap')
    c.jump(0xad,'next_delta');c.emit(0xc9,33);c.branch(0xb0,'no_overlap')
    c.jump(0x4c,'scan')
    c.label('no_overlap');c.emit(0xca)
    c.label('outgoing_ready');a(0xad,0x83ea)
    c.emit(0x38,0xe9,80,0x4a);a(0x8d,0x83ea);c.emit(0xa9,0);c.jump(0x8d,'incoming');c.jump(0x4c,'position')
    c.label('next');c.emit(0xe8,0xe0,len(HITS));c.branch(0xd0,'scan');c.jump(0x4c,'hide')
    c.label('future');c.jump(0xbd,'hit_lo');c.emit(0x38);a(0xed,0x83e2);a(0x8d,0x83ea)
    c.jump(0xbd,'hit_hi');a(0xed,0x83e3);c.branch(0xf0,'future_low');c.jump(0x4c,'hide')
    c.label('future_low');a(0xad,0x83ea);c.emit(0xc9,33);c.branch(0x90,'is_in');c.jump(0x4c,'hide')
    c.label('is_in');c.emit(0xa9,1);c.jump(0x8d,'incoming')
    c.label('position');c.jump(0x8e,'hit_index')
    # Shared displacement table gives distinct trajectories without runtime multiplication.
    for axis,workspace in (('x',0x83eb),('y',0x83ec)):
        c.jump(0xad,'incoming');c.branch(0xf0,f'{axis}_out')
        c.jump(0xbd,f'{axis}_in');c.jump(0x4c,f'{axis}_velocity')
        c.label(f'{axis}_out');c.jump(0xbd,f'{axis}_out_table')
        c.label(f'{axis}_velocity');c.emit(0x18);a(0x6d,0x83ea);c.emit(0xa8)
        c.jump(0xb9,'displacements');c.jump(0x8d,f'{axis}_delta')
        c.jump(0xbd,f'base_{axis}');c.emit(0x18);c.jump(0x6d,f'{axis}_delta');a(0x8d,workspace)
        # Clamp only the vertical address; hidden-offscreen horizontal positions
        # are allowed to wrap into the GTIA horizontal blank.
        if axis=='y':
            c.jump(0xad,f'{axis}_delta');c.branch(0x10,'y_positive')
            c.branch(0xb0,'y_range');c.emit(0xa9,0);a(0x8d,workspace);c.jump(0x4c,'y_range')
            c.label('y_positive');c.branch(0x90,'y_range');c.emit(0xa9,111);a(0x8d,workspace)
            c.label('y_range');a(0xad,workspace);c.emit(0xc9,112);c.branch(0x90,'y_done')
            c.emit(0xa9,111);a(0x8d,workspace);c.label('y_done')
    # Large incoming sphere is 32 rows high, centred on the same contact point.
    c.jump(0xad,'incoming');c.branch(0xf0,'fade_setup')
    a(0xad,0x83eb);c.emit(0x38,0xe9,8);a(0x8d,0x83eb)
    a(0xad,0x83ec);c.emit(0x38,0xe9,8);c.branch(0xb0,'large_y_positive');c.emit(0xa9,0)
    c.label('large_y_positive');c.emit(0xc9,97);c.branch(0x90,'large_y_done');c.emit(0xa9,96)
    c.label('large_y_done');a(0x8d,0x83ec)
    c.label('fade_setup')
    # Fade at the ends of the finite flight windows. This prevents balls and
    # satellites popping in/out at full brightness while still on screen.
    c.jump(0xad,'incoming');c.branch(0xf0,'fade_out')
    a(0xad,0x83ea);c.emit(0x38,0xe9,25);c.jump(0x4c,'fade_select')
    c.label('fade_out');a(0xad,0x83ea);c.emit(0x38,0xe9,20)
    c.label('fade_select');c.branch(0xb0,'fade_lookup');c.emit(0xa9,0)
    c.label('fade_lookup');c.emit(0xaa);c.jump(0xbd,'fade_masks');c.jump(0x8d,'fade_mask')
    c.label('buffer');a(0xad,0xd407);c.emit(0x29,0x80,0x49,0x80);a(0x8d,0x83e9)
    c.emit(0x09,9);c.jump(0x8d,'clear_m_hi')
    for plane in range(4):
        a(0xad,0x83e9);c.emit(0x09,10 if plane<2 else 11)
        c.jump(0x8d,f'clear{plane}_hi');c.jump(0x8d,f'put{plane}_hi')
    a(0xad,0x83e9);c.emit(0x09,9)
    for plane in range(4):
        for row in range(5):c.jump(0x8d,f'sat{plane}_{row}_read_hi');c.jump(0x8d,f'sat{plane}_{row}_write_hi')
    c.emit(0xa9,0,0xa2,127);c.label('clear');c.label('clear_m');a(0x9d,0x980)
    for plane in range(4):c.label(f'clear{plane}');a(0x9d,0xa00+plane*128)
    c.emit(0xca);c.branch(0x10,'clear')
    # Actual sphere masks: 16 large rotations and 8 small dunk rotations.
    c.jump(0xad,'incoming');c.branch(0xf0,'small_setup')
    a(0xad,0x83e2);c.emit(0x29,0x80,0x0a,0xa9,0,0x69,0)
    for plane in range(4):
        c.emit(0x18,0x69,0x73 if plane==0 else 2);c.jump(0x8d,f'read{plane}_hi')
    c.emit(0xa9,0)
    for plane in range(4):c.jump(0x8d,f'read{plane}_lo')
    a(0xad,0x83e2);c.emit(0x29,0x70,0x0a,0xaa);c.emit(0xa9,32);c.jump(0x8d,'rows_left');c.jump(0x4c,'blit_setup')
    c.label('small_setup')
    for plane in range(4):
        c.emit(0xa9,(0x7b00+plane*128)>>8);c.jump(0x8d,f'read{plane}_hi')
        c.emit(0xa9,(0x7b00+plane*128)&255);c.jump(0x8d,f'read{plane}_lo')
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x29,7,0x0a,0x0a,0x0a,0x0a,0xaa)
    c.emit(0xa9,16);c.jump(0x8d,'rows_left')
    c.label('blit_setup');a(0xac,0x83ec)
    c.label('blit')
    for plane in range(4):
        c.label(f'read{plane}');a(0xbd,0x7300+plane*512)
        c.label(f'put{plane}');a(0x99,0xa00+plane*128)
    c.emit(0xe8,0xc8);c.jump(0xce,'rows_left');c.branch(0xd0,'blit')
    # Four missiles: paired stars for the large ball, independent dunk orbits
    # for the small one. Compute all data in the inactive PMG before publishing.
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x29,31,0xaa)
    for plane in range(4):
        c.jump(0xad,'incoming');c.branch(0xf0,f'small_sat{plane}')
        a(0xbd,0x7e00+(plane//2)*64);c.emit(0x18);a(0x6d,0x83eb);c.emit(0x18,0x69,12+(4 if plane%2 else 0));c.jump(0x8d,f'mx{plane}')
        a(0xbd,0x7e00+(plane//2)*64+32);c.emit(0x18);a(0x6d,0x83ec);c.emit(0x18,0x69,15);c.jump(0x4c,f'sat_y{plane}')
        c.label(f'small_sat{plane}');a(0xbd,0x7d00+plane*64);c.emit(0x18);a(0x6d,0x83eb);c.emit(0x18,0x69,6);c.jump(0x8d,f'mx{plane}')
        a(0xbd,0x7d00+plane*64+32);c.emit(0x18);a(0x6d,0x83ec);c.emit(0x18,0x69,6)
        c.label(f'sat_y{plane}');c.emit(0xc9,123);c.branch(0x90,f'sat_visible{plane}');c.jump(0x4c,f'sat_done{plane}')
        c.label(f'sat_visible{plane}');c.emit(0xa8)
        for row in range(5):
            bits=((1,1,3,1,1) if plane%2==0 else (2,2,3,2,2))[row] << (2*plane)
            small_bits=(1,3,3,3,1)[row] << (2*plane)
            c.label(f'sat{plane}_{row}_read');a(0xb9,0x980+row)
            c.jump(0x8d,'sat_value');c.jump(0xad,'incoming');c.branch(0xf0,f'small_bits{plane}_{row}')
            c.jump(0xad,'sat_value');c.emit(0x09,bits);c.jump(0x4c,f'write_bits{plane}_{row}')
            c.label(f'small_bits{plane}_{row}');c.jump(0xad,'sat_value');c.emit(0x09,small_bits)
            c.label(f'write_bits{plane}_{row}');c.label(f'sat{plane}_{row}_write');a(0x99,0x980+row)
        c.label(f'sat_done{plane}')
    c.label('wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'wait');c.emit(0xc9,128);c.branch(0xb0,'wait')
    a(0xad,0x83e9);c.emit(0x09,8);a(0x8d,0xd407)
    for plane in range(4):
        if plane%2:
            c.jump(0xad,'incoming');c.branch(0xf0,f'player_x{plane}');a(0xad,0x83eb);c.emit(0x18,0x69,16);c.jump(0x4c,f'player_x_done{plane}')
            c.label(f'player_x{plane}')
        a(0xad,0x83eb)
        if plane%2:c.label(f'player_x_done{plane}')
        a(0x8d,0xd000+plane);c.jump(0xad,f'mx{plane}');a(0x8d,0xd004+plane)
        c.emit(0xa9,1);a(0x8d,0xd008+plane)
    # Vivid original palette conventions, with a bright shared missile colour.
    c.jump(0xad,'incoming');c.branch(0xf0,'small_colours')
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x29,7,0xaa)
    for plane in range(4):c.jump(0xbd,f'hues{plane}');c.jump(0x2d,'fade_mask');a(0x8d,0xd012+plane)
    c.jump(0xbd,'spark_hues');c.jump(0x2d,'fade_mask');a(0x8d,0xd019);c.emit(0xa9,0x11);a(0x8d,0xd01b)
    c.jump(0x4c,'colours_done')
    c.label('small_colours');a(0xad,0x83e2);c.emit(0x0a,0x0a,0x29,0xf0,0x09,6)
    for plane in range(4):
        c.emit(0x48);c.jump(0x2d,'fade_mask');a(0x8d,0xd012+plane);c.emit(0x68)
        if plane<3:c.emit(0x18,0x69,0x44 if plane==0 else 0x42)
    a(0xad,0x83ea);c.emit(0x0a,0x18,0x69,80,0x4a,0x4a,0x4a,0x29,15,0xaa)
    c.jump(0xbd,'impact_hues');c.emit(0x09,14);c.jump(0x2d,'fade_mask');a(0x8d,0xd019);c.emit(0xa9,1);a(0x8d,0xd01b)
    c.label('colours_done')
    for addr,val in ((0xd00c,0x55),(0xd01d,3),(0xd400,0x2e)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    c.label('hide');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'hide');c.emit(0xc9,128);c.branch(0xb0,'hide')
    c.emit(0xa9,0);a(0x8d,0xd01d);c.emit(0x60)
    for plane in range(4):
        for stem in ('clear','put'):c.labels[f'{stem}{plane}_hi']=c.labels[f'{stem}{plane}']+2
        for row in range(5):
            for stem in ('read','write'):c.labels[f'sat{plane}_{row}_{stem}_hi']=c.labels[f'sat{plane}_{row}_{stem}']+2
        c.labels[f'read{plane}_lo']=c.labels[f'read{plane}']+1;c.labels[f'read{plane}_hi']=c.labels[f'read{plane}']+2
    c.labels['clear_m_hi']=c.labels['clear_m']+2
    c.labels['displacements']=0x7f00
    for name,values in (('hit_lo',[v&255 for v in HITS]),('hit_hi',[v>>8 for v in HITS]),
        ('base_x',[160+impact_anchor(i)[0] for i in range(len(HITS))]),('base_y',[45+impact_anchor(i)[1] for i in range(len(HITS))]),
        ('x_in',[(x+3)*33 for x,y in IN_VECTORS]),('y_in',[(y+3)*33 for x,y in IN_VECTORS]),
        ('x_out_table',[(x+3)*33 for x,y in OUT_VECTORS]),('y_out_table',[(y+3)*33 for x,y in OUT_VECTORS])):
        c.label(name);c.emit(*values)
    hues=(0x40,0x60,0x80,0xa0,0xc0,0xe0,0x20,0x30)
    for plane,(offset,luma) in enumerate(((0,8),(1,10),(4,14),(5,12))):
        c.label(f'hues{plane}');c.emit(*(hues[(i+offset)%8]|luma for i in range(8)))
    c.label('spark_hues');c.emit(*(hues[(i+2)%8]|14 for i in range(8)))
    c.label('impact_hues');c.emit(*(IMPACT_HUES[(i+2)&15] for i in range(16)))
    c.label('fade_masks');c.emit(0xfe,0xfe,0xfc,0xfc,0xf8,0xf8,0xf0,0xf0)
    for name in ('incoming','rows_left','hit_index','x_delta','y_delta','sat_value','fade_mask','next_delta','mx0','mx1','mx2','mx3'):
        c.label(name);c.emit(0)
    data=bytes(c.finish());assert ENTRY+len(data)<=0x7000,len(data)
    return data


def install(bank):
    out=bytearray(bank);code=helper();assert not any(out[0x2800:0x2800+len(code)])
    out[0x2800:0x2800+len(code)]=code
    large=large_masks();small=spin_masks()
    blobs=[]
    blobs.append((0x7300,bytes(v for p in range(4) for f in large for v in f[p])))
    blobs.append((0x7b00,bytes(v for p in range(4) for f in small for v in f[p])))
    paths=satellite_orbits()
    blobs.append((0x7d00,bytes(point[axis]&255 for path in paths for axis in (0,1) for point in path)))
    big=[]
    for radius,phase in (((25,14),0),((40,23),8)):
        for axis in (0,1):
            big.extend(round((radius[0]*math.cos((step+phase)*math.tau/32)) if axis==0 else (radius[1]*math.sin((step+phase)*math.tau/32)))&255 for step in range(32))
    blobs.append((0x7e00,bytes(big)))
    blobs.append((0x7f00,bytes((velocity*d)&255 for velocity in range(-3,4) for d in range(33))))
    for address,data in blobs:
        off=address-0x4000;assert address+len(data)<=0x8000 and not any(out[off:off+len(data)])
        out[off:off+len(data)]=data
    return bytes(out)
