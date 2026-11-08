#!/usr/bin/env python3
"""Standalone pompom dance: original v035 music plus six preserved art banks."""
import argparse
import json
from pathlib import Path
from build_sequence import Code, dance_group_pixels
from dance_banks import frame_blob, frame_address
from extract_music import segments
import engine_effects

ENTRY=0x1000
STATE=0x13e0
EFFECT=0x1c00


def segment(address,data):
    return address.to_bytes(2,'little')+(address+len(data)-1).to_bytes(2,'little')+data


def packed(pixels):
    rows=[bytes(sum(pixels[y*160+x+k]<<(6-k*2) for k in range(4)) for x in range(0,160,4)) for y in range(192)]
    return frame_blob(rows)


def build(output,replace=False):
    if output.exists() and not replace:raise FileExistsError(output)
    art=b''.join(packed(dance_group_pixels(phase,count)) for count in (1,2,3) for phase in range(4))
    reference=Path('reference/dance_frames_v141.bin').read_bytes()
    assert art==reference,'preserved art changed from v141'
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    # The original player invokes this callback once per four music DLIs.
    c.label('snapshot')
    for i in (2,1,0):a(0xad,0x24a7+i);a(0x8d,STATE+2+i)
    for i in (1,2):a(0xad,0x24a7+i);a(0xcd,STATE+2+i);c.branch(0xd0,'snapshot')
    for i in (0,1):a(0xad,STATE+2+i);a(0x8d,STATE+8+i)
    c.label('mod')
    a(0xad,STATE+9);c.emit(0xc9,2992>>8);c.branch(0x90,'group');c.branch(0xd0,'subtract')
    a(0xad,STATE+8);c.emit(0xc9,2992&255);c.branch(0x90,'group')
    c.label('subtract');c.emit(0x38);a(0xad,STATE+8);c.emit(0xe9,2992&255);a(0x8d,STATE+8)
    a(0xad,STATE+9);c.emit(0xe9,2992>>8);a(0x8d,STATE+9);c.jump(0x4c,'mod')
    c.label('group');c.emit(0xa2,2)
    c.label('find_group');a(0xad,STATE+9);c.jump(0xdd,'group_hi');c.branch(0x90,'previous')
    c.branch(0xd0,'group_ready');a(0xad,STATE+8);c.jump(0xdd,'group_lo');c.branch(0xb0,'group_ready')
    c.label('previous');c.emit(0xca);c.branch(0x10,'find_group')
    c.label('group_ready');c.emit(0x8a,0x0a,0x0a);a(0x8d,STATE+7)
    a(0xad,STATE+2);c.emit(0x4a,0x4a,0x4a,0x4a,0x29,3,0x48,0x18);a(0x6d,STATE+7);a(0x8d,STATE+7)
    c.emit(0x68,0x18,0x69,2);a(0x8d,STATE)
    a(0xad,STATE+7);a(0xcd,STATE+26);c.branch(0xd0,'changed');c.jump(0x4c,'effects')
    c.label('changed');a(0x8d,STATE+26)
    c.emit(0x48,0x4a,0x18,0x69,8,0xaa);a(0xad,0xd301);c.emit(0x48)
    a(0xbd,0x26fc);a(0x8d,0xd301)
    a(0xad,STATE+7);c.emit(0x29,1,0x0a,0x0a,0x0a,0x0a,0x0a,0x09,0x40);c.jump(0x8d,'read_hi')
    a(0xad,STATE+6);c.jump(0x8d,'write_hi');c.emit(0xa0,0,0xa2,32)
    c.label('copy');c.label('read');c.emit(0xb9,0,0x40);c.label('write');c.emit(0x99,0,0xa0)
    c.emit(0xc8);c.branch(0xd0,'copy');c.jump(0xee,'read_hi');c.jump(0xee,'write_hi');c.emit(0xca);c.branch(0xd0,'copy')
    c.emit(0x68);a(0x8d,0xd301);c.emit(0x68)
    c.label('swap_wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'swap_wait');c.emit(0xc9,128);c.branch(0xb0,'swap_wait')
    a(0xad,STATE+6);c.emit(0xc9,0xa0);c.branch(0xf0,'dl_second')
    c.emit(0xa9,0x14);c.jump(0x4c,'dl_ready')
    c.label('dl_second');c.emit(0xa9,0x18)
    c.label('dl_ready');a(0x8d,0xd403);c.emit(0xa9,0);a(0x8d,0xd402)
    a(0xad,STATE+6);c.emit(0x49,0x20);a(0x8d,STATE+6)
    c.label('effects')
    c.label('effect_wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'effect_wait')
    for addr,value in ((0xd01a,0),(0xd016,0x5a),(0xd017,0xac),(0xd018,0x2e)):
        c.emit(0xa9,value);a(0x8d,addr)
    a(0x20,EFFECT);c.emit(0x60)
    c.label('music_entry');c.emit(0x48,0x8a,0x48,0x98,0x48);a(0x8d,0xd40a)
    a(0xad,0xd301);a(0x8d,STATE+14);a(0xac,0x24a5);a(0xb9,0x26fc);a(0x8d,0xd301);a(0x4c,0x2218)
    c.label('music_exit');a(0xad,STATE+14);a(0x8d,0xd301);c.emit(0x68,0xa8,0x68,0xaa,0x68,0x40)
    c.labels['read_hi']=c.labels['read']+2;c.labels['write_hi']=c.labels['write']+2
    c.label('group_lo');c.emit(*(v&255 for v in (0,748,1496)))
    c.label('group_hi');c.emit(*(v>>8 for v in (0,748,1496)))
    code=c.finish();assert ENTRY+len(code)<=STATE
    engine_effects.EFFECT_ORIGIN=EFFECT
    effect=engine_effects.effects_helper(state=STATE)
    assert EFFECT+len(effect)<0x2000
    def display(base,framebuffer):
        out=bytearray((0x80,0x70))
        for y in range(192):
            addr=frame_address(framebuffer,y)
            out.extend((0x4e|(0x80 if y+9 in (78,156) else 0),addr&255,addr>>8))
        out.extend((0x70,0x70,0x70,0x70,0x90,0x41,base&255,base>>8))
        return out
    state=bytearray(32);state[6]=0xa0;state[26]=255
    missiles,players=engine_effects.pmg_art()
    inserts=[(ENTRY,code),(STATE,state),(0x1400,display(0x1400,0x8000)),
             (0x1800,display(0x1800,0xa000)),(EFFECT,effect),(0x980,missiles),(0xa00,players)]
    # Split clears so the shared test memory loader does not mistake these
    # unbanked buffers for 8 KiB bank INIT payloads.
    for addr in (0x8000,0xa000):inserts.extend(((addr,bytes(8191)),(addr+8191,b'\0')))
    result=bytearray(b'\xff\xff');bank=-1
    for lo,hi,payload in segments(Path('player/less-i-know-release-v035.xex').read_bytes()):
        if (lo,hi)==(0x8000,0xbfff):
            bank+=1
            if bank>=8:
                assert set(payload)=={255}
                payload=art[(bank-8)*16384:(bank-7)*16384]
        if (lo,hi)==(0x2000,0x24b2):
            payload=bytearray(payload)
            assert payload[0x21bc-lo:0x21bc-lo+10]==bytes.fromhex('a9 00 8d 02 d4 a9 33 8d 03 d4')
            payload[0x21c2-lo]=0x14
            payload[0x220a-lo:0x220d-lo]=bytes((0x20,ENTRY&255,ENTRY>>8))
            payload[0x2210-lo:0x2213-lo]=bytes((0x4c,))+c.labels['music_entry'].to_bytes(2,'little')
            payload[0x2312-lo:0x2318-lo]=bytes((0x4c,))+c.labels['music_exit'].to_bytes(2,'little')+bytes((0xea,))*3
        if (lo,hi)==(0x2e0,0x2e1):
            for addr,data in inserts:result.extend(segment(addr,data))
        result.extend(segment(lo,payload))
    assert bank==13
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(result)
    output.with_suffix('.json').write_text(json.dumps({'callback':ENTRY,'state':STATE,
        'frame_count':12,'art_banks':6,'frame_bytes':8192,'framebuffers':[0x8000,0xa000],
        'display_lists':[0x1400,0x1800],'music_entry':c.labels['music_entry'],
        'music_exit':c.labels['music_exit'],'code_bytes':len(code)},indent=2)+'\n')
    (output.parent/'dance_frames.bin').write_bytes(art)
    print(f'Built {output}: {len(result)} bytes, 12 preserved frames / 6 art banks')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('build/pompom-dance-dev.xex'))
    parser.add_argument('--replace',action='store_true')
    args=parser.parse_args();build(args.output,args.replace)
