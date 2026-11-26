"""Four rainbow player bands and four missile spray streams, bank 15."""
import math
from scene_palette_io import emit as emit_scene_io
from build_sequence import Code
from engine_effects import PMBASE_SHADOW, EFFECT_ORIGIN
from crush_portraits import START as CRUSH_START
from scene_palettes import SCHOOL_GTIA, GYM_GTIA, PRACTICE_WALL_GTIA
ENTRY=0x6000
RESTORE=0x6f00
from gym_practice import PRACTICE_CUTS
SHOT_START,SHOT_END=PRACTICE_CUTS[1:3]
FLIGHT_FRAMES = (SHOT_END - SHOT_START + 3) // 4
SPRAY_DATA = 0x5200

def paths():
    # One sample per PAL frame over the existing 997-tick shot.
    assert FLIGHT_FRAMES <= 256
    times = (frame / (FLIGHT_FRAMES - 1) for frame in range(FLIGHT_FRAMES))
    return [(round(95+42*t), max(2, round(28+10*t-32*math.sin(math.pi*t))))
            for t in times]


def spray_data():
    from basketball_hero import satellite_orbits

    data = bytearray()
    for orbit in satellite_orbits(training=True):
        samples = []
        for frame, (x, y) in enumerate(paths()):
            dx, dy = orbit[frame % len(orbit)]
            samples.append((max(50, min(202, x+46+dx)),
                            max(9, min(103, (y+17)//2+6+dy))))
        for axis in zip(*samples):
            data.extend(axis)
    assert SPRAY_DATA + len(data) <= 0x5a00
    return bytes(data)


def spin_masks():
    """Compact opaque neon sphere, eight rotations in the existing 512 B.

    Four co-located players paint curved panels, a darker rim and a bright
    seam/glint. No transparent seams reveal the background through the ball.
    """
    frames=[]
    for phase in range(8):
        theta=phase*math.tau/8
        planes=[bytearray(16) for _ in range(4)]
        for y in range(16):
            v=(y-7.5)/7.8
            for x in range(8):
                u=(x-3.5)/3.9;r2=u*u+v*v
                if r2>1:continue
                z=math.sqrt(1-r2)
                sy=v*math.cos(.38)-z*math.sin(.38)
                sz=v*math.sin(.38)+z*math.cos(.38)
                sx=u*math.cos(theta)-sz*math.sin(theta)
                depth=u*math.sin(theta)+sz*math.cos(theta)
                seam=min(abs(sx),abs(sy),abs(depth))<.105
                glint=((u+.30)/.26)**2+((v+.38)/.18)**2<1
                panel=1+((sx>0) ^ (sy>0))
                ink=0 if r2>.78 else 3 if seam or glint else panel
                planes[ink][y]|=0x80>>x
        frames.append(planes)
    return frames


def helper(practice_entry):
    c=Code(ENTRY)
    def a(op,addr):emit_scene_io(c,op,addr)
    from whistle_pmg import ENTRY as WHISTLE_ENTRY
    # The first still of the school story shares the palette used by its later
    # encounter shots. Gym shots and dance scenes use a separate warm palette.
    a(0xad,0x83e0);c.emit(0xc9,7);c.branch(0xd0,'not_school_open')
    for address,color in zip((0xd016,0xd017,0xd018),SCHOOL_GTIA):
        c.emit(0xa9,color);a(0x8d,address)
    c.label('not_school_open')
    a(0xad,0x83e0);c.emit(0xc9,13);c.branch(0xf0,'gym_palette')
    c.emit(0xc9,15);c.branch(0xd0,'not_gym')
    c.label('gym_palette')
    for address,color in zip((0xd016,0xd017,0xd018),GYM_GTIA):
        c.emit(0xa9,color);a(0x8d,address)
    c.label('not_gym')
    a(0xad,0x83e0);c.emit(0xc9,13);c.branch(0xd0,'not_practice_wall')
    c.emit(0xa9,PRACTICE_WALL_GTIA);a(0x8d,0xd016)
    c.label('not_practice_wall')
    a(0xad,0x83e0);c.emit(0xc9,2);c.branch(0x90,'not_dance')
    c.emit(0xc9,6);c.branch(0xb0,'not_dance')
    for address,color in zip((0xd016,0xd017,0xd018),GYM_GTIA):
        c.emit(0xa9,color);a(0x8d,address)
    c.label('not_dance')
    # Warm, darker colours for the arena encounter and its reaction shots.
    a(0xad,0x83e0);c.emit(0xc9,8);c.branch(0x90,'encounter_done')
    c.emit(0xc9,13);c.branch(0xb0,'encounter_done')
    for address,color in zip((0xd016,0xd017,0xd018),SCHOOL_GTIA):
        c.emit(0xa9,color);a(0x8d,address)
    c.label('encounter_done')
    a(0xad,0x83e0);c.emit(0xc9,10);c.branch(0x90,'not_whistle')
    c.emit(0xc9,12);c.branch(0xb0,'not_whistle')
    a(0x4c,WHISTLE_ENTRY)
    c.label('not_whistle')
    a(0xad,0x83e0);c.emit(0xc9,14);c.branch(0xd0,'not_portrait')
    a(0xad,0x83e3);c.emit(0xc9,CRUSH_START>>8);c.branch(0x90,'not_portrait');a(0x4c,0x6900)
    c.label('not_portrait');a(0xad,0x83e0);c.emit(0xc9,13);c.branch(0xd0,'inactive')
    for threshold,low,high in ((SHOT_START,'closeup','after_start'),(SHOT_END,'active','stretch')):
        a(0xad,0x83e3);c.emit(0xc9,threshold>>8);c.branch(0x90,low);c.branch(0xd0,high)
        a(0xad,0x83e2);c.emit(0xc9,threshold&255);c.branch(0x90,low);c.jump(0x4c,high)
        if high=='after_start':c.label(high)
    c.label('inactive')
    a(0xad,0x83fe);c.emit(0xc9,1);c.branch(0xd0,'ordinary')
    c.emit(0xa9,0);a(0x8d,0x83fe);a(0x20,RESTORE)
    c.label('ordinary');a(0x4c,EFFECT_ORIGIN)
    c.label('closeup');c.emit(0xa2,0);a(0x4c,practice_entry)
    c.label('stretch')
    a(0xad,0x83fe);c.emit(0xc9,1);c.branch(0xd0,'notes')
    c.emit(0xa9,0);a(0x8d,0xd01d);a(0x8d,0x83fe);a(0x20,RESTORE)
    c.label('notes');c.emit(0xa2,1);a(0x4c,practice_entry)
    c.label('active')
    c.emit(0xa9,1);a(0x8d,0x83fe)
    # Keep the displayed ball live while building the next frame.
    a(0xad,PMBASE_SHADOW);c.emit(0x29,0x80,0x49,0x80)
    c.jump(0x8d,'back_page')
    destinations = []

    def back_buffer(label, op, address):
        destinations.append((label, address >> 8))
        c.label(label)
        a(op,address)

    c.jump(0x4c,'select_page')
    c.label('draw')
    # Use the complete 16-bit elapsed time; low-byte wrap never restarts flight.
    a(0xad,0x83e2);c.emit(0x38,0xe9,SHOT_START&255);a(0x8d,0x83fd)
    a(0xad,0x83e3);c.emit(0xe9,SHOT_START>>8)
    for _ in range(2):c.emit(0x4a);a(0x6e,0x83fd)
    a(0xad,0x83fd);a(0x8d,0x83ff)
    c.emit(0xa9,0,0xa2,0)
    c.label('clear')
    for i,base in enumerate((0x0980,0x0a00,0x0a80,0x0b00,0x0b80)):
        back_buffer(f'clear{i}',0x9d,base)
    c.emit(0xe8,0xe0,128);c.branch(0xd0,'clear')
    a(0xae,0x83ff)
    c.jump(0xbd,'ball_y');c.emit(0xa8)
    # Rotate both the colored panels and the curved seams around the ball.
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x29,7,0x0a,0x0a,0x0a,0x0a,0xaa)
    c.label('spin_rows')
    for player in range(4):
        c.jump(0xbd,f'spin{player}')
        back_buffer(f'put_ball{player}',0x99,0x0a00+128*player)
    c.emit(0xe8,0xc8,0x8a,0x29,15);c.branch(0xd0,'spin_rows')
    a(0xae,0x83ff)
    for i in range(4):
        c.jump(0xbd,f'spray_y{i}');c.emit(0xa8)
        for dy, bits in ((0,1),(2,3),(4,1)):
            back_buffer(f'get_spray{i}_{dy}',0xb9,0x0980+dy)
            c.emit(0x09,bits<<(i*2))
            back_buffer(f'put_spray{i}_{dy}',0x99,0x0980+dy)
    c.label('publish')
    a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'publish')
    c.emit(0xc9,128);c.branch(0xb0,'publish')
    c.jump(0xad,'back_page');c.emit(0x09,8)
    a(0x8d,PMBASE_SHADOW);a(0x8d,0xd407)
    a(0xae,0x83ff)
    c.jump(0xbd,'ball_x');c.emit(0x18,0x69,48)
    for i in range(4):a(0x8d,0xd000+i)
    for i in range(4):
        c.jump(0xbd,f'spray_x{i}');a(0x8d,0xd004+i)
    # Rotate through the Atari hue wheel, offset between the four stripes.
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x29,15,0xaa)
    for i in range(4):
        c.jump(0xbd,f'hues{i}');a(0x8d,0xd012+i)
    for addr,val in ((0xd01b,1),(0xd01d,3),(0xd400,0x2e),(0xd00c,0x55)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0xa9,1,0xa2,3)
    c.label('sizes');a(0x9d,0xd008);c.emit(0xca);c.branch(0x10,'sizes');c.emit(0x60)
    c.label('select_page')
    c.jump(0xad,'back_page');c.emit(0x09,9)
    for label, high in destinations:
        if high == 9:
            a(0x8d,c.labels[label]+2)
    for high in (10,11):
        c.jump(0xad,'back_page');c.emit(0x09,high)
        for label, dest_high in destinations:
            if high == dest_high:
                a(0x8d,c.labels[label]+2)
    c.jump(0x4c,'draw')
    c.label('back_page');c.emit(0)
    positions=paths()
    c.label('ball_x');c.emit(*(x-8 for x,y in positions))
    c.label('ball_y');c.emit(*((y+17)//2 for x,y in positions))
    frames=spin_masks()
    for player in range(4):
        c.label(f'spin{player}');c.emit(*(value for frame in frames for value in frame[player]))
    for i in range(4):
        c.labels[f'spray_x{i}'] = SPRAY_DATA + 2*i*FLIGHT_FRAMES
        c.labels[f'spray_y{i}'] = SPRAY_DATA + (2*i+1)*FLIGHT_FRAMES
        c.label(f'hues{i}');c.emit(*((((j+i*4)%15+1)<<4)|(6,10,12,14)[i] for j in range(16)))
    result=c.finish();assert ENTRY+len(result)<=WHISTLE_ENTRY
    return result
