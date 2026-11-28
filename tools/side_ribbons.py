"""Publish the profile dancer's PMG independently of bitmap drawing."""

from functools import lru_cache

from build_sequence import Code
from engine_effects import PMBASE_SHADOW
from scene_palette_io import emit as emit_scene_io

NMI_ENTRY = 0xd8e0
BLIT_ENTRY = 0xdf21
QUEUE_ENTRY = 0xdf50
CONTROL_BANK = 23  # The final arena bank has two frames below $5400.
CONTROL_ENTRY = 0x5400
RIBBON_BANK = 49
MIDPOINT_BANKS = (*range(3, 11), *range(41, 49))
MIDPOINT_ENTRY = 0x7e00  # Free tails in both banana variants.

PENDING_POSE, PENDING_X, ACTIVE_POSE, ACTIVE_X, PREPARED_POSE, PREPARED_X, \
    PREPARED_BITMAP, BACK, BACK_POSE, POSE, PHASE = range(0xdf40, 0xdf4b)
LIVE_TICK = 0x24a7
SCENE = 0x83e0
BACK_LIST = 0x83e6
PLANES = (0x0a00, 0x0a80, 0x0b00, 0x0b80, 0x0980)


def queue():
    """Signal an inactive profile bitmap, returning carry set for side poses."""
    c = Code(QUEUE_ENTRY)
    def a(op, addr):
        c.emit(op, addr & 255, addr >> 8)

    a(0xad, 0x83ed); c.emit(0xc9, 16); c.branch(0x90, 'done')
    c.emit(0xc9, 32); c.branch(0xb0, 'other')
    a(0xae, 0x83eb); c.branch(0xf0, 'side')
    a(0xae, 0x83fd); a(0x8e, PENDING_X)
    # This final store makes the completed bitmap and its anchors visible
    # to the interrupt handler as a single request.
    a(0x8d, PENDING_POSE)
    c.label('side'); c.emit(0x38, 0x60)
    c.label('other'); c.emit(0x18)
    c.label('done'); c.emit(0x60)
    return bytes(c.finish())


def nmi():
    from ribbon_dance import SIDE_START, SIDE_END, PUBLISH_VCOUNT_START, PUBLISH_VCOUNT_LIMIT

    c = Code(NMI_ENTRY)
    def a(op, addr):
        c.emit(op, addr & 255, addr >> 8)

    a(0xad, PENDING_POSE); a(0x0d, ACTIVE_POSE)
    c.branch(0xf0, 'done')
    a(0xad, SCENE); c.emit(0xc9, 14); c.branch(0xd0, 'reset')
    a(0xad, LIVE_TICK + 2); c.branch(0xd0, 'reset')
    a(0xad, LIVE_TICK + 1); c.emit(0xc9, SIDE_START >> 8); c.branch(0x90, 'reset')
    c.emit(0xc9, SIDE_END >> 8); c.branch(0x90, 'raster'); c.branch(0xd0, 'reset')
    a(0xad, LIVE_TICK); c.emit(0xc9, SIDE_END & 255); c.branch(0xb0, 'reset')

    # The second music DLI prepares the back buffer. The fourth has already
    # run the text commit when it reaches this early blanking window.
    c.label('raster'); a(0xad, 0xd40b); c.emit(0xc9, 40); c.branch(0x90, 'done')
    c.emit(0xa2, 0, 0xc9, 72); c.branch(0x90, 'bank')
    c.emit(0xc9, 121); c.branch(0x90, 'done')
    c.label('wait'); c.emit(0xc9, PUBLISH_VCOUNT_LIMIT); c.branch(0xb0, 'done')
    c.emit(0xc9, PUBLISH_VCOUNT_START); c.branch(0xb0, 'publish')
    a(0xad, 0xd40b); c.jump(0x4c, 'wait')
    c.label('publish'); c.emit(0xe8)
    c.label('bank')
    a(0xad, 0xd301); c.emit(0x48)
    a(0xad, 0x08c0 + CONTROL_BANK); a(0x8d, 0xd301)
    a(0x20, CONTROL_ENTRY)
    c.emit(0x68); a(0x8d, 0xd301)
    c.label('done'); c.emit(0x60)

    c.label('reset'); c.emit(0xa9, 0)
    for address in (PENDING_POSE, ACTIVE_POSE, PREPARED_POSE, BACK):
        a(0x8d, address)
    c.emit(0x60)
    assert NMI_ENTRY + len(c.data) <= 0xd960
    return bytes(c.finish())


def blitter():
    """X is the last row index and Y selects the source bank."""
    c = Code(BLIT_ENTRY)
    c.emit(0xad, 0x01, 0xd3, 0x48, 0xb9, 0xc0, 0x08, 0x8d, 0x01, 0xd3)
    c.label('rows')
    c.label('source'); c.emit(0xbd, 0, 0)
    c.label('target'); c.emit(0x9d, 0, 0)
    c.emit(0xca); c.branch(0x10, 'rows')
    c.emit(0x68, 0x8d, 0x01, 0xd3, 0x60)
    for name in ('source', 'target'):
        for suffix, offset in (('lo', 1), ('hi', 2)):
            c.labels[f'{name}_{suffix}'] = c.labels[name] + offset
    assert BLIT_ENTRY + len(c.data) <= PENDING_POSE
    return bytes(c.finish()), c.labels


def _clipped_stream(origin, first, end):
    # PMG is 128 rows tall. A wrapped top anchor starts above row zero.
    if origin >= 192:
        origin -= 256
    assert origin < 128
    first = max(first, -origin)
    end = min(end, 128 - origin)
    assert first < end
    return (first, origin + first, end - first)


def _exposed_rows(old, new):
    """Return the portions of the previous stream outside the next one."""
    _, first, count = old
    _, next_first, next_count = new
    end, next_end = first + count, next_first + next_count
    ranges = ((first, min(end, next_first)), (max(first, next_end), end))
    return tuple(((lo - 1) & 255, hi - 1) if lo < hi else (255, 255) for lo, hi in ranges)


def controller():
    from ribbon_dance import FRAME_COUNT, PALETTE, RIBBONS, metadata, ribbon_streams

    c = Code(CONTROL_ENTRY)
    _, blit = blitter()
    def a(op, addr):
        emit_scene_io(c, op, addr)

    c.emit(0xe0, 0); c.branch(0xf0, 'prepare'); c.jump(0x4c, 'publish')
    c.label('prepare')
    a(0xad, BACK); c.branch(0xd0, 'select'); c.emit(0x60)
    c.label('select')
    a(0xad, PENDING_POSE); c.branch(0xf0, 'held')
    a(0xae, BACK_POSE); c.branch(0xf0, 'pending')
    a(0x4d, BACK_POSE); c.emit(0x29, 0xfe); c.branch(0xd0, 'held')
    c.label('pending')
    a(0xad, PENDING_POSE); a(0x8d, PREPARED_BITMAP)
    a(0xae, PENDING_X); c.jump(0x4c, 'selected')
    c.label('held')
    c.emit(0xa9, 0); a(0x8d, PREPARED_BITMAP)
    a(0xad, ACTIVE_POSE); c.branch(0xd0, 'active'); c.emit(0x60)
    c.label('active'); a(0xae, ACTIVE_X)
    c.label('selected')
    a(0x8d, PREPARED_POSE); a(0x8e, PREPARED_X)
    c.emit(0x4a, 0x29, 7); a(0x8d, POSE)
    a(0xad, LIVE_TICK); c.emit(0x4a, 0x4a, 0x29, 31); a(0x8d, PHASE)

    for plane, dest in enumerate(PLANES):
        a(0xae, PHASE)
        c.jump(0xbd, f'source_hi{plane}'); a(0x8d, blit['source_hi'])
        c.jump(0xbc, 'source_bank')
        c.jump(0xbd, f'source_lo{plane}')
        a(0xae, POSE); c.emit(0x18)
        c.jump(0x7d, f'clip{plane}'); a(0x8d, blit['source_lo'])
        c.jump(0xbd, f'destination{plane}'); a(0x8d, blit['target_lo'])
        a(0xad, BACK); c.emit(0x09, (dest >> 8) & 7); a(0x8d, blit['target_hi'])
        c.jump(0xbd, f'rows{plane}'); c.emit(0xaa)
        a(0x20, BLIT_ENTRY)
    c.emit(0x60)

    c.label('publish')
    a(0xad, PREPARED_POSE); c.branch(0xd0, 'swap')
    a(0xad, BACK); c.branch(0xf0, 'prime')
    c.emit(0x60)
    c.label('prime')
    a(0xad, PMBASE_SHADOW); c.emit(0x49, 0x80, 0x29, 0x80, 0x09, 8)
    c.jump(0x4c, 'clear_back')

    c.label('swap')
    a(0xad, ACTIVE_POSE); a(0x8d, BACK_POSE)
    a(0xad, PREPARED_BITMAP); c.branch(0xf0, 'swap_pmg')
    a(0x8d, ACTIVE_POSE)
    a(0xad, PREPARED_X); a(0x8d, ACTIVE_X)
    c.emit(0xa9, 0); a(0x8d, 0xd402)
    a(0xad, BACK_LIST); a(0x8d, 0xd403)
    c.emit(0x49, 4); a(0x8d, BACK_LIST)
    # Set the playfield inks through their shadow writers for the text split.
    for addr, value in ((0xd01a, PALETTE[0]), *zip(range(0xd016, 0xd019), PALETTE[1:])):
        c.emit(0xa9, value); a(0x8d, addr)

    c.label('swap_pmg')
    a(0xad, BACK); a(0x8d, PMBASE_SHADOW); a(0x8d, 0xd407)
    a(0xae, POSE); a(0xac, PHASE)
    for plane in range(4):
        c.jump(0xbd, f'anchor{plane}'); c.emit(0x18); a(0x6d, PREPARED_X)
        a(0x8d, 0xd000 + plane)
        c.emit(0x18); c.jump(0x79, f'spark{plane}')
        a(0x8d, 0xd004 + plane)
    c.emit(0xa9, 3)
    for addr in (*range(0xd008, 0xd00c), 0xd01d):
        a(0x8d, addr)
    for addr, value in ((0xd00c, 0x55), (0xd01b, 0x11), (0xd400, 0x2e)):
        c.emit(0xa9, value); a(0x8d, addr)
    c.emit(0xa9, 0); a(0x8d, PREPARED_POSE)
    a(0xae, PREPARED_BITMAP); c.branch(0xf0, 'retire')
    a(0x8d, PENDING_POSE)
    c.label('retire'); a(0xad, BACK); c.emit(0x49, 0x80)
    a(0x8d, BACK)
    a(0xad, PENDING_POSE); c.branch(0xd0, 'next_pose')
    a(0xad, ACTIVE_POSE)
    c.label('next_pose'); c.emit(0xaa)
    a(0x4d, BACK_POSE); c.emit(0x29, 0xfe)
    c.branch(0xd0, 'clear_retired')
    c.emit(0x60)
    c.label('clear_retired'); a(0xad, BACK_POSE); c.branch(0xf0, 'clear_unknown')
    c.jump(0x4c, 'clear_shifted')
    c.label('clear_unknown'); a(0xad, BACK)

    # When inheriting a buffer from another scene, its row spans are unknown.
    c.label('clear_back'); a(0x8d, BACK)
    c.emit(0xa9, 0); a(0x8d, BACK_POSE)
    for plane, addr in enumerate(PLANES):
        a(0xad, BACK); c.emit(0x09, (addr >> 8) & 7)
        c.jump(0x8d, f'clear_hi{plane}')
    c.emit(0xa9, 0, 0xa2, 127)
    c.label('clear_rows')
    for plane, addr in enumerate(PLANES):
        c.labels[f'clear_hi{plane}'] = c.origin + len(c.data) + 2
        a(0x9d, addr)
    c.emit(0xca); c.branch(0x10, 'clear_rows'); c.emit(0x60)

    # The next blit overwrites the shared rows. Erase just the exposed rows
    # of the retired buffer, then use it with the new pose at the next DLI.
    c.label('clear_shifted')
    c.emit(0x29, 14, 0x0a, 0x0a); a(0x8d, POSE)
    c.emit(0x8a, 0x4a, 0x29, 7); a(0x0d, POSE); c.emit(0xa8)
    a(0x8e, BACK_POSE)
    for plane, addr in enumerate(PLANES):
        c.emit(0xa9, addr & 255); c.jump(0x8d, 'erase_lo')
        a(0xad, BACK); c.emit(0x09, (addr >> 8) & 7); c.jump(0x8d, 'erase_hi')
        for edge in ('above', 'below'):
            c.jump(0xbe, f'{edge}_last{plane}')
            c.jump(0xb9, f'{edge}_stop{plane}')
            c.jump(0x20, 'erase_span')
    c.emit(0x60)
    c.label('erase_span'); c.emit(0xe0, 255); c.branch(0xf0, 'erase_done')
    c.jump(0x8d, 'erase_stop')
    c.emit(0xa9, 0)
    c.label('erase'); a(0x9d, 0)
    c.emit(0xca)
    c.label('erase_bound'); c.emit(0xe0, 0); c.branch(0xd0, 'erase')
    c.label('erase_done'); c.emit(0x60)
    for label, insn, offset in (('erase_lo', 'erase', 1), ('erase_hi', 'erase', 2),
                                ('erase_stop', 'erase_bound', 1)):
        c.labels[label] = c.labels[insn] + offset

    c.label('source_bank')
    c.emit(*(bank for midpoint in MIDPOINT_BANKS for bank in (RIBBON_BANK, midpoint)))
    meta = metadata()
    streams = ribbon_streams(), midpoint_streams()
    exposure_tables = {}
    for plane, addr in enumerate(PLANES):
        source = [address for phase in range(16)
                  for address in (RIBBONS + plane*1024 + phase*64, MIDPOINT_ENTRY + plane*64)]
        for suffix, shift in (('lo', 0), ('hi', 8)):
            c.label(f'source_{suffix}{plane}')
            c.emit(*((address >> shift) & 255 for address in source))
        y_table = (4 + plane % 4) * FRAME_COUNT
        # Only copy rows used by at least one phase in this plane.
        used_rows = [row for row in range(64)
                     if any(stream[plane*1024 + phase*64 + row]
                            for stream in streams for phase in range(16))]
        spans = [_clipped_stream(meta[y_table + pose], used_rows[0], used_rows[-1]+1)
                 for pose in range(16, 32, 2)]
        for name, values in zip(('clip', 'destination', 'rows'), zip(*spans)):
            c.label(f'{name}{plane}')
            bias = (addr & 255) if name == 'destination' else -1 if name == 'rows' else 0
            c.emit(*(value + bias for value in values))
        exposures = [_exposed_rows(old, new) for old in spans for new in spans]
        for index, edge in enumerate(('above', 'below')):
            for part, bound in enumerate(('stop', 'last')):
                name = f'{edge}_{bound}{plane}'
                table = bytes(ranges[index][part] for ranges in exposures)
                if table in exposure_tables:
                    c.labels[name] = exposure_tables[table]
                else:
                    c.label(name)
                    exposure_tables[table] = c.labels[name]
                    c.emit(*table)
        if plane < 4:
            c.label(f'anchor{plane}')
            c.emit(*(meta[plane*FRAME_COUNT + pose] for pose in range(16, 32, 2)))
            c.label(f'spark{plane}')
            c.emit(*(14 + round((plane-1.5)*((phase/2 + plane*4) % 16)*.55)
                     for phase in range(32)))
    assert CONTROL_ENTRY + len(c.data) <= 0x6000
    return bytes(c.finish())


def install(bank, address, payload):
    offset = address - 0x4000
    assert len(bank) == 0x4000 and offset + len(payload) <= len(bank)
    assert not any(bank[offset:offset + len(payload)]), hex(address)
    return bank[:offset] + payload + bank[offset + len(payload):]


def install_midpoint(bank, index):
    phase = MIDPOINT_BANKS.index(index)
    streams = midpoint_streams()
    shape = b''.join(streams[plane*1024 + phase*64:plane*1024 + phase*64+64]
                     for plane in range(len(PLANES)))
    return install(bank, MIDPOINT_ENTRY, shape)


@lru_cache(maxsize=1)
def midpoint_streams():
    from ribbon_dance import ribbon_streams

    return ribbon_streams(halfway=True)
