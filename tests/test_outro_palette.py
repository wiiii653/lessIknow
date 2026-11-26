"""Terminal row palettes and the bitmap split preserve music timing."""
import json
import unittest
import test_sequence as seq
from trevor_awakens import START,HIT

class OutroPaletteTests(unittest.TestCase):
    def interrupt(self,cpu,line):
        m=cpu.memory;m[0xd40b]=line//2
        cpu.sp=0xfa;m[0x1fb:0x1fe]=[0x20,0,7]
        cpu.pc=json.loads(seq.METADATA.read_text())['music_entry']
        for _ in range(10000):
            if cpu.pc==0x700:return
            cpu.step()
        self.fail('NMI did not return')

    def test_raster_inks_and_body_split_do_not_clock_music(self):
        from outro_palette import GLYPH_INKS, INK_PHASES, ROW_DLI_STEP, TICKS_PER_PHASE
        from outro_text import (START as OUTRO_START, BODY_DLI_VCOUNT,
                                COLOR_FONT, TEXT_DLI_VCOUNT, TEXT_ROWS)

        cpu=None
        for tick in range(OUTRO_START+1000,OUTRO_START+1064,TICKS_PER_PHASE):
            cpu=seq.execute(tick,cpu);m=cpu.memory
            before=bytes(m[0x24a7:0x24aa])
            self.assertEqual(m[0xd409],COLOR_FONT>>8)
            glyph=COLOR_FONT+ord('H')*8
            for row,ink in enumerate(GLYPH_INKS):
                codes={(m[glyph+row]>>shift)&3 for shift in (6,4,2,0)}
                self.assertEqual(codes,{0,ink})
            body=bytes(m[0xd016:0xd019])
            phase=(tick//TICKS_PER_PHASE)&7
            row_dlis = [TEXT_DLI_VCOUNT, *range(
                BODY_DLI_VCOUNT - (TEXT_ROWS-1)*ROW_DLI_STEP,
                BODY_DLI_VCOUNT, ROW_DLI_STEP)]
            row_palettes = []
            for row, vcount in enumerate(row_dlis):
                self.interrupt(cpu, vcount*2)
                palette = bytes(m[0xd016:0xd019])
                self.assertEqual(palette, bytes(INK_PHASES[(phase+row)&7]))
                self.assertEqual(bytes(m[0x24a7:0x24aa]),before)
                self.assertEqual(m[0xd301],0xff)
                row_palettes.append(palette)
            self.assertEqual(len(set(row_palettes)), TEXT_ROWS)
            self.assertEqual(len({palette[0] for palette in row_palettes}), TEXT_ROWS)
            # The first music DLI of the next frame restores the portrait.
            self.interrupt(cpu,8)
            self.assertEqual(bytes(m[0xd016:0xd019]),body)
            self.assertEqual((m[0xd01a],m[0xd301]),(0,0xff))

    def test_live_phase_continues_through_a_page_change_and_stale_snapshot(self):
        from outro_palette import INK_PHASES, LIVE_TICK, TICKS_PER_PHASE
        from outro_text import HISTORY_ROWS, STATE_START, TEXT_DLI_VCOUNT, page_starts

        start = page_starts()[1]
        cpu = seq.execute(start-1)
        self.assertEqual(cpu.memory[STATE_START], 0)
        self.interrupt(cpu, TEXT_DLI_VCOUNT*2)
        previous = ((start-1)//TICKS_PER_PHASE)&7
        self.assertEqual(bytes(cpu.memory[0xd016:0xd019]), bytes(INK_PHASES[previous]))

        cpu = seq.execute(start, cpu)
        self.assertEqual(cpu.memory[STATE_START], HISTORY_ROWS)
        # Advance music across frames while foreground stays on the page start.
        for tick in range(start, start+4*TICKS_PER_PHASE, TICKS_PER_PHASE):
            cpu.memory[LIVE_TICK] = tick&255
            self.interrupt(cpu, TEXT_DLI_VCOUNT*2)
            phase = (tick//TICKS_PER_PHASE)&7
            self.assertEqual(bytes(cpu.memory[0xd016:0xd019]), bytes(INK_PHASES[phase]))

    def test_trevor_entrance_has_the_fighting_base_palette(self):
        cpu=None
        for tick,pf1 in ((START,0x68),(START+500,0x68),(HIT-1,0x66)):
            cpu=seq.execute(tick,cpu)
            self.assertEqual(cpu.memory[0xd016:0xd019],[0x48,pf1,0x2a])

    def test_final_card_fixed_inks_track_fade_without_clocking_music(self):
        from final_boy import END
        from outro_palette import (CARD_DLI_VCOUNT, CARD_FADE, CARD_INKS,
                                   CARD_RESTORE_COLORS, CARD_RESTORE_VCOUNT, fade_inks)

        cpu = seq.execute(END,seq.execute(END))
        m = cpu.memory
        original_clock = bytes(m[0x24a7:0x24aa])
        for level in (0, 2, 7):
            m[CARD_FADE] = level * 2
            for counter in range(0,32,4):
                m[0x24aa] = counter
                self.interrupt(cpu,CARD_DLI_VCOUNT*2)
                self.assertEqual(tuple(m[0xd016:0xd019]),fade_inks(level,CARD_INKS))
                self.interrupt(cpu,CARD_RESTORE_VCOUNT*2)
                self.assertEqual(tuple(m[0xd016:0xd019]),CARD_RESTORE_COLORS)
                self.assertEqual(bytes(m[0x24a7:0x24aa]),original_clock)
                self.assertEqual(m[0x24aa],counter)
                self.assertEqual(m[0xd301],0xff)
