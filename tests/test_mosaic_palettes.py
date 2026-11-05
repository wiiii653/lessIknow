"""Verify unique color pairs over the complete music timeline."""
import unittest
import math
from pmg_preview import atari_rgb
import test_sequence as sequence

@unittest.skipIf(sequence.MPU is None,'py65 required')
class MosaicPaletteTests(unittest.TestCase):
    def test_no_palette_repeats_across_both_mosaic_sections(self):
        pairs=[];cpu=None
        ticks=[11968+187*i for i in range(16)]+[32912+187*i for i in range(145)]
        for tick in ticks:
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            pair=(m[0xd016],m[0xd017])
            self.assertNotIn(pair,pairs,(tick,pair))
            self.assertNotEqual(*pair)
            self.assertGreaterEqual(math.dist(atari_rgb(pair[0]),atari_rgb(pair[1])),105)
            self.assertGreaterEqual(math.dist(atari_rgb(pair[0]-4),atari_rgb(pair[1]-4)),105)
            pairs.append(pair)
        self.assertEqual(len(pairs),161)
