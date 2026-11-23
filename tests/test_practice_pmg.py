"""Practice overlays protect the artwork and keep the visible PMG page intact."""
import unittest

import test_sequence as sequence
from gym_practice import PRACTICE_CUTS, practice_shot
from pmg_preview import player_masks
from whistle_pmg import SHAPES


@unittest.skipIf(sequence.MPU is None, 'py65 required')
class PracticePmgTests(unittest.TestCase):
    def test_ball_patches_and_sparks_leave_skin_uncovered(self):
        tick = PRACTICE_CUTS[0]
        art = practice_shot(tick)
        cpu = sequence.execute(tick)
        original = sequence.SequenceTests().raster(cpu)
        orbits = [set() for _ in range(4)]
        for tick in range(tick+4, tick+256, 4):
            m = cpu.memory
            front = (m[0xd407]&0xfc)<<8
            old = m[front+0x180:front+0x400]
            sequence.execute(tick, cpu)
            self.assertEqual(m[front+0x180:front+0x400], old)
            self.assertEqual(m[0xd301], 0xff)
            self.assertEqual(sequence.SequenceTests().raster(cpu), original)
            visible = player_masks(art, m, 192, pmg_color_offset=16)
            self.assertTrue(any(a != b for a,b in zip(art,visible)))
            self.assertTrue(all(b == 3 for a,b in zip(art,visible) if a == 3))
            for p, positions in enumerate(orbits):
                positions.add(m[0xd004+p])
        self.assertTrue(all(len(positions)>25 for positions in orbits))

    def test_wall_bars_reuses_the_note_silhouettes(self):
        start = PRACTICE_CUTS[2]
        cpu = sequence.execute(start)
        m = cpu.memory
        self.assertEqual(m[0xd000:0xd004], [158, 0, 0, 0])
        front = (m[0xd407]&0xfc)<<8
        old = m[front+0x180:front+0x400]
        sequence.execute(start+24*4, cpu)
        self.assertEqual(m[front+0x180:front+0x400], old)
        base = (m[0xd407]&0xfc)<<8
        self.assertEqual(m[0xd004:0xd008], [0]*4)
        for p, glyph in enumerate(SHAPES):
            start_row = base+0x200+p*128
            rows = bytes(m[start_row:start_row+128])
            self.assertEqual(rows.strip(b'\0'), bytes(glyph[::2]).strip(b'\0'))
        self.assertEqual(m[0xd301], 0xff)

    def test_whistle_phrases_alternate_between_the_two_girls(self):
        start = PRACTICE_CUTS[2]
        cpu = sequence.execute(start)
        for elapsed, position in ((0, 158), (255, 0), (256, 94), (511, 0), (512, 158)):
            sequence.execute(start+elapsed, cpu)
            self.assertEqual(cpu.memory[0xd000:0xd004], [position, 0, 0, 0])
