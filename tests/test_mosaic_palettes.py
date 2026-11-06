"""Verify unique color pairs over the complete music timeline."""
import unittest
import math
from pmg_preview import atari_rgb
import test_sequence as sequence

@unittest.skipIf(sequence.MPU is None,'py65 required')
class MosaicPaletteTests(unittest.TestCase):
    def test_visual_pulses_recover_v051_phase(self):
        # Compare the actual 6502 palette writes with the preserved release,
        # including both previously measured early transitions.
        old_xex = (sequence.ROOT / 'releases/visual-prototype-v051.xex').read_bytes()
        for tick in (12527, 12528, 12529, 12552, 33095, 33096, 33099, 33112):
            with self.subTest(tick=tick):
                memory = sequence.RuntimeMemory(old_xex)
                memory[0xd40b] = 124
                for offset in range(3):
                    memory[0x24a7 + offset] = (tick >> (8 * offset)) & 255
                cpu = sequence.MPU(memory=memory)
                cpu.sp = 0xfd
                memory[0x1fe:0x200] = [0xfe, 0x7f]
                cpu.pc = 0x1400
                for _ in range(100000):
                    if cpu.pc == 0x7fff:
                        break
                    cpu.step()
                else:
                    self.fail('v051 callback did not return')
                current = sequence.execute(tick).memory
                self.assertEqual(tuple(current[0xd016:0xd018]),
                                 tuple(memory[0xd016:0xd018]))

    def test_no_palette_repeats_across_both_mosaic_sections(self):
        pairs=[];cpu=None
        ticks=[11968+187*i for i in range(16)] + [32912+187*i for i in range(145)]
        for tick in ticks:
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            pair=(m[0xd016],m[0xd017])
            self.assertNotIn(pair,pairs,(tick,pair))
            self.assertNotEqual(*pair)
            self.assertGreaterEqual(math.dist(atari_rgb(pair[0]),atari_rgb(pair[1])),105)
            self.assertGreaterEqual(math.dist(atari_rgb(pair[0]-4),atari_rgb(pair[1]-4)),105)
            pairs.append(pair)
        self.assertEqual(len(pairs),161)
