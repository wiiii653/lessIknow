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

    def test_walk_matches_archived_v175_frames(self):
        from pathlib import Path
        from extract_music import segments
        from school_parallax import FACE_OFFSETS, FACE_DETAILS
        banks=[payload for lo,hi,payload in segments(
            Path('build/visual-prototype-v175.xex').read_bytes())
            if (lo,hi)==(0x8000,0xbfff)]
        for i,pixels in enumerate(frames()):
            packed=banks[14+19+i//4][(i%4)*2560:(i%4+1)*2560]
            expected=bytes(v>>shift&3 for v in packed for shift in (6,4,2,0))
            expected=bytearray(expected)
            for x,y,ink in FACE_DETAILS:
                pos=y*160+x+FACE_OFFSETS[i]
                self.assertEqual(expected[pos],3,(i,x,y))
                expected[pos]=ink
            self.assertEqual(pixels,bytes(expected),i)

    def test_boy_hair_and_jacket_stay_opaque_in_both_portraits(self):
        from school_story import load_rgb
        cpu=None
        for tick,path in ((2992,'build/school-neutral.rgb'),(4114,'build/school-neutral.rgb'),
                          (4488,'build/school.rgb'),(4862,'build/school-front.rgb'),
                          (5236,'build/school-front.rgb'),(5610,'build/school.rgb')):
            source=load_rgb(path);cpu=sequence.execute(tick,cpu)
            pixels=sequence.SequenceTests().raster(cpu)
            for x0,y0,x1,y1 in ((120,8,147,19),(117,56,130,64),(149,55,160,64)):
                for y in range(y0,y1):
                    for x in range(x0,x1):
                        for dy in range(3):
                            self.assertEqual(pixels[(y*3+dy)*160+x],source[y*160+x],(tick,x,y))

    def test_reaction_follows_girl_and_whistle_waits_for_doors(self):
        from school_story import boy_poses
        neutral,turned,whistle=boy_poses()
        self.assertNotEqual(neutral,turned)
        self.assertNotEqual(turned,whistle)
        for tick,expected in ((2992,neutral),(4114,neutral),(4488,turned),
                              (4862,whistle),(5236,whistle),(5610,turned)):
            cpu=sequence.execute(tick)
            pixels=sequence.SequenceTests().raster(cpu)
            for y in range(192):
                self.assertEqual(pixels[y*160+104:(y+1)*160],
                                 expected[y*160+104:(y+1)*160],(tick,y))
            # The notes above the entrance do not overlap any girl placement.
            for y in range(27,39):
                self.assertEqual(pixels[y*160+70:y*160+94],
                                 expected[y*160+70:y*160+94],(tick,y))
