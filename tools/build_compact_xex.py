"""Reduce XEX size by clearing staging RAM and omitting long zero runs."""
import argparse
from pathlib import Path
from build_sequence import Code
from build_visual_prototype import xex_segment
from extract_music import segments

def clear_code():
    c=Code(0x3a00)
    c.emit(0x08,0x78,0x48,0x8a,0x48,0x98,0x48)
    c.emit(0xa9,0x80);c.jump(0x8d,'store_hi')
    c.emit(0xa9,0,0xa2,0x40,0xa0,0)
    c.label('loop');c.emit(0x99,0x00);c.label('store_hi');c.emit(0x80)
    c.emit(0xc8);c.branch(0xd0,'loop')
    c.jump(0xee,'store_hi');c.emit(0xca);c.branch(0xd0,'loop')
    c.emit(0x68,0xa8,0x68,0xaa,0x68,0x28,0x60)
    return bytes(c.finish())

def build(data):
    out=bytearray(b'\xff\xff');count=0
    for start,end,blob in segments(data):
        if (start,end)!=(0x8000,0xbfff):
            out.extend(xex_segment(start,blob));continue
        count+=1
        out.extend(xex_segment(0x3a00,clear_code()))
        out.extend(xex_segment(0x02e2,b'\x00\x3a'))
        # A segment header costs four bytes. Longer zero runs are omitted;
        # short ones remain inside the neighbouring data segment.
        pos=0
        while pos<len(blob):
            while pos<len(blob) and blob[pos]==0:pos+=1
            if pos==len(blob):break
            first=pos
            while pos<len(blob):
                if blob[pos]!=0:pos+=1;continue
                stop=pos
                while stop<len(blob) and blob[stop]==0:stop+=1
                if stop-pos>=16:break
                pos=stop
            out.extend(xex_segment(0x8000+first,blob[first:pos]))
    assert count==64,count
    return bytes(out)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    result=build(a.source.read_bytes())
    with a.output.open('xb') as f:f.write(result)
    print(f'{len(result)} bytes; {len(result)/1048576:.3f} MiB')
