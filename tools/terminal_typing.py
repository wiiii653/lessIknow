"""Typed terminal rows in the reserved tail of the intro helper."""
from build_sequence import Code
ENTRY=0xeb44
TIMES=0xc828
COUNT=0x0dd8
LENGTHS=0xc8a8  # times/lengths occupy unused control glyphs in the font
PROMPT_DELAY=4
ENTER_DELAY=4
BLINK_MASK=64

def schedule():
    import outro_text as text
    ticks=[]
    starts=text.page_starts()
    for start,end,page in zip(starts,(*starts[1:],text.END),text.pages()):
        now=start
        for line in page:
            ticks.append(now);now+=PROMPT_DELAY+len(line)+ENTER_DELAY
        assert now<=end,(page,now,end)
        ticks.extend([end]*(text.HISTORY_ROWS-len(page)))
    return ticks+[text.END]*(text.HISTORY_ROWS+1)

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
    c.label('keys');c.emit(0x18,0x69,len(text.PROMPT));c.jump(0x4C,'ready')
    c.label('full');c.emit(0xa9,127);c.branch(0xd0,'ready')
    c.label('future');c.emit(0xa9,0)
    c.label('ready');a(0x8d,COUNT)
    a(0xB9,LENGTHS);c.emit(0x38);a(0xED,0x0DD5);c.branch(0xB0,'length_ready');c.emit(0xA9,0)
    c.label('length_ready');a(0x8D,0x0DD9);a(0xCD,COUNT);c.branch(0xB0,'length_kept');a(0x8D,COUNT)
    c.label('length_kept')
    # Cursor is visible only until the next logical line begins.
    c.emit(0xc8,0x38);a(0xad,0x83e2);a(0xf9,TIMES)
    a(0xad,0x83e3);a(0xf9,TIMES+len(schedule()));c.emit(0x08)
    c.jump(0xbd,'dest');c.jump(0x8d,'write_lo');c.jump(0x8d,'blank_lo');c.jump(0x8d,'cursor_lo');a(0x8d,0xdd3)
    c.emit(0xa9,0xbf);a(0x8d,0xdd4)
    a(0xAC,COUNT);c.branch(0xF0,'blank_start');c.emit(0x88)
    c.label('copy');c.label('read');c.emit(0xB9,0,0)
    c.label('write');c.emit(0x99,0,0xBF,0x88);c.branch(0x10,'copy')
    c.label('blank_start');a(0xAC,COUNT);c.emit(0xA9,32)
    c.label('blank');c.emit(0x99,0,0xBF,0xC8,0xC0,40);c.branch(0xD0,'blank')
    c.emit(0x28);c.branch(0xb0,'done')
    a(0xad,COUNT);c.branch(0xf0,'done');
    c.label('cursor');c.emit(0xa8)
    a(0xad,0x83e2);c.emit(0x29,BLINK_MASK);c.branch(0xd0,'done')
    c.emit(0xa9,0x5f)
    # Reuse the destination operand: a single extra STA instruction.
    c.label('cursor_value');c.emit(0x99,0,0xbf)
    c.label('done');c.emit(0x60)
    c.label('dest');c.emit(*(row*40 for row in range(text.HISTORY_ROWS)))
    c.labels['read_lo']=c.labels['read']+1;c.labels['read_hi']=c.labels['read']+2
    c.labels['write_lo']=c.labels['write']+1
    c.labels['blank_lo']=c.labels['blank']+1
    c.labels['cursor_lo']=c.labels['cursor_value']+1
    # Cursor uses the same row base as the copy loop.
    # Patched below with an absolute load/store in the row-setup code.
    return c

def inserts():
    c=helper();data=bytes(c.finish())
    if len(data)>220:raise ValueError(f'terminal helper too large: {len(data)}')
    assert TIMES+len(schedule())*2<=LENGTHS
    return [(ENTRY,data)]
