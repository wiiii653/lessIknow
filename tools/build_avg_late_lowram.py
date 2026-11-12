"""Stage low runtime RAM until the final non-returning INIT."""
import argparse
from pathlib import Path
from build_sequence import Code
from build_visual_prototype import xex_segment
from extract_music import segments

LOW=((0x0400,0x07e4),(0x0800,0x08bf),(0x0900,0x0974),
     (0x0980,0x09ff),(0x0a00,0x0bff))

def bootstrap(low=LOW):
    c=Code(0x4800)
    c.emit(0x78,0xa9,0,0x8d,0x0e,0xd4) # disable interrupts and NMI
    for index,(start,end) in enumerate(low):
        size=end-start+1
        full,tail=divmod(size,256)
        for page in range(full):
            src=0x4000+start-0x0400+page*256
            dst=start+page*256
            c.emit(0xa0,0);c.label(f'page{index}_{page}')
            c.emit(0xb9,src&255,src>>8,0x99,dst&255,dst>>8,0xc8)
            c.branch(0xd0,f'page{index}_{page}')
        if tail:
            src=0x4000+start-0x0400+full*256
            dst=start+full*256
            c.emit(0xa0,0);c.label(f'tail{index}')
            c.emit(0xb9,src&255,src>>8,0x99,dst&255,dst>>8,0xc8,0xc0,tail)
            c.branch(0xd0,f'tail{index}')
    c.emit(0x4c,0xe0,0x13)
    return bytes(c.finish())

def build(data):
    entries=list(segments(data)); last=max(i for i,(a,b,p) in enumerate(entries) if (a,b)==(0x02e2,0x02e3))
    limits={0x0400:0x07ff,0x0800:0x08bf,0x0900:0x097f,0x0980:0x09ff,0x0a00:0x0bff}
    low=tuple(sorted((a,b) for a,b,p in entries[last+1:] if a in limits))
    assert len(low)==len(limits) and {a for a,b in low}==set(limits),low
    assert all(a<=b<=limits[a] for a,b in low),low
    assert all((a,b) in low for a,b,p in entries[last+1:] if a<=0x0bff and b>=0x0400)
    staged=bytearray(0x800);found=set();out=bytearray(b'\xff\xff')
    for i,(a,b,p) in enumerate(entries):
        if i>last and (a,b) in low:
            staged[a-0x400:b-0x400+1]=p;found.add((a,b));continue
        if (a,b)==(0x02e0,0x02e1):
            assert found==set(low),found
            out.extend(xex_segment(0x4000,staged))
            out.extend(xex_segment(0x4800,bootstrap(low)))
            out.extend(xex_segment(0x02e2,b'\x00\x48'))
        out.extend(xex_segment(a,p))
    return bytes(out)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    with a.output.open('xb') as f:f.write(build(a.source.read_bytes()))
