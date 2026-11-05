"""Verify all precomposed two-layer frames and their clocked transitions."""
import unittest
import test_sequence as sequence
from school_parallax import frames

@unittest.skipIf(sequence.MPU is None,'py65 required')
class SchoolParallaxTests(unittest.TestCase):
    def test_each_frame_and_unchanged_timing(self):
        art=frames();self.assertEqual(len(art),18)
        self.assertEqual(len(set(art)),18)
        cpu=None
        for i in range(18):
            tick=3553+32*i
            cpu=sequence.execute(tick,cpu)
            expected=bytes(art[i][y//3*160+x] for y in range(192) for x in range(160))
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected,i)
            self.assertEqual(cpu.memory[0x83e0],14)
        self.assertEqual(sequence.execute(4114,cpu).memory[0x83e0],8)
        self.assertEqual(sequence.execute(4488,cpu).memory[0x83e0],9)

    def test_hair_strands_keep_fixed_anchored_roots(self):
        from pathlib import Path
        from school_parallax import HAIR_ROOTS, hair_strands
        from school_story import color
        rgba=Path('build/school-girl-cutout-v034.rgba').read_bytes()
        tips=[set() for _ in HAIR_ROOTS]
        for phase in range(6):
            strands=hair_strands(phase)
            for i,((root_x,root_y,_,_),strand) in enumerate(zip(HAIR_ROOTS,strands)):
                self.assertEqual(strand[-1],(root_x,root_y))
                offset=(root_y*160+root_x)*4
                self.assertGreaterEqual(rgba[offset+3],128)
                self.assertEqual(color(rgba[offset:offset+3]),3)
                self.assertTrue(all(abs(a[1]-b[1])<=1 and b[0]-a[0]==1 for a,b in zip(strand,strand[1:])))
                tips[i].add(strand[0][1])
        self.assertTrue(all(len(values)==3 for values in tips))
        self.assertGreaterEqual(len({hair_strands(p)[0][0][1]-hair_strands(p)[1][0][1] for p in range(6)}),3)
