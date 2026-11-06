"""Verify unique color pairs over the complete music timeline."""
import unittest
import math
from pmg_preview import atari_rgb
import test_sequence as sequence

@unittest.skipIf(sequence.MPU is None,'py65 required')
class MosaicPaletteTests(unittest.TestCase):
    def test_palette_stays_saturated_from_first_cycle_to_last(self):
        for tick in (11968,11969,12155,14958,32912,32913,59832):
            with self.subTest(tick=tick):
                memory=sequence.execute(tick).memory
                first,second=memory[0xd016],memory[0xd017]
                self.assertIn(first&15,(8,10,12,14))
                self.assertIn((second&15)-(first&15),(0,4))
                self.assertNotEqual(first>>4,second>>4)

    def test_no_palette_repeats_across_both_mosaic_sections(self):
        pairs=[];cpu=None
        ticks=[11968+187*i for i in range(16)] + [32912+187*i for i in range(145)]
        for tick in ticks:
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            pair=(m[0xd016],m[0xd017])
            self.assertNotIn(pair,pairs,(tick,pair))
            self.assertNotEqual(*pair)
            self.assertGreaterEqual(math.dist(atari_rgb(pair[0]),atari_rgb(pair[1])),105)
            dim=sequence.execute(tick+32,cpu).memory
            self.assertGreaterEqual(math.dist(atari_rgb(dim[0xd016]),atari_rgb(dim[0xd017])),105)
            pairs.append(pair)
        self.assertEqual(len(pairs),161)
