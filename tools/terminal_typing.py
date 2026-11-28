"""Typed terminal rows in the reserved tail of the intro helper."""
from build_sequence import Code
ENTRY=0xeb44
TIMES=0xc828
COUNT=0x0dd8
LENGTHS=0xc8a8  # times/lengths occupy unused control glyphs in the font
PROMPT_DELAY=4
ENTER_DELAY=4
BLINK_MASK=64
CACHED_LINES=0xbff0  # Tail of the $BF00 page after six 40-byte rows (4 displayed).
CACHED_INKS=0xbff6  # Visible length, with bit 7 marking a visible cursor.
ROW_STATE=0x0dd9
CACHE_ENTRY=0xc220
CACHE_LOOKUP=0xebcf

def schedule():
    import outro_text as text
    starts = text.page_starts()
    for start, end, line in zip(starts, (*starts[1:], text.END), text.typing_lines()):
        assert start + PROMPT_DELAY + len(line) + ENTER_DELAY <= end
    return ([text.START] * (text.HISTORY_ROWS-1) + list(starts)
            + [text.END] * (text.HISTORY_ROWS+1))

def helper():
    import outro_text as text
    c=Code(ENTRY)
    def a(op,v):c.emit(op,v&255,v>>8)
    # Y = logical terminal line, X = visible row, TMP_LO/HI = source.
    for address,label in ((0xdd3,'read_lo'),(0xdd4,'read_hi')):
        a(0xad,address);c.jump(0x8d,label)
    c.emit(0x38);a(0xad,0x83e2);a(0xf9,TIMES);a(0x8d,COUNT)
    a(0xad,0x83e3);a(0xf9,TIMES+len(schedule()));c.branch(0x90,'future');c.branch(0xd0,'full')
    a(0xad,COUNT)
    c.emit(0x38,0xE9,PROMPT_DELAY);c.branch(0xB0,'keys');c.emit(0xA9,len(text.PROMPT));c.branch(0xD0,'ready')
    # SBC left carry set. Key counts here are nonzero and fit in one byte.
    c.label('keys');c.emit(0x69,len(text.PROMPT)-1);c.branch(0xD0,'ready')
    c.label('full');c.emit(0xa9,127);c.branch(0xd0,'ready')
    c.label('future');c.emit(0xa9,0)
    c.label('ready');a(0x8d,COUNT)
    a(0xB9,LENGTHS);a(0xCD,COUNT);c.branch(0xB0,'length_kept');a(0x8D,COUNT)
    c.label('length_kept')
    a(0x20,CACHE_ENTRY);c.branch(0x90,'address')
    c.jump(0xbd,'dest');c.jump(0x8d,'write_lo');c.jump(0x8d,'blank_lo');c.jump(0x8d,'cursor_lo')
    a(0xAC,COUNT);c.branch(0xF0,'blank_start');c.emit(0x88)
    c.label('copy');c.label('read');c.emit(0xB9,0,0)
    c.label('write');c.emit(0x99,0,0xBF,0x88);c.branch(0x10,'copy')
    c.label('blank_start');a(0xAC,COUNT);c.emit(0xA9,32)
    c.label('blank');c.emit(0x99,0,0xBF,0xC8,0xC0,40);c.branch(0xD0,'blank')
    a(0xad,ROW_STATE);c.branch(0x10,'address')
    a(0xac,COUNT)
    c.emit(0xa9,0x5f)
    # Reuse the destination operand: a single extra STA instruction.
    c.label('cursor_value');c.emit(0x99,0,0xbf)
    c.label('address');c.jump(0xbd,'dest');a(0x8d,0xdd3)
    c.emit(0x60)
    c.label('dest');c.emit(*(row*40 for row in range(text.HISTORY_ROWS)))
    c.labels['read_lo']=c.labels['read']+1;c.labels['read_hi']=c.labels['read']+2
    c.labels['write_lo']=c.labels['write']+1
    c.labels['blank_lo']=c.labels['blank']+1
    c.labels['cursor_lo']=c.labels['cursor_value']+1
    # Cursor uses the same row base as the copy loop.
    # Patched below with an absolute load/store in the row-setup code.
    return c

def cache_helper():
    c=Code(CACHE_ENTRY)
    def a(op,v):c.emit(op,v&255,v>>8)
    # Cursor is visible only until the next logical line begins.
    c.emit(0xc8,0x38);a(0xad,0x83e2);a(0xf9,TIMES)
    a(0xad,0x83e3);a(0xf9,TIMES+len(schedule()));c.branch(0xb0,'plain')
    c.emit(0x8a);c.branch(0xf0,'plain')
    a(0xad,0x83e2);c.emit(0x29,BLINK_MASK);c.branch(0xd0,'plain')
    a(0xad,COUNT);c.branch(0xf0,'plain');c.emit(0x09,0x80)
    a(0x4c,CACHE_LOOKUP)
    c.label('plain');a(0xad,COUNT)
    a(0x4c,CACHE_LOOKUP)
    return bytes(c.finish())


def cache_lookup():
    c=Code(CACHE_LOOKUP)
    def a(op,v):c.emit(op,v&255,v>>8)
    a(0x8d,ROW_STATE)
    c.emit(0x88,0x98);a(0xdd,CACHED_LINES);c.branch(0xd0,'dirty')
    a(0xad,ROW_STATE);a(0xdd,CACHED_INKS);c.branch(0xf0,'clean')
    c.label('dirty');c.emit(0x98);a(0x9d,CACHED_LINES)
    a(0xad,ROW_STATE);a(0x9d,CACHED_INKS)
    c.emit(0x38,0x60)
    c.label('clean');c.emit(0x18,0x60)
    return bytes(c.finish())

def inserts():
    c=helper();data=bytes(c.finish())
    assert ENTRY+len(data)<=CACHE_LOOKUP
    assert TIMES+len(schedule())*2<=LENGTHS
    lookup=cache_lookup()
    from banana_variants import VARIANT_ENTRY
    assert CACHE_LOOKUP+len(lookup)<=VARIANT_ENTRY
    return [(ENTRY,data),(CACHE_LOOKUP,lookup)]
