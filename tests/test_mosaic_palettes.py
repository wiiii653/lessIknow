"""Verify unique color pairs over the complete music timeline."""
import unittest
import math
from pmg_preview import atari_rgb
import test_sequence as sequence
from final_boy import START as FINAL_SHOT
from banana_variants import variant_at

@unittest.skipIf(sequence.MPU is None,'py65 required')
class MosaicPaletteTests(unittest.TestCase):
    def test_palette_stays_saturated_from_first_cycle_to_last(self):
        for tick in (11968,11969,12155,14958,32912,32913,FINAL_SHOT-1):
            with self.subTest(tick=tick):
                memory=sequence.execute(tick).memory
                self.assertEqual(memory[0x83e0],6)
                first,second=memory[0xd016],memory[0xd017]
                if memory[0x83ed] < 32:
                    self.assertEqual((first,memory[0xd018]),(0xfa,0xfe) if variant_at(tick) else (0xf8,0xfe))
                    continue
                self.assertIn(first&15,(6,8,10,12))
                self.assertIn((second&15)-(first&15),(2,4))
                self.assertNotEqual(first>>4,second>>4)

    def test_no_palette_repeats_across_both_mosaic_sections(self):
        pairs=[];cpu=None
        ticks=[11968+187*i for i in range(16)] + [32912+187*i for i in range(145)]
        # V145 replaces the last 8C interval with its own picture and fade;
        # both samples of a mosaic colour pair must remain inside that effect.
        ticks=[tick for tick in ticks if tick+32<FINAL_SHOT]
        for tick in ticks:
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            self.assertEqual(m[0x83e0],6)
            if m[0x83ed] < 32:
                # Fruit inks are deliberately stable gold/yellow; only the
                # background cycles. Unique pairs apply to the tunnel.
                self.assertEqual((m[0xd016],m[0xd018]),(0xfa,0xfe) if variant_at(tick) else (0xf8,0xfe))
                continue
            pair=(m[0xd016],m[0xd017])
            self.assertNotIn(pair,pairs,(tick,pair))
            self.assertNotEqual(*pair)
            self.assertGreaterEqual(math.dist(atari_rgb(pair[0]),atari_rgb(pair[1])),105)
            dim=sequence.execute(tick+32,cpu).memory
            self.assertGreaterEqual(math.dist(atari_rgb(dim[0xd016]),atari_rgb(dim[0xd017])),105)
            pairs.append(pair)
        self.assertGreater(len(pairs),50)
