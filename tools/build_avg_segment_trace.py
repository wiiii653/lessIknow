"""Instrument the segment immediately after INIT 05, in 1 KiB chunks."""
from pathlib import Path
from build_sequence import Code
from build_visual_prototype import xex_segment
from extract_music import segments

SOURCE=Path('releases/avg-full-demo-load-only-001.xex')
OUTPUT=Path('releases/avg-bank05-segment-trace-001.xex')

def checkpoint(message):
    c=Code(0x3a00)
    c.emit(0x08,0x48,0x8a,0x48,0x98,0x48,0x20,0xa0,0x38,0xa2,0)
    c.label('copy');c.jump(0xbd,'text')
    c.emit(0x9d,0x28,0x38,0xe8,0xe0,40);c.branch(0xd0,'copy')
    c.emit(0x68,0xa8,0x68,0xaa,0x68,0x28,0x60)
    c.label('text');c.emit(*(ord(x)-32 for x in message.center(40)))
    data=bytes(c.finish());assert 0x3a00+len(data)<0x3c00
    return xex_segment(0x3a00,data)+xex_segment(0x02e2,b'\x00\x3a')

def main():
    out=bytearray(b'\xff\xff');number=0;pending=False;done=False
    for start,end,data in segments(SOURCE.read_bytes()):
        if pending and (start,end)==(0x8000,0xbfff):
            out.extend(checkpoint('AFTER INIT 05'))
            for part in range(16):
                addr=0x8000+part*1024
                out.extend(xex_segment(addr,data[part*1024:(part+1)*1024]))
                out.extend(checkpoint(f'BANK 05 PART {part+1:02d} OF 16'))
            pending=False;done=True;continue
        out.extend(xex_segment(start,data))
        if (start,end)==(0x02e2,0x02e3) and data==b'\x00\x39':
            number+=1
            if number==5:pending=True
    assert done
    with OUTPUT.open('xb') as f:f.write(out)

if __name__=='__main__':main()
