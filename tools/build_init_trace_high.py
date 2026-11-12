"""AVG trace using only high temporary RAM, retired before runtime starts."""
from pathlib import Path
from build_sequence import Code
from build_visual_prototype import xex_segment
from extract_music import segments
import loading_screen as ls

SOURCE=Path('releases/less-i-know-demo-release-009-stereo.xex')
OUTPUT=Path('releases/avg-full-demo-init-trace-002.xex')
HALT_LAST=False

def main():
    # These addresses are unused by original v035 load segments. The final
    # runtime scanline image replaces them only after the last asset INIT.
    old_entry=ls.ENTRY
    ls.SCREEN,ls.DLIST,ls.ENTRY=0x3800,0x3880,0x38a0
    out=bytearray(b'\xff\xff');out.extend(ls.segments())
    number=0;manifest=[]
    for start,end,data in segments(SOURCE.read_bytes()):
        if start in (0x0600,0x0700,old_entry):continue
        if (start,end)==(0x02e2,0x02e3) and int.from_bytes(data,'little')==old_entry:continue
        if (start,end)==(0x2000,0x24b2):
            data=bytearray(data)
            assert data[7:10]==bytes.fromhex('8d 00 d4')
            data[7:10]=b'\xea'*3
        if (start,end)==(0x02e2,0x02e3):
            number+=1;target=int.from_bytes(data,'little')
            # Relocate the wrapper and both source/target operands by
            # assembling it at its actual high-RAM origin.
            out.extend(xex_segment(0x3900,wrapper(number,target)))
            data=bytes.fromhex('00 39')
            manifest.append(f'{number:02d}: ${target:04X}')
        out.extend(xex_segment(start,data))
    with OUTPUT.open('xb') as f:f.write(out)
    OUTPUT.with_suffix('.stages.txt').write_text('\n'.join(manifest)+'\n')

def wrapper(number,target):
    c=Code(0x3900)
    for state in ('ENTER','RETURN'):
        if state=='RETURN':c.emit(0x20,target&255,target>>8)
        c.emit(0x08,0x48,0x8a,0x48,0x98,0x48)
        c.emit(0x20,ls.ENTRY&255,ls.ENTRY>>8,0xa2,0)
        c.label(state);c.jump(0xbd,state+'_text')
        c.emit(0x9d,(ls.SCREEN+40)&255,(ls.SCREEN+40)>>8,0xe8,0xe0,40)
        c.branch(0xd0,state)
        c.emit(0x68,0xa8,0x68,0xaa,0x68,0x28)
    if HALT_LAST and number==66:
        c.label('loaded');c.jump(0x4c,'loaded')
    else:c.emit(0x60)
    for state in ('ENTER','RETURN'):
        c.label(state+'_text')
        dots='.'*((number*2+(state=='RETURN'))%4)
        c.emit(*(ord(x)-32 for x in ('LOADING BANKS'+dots.ljust(3)).center(40)))
    result=bytes(c.finish());assert 0x3900+len(result)<0x3c00
    return result

if __name__=='__main__':main()
