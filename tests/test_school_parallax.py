"""Verify all precomposed two-layer frames and their clocked transitions."""
from hashlib import sha256
import unittest
import test_sequence as sequence
from school_parallax import FACE_OFFSETS, PROFILE_POLISH, frames, party_frames

class SchoolParallaxArtTests(unittest.TestCase):
    def test_v330_walk_with_profile_and_sleeve_polish(self):
        original = party_frames()
        self.assertEqual(sha256(b''.join(original)).hexdigest(),
                         'ca87ddba2adaed2cf082f42c4c013b3db221ce48e43803a956a1954b36b02fa4')
        for i, (before, after, offset) in enumerate(zip(original, frames(), FACE_OFFSETS)):
            changed = {n: b for n, (a, b) in enumerate(zip(before, after)) if a != b}
            expected = {y * 160 + x + offset: ink for x, y, ink in PROFILE_POLISH}
            for y in range(31, 36):
                for x in range(38, 44):
                    pixel = y * 160 + x + offset
                    if before[pixel] == 3:
                        expected[pixel] = 1
            self.assertEqual(changed, expected, i)


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

    def test_boy_hair_and_jacket_stay_opaque_in_both_portraits(self):
        from school_story import load_rgb
        cpu=None
        for tick,path in ((2992,'build/school-neutral.rgb'),(4114,'build/school-neutral.rgb'),
                          (4488,'build/school.rgb'),(4862,'build/school-front.rgb'),
                          (5236,'build/school-front.rgb'),(5610,'build/school.rgb')):
            source=load_rgb(path);cpu=sequence.execute(tick,cpu)
            pixels=sequence.SequenceTests().raster(cpu)
            for x0,y0,x1,y1 in ((120,8,147,19),(117,56,130,64),(149,55,158,64)):
                for y in range(y0,y1):
                    for x in range(x0,x1):
                        for dy in range(3):
                            self.assertEqual(pixels[(y*3+dy)*160+x],source[y*160+x],(tick,x,y))
            for y in range(55,64):
                self.assertEqual(pixels[(y*3)*160+158:(y*3)*160+160],bytes((1,1)))

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
            # Leave the notes' space clear while the boy is whistling.
            if expected is whistle:
                for y in range(27,39):
                    self.assertEqual(pixels[y*160+70:y*160+94],
                                     expected[y*160+70:y*160+94],(tick,y))
