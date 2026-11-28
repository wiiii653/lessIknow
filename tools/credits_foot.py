"""Patch the raised shoe in the credits portrait on alternate kick attacks."""

from build_sequence import Code
from music_timing import tick_at_bar, tick_at_beat
from outro_loader import ENTRY as OUTRO_ENTRY, FLAG as OUTRO_FLAG
from outro_text import END
from school_portrait_bank import bank_value

DISPATCH = 0xFFDA
PATCH_ENTRY = DISPATCH + 6
ENTRY = 0x5E00
BANK_LIMIT = 0x6000
LIFT_TICKS = 16
LEFT, TOP, WIDTH = 112, 33, 24
PORTRAIT = 0x9000
MUSIC_NEXT_TICK = 0x24A7

# The lifted shoe, traced from the reference on the portrait's native grid.
LIFTED = (
    '333332000000000000000200',
    '033333020020020000200200',
    '003330222202222222220000',
    '022330222202202220211011',
    '022102222220222222211000',
    '022222202202220001100000',
    '002222022200001111000000',
    '002222200011111000000000',
    '011001111100000000000000',
    '000110000000000000200000',
)
ROW_BYTES = WIDTH // 4
PATCH_BYTES = ROW_BYTES * len(LIFTED)
# The four-bar break has two kicks per bar. The first attack precedes the
# rounded credits cut by one tick. After the break the kick plays every beat.
ATTACKS = (
    *(tick_at_bar(bar) - (bar == 112) for bar in range(112, 116)),
    # Release 122's kick attacks lead the rounded score by one tick here.
    *(tick_at_beat(beat) - (124*4 <= beat < 135*4) for beat in range(116*4, 137*4, 2)),
)
LIFTS = tuple(tick-LIFT_TICKS for tick in ATTACKS)


def patches(portrait):
    offsets = tuple((TOP+row)*40 + LEFT//4 for row in range(len(LIFTED)))
    rest = b''.join(portrait[offset:offset+ROW_BYTES] for offset in offsets)
    lifted = bytes(int(row[column:column+4], 4)
                   for row in LIFTED for column in range(0, WIDTH, 4))
    return rest, lifted


def dispatch(bitmap_bank):
    selector = bank_value(bitmap_bank)
    return bytes((
        0x20, PATCH_ENTRY & 255, PATCH_ENTRY >> 8,
        0x4C, OUTRO_ENTRY & 255, OUTRO_ENTRY >> 8,
        0xAD, 0x01, 0xD3, 0x48,
        0xAD, selector & 255, selector >> 8, 0x8D, 0x01, 0xD3,
        0x20, ENTRY & 255, ENTRY >> 8,
        0x68, 0x8D, 0x01, 0xD3,
        0x60,
    ))


def helper(portrait):
    c = Code(ENTRY)

    def a(op, address):
        c.emit(op, address & 255, address >> 8)

    # Read the next packet index in early blanking, after the last music DLI.
    # Two packets will play at the top of the upcoming frame before ANTIC
    # reaches the shoe, so compare against the second packet's index.
    a(0xad, 0xd40b); c.emit(0xc9, 124); c.branch(0x90, 'skip')
    c.emit(0xc9, 132); c.branch(0x90, 'sample')
    c.label('skip'); c.emit(0x60)
    c.label('sample')
    c.emit(0xa0, 0)
    a(0xad, MUSIC_NEXT_TICK+2); c.branch(0xf0, 'clock16')
    c.jump(0x4c, 'pose')
    c.label('clock16')
    a(0xad, MUSIC_NEXT_TICK); c.emit(0x18, 0x69, 1); c.jump(0x8d, 'now_lo')
    a(0xad, MUSIC_NEXT_TICK+1); c.emit(0x69, 0); c.jump(0x8d, 'now_hi')
    a(0xad, OUTRO_FLAG); c.branch(0xd0, 'check_end')
    # The first callback has just copied the resting portrait.
    c.emit(0xa9, 0); c.jump(0x8d, 'displayed')
    c.label('check_end')
    c.jump(0xad, 'now_hi')
    c.emit(0xc9, END >> 8)
    c.branch(0x90, 'check_start'); c.branch(0xd0, 'pose')
    c.jump(0xad, 'now_lo'); c.emit(0xc9, END & 255); c.branch(0xb0, 'pose')
    c.label('check_start')
    # During the first lift's page, the next lift is still in a later page.
    assert LIFTS[0] >> 8 < LIFTS[1] >> 8
    c.jump(0xad, 'now_hi'); c.emit(0xc9, LIFTS[0] >> 8); c.branch(0x90, 'pose')
    c.branch(0xd0, 'find')
    c.jump(0xad, 'now_lo'); c.emit(0x38); c.jump(0xed, 'lift_lo')
    c.branch(0x90, 'pose')
    c.emit(0xc9, LIFT_TICKS); c.branch(0xb0, 'pose')
    c.emit(0xc8); c.branch(0xd0, 'pose')
    c.label('find'); c.emit(0xa2, len(LIFTS)-1)
    c.label('previous')
    c.jump(0xad, 'now_lo'); c.emit(0x38); c.jump(0xfd, 'lift_lo')
    c.emit(0x48)
    c.jump(0xad, 'now_hi'); c.jump(0xfd, 'lift_hi')
    c.branch(0x90, 'earlier')
    c.branch(0xd0, 'rest_high')
    c.emit(0x68, 0xc9, LIFT_TICKS); c.branch(0xb0, 'pose')
    c.emit(0xc8); c.branch(0xd0, 'pose')
    c.label('rest_high'); c.emit(0x68); c.jump(0x4c, 'pose')
    c.label('earlier'); c.emit(0x68, 0xca); c.branch(0x10, 'previous')

    c.label('pose'); c.emit(0x98); c.jump(0xcd, 'displayed')
    c.branch(0xf0, 'done')
    c.emit(0x98); c.jump(0x8d, 'displayed')
    c.emit(0xa2, ROW_BYTES-1, 0xc0, 0); c.branch(0xf0, 'column')
    c.emit(0xa2, PATCH_BYTES+ROW_BYTES-1)
    c.label('column'); c.emit(0xa0, ROW_BYTES-1)
    c.label('copy')
    for row in range(len(LIFTED)):
        c.jump(0xbd, f'row{row}')
        a(0x99, PORTRAIT+(TOP+row)*40+LEFT//4)
    c.emit(0xca, 0x88); c.branch(0x10, 'copy')
    c.label('done'); c.emit(0x60)
    c.label('now_lo'); c.emit(0)
    c.label('now_hi'); c.emit(0)
    c.label('displayed'); c.emit(0)
    c.label('lift_lo'); c.emit(*(tick & 255 for tick in LIFTS))
    c.label('lift_hi'); c.emit(*(tick >> 8 for tick in LIFTS))
    for row in range(len(LIFTED)):
        c.labels[f'row{row}'] = c.origin+len(c.data)+row*ROW_BYTES
    for patch in patches(portrait):
        c.emit(*patch)
    code = bytes(c.finish())
    assert ENTRY+len(code) <= BANK_LIMIT
    return code
