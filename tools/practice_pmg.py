"""PMG overlays for the held close-up and the wall bars in the practice atlas."""
import math

from engine_effects import PMBASE_SHADOW
from build_sequence import Code
from gym_practice import PRACTICE_CUTS, practice_pixels
from whistle_pmg import SHAPES

ENTRY, LIMIT = 0x5000, 0x6000
NOTE_DATA = 0x4b10
NOTE_DATA_LIMIT = 0x4f00  # Existing cleanup routine.
BALL_LEFT, BALL_TOP = 75, 46 * 3
BALL_ROW = (BALL_TOP + 17) // 2
BALL_ROWS = 27
PHASES = 64
# Inclusive left, exclusive right. Ink 1 inside this trace is ball fabric.
# Cut out the fingers, dark outlines and ball seams at the native art resolution.
BALL_TRACE = (
    (83, 95), (80, 97), (79, 100), (82, 102), (84, 102), (78, 101),
    (75, 103), (81, 104), (81, 101), (79, 101), (78, 87), (80, 103),
    (82, 104), (82, 103), (81, 102), (79, 102), (75, 104), (75, 104),
)
BALL_COLORS = (0x3c, 0x5a, 0x8c, 0xac)
NOTE_COLORS = (0x2e, 0x9e, 0x5e, 0xce)
NOTE_MOUTH = (110, 84)
SECOND_NOTE_MOUTH = (36, 64)


def patch_frames(art):
    """Four adjacent narrow players cover the visible, 32-pixel ball."""
    for phase in range(8):
        planes = [bytearray(BALL_ROWS) for _ in range(4)]
        for row in range(BALL_ROWS):
            y0 = 2 * (BALL_ROW + row) - 17
            ys = (y0 // 3, (y0 + 1) // 3)
            for x in range(BALL_LEFT, BALL_LEFT + 32):
                if not all(46 <= y < 64 and
                           BALL_TRACE[y-46][0] <= x < BALL_TRACE[y-46][1] and
                           art[y*160+x] == 1 for y in ys):
                    continue
                # A curved moving highlight travels across the underlying seams.
                q = (x + phase + (row-12)**2//18) & 7
                if 1 <= q < 6:
                    plane, bit = divmod(x-BALL_LEFT, 8)
                    planes[plane][row] |= 0x80 >> bit
        yield planes


def sparks(art, plane):
    """Two crossed, tilted ellipses, each with two opposite particles."""
    tilt = math.radians(29 if plane < 2 else -31)
    for phase in range(PHASES):
        angle = math.tau * ((phase if plane < 2 else -phase) / PHASES
                            + (plane & 1)*.5 + (0 if plane < 2 else .19))
        u, v = 38*math.cos(angle), 19*math.sin(angle)
        x = round(89 + u*math.cos(tilt) - v*math.sin(tilt))
        y = round(154 + u*math.sin(tilt) + v*math.cos(tilt))
        row = (y+17)//2-2
        pattern = []
        for dy, shape in enumerate((1, 3, 3, 0, 2)):
            bits = 0
            ys = (2*(row+dy)-17, 2*(row+dy)-16)
            for bit in range(2):
                # Leave a one-cell margin around the skin to preserve outlines.
                xx = x + bit
                if (shape & (2 >> bit) and all(0 <= yy < 192 and
                        all(art[(yy//3)*160+sx] != 3 for sx in range(xx-1, xx+2))
                        for yy in ys)):
                    bits |= 2 >> bit
            pattern.append(bits << (2*plane))
        yield x+48, row, *pattern


def note_positions(plane):
    for phase in range(PHASES):
        age = (phase-plane*8) & (PHASES-1)
        if age >= 34:
            yield 0, 0
            continue
        t = age / 33
        x = NOTE_MOUTH[0] + round(32*t + 2*math.sin(t*math.tau))
        y = NOTE_MOUTH[1] - round(56*t + 5*math.sin(math.pi*t))
        yield 48+x, (y+17)//2-8


def helper():
    c = Code(ENTRY)

    def a(op, address):
        c.emit(op, address & 255, address >> 8)

    state = c.jump

    def clock(origin):
        a(0xad, 0x83e2)
        c.emit(0x38, 0xe9, origin & 255, 0x4a, 0x4a, 0xaa)
        state(0x8e, 'phase')

    def patch_high(label, high):
        state(0xad, 'page')
        c.emit(0x09, high)
        state(0x8d, label+'_hi')

    # X is 0 for the close-up and 1 for the stretching shot.
    # PMBASE is write-only. A new shot starts on the upper buffer, and
    # subsequent callbacks use the page recorded at publication.
    state(0xec, 'mode')
    c.branch(0xf0, 'same_mode')
    state(0x8e, 'mode')
    c.emit(0xa9, 0x80)
    c.branch(0xd0, 'prepare_page')
    c.label('same_mode')
    state(0xad, 'visible_page')
    c.emit(0x49, 0x80)
    c.label('prepare_page')
    state(0x8d, 'page')
    for i, high in enumerate((9, 10, 10, 11, 11)):
        patch_high(f'clear{i}', high)
    c.emit(0xa9, 0, 0xa2, 127)
    c.label('clear')
    for i, addr in enumerate((0x980, 0xa00, 0xa80, 0xb00, 0xb80)):
        c.label(f'clear{i}')
        a(0x9d, addr)
    c.emit(0xca)
    c.branch(0x10, 'clear')
    state(0xad, 'mode')
    c.branch(0xf0, 'closeup')
    c.jump(0x4c, 'notes')

    c.label('closeup')
    clock(PRACTICE_CUTS[0])
    for p in range(4):
        patch_high(f'patch{p}', 10 + p//2)
        state(0xad, 'phase')
        c.emit(0x29, 7, 0xaa)
        state(0xbd, 'mask_lo')
        state(0x8d, f'load{p}_lo')
        c.emit(0x18)
        state(0xbd, 'mask_hi')
        c.emit(0x69, p)
        state(0x8d, f'load{p}_hi')
        c.emit(0xa2, BALL_ROWS-1)
        c.label(f'patch_loop{p}')
        c.label(f'load{p}')
        c.emit(0xbd, 0, 0)
        c.label(f'patch{p}')
        a(0x9d, 0xa00+p*128+BALL_ROW)
        c.emit(0xca)
        c.branch(0x10, f'patch_loop{p}')
        c.emit(0xa9, 48+BALL_LEFT+p*8)
        state(0x8d, f'px{p}')
    for p in range(4):
        state(0xae, 'phase')
        state(0xbd, f'sx{p}')
        state(0x8d, f'mx{p}')
        state(0xbc, f'sy{p}')
        for row in range(5):
            key = f'spark{p}_{row}'
            patch_high(key+'read', 9)
            state(0x8d, key+'write_hi')
            c.label(key+'read')
            a(0xb9, 0x0980+row)
            state(0x1d, f'spark_bits{p}_{row}')
            c.label(key+'write')
            a(0x99, 0x0980+row)
    c.jump(0x4c, 'wait')

    c.label('notes')
    clock(PRACTICE_CUTS[2])
    # The elapsed high byte advances once per 64-frame phrase.
    a(0xad, 0x83e2)
    c.emit(0x38, 0xe9, PRACTICE_CUTS[2] & 255)
    a(0xad, 0x83e3)
    c.emit(0xe9, PRACTICE_CUTS[2] >> 8, 0x29, 1)
    state(0x8d, 'whistler')
    for p in range(4):
        patch_high(f'note{p}', 10+p//2)
        state(0xae, 'phase')
        state(0xbd, f'nx{p}')
        state(0x8d, f'px{p}')
        c.emit(0xa9, 0)
        state(0x8d, f'mx{p}')
        state(0xad, f'px{p}')
        c.branch(0xf0, f'note_done{p}')
        state(0xac, 'whistler')
        c.branch(0xf0, f'note_y{p}')
        c.emit(0x38, 0xe9, NOTE_MOUTH[0]-SECOND_NOTE_MOUTH[0])
        state(0x8d, f'px{p}')
        c.label(f'note_y{p}')
        state(0xbd, f'ny{p}')
        state(0xac, 'whistler')
        c.branch(0xf0, f'note_row{p}')
        c.emit(0x38, 0xe9, (NOTE_MOUTH[1]-SECOND_NOTE_MOUTH[1])//2)
        c.label(f'note_row{p}')
        c.emit(0xa8)
        c.emit(0xa2, 0)
        c.label(f'note_loop{p}')
        state(0xbd, f'glyph{p}')
        c.label(f'note{p}')
        a(0x99, 0xa00+p*128)
        c.emit(0xc8, 0xe8, 0xe0, len(SHAPES[p])//2)
        c.branch(0xd0, f'note_loop{p}')
        c.label(f'note_done{p}')

    c.label('wait')
    a(0xad, 0xd40b)
    c.emit(0xc9, 124)
    c.branch(0x90, 'wait')
    c.emit(0xc9, 128)
    c.branch(0xb0, 'wait')
    state(0xad, 'page')
    state(0x8d, 'visible_page')
    c.emit(0x09, 8)
    a(0x8d,PMBASE_SHADOW);a(0x8d,0xd407)
    for p in range(4):
        state(0xad, f'px{p}')
        a(0x8d, 0xd000+p)
        state(0xad, f'mx{p}')
        a(0x8d, 0xd004+p)
    state(0xae, 'mode')
    for p in range(4):
        state(0xbd, f'color{p}')
        a(0x8d, 0xd012+p)
    for addr, value in [(0xd00c, 0), (0xd01b, 1), (0xd01d, 3), (0xd400, 0x2e),
                        *((0xd008+p, 0) for p in range(4))]:
        c.emit(0xa9, value)
        a(0x8d, addr)
    c.emit(0x60)

    patched = [f'clear{i}' for i in range(5)]
    for p in range(4):
        patched.extend((f'patch{p}', f'load{p}', f'note{p}'))
        for row in range(5):
            patched.extend((f'spark{p}_{row}read', f'spark{p}_{row}write'))
        c.labels[f'load{p}_lo'] = c.labels[f'load{p}']+1
    for label in patched:
        c.labels[label+'_hi'] = c.labels[label]+2
    for name in ('page', 'visible_page', 'mode', 'phase', 'whistler', *(f'{axis}{p}' for axis in ('px','mx') for p in range(4))):
        c.label(name)
        c.emit(0xff if name == 'mode' else 0)
    art = practice_pixels()[:160*64]
    note_data = bytearray()
    for p in range(4):
        c.labels[f'color{p}'] = NOTE_DATA+len(note_data)
        note_data.extend((BALL_COLORS[p], NOTE_COLORS[p]))
        c.labels[f'glyph{p}'] = NOTE_DATA+len(note_data)
        note_data.extend(SHAPES[p][::2])
        for name, values in zip((f'nx{p}', f'ny{p}'), zip(*note_positions(p))):
            c.labels[name] = NOTE_DATA+len(note_data)
            note_data.extend(values)
        for name, values in zip((f'sx{p}', f'sy{p}', *(f'spark_bits{p}_{i}' for i in range(5))),
                                zip(*sparks(art, p))):
            c.label(name)
            c.emit(*values)
    # The four planes are page-separated. Store eight short masks per page.
    # Separate the code and table addresses so the bank budget is asserted.
    for part in ('lo', 'hi'):
        c.label('mask_'+part)
        for phase in range(8):
            addr = 0x5c00 + phase*BALL_ROWS
            c.emit(addr & 255 if part == 'lo' else addr >> 8)
    code = bytes(c.finish())
    assert ENTRY+len(code) <= 0x5c00, len(code)
    masks = [bytearray(256) for _ in range(4)]
    for phase, planes in enumerate(patch_frames(art)):
        for p, plane in enumerate(planes):
            start = phase*BALL_ROWS
            masks[p][start:start+BALL_ROWS] = plane
    assert 0x5c00 + sum(map(len, masks)) == LIMIT
    assert NOTE_DATA+len(note_data) <= NOTE_DATA_LIMIT
    return note_data, code.ljust(0x5c00-ENTRY, b'\0') + b''.join(masks)


def install(bank):
    for address, data in zip((NOTE_DATA, ENTRY), helper()):
        start = address-0x4000
        end = start+len(data)
        assert not any(bank[start:end]), 'practice effects overlap data in bank 8'
        bank[start:end] = data
