"""One additional video bank following the player's detected fourteen banks."""
from build_sequence import Code
from build_visual_prototype import xex_segment
BANK_VALUE=0x24b3
DOTS=0x0641
DOT_STATE=0x06ff

def bank_value(index):
    return BANK_VALUE+index if index<3 else 0x08c0+index

def loader(frame, index=0, progress=False):
    assert len(frame) in (8192,16384)
    c=Code(0x1000)
    c.emit(0x08,0x78,0xad,1,0xd3,0x48)
    if index<2:
        # Continue the two remaining slots in the original sixteen-bank group.
        c.emit(0xae,0xfc,0x26,0xe0,0x81)
        c.branch(0xf0,'two')
        c.emit(0xa9,4*(index+1));c.jump(0x4c,'add')
        c.label('two');c.emit(0xa9,2*(index+1))
        c.label('add');c.emit(0x18,0x6d,9,0x27,0x8d,1,0xd3,0x29,0xfe,0x8d,0xb3+index,0x24)
    else:
        if not 2<=index<50:raise ValueError('1 MB bank limit')
        destination=bank_value(index)
        # Probe the next bank without aliasing any of the sixteen loaded banks.
        c.emit(0xa2,0)
        c.label('candidate');c.jump(0xbd,'candidates');c.emit(0x8d,0xb7,0x24,0x8d,1,0xd3,0xad,0,0x40,0x8d,0xb6,0x24,0xa9,0x55,0x8d,0,0x40,0xa0,0)
        c.label('known_loop');c.jump(0x20,'known');c.emit(0xc9,0x55);c.branch(0xd0,'next_known')
        c.emit(0xad,0xb7,0x24,0x8d,1,0xd3,0xa9,0xaa,0x8d,0,0x40)
        c.jump(0x20,'known');c.emit(0xc9,0xaa);c.branch(0xf0,'alias')
        c.emit(0xad,0xb7,0x24,0x8d,1,0xd3,0xa9,0x55,0x8d,0,0x40)
        c.label('next_known');c.emit(0xc8,0xc0,14+index);c.branch(0xd0,'known_loop')
        c.jump(0x20,'restore_probe');c.emit(0xad,0xb7,0x24,0x29,0xfe,0x8d,destination&255,destination>>8)
        c.jump(0x4c,'probe_done')
        c.label('alias');c.jump(0x20,'restore_probe');c.emit(0xe8,0xe0,64);c.branch(0x90,'candidate')
        c.label('no_bank');c.emit(0xa9,0x32,0x8d,0x1a,0xd0);c.jump(0x4c,'no_bank')
        c.label('known');c.emit(0xc0,17);c.branch(0x90,'first_group');c.emit(0xb9,0xb2,0x08);c.jump(0x4c,'read_known')
        c.label('first_group');c.emit(0xc0,14);c.branch(0x90,'original_known');c.emit(0xb9,0xa5,0x24);c.jump(0x4c,'read_known')
        c.label('original_known');c.emit(0xb9,0xfc,0x26)
        c.label('read_known');c.emit(0x09,1,0x8d,1,0xd3,0xad,0,0x40,0x60)
        c.label('restore_probe');c.emit(0xad,0xb7,0x24,0x8d,1,0xd3,0xad,0xb6,0x24,0x8d,0,0x40,0x60)
        c.label('candidates');c.emit(*[b+i+1 for b in (0x80,0xa0,0xc0,0xe0,0,0x20,0x40,0x60) for i in range(0,16,2)])
        c.label('probe_done')
    c.emit(0xa2,len(frame)//256,0xa0,0)
    c.label('copy');c.label('read');c.emit(0xb9,0,0x80);c.label('write');c.emit(0x99,0,0x40,0xc8);c.branch(0xd0,'copy')
    for label in ('read','write'):
        addr=c.labels[label]+2;c.emit(0xee,addr&255,addr>>8)
    c.emit(0xca);c.branch(0xd0,'copy')
    if progress:
        # Advance the loader ellipsis once after each bank has been copied.
        # The label stays fixed; only these three screen cells change.
        c.emit(0xee,DOT_STATE&255,DOT_STATE>>8,0xad,DOT_STATE&255,DOT_STATE>>8,
               0x29,0x03,0x8d,DOT_STATE&255,DOT_STATE>>8,
               0xc9,0x00);c.branch(0xf0,'dots_none')
        c.emit(0xc9,0x01);c.branch(0xf0,'dots_one')
        c.emit(0xc9,0x02);c.branch(0xf0,'dots_two')
        c.emit(0xa9,14)
        for address in range(DOTS,DOTS+3): c.emit(0x8d,address&255,address>>8)
        c.jump(0x4c,'dots_done')
        c.label('dots_none')
        c.emit(0xa9,0)
        for address in range(DOTS,DOTS+3): c.emit(0x8d,address&255,address>>8)
        c.jump(0x4c,'dots_done')
        c.label('dots_one')
        c.emit(0xa9,14,0x8d,DOTS&255,DOTS>>8,0xa9,0)
        for address in range(DOTS+1,DOTS+3): c.emit(0x8d,address&255,address>>8)
        c.jump(0x4c,'dots_done')
        c.label('dots_two')
        c.emit(0xa9,14)
        for address in range(DOTS,DOTS+2): c.emit(0x8d,address&255,address>>8)
        c.emit(0xa9,0,0x8d,(DOTS+2)&255,(DOTS+2)>>8)
        c.label('dots_done')
    c.emit(0x68,0x8d,1,0xd3,0x28,0x60)
    return xex_segment(0x8000,frame)+xex_segment(0x1000,c.finish())+xex_segment(0x2e2,b'\x00\x10')
