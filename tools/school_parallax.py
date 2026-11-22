"""The party arena parallax, with eighteen music-clocked walk frames."""
from pathlib import Path

from engine_effects import COPY_PAGES, cached_display_list
from build_sequence import Code
from music_timing import tick_at_bar
ENTRY=0x7000
START=tick_at_bar(19,2)
# Horizontal displacement of the face in the precomposed walk.
FACE_OFFSETS = (0, 2, 4, 6, 8, 11, 13, 15, 17, 20, 22, 24, 26, 29, 31, 33, 35, 38)
PARTY_FACE = ((53, 12, 0), (55, 14, 1), (54, 16, 1))
# A softer temple/ear break and a clean chin highlight.
PROFILE_POLISH = ((50, 11, 1), (50, 12, 1), (49, 13, 1), (54, 16, 3))


def party_frames():
    """Exact v330 pan as used in release 058, including its three face pixels."""
    packed = Path('assets/art/reference/v175/arena-pan.bin').read_bytes()
    if len(packed) != len(FACE_OFFSETS) * 2560:
        raise ValueError('party arena pan must contain eighteen 160x64 frames')
    result = []
    for i, offset in enumerate(FACE_OFFSETS):
        frame = bytearray(value >> shift & 3 for value in packed[i * 2560:(i + 1) * 2560]
                          for shift in (6, 4, 2, 0))
        for x, y, ink in PARTY_FACE:
            frame[y * 160 + x + offset] = ink
        result.append(bytes(frame))
    return result


def frames():
    result = []
    for original, offset in zip(party_frames(), FACE_OFFSETS):
        frame = bytearray(original)
        for x, y, ink in PROFILE_POLISH:
            frame[y * 160 + x + offset] = ink
        # Remove the light Fuji stitching from the moving near sleeve.
        for y in range(31, 36):
            for x in range(38, 44):
                pixel = y*160+x+offset
                if frame[pixel] == 3:
                    frame[pixel] = 1
        result.append(bytes(frame))
    return result


def helper():
    c=Code(ENTRY)
    def a(op,address):c.emit(op,address&255,address>>8)
    # Frame number is computed from the coherent music clock by the main callback.
    a(0xad,0x83ed);c.emit(0x09,0xc0);a(0xcd,0x83fa)
    c.branch(0xd0,'changed');c.jump(0x4c,'colors')
    c.label('changed');a(0x8d,0x83fa)
    a(0xad,0x83ed);c.emit(0x29,3,0xaa)
    c.jump(0xbd,'source_hi');c.emit(0x48)
    a(0xad,0x83e6);c.emit(0x29,4,0x0a,0x0a,0x0a,0x49,0xb0);a(0x8d,0x83fe)
    c.emit(0x68,0xa2,2);a(0x20,COPY_PAGES)
    cached_display_list(c, 2)
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
    c.label('colors')
    c.label('color_wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'color_wait')
    # Match the complete first-story palette, including the opening pan.
    for addr,val in ((0xd01a,0),(0xd016,0x38),(0xd017,0x88),(0xd018,0x2c),(0xd01d,0),(0xd400,0x22)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    for label in ('dl1','dl2'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    c.label('source_hi');c.emit(0x40,0x4a,0x54,0x5e)
    c.label('row_lo');c.emit(*((y//3*40)&255 for y in range(192)))
    c.label('row_hi');c.emit(*((y//3*40)>>8 for y in range(192)))
    result=c.finish();assert len(result)<=4096,len(result)
    return result


def banks():
    pictures=frames(); code=helper()
    for group in range(5):
        out=bytearray(16384);out[0x3000:0x3000+len(code)]=code
        for i in range(4):
            p=pictures[min(group*4+i,17)]
            data=bytes(sum(p[j+k]<<(6-2*k) for k in range(4)) for j in range(0,len(p),4))
            out[i*2560:(i+1)*2560]=data
        yield bytes(out)
