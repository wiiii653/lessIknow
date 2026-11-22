"""Reuse the finale's star artwork in the early XEX loading display."""
from itertools import groupby

from build_sequence import Code
from build_visual_prototype import xex_segment
from extract_music import segments
from outro_text import FINAL_MARK_ROWS, FINAL_MARK_WIDTH, GLYPHS, final_mark

FONT = 0x0c00  # Restored by the late runtime segment, after all INIT refreshes.
MARK = 0x3b00
PHASE = MARK + 120
REFRESH = 0x3b80


DELTAS = 0x1400
VBI_CODE = 0x1100
VBI_VECTOR = 0x0222  # Immediate OS vertical blank vector.
SETVBV = 0xe45c


def frame_deltas(frames):
    encoded = bytearray()
    for before, after in zip(frames, frames[1:] + frames[:1]):
        delta = (a ^ b for a, b in zip(before, after))
        for changed, group in groupby(delta, bool):
            run = bytes(group)
            assert 0 < len(run) < 127
            encoded.append(len(run) | (128 if changed else 0))
            if changed:
                encoded.extend(run)
        encoded.append(0)
    return bytes(encoded + b'\xff')


def frame_callback(glyph_start):
    c = Code(VBI_CODE)

    def absolute(op, addr):
        c.emit(op, addr & 255, addr >> 8)

    c.label('install')
    c.jump(0xad, 'installed')
    c.branch(0xd0, 'return')
    for i in range(2):
        absolute(0xad, VBI_VECTOR+i)
        c.jump(0x8d, 'old_vbi_' + str(i))
    c.emit(0xa9, 1)
    c.jump(0x8d, 'installed')
    c.emit(0xa9, 6)
    c.labels['install_x'] = c.origin + len(c.data) + 1
    c.emit(0xa2, 0)
    c.labels['install_y'] = c.origin + len(c.data) + 1
    c.emit(0xa0, 0)
    absolute(0x4c, SETVBV)
    c.label('return')
    c.emit(0x60)

    c.label('stop')
    c.jump(0xae, 'old_vbi_1')
    c.jump(0xac, 'old_vbi_0')
    c.emit(0xa9, 6)
    absolute(0x20, SETVBV)
    absolute(0x4c, 0x38a0)

    c.label('vbi')
    c.emit(0x08, 0x48, 0x8a, 0x48, 0x98, 0x48, 0xa2, 0)
    c.label('command')
    c.jump(0x20, 'read')
    c.emit(0xc9, 0xff)
    c.branch(0xd0, 'decode')
    c.emit(0xa9, DELTAS & 255)
    c.jump(0x8d, 'ptr_lo')
    c.emit(0xa9, DELTAS >> 8)
    c.jump(0x8d, 'ptr_hi')
    c.jump(0x4c, 'command')
    c.label('decode')
    c.emit(0xa8)
    c.branch(0xf0, 'restore')
    c.branch(0x30, 'literal')
    c.emit(0x8a, 0x18)
    c.jump(0x6d, 'token')
    c.emit(0xaa)
    c.jump(0x4c, 'command')
    c.label('literal')
    c.emit(0x29, 127, 0xa8)
    c.label('xor')
    c.jump(0x20, 'read')
    absolute(0x5d, glyph_start)
    absolute(0x9d, glyph_start)
    c.emit(0xe8, 0x88)
    c.branch(0xd0, 'xor')
    c.jump(0x4c, 'command')
    c.label('restore')
    c.emit(0x68, 0xa8, 0x68, 0xaa, 0x68, 0x28)
    c.label('chain')
    c.emit(0x4c, 0, 0)
    c.labels['old_vbi_0'] = c.labels['chain']+1
    c.labels['old_vbi_1'] = c.labels['chain']+2
    c.label('read')
    c.label('ptr')
    absolute(0xad, DELTAS)
    c.jump(0xee, 'ptr_lo')
    c.branch(0xd0, 'read_done')
    c.jump(0xee, 'ptr_hi')
    c.label('read_done')
    c.jump(0x8d, 'token')
    c.emit(0x60)
    c.labels['ptr_lo'] = c.labels['ptr']+1
    c.labels['ptr_hi'] = c.labels['ptr']+2
    c.label('token')
    c.emit(0)
    c.label('installed')
    c.emit(0)
    c.data[c.labels['install_x']-c.origin] = c.labels['vbi'] >> 8
    c.data[c.labels['install_y']-c.origin] = c.labels['vbi'] & 255
    return bytes(c.finish()), c.labels


def install(data, *, full_rate=False):
    entries = list(segments(data))
    title = 'THE LESS I KNOW THE BETTER'
    credit = 'A\\SLOP BY OGNJEN / SILLY VENTURE 2026 WE'
    alphabet = ' ' + ''.join(sorted(set(title + credit + 'LOADING. ') - {' '}))
    codes = {ch: i for i, ch in enumerate(alphabet)}

    def text(line):
        return bytes(codes[ch] for ch in line.center(40))

    def loading(dots=0):
        return text(('LOADING' + '.'*dots).ljust(len('LOADING...')))

    font = bytearray(1024)
    for ch, i in codes.items():
        if ch != ' ':
            rows = GLYPHS[ch]
            if full_rate:
                # Mode 4 uses the same background register as the mark.
                rows = ((int(row[0]) << 6) | (int(row[1:3] != '00') << 4) |
                        (int(row[3]) << 2) | int(row[4]) for row in rows)
                font[i*8+1:i*8+8] = bytes(rows)
            else:
                font[i*8+1:i*8+8] = bytes(int(row, 2) << 2 for row in rows)
    tiles_per_frame = FINAL_MARK_WIDTH * FINAL_MARK_ROWS
    for i in range(1 if full_rate else 4):
        _, glyphs = final_mark(i*8)
        start = 8*(len(codes) + tiles_per_frame*i)
        assert len(glyphs) == tiles_per_frame*8 and start + len(glyphs) <= len(font)
        font[start:start+len(glyphs)] = glyphs

    dlist = bytes.fromhex('70707045003b05057070420038425038422838418038')
    mark = bytearray(121)
    x = (40 - FINAL_MARK_WIDTH)//2
    for row in range(FINAL_MARK_ROWS):
        offset = row*40 + x
        start = len(codes) + row*FINAL_MARK_WIDTH
        mark[offset:offset+FINAL_MARK_WIDTH] = bytes(range(start, start+FINAL_MARK_WIDTH))
    c = Code(REFRESH)
    c.emit(0xad, PHASE&255, PHASE>>8, 0xaa)
    c.jump(0xbd, 'frames')
    c.emit(0xa2, 0)
    c.label('tiles')
    for row in range(FINAL_MARK_ROWS):
        dest = MARK + row*40 + x
        if row:
            c.emit(0x18, 0x69, FINAL_MARK_WIDTH)
        c.emit(0x9d, dest&255, dest>>8)
    c.emit(0x38, 0xe9, 2*FINAL_MARK_WIDTH-1, 0xe8, 0xe0, FINAL_MARK_WIDTH)
    c.branch(0xd0, 'tiles')
    c.emit(0xad,PHASE&255,PHASE>>8,0x18,0x69,1,0x29,3,0x8d,PHASE&255,PHASE>>8,0x60)
    c.label('frames')
    c.emit(*(len(codes)+tiles_per_frame*i for i in range(4)))
    refresh = bytes(c.finish())

    last_wrapper = max(i for i, (addr, _, _) in enumerate(entries) if addr == 0x3900)
    early_blocks = [(FONT,font),(MARK,mark),(REFRESH,refresh)]
    refresh_entry = REFRESH
    if full_rate:
        glyph_start = FONT + len(codes)*8
        animation = frame_deltas([final_mark(i)[1] for i in range(32)])
        vbi, labels = frame_callback(glyph_start)
        early_blocks = [(FONT,font),(MARK,mark),(VBI_CODE,vbi),(DELTAS,animation)]
        for address, block in early_blocks:
            assert all(end < address or start >= address+len(block)
                       for start, end, _ in entries[:last_wrapper+2])
        refresh_entry = labels['install']
        dlist = dlist.replace(b'\x42', b'\x44')

    out = bytearray(b'\xff\xff')
    for index, (addr, _, payload) in enumerate(entries):
        if index == 0:
            assert addr == 0x3800
            for address, block in early_blocks:
                out.extend(xex_segment(address,block))
            payload = text(title) + loading() + text(credit)
        elif index == 1:
            assert addr == 0x3880
            payload = dlist
        elif index == 2:
            assert addr == 0x38a0 and payload[-1] == 0x60
            for target in (bytes.fromhex('8df402'), bytes.fromhex('8d09d4')):
                old = bytes.fromhex('a9e0') + target
                assert payload.count(old) == 1
                payload = payload.replace(old, bytes((0xa9,FONT>>8)) + target)
            # ANTIC 2 uses PF2 for its background, while ANTIC 5 uses COLBK.
            for target in (bytes.fromhex('8dc602'), bytes.fromhex('8d18d0')):
                old = bytes.fromhex('a988') + target
                assert payload.count(old) == 1
                payload = payload.replace(old, bytes.fromhex('a982') + target)
            if full_rate:
                for shadow, hardware, old_value, new_value in (
                    (0x02c4,0xd016,0x38,0x0e), (0x02c5,0xd017,0x2c,0x9a),
                    (0x02c6,0xd018,0x82,0x2c), (0x02c8,0xd01a,0x82,0),
                ):
                    for address in (shadow, hardware):
                        store = bytes((0x8d,address&255,address>>8))
                        old = bytes((0xa9,old_value)) + store
                        assert payload.count(old) == 1
                        payload = payload.replace(old, bytes((0xa9,new_value)) + store)
            payload = payload[:-1] + bytes((0x4c,refresh_entry&255,refresh_entry>>8))
        elif addr == 0x3900:
            # Keep both refresh calls and the original INIT dispatch intact.
            assert len(payload) == 140
            count = payload[60:100].count(14)
            end_count = payload[100:140].count(14)
            prefix = payload[:60]
            if full_rate and index == last_wrapper:
                call = prefix.rindex(bytes.fromhex('20a038'))
                prefix = prefix[:call+1] + labels['stop'].to_bytes(2,'little') + prefix[call+3:]
            payload = prefix + loading(count) + loading(end_count)
        out.extend(xex_segment(addr,payload))
    assert len(out) < 1024*1024
    return bytes(out)
