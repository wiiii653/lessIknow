"""Show each segment after the last main INIT in the compact AVG candidate."""
from pathlib import Path
from build_sequence import Code
from build_visual_prototype import xex_segment
from extract_music import segments
import loading_screen as ls

SOURCE=Path('releases/avg-compact-late-start-001.xex')
OUTPUT=Path('releases/avg-final-segment-trace-001.xex')

def marker(index,start,end):
    c=Code(0x5100)
    c.emit(0x08,0x48,0x8a,0x48,0x98,0x48,0x20,0xa0,0x50,0xa2,0)
    c.label('copy');c.jump(0xbd,'text')
    c.emit(0x9d,0x28,0x50,0xe8,0xe0,40);c.branch(0xd0,'copy')
    c.emit(0x68,0xa8,0x68,0xaa,0x68,0x28,0x60)
    c.label('text')
    c.emit(*(ord(x)-32 for x in f'POST {index:02d} ${start:04X}-${end:04X}'.center(40)))
    return bytes(c.finish())

def main():
    entries=list(segments(SOURCE.read_bytes()))
    last=max(i for i,(a,b,p) in enumerate(entries) if (a,b,p)==(0x02e2,0x02e3,b'\x00\x39'))
    out=bytearray(b'\xff\xff');count=0;manifest=[]
    ls.SCREEN,ls.DLIST,ls.ENTRY=0x5000,0x5080,0x50a0
    for i,(a,b,p) in enumerate(entries):
        out.extend(xex_segment(a,p))
        if i==last:out.extend(ls.segments())
        elif i>last and (a,b) not in ((0x02e2,0x02e3),(0x02e0,0x02e1)):
            count+=1
            out.extend(xex_segment(0x5100,marker(count,a,b)))
            out.extend(xex_segment(0x02e2,b'\x00\x51'))
            manifest.append(f'{count:02d}: ${a:04X}-${b:04X}')
    with OUTPUT.open('xb') as f:f.write(out)
    OUTPUT.with_suffix('.stages.txt').write_text('\n'.join(manifest)+'\n')

if __name__=='__main__':main()
