"""Act 3: tunnel cutaway, arena dribble and one fast backboard-breaking dunk."""
from pathlib import Path
from functools import lru_cache
import math
from engine_effects import cached_display_list
from build_sequence import Code
from music_timing import tick_at_bar
from trevor_awakens import FLIGHT_START as TREVOR_FLIGHT_START
from rainbow_ball import spin_masks
CUTAWAY_START,START,DUNK,END=(tick_at_bar(bar) for bar in (56,58,62,64))
DUNK_PHASE_TICKS=8
DUNK_OFFSET=DUNK-START
ENTRY,DATA,HEIGHT=0x4000,0x4b80,56
BANK_VALUE=0x24b4
DRIBBLE_X, DRIBBLE_WIDTH = 64, 44
DRIBBLE_Y, DRIBBLE_HEIGHT = 16, 28
DRIBBLE_PATCH_BYTES = DRIBBLE_WIDTH//4 * DRIBBLE_HEIGHT
SHATTER_X, SHATTER_Y, SHATTER_WIDTH, SHATTER_HEIGHT = 112,0,48,24
SHATTER_PATCH_BYTES = SHATTER_WIDTH//4*SHATTER_HEIGHT
SHATTER_DATA = DATA+5*2240+3*DRIBBLE_PATCH_BYTES
ORBIT_DATA=0x7e40


def satellite_orbits():
    """Four relative missile paths; Y units are double-line PMG rows."""
    paths=[]
    for plane,(rx,ry,direction,speed,phase,tilt) in enumerate((
            (18,7,1,1,0,0), (11,11,-1,1,8,0),
            (25,5,1,2,4,0), (17,8,-1,1,20,.6))):
        path=[]
        for step in range(32):
            theta=(direction*speed*step+phase)*math.tau/32
            x,y=rx*math.cos(theta),ry*math.sin(theta)
            # Rotate in display proportions: one Y row equals two scanlines.
            path.append((round(x*math.cos(tilt)-2*y*math.sin(tilt)),
                         round(x*.5*math.sin(tilt)+y*math.cos(tilt))))
        paths.append(path)
    return paths


def orbit_data():
    return bytes(v&255 for path in satellite_orbits()
                 for axis,origin in ((0,46),(1,6)) for point in path
                 for v in (point[axis]+origin,))


@lru_cache(maxsize=1)
def reference_art():
    """Exact v175 keyframes, arm patches and board fracture patches."""
    raw=Path('assets/art/reference/v175/basketball.bin').read_bytes()
    expected=5*2240+3*DRIBBLE_PATCH_BYTES+3*SHATTER_PATCH_BYTES
    if len(raw)!=expected:raise ValueError('invalid v175 basketball asset size')
    return raw


def unpack(raw):
    return bytes(value>>shift&3 for value in raw for shift in (6,4,2,0))

@lru_cache(maxsize=1)
def cleaned_art():
    """Retain release 001 poses while replacing small leaked background areas."""
    from hero_mask_cleanup import clean
    raw=reference_art()
    original=[unpack(raw[i*2240:(i+1)*2240]) for i in range(5)]
    corrected=[clean(frame,index) for index,frame in enumerate(original)]
    def pack(pixels):
        return bytes(sum(pixels[i+j]<<(6-2*j) for j in range(4)) for i in range(0,len(pixels),4))
    patches=[];offset=5*2240
    for _ in range(3):
        patch=unpack(raw[offset:offset+DRIBBLE_PATCH_BYTES]);offset+=DRIBBLE_PATCH_BYTES
        image=bytearray(original[0])
        for y in range(DRIBBLE_HEIGHT):
            at=(DRIBBLE_Y+y)*160+DRIBBLE_X
            image[at:at+DRIBBLE_WIDTH]=patch[y*DRIBBLE_WIDTH:(y+1)*DRIBBLE_WIDTH]
        image=clean(image,0)
        pixels=bytes(image[(DRIBBLE_Y+y)*160+x]
                     for y in range(DRIBBLE_HEIGHT) for x in range(DRIBBLE_X,DRIBBLE_X+DRIBBLE_WIDTH))
        patches.append(pack(pixels))
    return b''.join(map(pack,corrected))+b''.join(patches)+raw[offset:]


@lru_cache(maxsize=1)
def frames():
    raw=cleaned_art()
    full=[unpack(raw[i*2240:(i+1)*2240]) for i in range(5)]
    poses={0:full[0],**{i+2:p for i,p in enumerate(full[1:])}}
    offset=5*2240
    for index in (1,6,7):
        patch=unpack(raw[offset:offset+DRIBBLE_PATCH_BYTES]);offset+=DRIBBLE_PATCH_BYTES
        image=bytearray(full[0])
        for y in range(DRIBBLE_HEIGHT):
            start=(DRIBBLE_Y+y)*160+DRIBBLE_X
            image[start:start+DRIBBLE_WIDTH]=patch[y*DRIBBLE_WIDTH:(y+1)*DRIBBLE_WIDTH]
        poses[index]=bytes(image)
    return [poses[i] for i in range(8)]

def shatter_stage(phase):
    return 0 if phase<75 else 1 if phase<81 else 2 if phase<87 else 3


def shattered_frame(stage):
    if stage==0:return frames()[5]
    if stage not in (1,2,3):raise ValueError('invalid board fracture stage')
    offset=5*2240+3*DRIBBLE_PATCH_BYTES+(stage-1)*SHATTER_PATCH_BYTES
    patch=unpack(cleaned_art()[offset:offset+SHATTER_PATCH_BYTES])
    image=bytearray(frames()[5])
    for y in range(SHATTER_HEIGHT):
        start=y*160+SHATTER_X
        image[start:start+SHATTER_WIDTH]=patch[y*SHATTER_WIDTH:(y+1)*SHATTER_WIDTH]
    return bytes(image)


def scene_frame(tick,pose):
    phase=(tick-DUNK)//DUNK_PHASE_TICKS
    return shattered_frame(shatter_stage(phase)) if tick>=DUNK and shatter_stage(phase) else frames()[pose]


def packed():
    return cleaned_art()


def ball_paths():
    # Screen coordinates: centre the ball below the palm, then bounce off
    # the floor. Serialization below converts Y into double-line PMG rows.
    dribble=[(84,round(94+66*math.sin(math.pi*i/46)**1.5)) for i in range(47)]
    # Positions are anchored to the illustrated ball hand in each pose.
    # The first wind-up is held, then two quick airborne poses and the dunk.
    dunk=[]
    for i in range(94):
        if i<47: x,cy=85,102
        elif i<61: x,cy=99,28
        elif i<75: x,cy=115,18
        elif i<82: x,cy=124,32
        else:
            t=(i-82)/11
            x,cy=round(124+5*t),round(32+99*t)
        dunk.append((x,max(0,cy-16)))
    return dribble,dunk

def dribble_phase(elapsed):
    phase=elapsed%374
    return (phase if phase<94 else phase-94)//2 if phase<188 else (phase-188)//4

def helper(bank_wrapper=0, bank_operand=0, cutaway_entry=0):
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # Delegate Act 4 through the unbanked bank-switch trampoline.
    a(0xad,0x83e4);c.branch(0xd0,'trevor')
    a(0xad,0x83e3);c.emit(0xc9,END>>8);c.branch(0x90,'hero');c.branch(0xd0,'trevor')
    a(0xad,0x83e2);c.emit(0xc9,END&255);c.branch(0x90,'hero')
    c.label('trevor');a(0xad,0x83e3);c.emit(0xc9,TREVOR_FLIGHT_START>>8);c.branch(0x90,'trevor_quiet')
    c.branch(0xd0,'trevor_tunnel');a(0xad,0x83e2);c.emit(0xc9,TREVOR_FLIGHT_START&255);c.branch(0x90,'trevor_quiet')
    c.label('trevor_tunnel');a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x18,0x69,0xd8);c.jump(0x4c,'trevor_bank_ready')
    c.label('trevor_quiet');c.emit(0xa9,0xf1)  # dedicated quiet bank, index 49
    c.label('trevor_bank_ready');a(0x8d,bank_operand)
    c.emit(0xa9,0x08);a(0x8d,bank_operand+1);a(0x20,bank_wrapper)
    c.emit(0xa9,0xb3);a(0x8d,bank_operand);c.emit(0xa9,0x24);a(0x8d,bank_operand+1);c.emit(0x60)
    c.label('hero')
    # User-approved two-bar tunnel after the unchanged ribbon/throw shot.
    a(0xad,0x83e3);c.emit(0xc9,START>>8);c.branch(0x90,'cutaway');c.branch(0xd0,'hero_start')
    a(0xad,0x83e2);c.emit(0xc9,START&255);c.branch(0xb0,'hero_start')
    c.label('cutaway');c.emit(0xa9,0x80);c.jump(0x8d,'pmg_page');a(0x4c,cutaway_entry)
    c.label('hero_start')
    # Elapsed player ticks, coherent snapshot supplied by the main callback.
    a(0xad,0x83e2);c.emit(0x38,0xe9,START&255);a(0x8d,0x83ea)
    a(0xad,0x83e3);c.emit(0xe9,START>>8);a(0x8d,0x83eb)
    c.emit(0xc9,DUNK_OFFSET>>8);c.branch(0x90,'dribble');c.branch(0xd0,'dunk')
    a(0xad,0x83ea);c.emit(0xc9,DUNK_OFFSET&255);c.branch(0xb0,'dunk')
    c.label('dribble')
    a(0xad,0x83eb);c.emit(0xc9,1);c.branch(0x90,'dribble_tempo');c.branch(0xd0,'subtract_beat')
    a(0xad,0x83ea);c.emit(0xc9,118);c.branch(0x90,'dribble_tempo')
    c.label('subtract_beat');a(0xad,0x83ea);c.emit(0x38,0xe9,118);a(0x8d,0x83ea);a(0xad,0x83eb);c.emit(0xe9,1);a(0x8d,0x83eb);c.jump(0x4c,'dribble')
    c.label('dribble_tempo');a(0xad,0x83eb);c.branch(0xd0,'slow_dribble')
    a(0xad,0x83ea);c.emit(0xc9,188);c.branch(0xb0,'slow_dribble')
    c.emit(0xc9,94);c.branch(0x90,'fast_dribble');c.emit(0x38,0xe9,94)
    c.label('fast_dribble');c.emit(0x4a);c.jump(0x4c,'dribble_phase')
    c.label('slow_dribble');a(0xad,0x83ea);c.emit(0x38,0xe9,188,0x4a,0x4a)
    c.label('dribble_phase');a(0x8d,0x83ff);c.emit(0xa9,0);a(0x8d,0x83ed)
    a(0xad,0x83ff);c.emit(0xc9,9,0xa9,0);c.branch(0x90,'pose_ready')
    a(0xad,0x83ff);c.emit(0xc9,18,0xa9,1);c.branch(0x90,'pose_ready')
    a(0xad,0x83ff);c.emit(0xc9,32,0xa9,6);c.branch(0x90,'pose_ready')
    a(0xad,0x83ff);c.emit(0xc9,42,0xa9,7);c.branch(0x90,'pose_ready')
    c.emit(0xa9,0);c.jump(0x4c,'pose_ready')
    c.label('dunk');a(0xad,0x83ea);c.emit(0x38,0xe9,DUNK_OFFSET&255);a(0x8d,0x83ea);a(0xad,0x83eb);c.emit(0xe9,DUNK_OFFSET>>8)
    for _ in range(3):c.emit(0x4a);a(0x6e,0x83ea)
    a(0xad,0x83ea);a(0x8d,0x83ff);c.emit(0xa9,1);a(0x8d,0x83ed)
    a(0xad,0x83ff);c.emit(0xc9,75,0xa9,5);c.branch(0xb0,'pose_ready')
    a(0xad,0x83ff);c.emit(0xc9,61,0xa9,4);c.branch(0xb0,'pose_ready')
    a(0xad,0x83ff);c.emit(0xc9,47,0xa9,3);c.branch(0xb0,'pose_ready');c.emit(0xa9,2)
    c.label('pose_ready');a(0x8d,0x83ec)
    c.emit(0xa9,0);a(0x8d,0x83e5);a(0xad,0x83ed);c.branch(0xf0,'stage_ready')
    a(0xad,0x83ff);c.emit(0xc9,75);c.branch(0x90,'stage_ready')
    c.emit(0xa2,1,0xc9,81);c.branch(0x90,'save_stage');c.emit(0xe8,0xc9,87);c.branch(0x90,'save_stage');c.emit(0xe8)
    c.label('save_stage');a(0x8e,0x83e5)
    c.label('stage_ready');c.emit(0xa9,0);c.jump(0x8d,'pending_dl')
    a(0xad,0x83e5);c.emit(0x0a,0x0a,0x0a,0x18);a(0x6d,0x83ec);c.emit(0x69,0x50)
    a(0xcd,0x83fa);c.branch(0xd0,'changed');c.jump(0x4c,'wait')
    c.label('changed');a(0x8d,0x83fa)
    a(0xad,0x83ed);c.branch(0xd0,'full_copy')
    a(0xad,0x83e6);c.emit(0x29,4,0x4a,0x4a,0x49,1,0xaa)
    a(0xbd,0x83f8);c.emit(0x29,0xf8,0xc9,0x40);c.branch(0xd0,'dribble_init')
    c.jump(0x4c,'dribble_patch')
    c.label('dribble_init');c.emit(0xa2,0);c.jump(0x4c,'full_source')
    c.label('full_copy');a(0xae,0x83ec)
    c.label('full_source')
    c.jump(0xbd,'source_lo');c.jump(0x8d,'read_lo');c.jump(0xbd,'source_hi');c.jump(0x8d,'read_hi')
    a(0xad,0x83e6);c.emit(0x29,4,0x0a,0x0a,0x0a,0x49,0xb0);a(0x8d,0x83fe);c.jump(0x8d,'write_hi')
    c.emit(0xa9,0);c.jump(0x8d,'write_lo');c.emit(0xa2,8,0xa0,0)
    c.label('copy');c.label('read');c.emit(0xb9,0,0);c.label('write');c.emit(0x99,0,0,0xc8);c.branch(0xd0,'copy')
    for label in ('read_hi','write_hi'):c.jump(0xee,label)
    c.emit(0xca);c.branch(0xd0,'copy')
    # Patch the tail once, then copy its 192 bytes inline.
    for source,target in (('read','tail_read'),('write','tail_write')):
        c.jump(0xad,source+'_lo');c.jump(0x8d,target+'_lo');c.jump(0xad,source+'_hi');c.jump(0x8d,target+'_hi')
    c.label('tail');c.label('tail_read');c.emit(0xb9,0,0)
    c.label('tail_write');c.emit(0x99,0,0,0xc8,0xc0,192);c.branch(0xd0,'tail')
    a(0xad,0x83ed);c.branch(0xd0,'bitmap_ready')
    c.label('dribble_patch');a(0xae,0x83ec)
    for table, operand in (('patch_lo','patch_read_lo'),('patch_hi','patch_read_hi'),('patch_stride','patch_step')):
        c.jump(0xbd,table);c.jump(0x8d,operand)
    c.emit(0xa9,(DRIBBLE_Y*40+DRIBBLE_X//4)&255);c.jump(0x8d,'patch_write_lo')
    a(0xad,0x83e6);c.emit(0x29,4,0x0a,0x0a,0x0a,0x49,0xb0);a(0x8d,0x83fe)
    c.emit(0x18,0x69,(DRIBBLE_Y*40+DRIBBLE_X//4)>>8);c.jump(0x8d,'patch_write_hi')
    c.emit(0xa2,DRIBBLE_HEIGHT)
    c.label('patch_row');c.emit(0xa0,0)
    c.label('patch_pixel');c.label('patch_read');c.emit(0xb9,0,0)
    c.label('patch_write');c.emit(0x99,0,0,0xc8,0xc0,DRIBBLE_WIDTH//4);c.branch(0xd0,'patch_pixel')
    c.emit(0x18);c.jump(0xad,'patch_read_lo');c.label('patch_add');c.emit(0x69,40);c.jump(0x8d,'patch_read_lo')
    c.branch(0x90,'patch_src_ok');c.jump(0xee,'patch_read_hi');c.label('patch_src_ok')
    c.emit(0x18);c.jump(0xad,'patch_write_lo');c.emit(0x69,40);c.jump(0x8d,'patch_write_lo')
    c.branch(0x90,'patch_dst_ok');c.jump(0xee,'patch_write_hi');c.label('patch_dst_ok')
    c.emit(0xca);c.branch(0xd0,'patch_row')
    a(0xad,0x83e6);c.emit(0x29,4,0x4a,0x4a,0x49,1,0xaa)
    a(0xad,0x83ec);c.emit(0x09,0x40);a(0x9d,0x83f8)
    c.label('bitmap_ready')
    a(0xae,0x83e5);c.branch(0xf0,'shatter_done');c.emit(0xca)
    for table,operand in (('shatter_lo','shatter_read_lo'),('shatter_hi','shatter_read_hi')):
        c.jump(0xbd,table);c.jump(0x8d,operand)
    c.emit(0xa9,SHATTER_X//4);c.jump(0x8d,'shatter_write_lo')
    a(0xad,0x83fe);c.jump(0x8d,'shatter_write_hi');c.emit(0xa2,SHATTER_HEIGHT)
    c.label('shatter_row');c.emit(0xa0,0)
    c.label('shatter_byte');c.label('shatter_read');c.emit(0xb9,0,0)
    c.label('shatter_write');c.emit(0x99,0,0,0xc8,0xc0,SHATTER_WIDTH//4);c.branch(0xd0,'shatter_byte')
    for name,stride in (('shatter_read',SHATTER_WIDTH//4),('shatter_write',40)):
        c.jump(0xad,name+'_lo');c.emit(0x18,0x69,stride);c.jump(0x8d,name+'_lo');c.branch(0x90,name+'_ready');c.jump(0xee,name+'_hi');c.label(name+'_ready')
    c.emit(0xca);c.branch(0xd0,'shatter_row')
    c.label('shatter_done')
    cached_display_list(c, 3)
    a(0xad,0x83e6);c.jump(0x8d,'dl1_hi');c.jump(0x8d,'dl2_hi')
    c.emit(0xa9,3);c.jump(0x8d,'dl1_lo');c.emit(0xa9,4);c.jump(0x8d,'dl2_lo');c.emit(0xa0,0)
    c.label('rows');c.jump(0xb9,'row_lo');c.label('dl1');c.emit(0x8d,0,0)
    c.jump(0xb9,'row_hi');c.emit(0x18);a(0x6d,0x83fe);c.label('dl2');c.emit(0x8d,0,0)
    for label in ('dl1','dl2'):
        c.emit(0x18);c.jump(0xad,label+'_lo');c.emit(0x69,3);c.jump(0x8d,label+'_lo');c.branch(0x90,label+'ok');c.jump(0xee,label+'_hi');c.label(label+'ok')
    c.emit(0xc8,0xc0,192);c.branch(0xd0,'rows')
    c.label('swap');c.jump(0xee,'pending_dl')
    a(0xad,0x83ed);c.branch(0xf0,'wait')
    c.emit(0xa9,255);a(0x8d,0x83f8);a(0x8d,0x83f9)
    c.label('wait')
    # The tunnel before the hero uses $0800. Start with the upper PMG and
    # alternate after publication, without reading the write-only PMBASE.
    c.jump(0xad,'pmg_page');c.emit(0x09,9)
    for label in ('clear0','missile_read','missile_write'):c.jump(0x8d,label+'_hi')
    c.emit(0x49,3)
    for label in ('clear1','clear2','put0','put1'):c.jump(0x8d,label+'_hi')
    c.emit(0x09,1)
    for label in ('clear3','clear4','put2','put3'):c.jump(0x8d,label+'_hi')
    c.emit(0xa9,0,0xa2,127);c.label('clear')
    for i,address in enumerate((0x0980,0x0a00,0x0a80,0x0b00,0x0b80)):
        c.label(f'clear{i}');a(0x9d,address)
    c.emit(0xca);c.branch(0x10,'clear')

    a(0xae,0x83ff);a(0xad,0x83ed);c.branch(0xd0,'dunk_ball')
    c.jump(0xbd,'dribble_x');a(0x8d,0x83e8);c.jump(0xbd,'dribble_y');c.jump(0x4c,'ball_position')
    c.label('dunk_ball');c.jump(0xbd,'dunk_x');a(0x8d,0x83e8);c.jump(0xbd,'dunk_y')
    c.label('ball_position');a(0x8d,0x83e9);c.emit(0xa8)
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x29,7,0x0a,0x0a,0x0a,0x0a,0xaa)
    c.label('spin')
    for i in range(4):
        c.jump(0xbd,f'spin{i}');c.label(f'put{i}');a(0x99,0x0a00+i*128)
    c.emit(0xe8,0xc8,0x8a,0x29,15);c.branch(0xd0,'spin')
    a(0xad,0x83e5);c.branch(0xd0,'shattered_droplets')
    a(0xad,0x83ed);c.branch(0xd0,'choose_orbits');c.jump(0x4c,'ball_droplets')
    c.label('choose_orbits');c.jump(0x4c,'orbit_satellites')
    c.label('shattered_droplets')
    a(0xad,0x83ff);c.emit(0x38,0xe9,75,0xaa)
    for i in range(4):
        c.jump(0xbd,f'shard_x{i}');c.jump(0x8d,f'hpos{i}')
        c.jump(0xbd,f'shard_y{i}');c.emit(0xa8)
        c.emit(0xa9,3<<(2*i));c.jump(0x20,'put_missile')
        c.emit(0xc8,0xa9,1<<(2*i));c.jump(0x20,'put_missile')
        c.emit(0xc8,0xc8,0xa9,2<<(2*i));c.jump(0x20,'put_missile')
    c.jump(0x4c,'spray_ready')
    c.label('ball_droplets')
    for i,dx in enumerate((-14,-7,13,20)):
        a(0xad,0x83e8);c.emit(0x18,0x69,48+dx);c.jump(0x8d,f'hpos{i}')
        a(0xad,0x83e9);c.emit(0x18,0x69,i*3+1,0xa8,0xa9,3<<(2*i));c.jump(0x20,'put_missile')
        c.emit(0x98,0x18,0x69,5,0xa8,0xa9,3<<(2*i));c.jump(0x20,'put_missile')
    c.jump(0x4c,'spray_ready')
    c.label('orbit_satellites')
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x29,31,0xaa)
    for i in range(4):
        a(0xbd,ORBIT_DATA+i*64);c.emit(0x18);a(0x6d,0x83e8);c.jump(0x8d,f'hpos{i}')
        a(0xbd,ORBIT_DATA+i*64+32);c.emit(0x18);a(0x6d,0x83e9);c.emit(0xa8)
        for dy,bits in enumerate((1,3,1)):
            if dy:c.emit(0xc8)
            c.emit(0xa9,bits<<(2*i));c.jump(0x20,'put_missile')
    c.label('spray_ready')
    # Only register writes happen during this early blanking window.
    c.label('publish');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'publish')
    c.emit(0xc9,128);c.branch(0xb0,'publish')
    c.jump(0xad,'pending_dl');c.branch(0xf0,'publish_pmg')
    c.emit(0xa9,0);a(0x8d,0xd402);a(0xad,0x83e6);a(0x8d,0xd403);c.emit(0x49,4);a(0x8d,0x83e6)
    c.label('publish_pmg');c.jump(0xad,'pmg_page');c.emit(0x09,8);a(0x8d,0xd407)
    c.emit(0x49,0x88);c.jump(0x8d,'pmg_page')
    for i in range(4):c.jump(0xad,f'hpos{i}');a(0x8d,0xd004+i)
    a(0xad,0x83e8);c.emit(0x18,0x69,40)
    for i in range(4):a(0x8d,0xd000+i)
    a(0xad,0x83e2);c.emit(0x0a,0x0a,0x29,0xf0,0x09,6)
    for i in range(4):a(0x8d,0xd012+i);c.emit(0x18,0x69,0x44 if i==0 else 0x42)
    for addr,val in ((0xd01a,0),(0xd016,0x38),(0xd017,0x68),(0xd018,0x2a),(0xd01b,1),(0xd01d,3),(0xd400,0x2e),(0xd00c,0)):
        c.emit(0xa9,val);a(0x8d,addr)
    a(0xad,0x83ed);c.branch(0xf0,'missile_size_ready')
    a(0xad,0x83e5);c.branch(0xd0,'missile_size_ready')
    c.emit(0xa9,0x55);a(0x8d,0xd00c)
    c.label('missile_size_ready');a(0xad,0x83ed);c.branch(0xf0,'no_flash');a(0xad,0x83ff);c.emit(0xc9,82);c.branch(0x90,'no_flash');c.emit(0xc9,85);c.branch(0xb0,'no_flash');c.emit(0xa9,14);a(0x8d,0xd017)
    c.label('no_flash');c.emit(0xa9,1,0xa2,3)
    c.label('sizes');a(0x9d,0xd008);c.emit(0xca);c.branch(0x10,'sizes');c.emit(0x60)
    c.label('put_missile');c.label('missile_read');a(0x19,0x0980)
    c.label('missile_write');a(0x99,0x0980);c.emit(0x60)
    c.label('pmg_page');c.emit(0x80)
    c.label('pending_dl');c.emit(0)
    for i in range(4):c.label(f'hpos{i}');c.emit(0)
    for label in ('missile_read','missile_write',*(f'clear{i}' for i in range(5)),
                  *(f'put{i}' for i in range(4))):c.labels[label+'_hi']=c.labels[label]+2
    for label in ('read','write','dl1','dl2','tail_read','tail_write'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    for label in ('patch_read','patch_write'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    for label in ('shatter_read','shatter_write'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    for part,shift in (('lo',0),('hi',8)):
        c.label('shatter_'+part);c.emit(*(((SHATTER_DATA+i*SHATTER_PATCH_BYTES)>>shift)&255 for i in range(3)))
    for i in range(4):
        c.label(f'shard_x{i}');c.emit(*(round(130+(i-1.5)*(5+age*.7))+48 for age in range(19)))
        c.label(f'shard_y{i}');c.emit(*(round(17+i*2-age*.7+age*age*.105) for age in range(19)))
    c.labels['patch_step']=c.labels['patch_add']+1
    sources=[DATA+DRIBBLE_Y*40+DRIBBLE_X//4,DATA+5*2240,0,0,0,0,
             DATA+5*2240+DRIBBLE_PATCH_BYTES,DATA+5*2240+2*DRIBBLE_PATCH_BYTES]
    c.label('patch_lo');c.emit(*(v&255 for v in sources))
    c.label('patch_hi');c.emit(*(v>>8 for v in sources))
    c.label('patch_stride');c.emit(40,*([DRIBBLE_WIDTH//4]*7))
    addresses=[DATA,DATA]+[DATA+(i-1)*2240 for i in range(2,6)]+[DATA,DATA]
    c.label('source_lo');c.emit(*(v&255 for v in addresses))
    c.label('source_hi');c.emit(*(v>>8 for v in addresses))
    c.label('row_lo');c.emit(*((y*56//192*40)&255 for y in range(192)))
    c.label('row_hi');c.emit(*((y*56//192*40)>>8 for y in range(192)))
    masks=spin_masks()
    for i in range(4):c.label(f'spin{i}');c.emit(*(v for frame in masks for v in frame[i]))
    for name,path in zip(('dribble','dunk'),ball_paths()):
        c.label(name+'_x');c.emit(*(x for x,y in path))
        c.label(name+'_y');c.emit(*((y+17)//2 for x,y in path))
    code=c.finish();assert ENTRY+len(code)<=DATA,(len(code),DATA-ENTRY)
    return code

def bank(bank_wrapper=0, bank_operand=0, cutaway_entry=0):
    out=bytearray(16384);code=helper(bank_wrapper,bank_operand,cutaway_entry);out[:len(code)]=code;payload=packed()
    assert DATA+len(payload)<=0x8000
    assert DATA+len(payload)<=ORBIT_DATA
    orbits=orbit_data();assert ORBIT_DATA+len(orbits)<=0x8000
    out[DATA-ENTRY:DATA-ENTRY+len(payload)]=payload
    out[ORBIT_DATA-ENTRY:ORBIT_DATA-ENTRY+len(orbits)]=orbits
    return bytes(out)
