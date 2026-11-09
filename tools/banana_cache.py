"""Lifetime overlay: retired title banks become raw banana playback banks.

Prepare one 256-byte page per foreground callback before the first rotator.
The eight compressed source banks are expanded from the last frame backwards;
frames whose source overlaps their destination use spare title bank 48.
"""
from build_sequence import Code
from school_portrait_bank import bank_value
import banana_variants as variants
import mosaic

ENTRY=0xe580
BUFFER=0xea00
STATE=0xeb00
JOB,STAGE,FRAME,PAGE=STATE,STATE+1,STATE+2,STATE+3
SRC,OUTBANK,OUTHI,PEELED,STAGED=STATE+4,STATE+6,STATE+7,STATE+8,STATE+9
READBANK,READHI,WRITEBANK,WRITEHI,N=STATE+10,STATE+11,STATE+12,STATE+13,STATE+14
FLAG=0x0ddf
RESOURCE_BANK=46
SPARE=48
BOOT=0x6800
SOURCE=0x6000
SELECT=0xe940


def helper_templates():
    return b''.join(mosaic.helper(0x7c00,cache_key=variants.KEY,banana_only=True,
                                  cache_address=variants.CACHE,raw=True,peeled=bool(v)).ljust(1024,b'\0')
                    for v in range(2))


def worker():
    c=Code(ENTRY)
    def a(op,v):c.emit(op,v&255,v>>8)
    def setv(addr,v):c.emit(0xa9,v);a(0x8d,addr)
    def bank_original():a(0xae,JOB);a(0xbd,bank_value(3));a(0x8d,0xd301)
    c.label('service');a(0xad,FLAG);c.emit(0xc9,2);c.branch(0xd0,'work');c.emit(0x60)
    c.label('work');a(0xad,0xd301);c.emit(0x48)
    a(0xad,STAGE)
    for stage,label in enumerate(('templates','setup','decode','copyback','helpers')):
        c.emit(0xc9,stage);c.branch(0xd0,f'not{stage}');c.jump(0x20,label);c.jump(0x4c,'return');c.label(f'not{stage}')
    c.label('return');c.emit(0x68);a(0x8d,0xd301);c.emit(0x60)
    c.label('templates')
    a(0xad,bank_value(RESOURCE_BANK));a(0x8d,READBANK);a(0xad,bank_value(SPARE));a(0x8d,WRITEBANK)
    a(0xad,PAGE);c.emit(0x18,0x69,0x54);a(0x8d,READHI)
    a(0xad,PAGE);c.emit(0x18,0x69,0x60);a(0x8d,WRITEHI);c.jump(0x20,'copy_page')
    a(0xee,PAGE);a(0xad,PAGE);c.emit(0xc9,8);c.branch(0xd0,'template_done');setv(STAGE,1);setv(FRAME,4)
    c.label('template_done');c.emit(0x60)
    c.label('setup');bank_original();a(0xae,FRAME);a(0xbd,variants.POINTERS);a(0x8d,SRC);a(0xbd,variants.POINTERS+8);a(0x8d,SRC+1)
    a(0xad,FRAME);c.emit(0x29,3,0xaa);c.jump(0xbd,'frame_hi');a(0x8d,OUTHI)
    setv(PAGE,0);setv(STAGED,0)
    a(0xad,FRAME);c.emit(0xc9,4);c.branch(0x90,'bunch')
    a(0xae,JOB);a(0xbd,bank_value(40));a(0x8d,OUTBANK);c.jump(0x4c,'setup_done')
    c.label('bunch');a(0xae,JOB);a(0xbd,bank_value(3));a(0x8d,OUTBANK)
    # Direct output is safe only when the entire compressed frame precedes it.
    a(0xae,FRAME);c.emit(0xe8);a(0xbd,variants.POINTERS+8);a(0xcd,OUTHI);c.branch(0x90,'setup_done')
    c.branch(0xd0,'stage_frame');a(0xbd,variants.POINTERS);c.branch(0xf0,'setup_done')
    c.label('stage_frame');setv(STAGED,1);a(0xad,bank_value(SPARE));a(0x8d,OUTBANK);setv(OUTHI,0x40)
    c.label('setup_done');setv(STAGE,2);c.emit(0x60)
    c.label('decode');bank_original();c.jump(0x20,'decode_page')
    a(0xad,OUTBANK);a(0x8d,WRITEBANK);a(0xad,OUTHI);c.emit(0x18);a(0x6d,PAGE);a(0x8d,WRITEHI);c.jump(0x20,'write_page')
    a(0xee,PAGE);a(0xad,PAGE);c.emit(0xc9,15);c.branch(0xd0,'decode_done')
    a(0xad,STAGED);c.branch(0xf0,'advance_frame');setv(PAGE,0);setv(STAGE,3)
    c.label('decode_done');c.emit(0x60)
    c.label('copyback');a(0xad,bank_value(SPARE));a(0x8d,READBANK);a(0xae,JOB);a(0xbd,bank_value(3));a(0x8d,WRITEBANK)
    a(0xad,PAGE);c.emit(0x18,0x69,0x40);a(0x8d,READHI)
    a(0xae,FRAME);c.jump(0xbd,'frame_hi');c.emit(0x18);a(0x6d,PAGE);a(0x8d,WRITEHI);c.jump(0x20,'copy_page')
    a(0xee,PAGE);a(0xad,PAGE);c.emit(0xc9,15);c.branch(0xf0,'advance_frame');c.emit(0x60)
    c.label('advance_frame');a(0xad,FRAME);c.emit(0xc9,4);c.branch(0x90,'bunch_next')
    a(0xee,FRAME);a(0xad,FRAME);c.emit(0xc9,8);c.branch(0xf0,'helper_start');c.jump(0x4c,'next_frame')
    c.label('bunch_next');a(0xce,FRAME);c.branch(0x30,'helper_start')
    c.label('next_frame');setv(STAGE,1);c.emit(0x60)
    c.label('helper_start');setv(PAGE,0);setv(STAGE,4);c.emit(0x60)
    c.label('helpers');a(0xad,bank_value(SPARE));a(0x8d,READBANK)
    a(0xad,PEELED);c.branch(0xd0,'helper_bunch');a(0xae,JOB);a(0xbd,bank_value(40));a(0x8d,WRITEBANK)
    a(0xad,PAGE);c.emit(0x18,0x69,0x64);a(0x8d,READHI);c.jump(0x4c,'helper_copy')
    c.label('helper_bunch');a(0xae,JOB);a(0xbd,bank_value(3));a(0x8d,WRITEBANK)
    a(0xad,PAGE);c.emit(0x18,0x69,0x60);a(0x8d,READHI)
    c.label('helper_copy');a(0xad,PAGE);c.emit(0x18,0x69,0x7c);a(0x8d,WRITEHI);c.jump(0x20,'copy_page')
    a(0xee,PAGE);a(0xad,PAGE);c.emit(0xc9,4);c.branch(0xf0,'helper_finished');c.emit(0x60)
    c.label('helper_finished');a(0xad,PEELED);c.branch(0xd0,'job_finished');setv(PEELED,1);setv(FRAME,3);c.jump(0x4c,'next_frame')
    c.label('job_finished');a(0xee,JOB);a(0xad,JOB);c.emit(0xc9,8);c.branch(0xf0,'ready');setv(PEELED,0);setv(FRAME,4);c.jump(0x4c,'next_frame')
    c.label('ready');setv(FLAG,2);c.emit(0x60)
    c.label('copy_page');a(0xad,READBANK);a(0x8d,0xd301);a(0xad,READHI);c.jump(0x8d,'read_hi');c.emit(0xa0,0)
    c.label('read_loop');c.label('read');c.emit(0xb9,0,0x40);a(0x99,BUFFER);c.emit(0xc8);c.branch(0xd0,'read_loop')
    c.label('write_page');a(0xad,WRITEBANK);a(0x8d,0xd301);a(0xad,WRITEHI);c.jump(0x8d,'write_hi');c.emit(0xa0,0)
    c.label('write_loop');a(0xb9,BUFFER);c.label('write');c.emit(0x99,0,0x40,0xc8);c.branch(0xd0,'write_loop');c.emit(0x60)
    c.label('decode_page');a(0xad,SRC+1)
    for label in ('control','literal','value'):c.jump(0x8d,label+'_hi')
    a(0xae,SRC);c.emit(0xa0,0)
    c.label('packet');c.label('control');c.emit(0xbd,0,0x40);c.branch(0xd0,'packet_nonzero');c.jump(0x20,'source_page');c.jump(0x4c,'packet')
    c.label('packet_nonzero');c.emit(0xe8);c.branch(0xd0,'control_next');c.emit(0x48);c.jump(0x20,'source_page');c.emit(0x68)
    c.label('control_next');c.emit(0x09,0);c.branch(0x30,'run')
    a(0x8c,N);c.emit(0x18);a(0x6d,N);c.jump(0x8d,'literal_end_lo')
    c.label('literal_loop');c.label('literal');c.emit(0xbd,0,0x40);a(0x99,BUFFER);c.emit(0xe8);c.branch(0xd0,'literal_next');c.jump(0x20,'source_page')
    c.label('literal_next');c.emit(0xc8);c.label('literal_end');c.emit(0xc0,0);c.branch(0xd0,'literal_loop');c.jump(0x4c,'packet_done')
    c.label('run');c.emit(0x29,127);a(0x8c,N);c.emit(0x18);a(0x6d,N);c.jump(0x8d,'run_end_lo');c.label('value');c.emit(0xbd,0,0x40,0xe8);c.branch(0xd0,'value_next');c.emit(0x48);c.jump(0x20,'source_page');c.emit(0x68)
    c.label('value_next');c.label('run_loop');a(0x99,BUFFER);c.emit(0xc8);c.label('run_end');c.emit(0xc0,0);c.branch(0xd0,'run_loop')
    c.label('packet_done');c.emit(0xc0,0);c.branch(0xd0,'packet');a(0x8e,SRC);c.jump(0xad,'control_hi');a(0x8d,SRC+1);c.emit(0x60)
    c.label('source_page');c.emit(0xa2,0)
    for label in ('control','literal','value'):c.jump(0xee,label+'_hi')
    c.emit(0x60)
    c.label('frame_hi');c.emit(0x40,0x4f,0x5e,0x6d)
    for label in ('read','write','control','literal','value'):c.labels[label+'_hi']=c.labels[label]+2
    for label in ('literal_end','run_end'):c.labels[label+'_lo']=c.labels[label]+1
    assert c.origin+len(c.data)<=SELECT,(len(c.data),hex(c.origin+len(c.data)))
    c.emit(*bytes(SELECT-c.origin-len(c.data)))
    # Only needed for seeks during preparation; normal playback is fully ready.
    c.label('select');a(0x2c,variants.KEY);c.branch(0x50,'selected');a(0xec,JOB);c.branch(0x90,'peeled_raw');c.branch(0xd0,'selected')
    a(0xad,PEELED);c.branch(0xf0,'selected')
    c.label('peeled_raw');c.emit(0x8a,0x18,0x69,37,0xaa)
    c.label('selected');c.emit(0x60)
    code=c.finish();assert ENTRY+len(code)<=BUFFER,(len(code),hex(ENTRY+len(code)))
    return bytes(code)


def bootstrap(hook_address):
    code=worker();c=Code(BOOT)
    def a(op,v):c.emit(op,v&255,v>>8)
    # Copy retired-intro replacement while the resource bank is selected.
    for page in range((len(code)+255)//256):
        c.emit(0xa0,0);c.label(f'p{page}');a(0xb9,SOURCE+page*256);a(0x99,ENTRY+page*256);c.emit(0xc8);c.branch(0xd0,f'p{page}')
    c.emit(0xa9,0,0xa2,31);c.label('clear');a(0x9d,STATE);c.emit(0xca);c.branch(0x10,'clear')
    c.emit(0xa9,ENTRY&255);a(0x8d,hook_address+1);c.emit(0xa9,ENTRY>>8);a(0x8d,hook_address+2)
    c.emit(0xa9,1);a(0x8d,FLAG);c.emit(0x60)
    return bytes(c.finish())


def install(bank,index,hook_address):
    if index!=RESOURCE_BANK:return bank
    out=bytearray(bank)
    for address,data in ((0x5400,helper_templates()),(SOURCE,worker()),(BOOT,bootstrap(hook_address))):
        offset=address-0x4000
        assert not any(out[offset:offset+len(data)]),(hex(address),len(data))
        out[offset:offset+len(data)]=data
    return bytes(out)
