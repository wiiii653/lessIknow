"""Small unbanked helper routines and preloaded PMG beat accents."""
from build_sequence import Code

COPY_ORIGIN = 0xcf00
EFFECT_ORIGIN = 0xaf00


def copy_helper():
    c = Code(COPY_ORIGIN)
    c.label('pixels')
    for page in range(31):
        if page == 4:
            c.label('dirty_pixels')
        c.emit(0xbd, 0, 0x40 + page, 0x9d, 0, 0x90 + page)
        if page == 24:
            c.label('gate')
            c.jump(0x4c, 'tail')
            c.label('tail')
    c.label('end')
    c.emit(0xe8)
    c.branch(0xf0, 'done')
    c.label('repeat')
    c.jump(0x4c, 'pixels')
    c.label('done')
    c.emit(0x60)
    data = c.finish()
    assert len(data) <= 256
    return data, c.labels


def effects_helper(state=0x83e0, intro_color=0):
    c = Code(EFFECT_ORIGIN)
    def absop(op, address):
        c.emit(op, address & 255, address >> 8)
    # Called at vblank, even when the underlying picture remains unchanged.
    c.emit(0xa9, 0)
    absop(0x8d, 0xd01d)
    absop(0x8d, 0xd01b)
    c.emit(0xa9, 0x22)
    absop(0x8d, 0xd400)
    absop(0xad, state)
    c.emit(0xc9, 2)
    c.branch(0xb0, 'check_dance')
    # GTIA 11: sixteen hues at one luminance for the two opening cards.
    c.emit(0xa9, 0xc0)
    absop(0x8d, 0xd01b)
    absop(0x20, intro_color)
    c.emit(*([0xea] * 12))
    c.emit(0x60)
    c.label('check_dance')
    c.emit(0xc9, 6)
    c.branch(0x90, 'check_slide')
    c.emit(0x60)
    c.label('check_slide')
    absop(0xad, state + 1)
    c.branch(0xf0, 'animate')
    c.emit(0x60)
    c.label('animate')
    c.emit(0xa2, 31)
    c.label('find_beat')
    absop(0xad, state + 3)
    c.jump(0xdd, 'beat_hi')
    c.branch(0x90, 'previous')
    c.branch(0xd0, 'found')
    absop(0xad, state + 2)
    c.jump(0xdd, 'beat_lo')
    c.branch(0xb0, 'found')
    c.label('previous')
    c.emit(0xca)
    c.branch(0x10, 'find_beat')
    c.emit(0x60)
    c.label('found')
    c.emit(0x38)
    absop(0xad, state + 2)
    c.jump(0xfd, 'beat_lo')
    c.emit(0xa8)
    absop(0xad, state + 3)
    c.jump(0xfd, 'beat_hi')
    c.branch(0xd0, 'done')
    c.emit(0xc0, 24)
    c.branch(0xb0, 'done')
    # Warm -> cyan -> pink decay, matching existing playfield colors.
    c.emit(0xa9, 0x2c, 0xc0, 8)
    c.branch(0x90, 'ink')
    c.emit(0xa9, 0x9a, 0xc0, 16)
    c.branch(0x90, 'ink')
    c.emit(0xa9, 0x48)
    c.label('ink')
    c.emit(0xa2, 3)
    c.label('set_ink')
    absop(0x9d, 0xd012)
    # Four independently colored players; missiles inherit their colors.
    c.emit(0x18, 0x69, 0x40)
    c.emit(0xca)
    c.branch(0x10, 'set_ink')
    # A short outward sweep follows each beat without copying PMG bitmaps.
    c.emit(0x98, 0x4a, 0x4a, 0x29, 3)
    c.jump(0x8d, 'position_offset_operand')
    c.emit(0xa2, 3)
    c.label('set_positions')
    c.jump(0xbd, 'positions')
    c.emit(0x18)
    c.label('position_offset')
    c.emit(0x69, 0)
    absop(0x9d, 0xd000)
    c.emit(0x18, 0x69, 9)
    absop(0x9d, 0xd004)
    c.emit(0xca)
    c.branch(0x10, 'set_positions')
    c.emit(0xa9, 0, 0xa2, 4)
    c.label('set_sizes')
    absop(0x9d, 0xd008)
    c.emit(0xca)
    c.branch(0x10, 'set_sizes')
    c.emit(0xa9, 8)
    absop(0x8d, 0xd407)
    c.emit(0xa9, 1)
    absop(0x8d, 0xd01b)
    c.emit(0xa9, 3)
    absop(0x8d, 0xd01d)
    c.emit(0xa9, 0x2e)
    absop(0x8d, 0xd400)
    c.label('done')
    c.emit(0x60)
    # Match the visual accent phase of v051 independently of scene timing.
    beats = [8976 + i * 374 // 4 for i in range(32)]
    c.label('positions'); c.emit(*(x + 48 for x in (20, 55, 99, 136)))
    c.label('beat_lo'); c.emit(*(t & 255 for t in beats))
    c.label('beat_hi'); c.emit(*(t >> 8 for t in beats))
    c.labels['position_offset_operand'] = c.labels['position_offset'] + 1
    data = c.finish()
    assert len(data) <= 256, len(data)
    return data


def pmg_art():
    players = bytearray(512)
    missiles = bytearray(128)
    for i, row in enumerate((14, 10, 15, 11)):
        players[i*128+row:i*128+row+7] = bytes((0x10, 0x10, 0x38, 0xfe, 0x38, 0x10, 0x10))
        for y in range(row - 3, row):
            missiles[y] |= 3 << (2 * i)
    return bytes(missiles), bytes(players)

# Reserved independently of the packed scanline pool. Both bytes describe the
# LMS mapping of an entire display list, never the framebuffer's pixel content.
RUNTIME_ORIGIN = 0x0c00
RUNTIME_END = 0x0e00
DL_KEYS = 0x0dfe
COPY_PAGES = RUNTIME_ORIGIN
DL_CHECK = 0x0d40


def runtime_helper():
    """Copy 5*X aligned pages from A:$00 to STATE+30:$00, preserving banks.

    Only call with X=2 or 3. Code and operands are unbanked so music NMIs may
    switch banks safely. Source and target must not overlap this helper.
    """
    c = Code(RUNTIME_ORIGIN)
    def a(op, addr): c.emit(op, addr & 255, addr >> 8)
    for page in range(5):
        c.jump(0x8d, f'read{page}_hi')
        c.emit(0x18, 0x69, 1)
    a(0xad, 0x83fe)
    for page in range(5):
        c.jump(0x8d, f'write{page}_hi')
        c.emit(0x18, 0x69, 1)
    c.emit(0xa0, 0)
    c.label('copy')
    for page in range(5):
        c.label(f'read{page}'); c.emit(0xb9, 0, 0x40)
        c.label(f'write{page}'); c.emit(0x99, 0, 0x90)
    c.emit(0xc8); c.branch(0xd0, 'copy')
    c.emit(0xca); c.branch(0xf0, 'copied')
    for page in range(5):
        for op in ('read', 'write'):
            c.jump(0xad, f'{op}{page}_hi'); c.emit(0x18, 0x69, 5)
            c.jump(0x8d, f'{op}{page}_hi')
    c.jump(0x4c, 'copy')
    c.label('copied'); c.emit(0x60)
    for page in range(5):
        for op in ('read', 'write'):
            c.labels[f'{op}{page}_hi'] = c.labels[f'{op}{page}'] + 2
    code = c.finish()
    if RUNTIME_ORIGIN + len(code) > DL_CHECK:
        raise ValueError('copy helper overlaps DL cache helper')
    code.extend(bytes(DL_CHECK - RUNTIME_ORIGIN - len(code)))
    d = Code(DL_CHECK)
    # A = layout key. Return A=0/Z if already built; A=1 otherwise.
    d.emit(0x48, 0xad, 0xe6, 0x83, 0x29, 4, 0x4a, 0x4a, 0xaa, 0x68,
           0xdd, DL_KEYS & 255, DL_KEYS >> 8)
    d.branch(0xf0, 'hit')
    d.emit(0x9d, DL_KEYS & 255, DL_KEYS >> 8, 0xa9, 1, 0x60)
    d.label('hit'); d.emit(0xa9, 0, 0x60)
    code.extend(d.finish())
    assert len(code) <= DL_KEYS - RUNTIME_ORIGIN
    code.extend(bytes(RUNTIME_END - RUNTIME_ORIGIN - len(code)))
    return code


def cached_display_list(c, key):
    """Guard the caller's existing row builder using the inactive DL's key."""
    c.emit(0xa9, key, 0x20, DL_CHECK & 255, DL_CHECK >> 8)
    c.branch(0xd0, 'build_rows')
    c.jump(0x4c, 'swap')
    c.label('build_rows')


def clear_pmg(c, label):
    """Clear $0980–$0BFF once each, five 128-byte spans per iteration."""
    c.emit(0xa9, 0, 0xa2, 127)
    c.label(label)
    for base in (0x0980, 0x0a00, 0x0a80, 0x0b00, 0x0b80):
        c.emit(0x9d, base & 255, base >> 8)
    c.emit(0xca)
    c.branch(0x10, label)
