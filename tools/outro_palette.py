"""Display-list-driven terminal palette; the extra split never clocks music."""
from build_sequence import Code
ENTRY=0x2451

def helper():
    c=Code(ENTRY)
    def a(op,v):c.emit(op,v&255,v>>8)
    a(0xad,0x83e0);c.emit(0xc9,17);c.branch(0xd0,'music')
    a(0xad,0x0dd0);c.emit(0xc9,2);c.branch(0xd0,'music')
    from outro_text import PALETTE_VCOUNT
    a(0xad,0xd40b);c.emit(0xc9,PALETTE_VCOUNT);c.branch(0xf0,'body')
    c.emit(0xc9,8);c.branch(0xb0,'music')
    a(0xad,0x83e2);c.emit(0x29,0xfc);c.branch(0xd0,'green')
    c.emit(0xA9,0x0E);c.branch(0xD0,'text_ink')
    c.label('green');a(0xad,0x83ec);c.branch(0xf0,'text_ink');c.emit(0x09,0xc2)
    c.label('text_ink');a(0x8d,0xd016);c.jump(0x4c,'music')
    c.label('body');a(0x8d,0xd40a)
    a(0xad,0x83ec);c.branch(0xf0,'body_ink');c.emit(0x09,0x40)
    c.label('body_ink');a(0x8d,0xd016)
    # Discard this JSR's return address, restore saved Y/X/A, then RTI.
    c.emit(0x68,0x68,0x68,0xa8,0x68,0xaa,0x68,0x40)
    c.label('music');a(0x8d,0xd40a);c.emit(0x60)
    data=bytes(c.finish())
    assert ENTRY+len(data)<=0x249c
    return data
