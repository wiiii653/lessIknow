"""Generate continuous PMG trajectories for the terminal and final shot."""
import math

from build_sequence import Code

ENTRY = 0x66a0
MIDPOINT_ENTRY = 0x69c4  # Formerly the unused original orbit coordinates.
VALUES_X = 0x69b8
VALUES_Y = 0x69bc
AMOUNT = 0x69c0
PHASE_SHIFT = 2
PHASE_MASK = 63
TICK_LOW, TICK_HIGH = 0x83e2, 0x83e3  # Stable scene clock snapshot.
ANGLE_INDEX, SHAPE_OFFSET = 0x0dd8, 0x0dd9


def morph_amount(tick):
    """The path breathes from a tall loop to a wide sweep and back."""
    step = (tick >> 6) & 15
    return min(step, 15-step)


def position(index, amount, plane=0):
    from final_boy import HEAD_X, HEAD_Y

    angle = ((index + plane*8) & 31) * math.tau / 32
    blend = amount / 7
    # Blend the same point on two different curves. Keep their traversal
    # direction so a sprite never turns back or jumps when the path changes.
    tall_x = 12*math.cos(angle) - 6*math.sin(angle)
    tall_y = 30*math.sin(angle) + 4*math.cos(angle)
    wide_x = 34*math.cos(angle) + 5*math.sin(2*angle)
    wide_y = 8*math.sin(angle) + 6*math.cos(2*angle) - 5*math.cos(angle)
    x = HEAD_X + round(tall_x + (wide_x-tall_x)*blend) - 4 + 48
    yoff = tall_y + (wide_y-tall_y)*blend
    y = round((HEAD_Y+yoff-7+17)/2) + 16
    return x, y


def animated_position(phase, amount, plane=0):
    index, halfway = divmod(phase, 2)
    start = position(index, amount, plane)
    if not halfway:
        return start
    end = position(index+1, amount, plane)
    return tuple((a+b)//2 for a, b in zip(start, end))


def helper():
    c = Code(ENTRY)

    def a(op, addr):
        c.emit(op, addr & 255, addr >> 8)

    # Fold the low four bits of tick >> 6 into a triangle. Deriving both
    # clocks from the snapshot keeps skipped or repeated draws in phase.
    a(0xad, TICK_HIGH)
    c.emit(0x0a, 0x0a)
    a(0x8d, SHAPE_OFFSET)
    a(0xad, TICK_LOW)
    c.emit(*([0x4a]*6))
    a(0x0d, SHAPE_OFFSET)
    c.emit(0x29, 15, 0xc9, 8)
    c.branch(0x90, 'shape_ready')
    c.emit(0x49, 15)
    c.label('shape_ready')
    a(0x8d, AMOUNT)
    c.emit(*([0x0a]*5))
    a(0x8d, SHAPE_OFFSET)

    # Each PAL frame advances half a table interval.
    a(0xad, TICK_LOW)
    c.emit(0x4a, 0x4a, 0x4a)
    a(0x8d, ANGLE_INDEX)
    c.emit(0x4a)
    a(0x8d, 0x83ff)  # Keep the existing 16-entry colour cycle.
    c.emit(0xa0, 0)
    c.label('plane')
    c.emit(0x98, 0x0a, 0x0a, 0x0a, 0x18)
    a(0x6d, ANGLE_INDEX)
    c.emit(0x29, 31)
    a(0x0d, SHAPE_OFFSET)
    c.emit(0xaa)
    for table, values in (('xs', VALUES_X), ('ys', VALUES_Y)):
        c.jump(0xbd, table)
        a(0x99, values)
    a(0xad, TICK_LOW)
    c.emit(0x29, 1 << PHASE_SHIFT)
    c.branch(0xf0, 'next_plane')
    a(0x20, MIDPOINT_ENTRY)
    c.label('next_plane')
    c.emit(0xc8, 0xc0, 4)
    c.branch(0xd0, 'plane')
    c.emit(0x60)
    for axis, name in enumerate(('xs', 'ys')):
        c.label(name)
        c.emit(*(position(index, amount)[axis]
                 for amount in range(8) for index in range(32)))
    code = bytes(c.finish())
    from outro_text import FINAL_MARK_GLYPHS
    assert ENTRY+len(code) <= FINAL_MARK_GLYPHS, len(code)
    return code, midpoint(c.labels)


def midpoint(tables):
    c = Code(MIDPOINT_ENTRY)
    for name in ('xs', 'ys'):
        c.labels[name] = tables[name]

    def a(op, addr):
        c.emit(op, addr & 255, addr >> 8)

    c.emit(0xe8, 0x8a, 0x29, 31)
    a(0x0d, SHAPE_OFFSET)
    c.emit(0xaa)
    for table, values in (('xs', VALUES_X), ('ys', VALUES_Y)):
        c.jump(0xbd, table)
        c.emit(0x18)
        a(0x79, values)
        c.emit(0x6a)
        a(0x99, values)
    c.emit(0x60)
    code = bytes(c.finish())
    assert len(code) <= 32
    return code


def install(bank):
    out = bytearray(bank)
    for addr, data in zip((ENTRY, MIDPOINT_ENTRY), helper()):
        offset = addr - 0x4000
        assert not any(out[offset:offset+len(data)])
        out[offset:offset+len(data)] = data
    assert not any(out[VALUES_X-0x4000:0x69c4-0x4000])
    return bytes(out)
