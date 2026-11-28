"""Exercise the caption renderer, blanking handoff and footer lifetime."""

import json
import unittest
from bisect import bisect_right

import test_sequence as sequence
import test_outro_palette
import basketball_hero as hero
import girl_eyes
from ribbon_dance import SIDE_START, SIDE_END, CUTS as RIBBON_CUTS, LAUNCH_PREP
from launch_kiss import START as KISS_START
from build_sequence import DANCE_TICK
from gym_practice import PRACTICE_CUTS, practice_shot
from music_timing import tick_at_bar
from school_story import SCHOOL_PORTRAIT_TICK
from outro_text import TEXT_DLI_VCOUNT
from scene_palette_io import SHADOW
from main_act_terminal import (
    BITMAP_ROWS, CREDITS_START, CUES, DISPLAY_LISTS, DRAW_ROW, FOOTER_OFFSET,
    GLYPH_ROWS, PALETTES, PALETTE_ENTRY, PALETTE_STEPS, PALETTE_STEP_TICKS,
    ROW_BYTES, ROW_COUNT, TYPE_STEP, WIDTH, line_starts, palette_steps, resources,
    typing_lines,
)


@unittest.skipIf(sequence.MPU is None, 'install py65 for terminal checks')
class MainActTerminalTests(unittest.TestCase):
    def test_captions_finish_during_the_shots_they_describe(self):
        lines = dict(zip(typing_lines(), line_starts()))
        windows = (
            ('ATARI ARENA. TRACKING ARRIVAL.', CUES[0], SCHOOL_PORTRAIT_TICK),
            ('CLOSE-UP. HE HOLDS THE BALL.', *PRACTICE_CUTS[:2]),
            ('HE SHOOTS. TRACKING THE BALL.', *PRACTICE_CUTS[1:]),
            ('STRETCHING AT THE WALL BARS.', PRACTICE_CUTS[2], DANCE_TICK),
            ('TRACKING A SINGLE DANCER.', SIDE_START, SIDE_END),
            ('SPIRAL REVERSES.', tick_at_bar(34), tick_at_bar(35)),
            ('ORGANIC REVERSES.', tick_at_bar(35), tick_at_bar(36)),
            ('BACK TO SPIRAL.', tick_at_bar(36), tick_at_bar(37)),
            ('BACK TO ORGANIC.', tick_at_bar(37), tick_at_bar(38)),
            ('TWO DANCERS FLANK THE LEAD.', RIBBON_CUTS[0], RIBBON_CUTS[1]),
            ('CUTTING TO THE LEAD DANCER ALONE.', RIBBON_CUTS[1], RIBBON_CUTS[2]),
            ('THE TRIO RETURNS.', RIBBON_CUTS[2], LAUNCH_PREP),
            ('LIFT.', LAUNCH_PREP, KISS_START),
            ('A KISS.', KISS_START, hero.CUTAWAY_START),
            ('BACK THROUGH THE TUNNEL TO THE COURT.', hero.CUTAWAY_START, hero.START),
            ('TRACKING THE DUNK.', hero.DUNK, hero.SHATTER_START),
            ('CRACK', hero.SHATTER_START, hero.END),
            ('HOLDING THE CLOSE-UP ON HER EYES.', girl_eyes.START, girl_eyes.END),
            ('FOLLOWING THE LAST BANANA PASS.', girl_eyes.END, tick_at_bar(110)),
        )
        for text, action, cut in windows:
            with self.subTest(text=text):
                line = '> '+text
                start = lines[line]
                self.assertLessEqual(action, start)
                self.assertLess(start-action, TYPE_STEP)
                self.assertLess(start+TYPE_STEP*len(line), cut)

    def test_caption_waits_for_next_frame_if_music_overruns_blanking(self):
        class LateRaster(sequence.RuntimeMemory):
            counts = None

            def __getitem__(self, address):
                if address == 0xd40b and self.counts is not None:
                    return next(self.counts, 128)
                return super().__getitem__(address)

        metadata = json.loads(sequence.METADATA.read_text())
        memory = LateRaster(sequence.XEX.read_bytes())
        cpu = sequence.execute(CUES[0], sequence.MPU(memory=memory))
        footer = DISPLAY_LISTS[0] + FOOTER_OFFSET

        def call(name, steps):
            cpu.sp = 0xfd
            memory[0x1fe:0x200] = [0xfe, 0x7f]
            cpu.pc = metadata[name]
            for _ in range(steps):
                if cpu.pc == 0x7fff:
                    return
                cpu.step()
            self.fail(f'{name} did not return')

        call('main_terminal_update', 2000)
        memory.counts = iter((123, 128))
        call('main_terminal_commit', 256)
        self.assertEqual(memory[footer], 0x70)
        memory.counts = None
        memory[0xd40b] = 124
        call('main_terminal_commit', 256)
        self.assertEqual(memory[footer], 1)

    def test_continuous_log_scrolls_and_scene_cuts_only_change_palette(self):
        metadata = json.loads(sequence.METADATA.read_text())
        glyphs, codes, lines = resources()
        glyph_count = len(codes)+1
        starts = line_starts()
        ramps = palette_steps()
        cpu = None

        def call(name, interrupt_at=None):
            bank = cpu.memory[0xd301]
            cpu.sp = 0xfd
            cpu.memory[0x1fe:0x200] = [0xfe, 0x7f]
            cpu.pc = metadata[name]
            for _ in range(10000):
                if cpu.pc == 0x7fff:
                    self.assertIsNone(interrupt_at)
                    self.assertEqual(cpu.memory[0xd301], bank)
                    return
                if interrupt_at == cpu.pc:
                    cpu.memory[0xd40b] = 43
                    cpu.nmi()
                    interrupt_at = None
                cpu.step()
            self.fail(f'{name} did not return')

        def tail(base):
            m = cpu.memory
            offset = base + FOOTER_OFFSET
            self.assertEqual(m[offset], 1)
            address = m[offset+1] + m[offset+2]*256
            self.assertEqual(m[address], 0x90)
            rows = []
            for row in range(ROW_COUNT):
                p = address+1+row*10
                self.assertEqual(m[p:p+2], [0, 0x4c])
                self.assertEqual(m[p+4:p+10], [0x0c]*5+[0x8c if row==ROW_COUNT-1 else 0x0c])
                rows.append(m[p+2] | (m[p+3] << 8))
            self.assertEqual(m[address+41:address+44], [0x41, 0, base >> 8])
            self.assertIn(frozenset(rows), (frozenset(BITMAP_ROWS[:4]), frozenset(BITMAP_ROWS[4:])))
            return rows

        def bitmap_rows(front):
            return [bytes(cpu.memory[row:row+ROW_BYTES]) for row in front]

        def expected_bitmap(row):
            return bytes(
                glyphs[y*glyph_count+row[x]] << 4 | glyphs[y*glyph_count+row[x+1]]
                for y in range(GLYPH_ROWS) for x in range(0, WIDTH, 2)
            )

        practice_samples = {*PRACTICE_CUTS, PRACTICE_CUTS[0]+420}
        palette_samples = {CUES[0], *(cue+step*PALETTE_STEP_TICKS for cue in CUES[1:]
                                      for step in range(PALETTE_STEPS+1))}
        samples = {CREDITS_START-1, *palette_samples, *practice_samples}
        samples.update(cue-1 for cue in CUES[1:])
        for start,line in zip(starts, lines):
            samples.update((start-1, start, start+TYPE_STEP, start+len(line)*TYPE_STEP))

        front = None
        for tick in (*sorted(samples), starts[0]+TYPE_STEP):
            cpu = sequence.execute(tick, cpu)
            if tick in practice_samples:
                cpu = sequence.execute(tick, cpu)
                self.assertEqual(sequence.SequenceTests().raster(cpu), practice_shot(tick))
            previous_front = front
            previous_rows = None if front is None else bitmap_rows(front)
            interrupt_at = None
            if tick == CUES[1]+3*PALETTE_STEP_TICKS:
                interrupt_at = PALETTE_ENTRY
            if tick == starts[0]+TYPE_STEP:
                interrupt_at = DRAW_ROW
            call('main_terminal_update', interrupt_at)
            if front is not None:
                self.assertEqual(tail(DISPLAY_LISTS[0]), front)
                self.assertEqual(bitmap_rows(front), previous_rows)
            cpu.memory[0xd40b] = 80
            call('main_terminal_commit')
            if front is not None:
                self.assertEqual(tail(DISPLAY_LISTS[0]), front)
            cpu.memory[0xd40b] = 124
            call('main_terminal_commit')
            front = tail(DISPLAY_LISTS[0])
            self.assertEqual(tail(DISPLAY_LISTS[1]), front)
            current = bisect_right(starts, tick)-1
            rows = []
            for line_index in range(current-3, current+1):
                row = lines[line_index] if line_index >= 0 else b''
                if line_index == current and current >= 0:
                    row = row[:(tick-starts[current])//TYPE_STEP]
                    if tick & 64 == 0:
                        row += bytes([codes['_']])
                rows.append(row.ljust(WIDTH, b'\0'))
            actual = bitmap_rows(front)
            self.assertEqual(actual, [expected_bitmap(row) for row in rows], tick)
            if tick in CUES[1:]:
                self.assertEqual(front, previous_front, tick)
                self.assertEqual(actual, previous_rows, tick)
            if tick not in palette_samples:
                continue
            index = bisect_right(CUES,tick)-1
            step = min((tick-CUES[index])//PALETTE_STEP_TICKS, PALETTE_STEPS-1)

            palette = bytes(cpu.memory[0xd016:0xd019])
            self.assertEqual(cpu.memory[SHADOW], palette[0])
            interrupt = test_outro_palette.OutroPaletteTests().interrupt
            live_low = cpu.memory[0x24a7]
            for low in (live_low, live_low ^ 7):
                cpu.memory[0x24a7] = low
                music_tick = bytes(cpu.memory[0x24a7:0x24aa])
                interrupt(cpu, 2*TEXT_DLI_VCOUNT)
                self.assertEqual(bytes(cpu.memory[0xd016:0xd019]),
                                 bytes((ramps[index*PALETTE_STEPS+step], *palette[1:])))
                self.assertEqual(bytes(cpu.memory[0x24a7:0x24aa]), music_tick)
            cpu.memory[0x24a7] = live_low
            interrupt(cpu, 8)
            self.assertEqual(bytes(cpu.memory[0xd016:0xd019]), palette)

        for tick in (CREDITS_START, 0):
            cpu = sequence.execute(tick, cpu)
            for base in DISPLAY_LISTS:
                self.assertEqual(bytes(cpu.memory[base+FOOTER_OFFSET:base+FOOTER_OFFSET+3]),
                                 b'\x70\x70\x70')

    def test_palette_ramps_connect_scene_inks_in_small_steps(self):
        ramps = palette_steps()
        for index, target in enumerate(PALETTES):
            ramp = ramps[index*PALETTE_STEPS:(index+1)*PALETTE_STEPS]
            self.assertEqual(ramp[0], PALETTES[max(0,index-1)])
            self.assertEqual(ramp[-1], target)
            for before, after in zip(ramp, ramp[1:]):
                hue_gap = abs((before>>4)-(after>>4))
                self.assertLessEqual(min(hue_gap, 15-hue_gap), 1)
                self.assertLessEqual(abs((before&14)-(after&14)), 2)
