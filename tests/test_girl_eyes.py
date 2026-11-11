"""Actual callback chooses the eye close-up only in its montage window."""
import unittest
import test_sequence as sequence
from girl_eyes import START, END, frame_at, pixels
import post_trevor_director as director

@unittest.skipIf(sequence.MPU is None, 'py65 required')
class GirlEyesTests(unittest.TestCase):
    def test_scene_boundaries_animation_and_bank_restoration(self):
        cpu = None
        seen = set()
        for tick in (START-1, START, START+32, START+64, START+96, END-1, END):
            cpu=sequence.execute(tick,cpu)
            m=cpu.memory
            expected=frame_at(tick,director.frame_at(tick))
            self.assertEqual(m[0x83ed],expected,tick)
            self.assertEqual(m[0xd301],0xff)
            if START<=tick<END:
                seen.add(expected)
                art=pixels(expected-60)
                wanted=bytes(art[y//2*160+x] for y in range(192) for x in range(160))
                self.assertEqual(sequence.SequenceTests().raster(cpu),wanted,tick)
            else:
                self.assertLess(expected,60)
        self.assertEqual(seen,{60,61,62,63})
