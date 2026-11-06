"""Patch the inactive display list between ANTIC F and E without extra DLI."""
from build_sequence import Code
from music_timing import tick_at_bar

ENTRY = 0xfef0


def helper():
    c = Code(ENTRY)
    def a(op, addr):
        c.emit(op, addr & 255, addr >> 8)
    # A zero/one flag is the low bit of ANTIC mode E/F.  Use the music
    # clock rather than the previous scene; BACK is always the inactive list.
    a(0xad, 0x83e4);c.branch(0xd0, 'normal')
    a(0xad, 0x83e3);c.emit(0xc9, tick_at_bar(8) >> 8)
    c.branch(0x90, 'gtia');c.branch(0xd0, 'normal')
    a(0xad, 0x83e2);c.emit(0xc9, tick_at_bar(8) & 255);c.branch(0x90, 'gtia')
    # Once both lists are back in ANTIC E, later scenes take the short path.
    # A restart into the intro still takes the GTIA path and marks them dirty.
    c.label('normal');c.jump(0xad, 'dirty');c.branch(0xd0, 'normal_patch');c.emit(0x60)
    c.label('normal_patch');c.emit(0xa9, 0);c.jump(0x4c, 'selected')
    c.label('gtia');c.emit(0xa9, 1)
    c.label('selected');a(0x8d, 0x83e8)
    # Avoid touching display-list RAM when this buffer is already correct.
    a(0xae, 0x83e6);c.jump(0x8e, 'probe_hi')
    c.label('probe');c.emit(0xad, 2, 0x80, 0x29, 1);a(0xcd, 0x83e8)
    c.branch(0xd0, 'patch');c.emit(0x60)
    c.label('patch')
    for block in range(3):
        offset = 2 + block * 192
        a(0xad, 0x83e6);c.emit(0x18, 0x69, offset >> 8)
        c.jump(0x8d, f'read{block}_hi');c.jump(0x8d, f'write{block}_hi')
        c.emit(0xa2, 0)
        c.label(f'loop{block}')
        c.label(f'read{block}');c.emit(0xbd, offset & 255, 0x80)
        c.emit(0x29, 0xfe);a(0x0d, 0x83e8)
        c.label(f'write{block}');c.emit(0x9d, offset & 255, 0x80)
        c.emit(0xe8, 0xe8, 0xe8, 0xe0, 192);c.branch(0xd0, f'loop{block}')
        c.labels[f'read{block}_hi'] = c.labels[f'read{block}'] + 2
        c.labels[f'write{block}_hi'] = c.labels[f'write{block}'] + 2
    # Remember whether either list still contains GTIA/ANTIC F opcodes.
    a(0xad, 0x8002);a(0x0d, 0x8402);c.emit(0x29, 1);c.jump(0x8d, 'dirty')
    c.emit(0x60)
    c.labels['probe_hi'] = c.labels['probe'] + 2
    c.label('dirty');c.emit(0)
    result = c.finish()
    assert ENTRY + len(result) <= 0xfff0, len(result)
    return result
