"""Act 3: low-angle dribble then slow-motion dunk, with a PMG ball."""
from pathlib import Path
from build_sequence import Code
from music_timing import tick_at_bar
from trevor_awakens import HIT as TREVOR_HIT
from rainbow_ball import spin_masks
START,DUNK,END=tick_at_bar(56),tick_at_bar(60),tick_at_bar(64)
DUNK_OFFSET=DUNK-START
ENTRY,DATA,HEIGHT=0x4000,0x4b80,56
BANK_VALUE=0x24b4
DRIBBLE_X, DRIBBLE_WIDTH = 64, 44
DRIBBLE_Y, DRIBBLE_HEIGHT = 16, 28
DRIBBLE_PATCH_BYTES = DRIBBLE_WIDTH//4 * DRIBBLE_HEIGHT

def _inside(x, y, polygon):
    odd = False
    for (ax,ay),(bx,by) in zip(polygon, polygon[1:]+polygon[:1]):
        if (ay>y)!=(by>y) and x < (bx-ax)*(y-ay)/(by-ay)+ax:
            odd = not odd
    return odd


def _original_arm(image):
    """Extract the outlined skin component of the right arm in the old art."""
    visited=set()
    candidates=[]
    for pos,value in enumerate(image):
        if value != 3 or pos in visited:
            continue
        todo=[pos];visited.add(pos);component=set()
        while todo:
            n=todo.pop();component.add((n%160,n//160))
            x,y=n%160,n//160
            for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                nxt=yy*160+xx
                if 0<=xx<160 and 0<=yy<56 and nxt not in visited and image[nxt]==3:
                    visited.add(nxt);todo.append(nxt)
        if (len(component)>=50 and min(x for x,y in component)>=64
            and max(x for x,y in component)<100 and min(y for x,y in component)>=13
            and max(y for x,y in component)<44):
            candidates.append(component)
    if len(candidates)!=1:
        raise ValueError('cannot uniquely isolate the original dribbling arm')
    skin=candidates[0]
    outline=set(skin)
    for _ in range(2):
        edge=set(outline)
        for x,y in edge:
            for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)):
                xx,yy=x+dx,y+dy
                if 0<=xx<160 and 0<=yy<56 and image[yy*160+xx]==0:
                    outline.add((xx,yy))
    return outline


def stable_dribble(pictures):
    # Preserve the anatomy, wrist and fingers of the two original illustrated
    # arms (verified against v100), with two eased in-between poses.
    masks=[_original_arm(p) for p in pictures]
    base=bytearray(pictures[0])
    for x,y in masks[0]:
        base[y*160+x]=pictures[0][y*160+108+x%12]
    # The old downstroke has detached black finger accents below the palm;
    # clear those too so they cannot remain floating under a raised hand.
    for y in range(32,44):
        for x in range(80,96):
            base[y*160+x]=1
    poses=[]
    # source, source shoulder Y, destination shoulder Y, vertical extension.
    # Only the articulated arm is sampled; body and gym remain identical.
    for source,pivot,target,scale in ((1,15,19,1.0),(0,19,19,.75),
                                      (0,19,19,1.0),(1,15,19,1.27)):
        image=bytearray(base)
        for y in range(DRIBBLE_Y,DRIBBLE_Y+DRIBBLE_HEIGHT):
            sy=round(pivot+(y-target)/scale)
            for x in range(DRIBBLE_X,DRIBBLE_X+DRIBBLE_WIDTH):
                if (x,sy) in masks[source]:
                    image[y*160+x]=pictures[source][sy*160+x]
        poses.append(bytes(image))
    return poses


def frames():
    rgb=Path('build/basketball-hero.rgb').read_bytes()
    palette=((0,0,0),(255,50,160),(0,220,255),(255,190,150))
    assert len(rgb)==320*168*3
    p=bytes(min(range(4),key=lambda j:sum((rgb[i+c]-palette[j][c])**2 for c in range(3))) for i in range(0,len(rgb),3))
    pictures=[bytes(p[(r*56+y)*320+col*160+x] for y in range(56) for x in range(160)) for r in range(3) for col in range(2)]
    poses=stable_dribble(pictures[:2])
    return poses[:2]+pictures[2:]+poses[2:]

def packed():
    art=frames()
    full=[bytes(sum(p[y*160+x+k]<<(6-2*k) for k in range(4)) for y in range(56) for x in range(0,160,4)) for p in art]
    patches=[b''.join(full[index][y*40+DRIBBLE_X//4:y*40+(DRIBBLE_X+DRIBBLE_WIDTH)//4]
                       for y in range(DRIBBLE_Y,DRIBBLE_Y+DRIBBLE_HEIGHT)) for index in (1,6,7)]
    return b''.join([full[0]]+full[2:6]+patches)

def ball_paths():
    dribble=[(97,round(94+66*((i/23) if i<=23 else ((46-i)/23))**1.5)) for i in range(47)]
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

def helper(bank_wrapper=0, bank_operand=0):
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # Delegate Act 4 through the unbanked bank-switch trampoline.
    a(0xad,0x83e4);c.branch(0xd0,'trevor')
    a(0xad,0x83e3);c.emit(0xc9,END>>8);c.branch(0x90,'hero');c.branch(0xd0,'trevor')
    a(0xad,0x83e2);c.emit(0xc9,END&255);c.branch(0x90,'hero')
    c.label('trevor');a(0xad,0x83e3);c.emit(0xc9,TREVOR_HIT>>8);c.branch(0x90,'trevor_quiet')
    c.branch(0xd0,'trevor_tunnel');a(0xad,0x83e2);c.emit(0xc9,TREVOR_HIT&255);c.branch(0x90,'trevor_quiet')
    c.label('trevor_tunnel');a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x18,0x69,0xd8);c.jump(0x4c,'trevor_bank_ready')
    c.label('trevor_quiet');c.emit(0xa9,0xf1)  # dedicated quiet bank, index 49
    c.label('trevor_bank_ready');a(0x8d,bank_operand)
    c.emit(0xa9,0x08);a(0x8d,bank_operand+1);a(0x20,bank_wrapper)
    c.emit(0xa9,0xb3);a(0x8d,bank_operand);c.emit(0xa9,0x24);a(0x8d,bank_operand+1);c.emit(0x60)
    c.label('hero')
    # Elapsed player ticks, coherent snapshot supplied by the main callback.
    a(0xad,0x83e2);c.emit(0x38,0xe9,START&255);a(0x8d,0x83ea)
    a(0xad,0x83e3);c.emit(0xe9,START>>8);a(0x8d,0x83eb)
    c.emit(0xc9,DUNK_OFFSET>>8);c.branch(0x90,'dribble');c.branch(0xd0,'dunk')
    a(0xad,0x83ea);c.emit(0xc9,DUNK_OFFSET&255);c.branch(0xb0,'dunk')
    c.label('dribble')
    a(0xad,0x83eb);c.branch(0xd0,'subtract_beat');a(0xad,0x83ea);c.emit(0xc9,187);c.branch(0x90,'dribble_phase')
    c.label('subtract_beat');a(0xad,0x83ea);c.emit(0x38,0xe9,187);a(0x8d,0x83ea);a(0xad,0x83eb);c.emit(0xe9,0);a(0x8d,0x83eb);c.jump(0x4c,'dribble')
    c.label('dribble_phase');c.emit(0x4a,0x4a);a(0x8d,0x83ff);c.emit(0xa9,0);a(0x8d,0x83ed)
    a(0xad,0x83ff);c.emit(0xc9,9,0xa9,0);c.branch(0x90,'pose_ready')
    a(0xad,0x83ff);c.emit(0xc9,18,0xa9,1);c.branch(0x90,'pose_ready')
    a(0xad,0x83ff);c.emit(0xc9,32,0xa9,6);c.branch(0x90,'pose_ready')
    a(0xad,0x83ff);c.emit(0xc9,42,0xa9,7);c.branch(0x90,'pose_ready')
    c.emit(0xa9,0);c.jump(0x4c,'pose_ready')
    c.label('dunk');a(0xad,0x83ea);c.emit(0x38,0xe9,DUNK_OFFSET&255);a(0x8d,0x83ea);a(0xad,0x83eb);c.emit(0xe9,DUNK_OFFSET>>8)
    for _ in range(4):c.emit(0x4a);a(0x6e,0x83ea)
    a(0xad,0x83ea);a(0x8d,0x83ff);c.emit(0xa9,1);a(0x8d,0x83ed)
    a(0xad,0x83ff);c.emit(0xc9,75,0xa9,5);c.branch(0xb0,'pose_ready')
    a(0xad,0x83ff);c.emit(0xc9,61,0xa9,4);c.branch(0xb0,'pose_ready')
    a(0xad,0x83ff);c.emit(0xc9,47,0xa9,3);c.branch(0xb0,'pose_ready');c.emit(0xa9,2)
    c.label('pose_ready');a(0x8d,0x83ec);c.emit(0xaa,0x09,0x50);a(0xcd,0x83fa);c.branch(0xd0,'changed');c.jump(0x4c,'wait')
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
    # Copy the remaining 192 bytes through the same operands with a local JSR.
    c.label('tail');c.jump(0x20,'tail_byte');c.emit(0xc8,0xc0,192);c.branch(0xd0,'tail')
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
    a(0xad,0x83e6);c.jump(0x8d,'dl1_hi');c.jump(0x8d,'dl2_hi')
    c.emit(0xa9,3);c.jump(0x8d,'dl1_lo');c.emit(0xa9,4);c.jump(0x8d,'dl2_lo');c.emit(0xa0,0)
    c.label('rows');c.jump(0xb9,'row_lo');c.label('dl1');c.emit(0x8d,0,0)
    c.jump(0xb9,'row_hi');c.emit(0x18);a(0x6d,0x83fe);c.label('dl2');c.emit(0x8d,0,0)
    for label in ('dl1','dl2'):
        c.emit(0x18);c.jump(0xad,label+'_lo');c.emit(0x69,3);c.jump(0x8d,label+'_lo');c.branch(0x90,label+'ok');c.jump(0xee,label+'_hi');c.label(label+'ok')
    c.emit(0xc8,0xc0,192);c.branch(0xd0,'rows')
    c.label('swap');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'swap')
    c.emit(0xa9,0);a(0x8d,0xd402);a(0xad,0x83e6);a(0x8d,0xd403);c.emit(0x49,4);a(0x8d,0x83e6)
    a(0xad,0x83ed);c.branch(0xf0,'wait')
    c.emit(0xa9,255);a(0x8d,0x83f8);a(0x8d,0x83f9)
    c.label('wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'wait')
    # Four rainbow bands and missile droplets use the existing PMG buffer.
    c.emit(0xa9,0,0xa2,0)
    c.label('clear');
    for base in (0x0980,0x0a00,0x0b00):a(0x9d,base)
    c.emit(0xe8);c.branch(0xd0,'clear')
    a(0xae,0x83ff);a(0xad,0x83ed);c.branch(0xd0,'dunk_ball')
    c.jump(0xbd,'dribble_x');a(0x8d,0x83e8);c.jump(0xbd,'dribble_y');c.jump(0x4c,'ball_position')
    c.label('dunk_ball');c.jump(0xbd,'dunk_x');a(0x8d,0x83e8);c.jump(0xbd,'dunk_y')
    c.label('ball_position');a(0x8d,0x83e9);c.emit(0xa8)
    a(0xad,0x83e8);c.emit(0x18,0x69,40)
    for i in range(4):a(0x8d,0xd000+i)
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x29,7,0x0a,0x0a,0x0a,0x0a,0xaa)
    c.label('spin');
    for i in range(4):c.jump(0xbd,f'spin{i}');a(0x99,0x0a00+i*128)
    c.emit(0xe8,0xc8,0x8a,0x29,15);c.branch(0xd0,'spin')
    for i,dx in enumerate((-14,-7,13,20)):
        a(0xad,0x83e8);c.emit(0x18,0x69,48+dx);a(0x8d,0xd004+i)
        a(0xad,0x83e9);c.emit(0x18,0x69,i*3);c.emit(0xa8)
        for dy in (1,6):
            a(0xb9,0x980+dy);c.emit(0x09,3<<(2*i));a(0x99,0x980+dy)
    a(0xad,0x83e2);c.emit(0x0a,0x0a,0x29,0xf0,0x09,10)
    for i in range(4):a(0x8d,0xd012+i);c.emit(0x18,0x69,0x40)
    for addr,val in ((0xd01a,0),(0xd016,0x48),(0xd017,0x9a),(0xd018,0x2c),(0xd407,8),(0xd01b,1),(0xd01d,3),(0xd400,0x2e),(0xd00c,0)):
        c.emit(0xa9,val);a(0x8d,addr)
    a(0xad,0x83ed);c.branch(0xf0,'no_flash');a(0xad,0x83ff);c.emit(0xc9,82);c.branch(0x90,'no_flash');c.emit(0xc9,85);c.branch(0xb0,'no_flash');c.emit(0xa9,14);a(0x8d,0xd017)
    c.label('no_flash');c.emit(0xa9,1,0xa2,3)
    c.label('sizes');a(0x9d,0xd008);c.emit(0xca);c.branch(0x10,'sizes');c.emit(0x60)
    # Tail helper borrows the already incremented copy operands.
    c.label('tail_byte')
    for source,target in (('read','tail_read'),('write','tail_write')):
        c.jump(0xad,source+'_lo');c.jump(0x8d,target+'_lo');c.jump(0xad,source+'_hi');c.jump(0x8d,target+'_hi')
    c.label('tail_read');c.emit(0xb9,0,0);c.label('tail_write');c.emit(0x99,0,0,0x60)
    for label in ('read','write','dl1','dl2','tail_read','tail_write'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    for label in ('patch_read','patch_write'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
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

def bank(bank_wrapper=0, bank_operand=0):
    out=bytearray(16384);code=helper(bank_wrapper,bank_operand);out[:len(code)]=code;payload=packed();out[DATA-ENTRY:DATA-ENTRY+len(payload)]=payload;return bytes(out)
