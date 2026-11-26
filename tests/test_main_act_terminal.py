"""Exercise the caption renderer, blanking handoff and footer lifetime."""

import json
import unittest

import test_sequence as sequence
import test_outro_palette
from gym_practice import PRACTICE_CUTS, practice_shot
from outro_text import TEXT_DLI_VCOUNT
from scene_palette_io import SHADOW
from main_act_terminal import (
    CAPTIONS, CREDITS_START, CUES, DISPLAY_LISTS, FONT, FOOTER_OFFSET, PALETTES,
    SCREENS, WIDTH, resources,
)


@unittest.skipIf(sequence.MPU is None, 'install py65 for terminal checks')
class MainActTerminalTests(unittest.TestCase):
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

    def test_ten_pages_use_inactive_screen_and_release_both_footers(self):
        metadata = json.loads(sequence.METADATA.read_text())
        _, pages = resources()
        cpu = None

        def call(name):
            cpu.sp = 0xfd
            cpu.memory[0x1fe:0x200] = [0xfe, 0x7f]
            cpu.pc = metadata[name]
            for _ in range(10000):
                if cpu.pc == 0x7fff:
                    return
                cpu.step()
            self.fail(f'{name} did not return')

        def tail(base):
            m = cpu.memory
            offset = base + FOOTER_OFFSET
            self.assertEqual(m[offset], 1)
            address = m[offset+1] + m[offset+2]*256
            self.assertEqual(bytes(m[address:address+3]), bytes((0x90, 0x44, SCREENS[0] & 255)))
            self.assertEqual(bytes(m[address+4:address+10]),
                             bytes((0x04, 0x04, 0x84, 0x41, 0, base >> 8)))
            return m[address+3] * 256 + m[address+2]

        front = None
        for index, (cue, record) in enumerate(zip(CUES, pages)):
            cpu = sequence.execute(cue, cpu)
            call('main_terminal_update')
            if front is not None:
                self.assertEqual(tail(DISPLAY_LISTS[0]), front)
            cpu.memory[0xd40b] = 80
            call('main_terminal_commit')
            if front is not None:
                self.assertEqual(tail(DISPLAY_LISTS[0]), front)
            cpu.memory[0xd40b] = 124
            call('main_terminal_commit')
            new_front = tail(DISPLAY_LISTS[0])
            self.assertEqual(tail(DISPLAY_LISTS[1]), new_front)
            self.assertEqual(cpu.memory[0xd409], FONT >> 8)
            self.assertIn(new_front, SCREENS)
            self.assertNotEqual(front, new_front)
            self.assertEqual(bytes(cpu.memory[new_front:new_front+WIDTH]),
                             record[:1].ljust(WIDTH, b'\0'))

            cpu = sequence.execute(cue+410, cpu)
            call('main_terminal_update')
            call('main_terminal_commit')
            front = tail(DISPLAY_LISTS[0])
            rows = record.split(b'\0')[:-1]
            self.assertEqual(len(rows), 1+len(CAPTIONS[index]))
            self.assertEqual(bytes(cpu.memory[front:front+4*WIDTH]),
                             b''.join(row.ljust(WIDTH, b'\0') for row in rows))

            palette = bytes(cpu.memory[0xd016:0xd019])
            self.assertEqual(bytes(cpu.memory[SHADOW:SHADOW+3]), palette)
            interrupt = test_outro_palette.OutroPaletteTests().interrupt
            live_low = cpu.memory[0x24a7]
            for low in (live_low, live_low ^ 7):
                cpu.memory[0x24a7] = low
                music_tick = bytes(cpu.memory[0x24a7:0x24aa])
                interrupt(cpu, 2*TEXT_DLI_VCOUNT)
                self.assertEqual(bytes(cpu.memory[0xd016:0xd019]), bytes(PALETTES[index]))
                self.assertEqual(bytes(cpu.memory[0x24a7:0x24aa]), music_tick)
            cpu.memory[0x24a7] = live_low
            interrupt(cpu, 8)
            self.assertEqual(bytes(cpu.memory[0xd016:0xd019]), palette)

            if cue == PRACTICE_CUTS[0]:
                # The practice renderer alternates legacy framebuffer maps
                # while the caption keeps the same text page.
                for tick in (PRACTICE_CUTS[0] + 420, *PRACTICE_CUTS[1:]):
                    for _ in range(2):
                        cpu = sequence.execute(tick, cpu)
                        self.assertEqual(sequence.SequenceTests().raster(cpu), practice_shot(tick))
                        self.assertEqual(tail(DISPLAY_LISTS[0]), front)

        for tick in (CREDITS_START, 0):
            cpu = sequence.execute(tick, cpu)
            for base in DISPLAY_LISTS:
                self.assertEqual(bytes(cpu.memory[base+FOOTER_OFFSET:base+FOOTER_OFFSET+3]),
                                 b'\x70\x70\x70')
