"""Act 3: low-angle dribble then slow-motion dunk, with a PMG ball."""
import math
from pathlib import Path
from build_sequence import Code
from rainbow_ball import spin_masks
START,DUNK,END=20944,22440,23936
ENTRY,DATA,HEIGHT=0x4000,0x4b80,56
BANK_VALUE=0x24b4

def frames():
    rgb=Path('build/basketball-hero.rgb').read_bytes()
    palette=((0,0,0),(255,50,160),(0,220,255),(255,190,150))
    assert len(rgb)==320*168*3
    p=bytes(min(range(4),key=lambda j:sum((rgb[i+c]-palette[j][c])**2 for c in range(3))) for i in range(0,len(rgb),3))
    return [bytes(p[(r*56+y)*320+col*160+x] for y in range(56) for x in range(160)) for r in range(3) for col in range(2)]

def packed():
    return b''.join(bytes(sum(p[y*160+x+k]<<(6-2*k) for k in range(4)) for y in range(56) for x in range(0,160,4)) for p in frames())

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
    c.label('trevor');a(0xad,0x83e3);c.emit(0xc9,26928>>8);c.branch(0x90,'trevor_quiet')
    c.branch(0xd0,'trevor_tunnel');a(0xad,0x83e2);c.emit(0xc9,26928&255);c.branch(0x90,'trevor_quiet')
    c.label('trevor_tunnel');a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x18,0x69,0xd8);c.jump(0x4c,'trevor_bank_ready')
    c.label('trevor_quiet');c.emit(0xa9,0xd8)
    c.label('trevor_bank_ready');a(0x8d,bank_operand)
    c.emit(0xa9,0x08);a(0x8d,bank_operand+1);a(0x20,bank_wrapper)
    c.emit(0xa9,0xb3);a(0x8d,bank_operand);c.emit(0xa9,0x24);a(0x8d,bank_operand+1);c.emit(0x60)
    c.label('hero')
    # Elapsed player ticks, coherent snapshot supplied by the main callback.
    a(0xad,0x83e2);c.emit(0x38,0xe9,START&255);a(0x8d,0x83ea)
    a(0xad,0x83e3);c.emit(0xe9,START>>8);a(0x8d,0x83eb)
    c.emit(0xc9,1496>>8);c.branch(0x90,'dribble');c.branch(0xd0,'dunk')
    a(0xad,0x83ea);c.emit(0xc9,1496&255);c.branch(0xb0,'dunk')
    c.label('dribble')
    a(0xad,0x83eb);c.branch(0xd0,'subtract_beat');a(0xad,0x83ea);c.emit(0xc9,187);c.branch(0x90,'dribble_phase')
    c.label('subtract_beat');a(0xad,0x83ea);c.emit(0x38,0xe9,187);a(0x8d,0x83ea);a(0xad,0x83eb);c.emit(0xe9,0);a(0x8d,0x83eb);c.jump(0x4c,'dribble')
    c.label('dribble_phase');c.emit(0x4a,0x4a);a(0x8d,0x83ff);c.emit(0xa9,0);a(0x8d,0x83ed)
    a(0xad,0x83ff);c.emit(0xc9,24,0xa9,0);c.branch(0x90,'pose_ready');c.emit(0xa9,1);c.jump(0x4c,'pose_ready')
    c.label('dunk');a(0xad,0x83ea);c.emit(0x38,0xe9,1496&255);a(0x8d,0x83ea);a(0xad,0x83eb);c.emit(0xe9,1496>>8)
    for _ in range(4):c.emit(0x4a);a(0x6e,0x83ea)
    a(0xad,0x83ea);a(0x8d,0x83ff);c.emit(0xa9,1);a(0x8d,0x83ed)
    a(0xad,0x83ff);c.emit(0xc9,75,0xa9,5);c.branch(0xb0,'pose_ready')
    a(0xad,0x83ff);c.emit(0xc9,61,0xa9,4);c.branch(0xb0,'pose_ready')
    a(0xad,0x83ff);c.emit(0xc9,47,0xa9,3);c.branch(0xb0,'pose_ready');c.emit(0xa9,2)
    c.label('pose_ready');a(0x8d,0x83ec);c.emit(0xaa,0x09,0x50);a(0xcd,0x83fa);c.branch(0xd0,'changed');c.jump(0x4c,'wait')
    c.label('changed');a(0x8d,0x83fa)
    c.jump(0xbd,'source_lo');c.jump(0x8d,'read_lo');c.jump(0xbd,'source_hi');c.jump(0x8d,'read_hi')
    a(0xad,0x83e6);c.emit(0x29,4,0x0a,0x0a,0x0a,0x49,0xb0);a(0x8d,0x83fe);c.jump(0x8d,'write_hi')
    c.emit(0xa9,0);c.jump(0x8d,'write_lo');c.emit(0xa2,8,0xa0,0)
    c.label('copy');c.label('read');c.emit(0xb9,0,0);c.label('write');c.emit(0x99,0,0,0xc8);c.branch(0xd0,'copy')
    for label in ('read_hi','write_hi'):c.jump(0xee,label)
    c.emit(0xca);c.branch(0xd0,'copy')
    # Copy the remaining 192 bytes through the same operands with a local JSR.
    c.label('tail');c.jump(0x20,'tail_byte');c.emit(0xc8,0xc0,192);c.branch(0xd0,'tail')
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
    c.label('source_lo');c.emit(*((DATA+i*2240)&255 for i in range(6)))
    c.label('source_hi');c.emit(*((DATA+i*2240)>>8 for i in range(6)))
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
    out=bytearray(16384);code=helper(bank_wrapper,bank_operand);out[:len(code)]=code;out[DATA-ENTRY:]=packed();return bytes(out)
