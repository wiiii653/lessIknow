"""Instrument full demo INITs without changing its runtime image."""
import argparse
from pathlib import Path
from build_sequence import Code
from build_visual_prototype import xex_segment
from extract_music import segments
import loading_screen as ls

def wrapper(number, target):
    c=Code(0x1200)
    for state in ('ENTER', 'RETURN'):
        if state=='RETURN':c.emit(0x20,target&255,target>>8)
        c.emit(0x08,0x48,0x8a,0x48,0x98,0x48)
        c.emit(0x20,ls.ENTRY&255,ls.ENTRY>>8,0xa2,0)
        c.label(state)
        c.jump(0xbd,state+'_text')
        c.emit(0x9d,0x28,0x06,0xe8,0xe0,40)
        c.branch(0xd0,state)
        c.emit(0x68,0xa8,0x68,0xaa,0x68,0x28)
    c.emit(0x60)
    for state in ('ENTER','RETURN'):
        c.label(state+'_text')
        c.emit(*(ord(x)-32 for x in f'INIT {number:02d} {state} ${target:04X}'.center(40)))
    data=bytes(c.finish())
    assert 0x1200+len(data)<=0x13e0
    return data

def build(data):
    out=bytearray(b'\xff\xff');out.extend(ls.segments())
    number=0; manifest=[]
    for start,end,payload in segments(data):
        if (start,end)==(0x02e2,0x02e3):
            target=int.from_bytes(payload,'little')
            if target!=ls.ENTRY:
                number+=1;manifest.append(f'{number:02d}: ${target:04X}')
                out.extend(xex_segment(0x1200,wrapper(number,target)))
                payload=bytes.fromhex('00 12')
        out.extend(xex_segment(start,payload))
    return bytes(out),'\n'.join(manifest)+'\n'

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    data,manifest=build(a.source.read_bytes())
    with a.output.open('xb') as f:f.write(data)
    a.output.with_suffix('.stages.txt').write_text(manifest)
