"""Compare the encounter artwork with the actual v330 raster."""
from hashlib import sha256
import unittest

from school_story import GIRL_PLACEMENTS, boy_poses, foreground_girl, party_girl, story_frames


class GirlBackArtTests(unittest.TestCase):
    def test_untouched_party_sprite(self):
        self.assertEqual(
            sha256(b''.join(party_girl())).hexdigest(),
            '7048e7bc1244e3a55522169e37c3e10da002d55c52d0d73cfc77d64e6db2663a')

    def test_foreground_uses_one_source_cell_per_scene_cell(self):
        left, top, width, height = GIRL_PLACEMENTS[0]
        girl, mask = foreground_girl()
        self.assertEqual(len(girl), width * height)
        foreground = story_frames()[2]
        turned = boy_poses()[1]
        expected = bytearray(turned)
        for y in range(64 - top):
            for x in range(width):
                at = y * width + x
                if mask[at]:
                    for dy in range(3):
                        expected[((top + y) * 3 + dy) * 160 + left + x] = girl[at]
        self.assertEqual(foreground, expected)

        # Native hair detail includes both unequal pixel pairs and unequal
        # row pairs inside the sprite, where a doubled 48x64 image repeats.
        self.assertTrue(any(mask[i] and mask[i+1] and girl[i] != girl[i+1]
                            for i in range(0, 23 * width, 2)))
        self.assertTrue(any(mask[i] and mask[i+width] and girl[i] != girl[i+width]
                            for y in range(0, 22, 2)
                            for i in range(y * width, (y + 1) * width)))

    def test_three_distant_views_show_the_blue_skirt_and_small_bolt(self):
        self.assertEqual([sha256(frame).hexdigest() for frame in story_frames()[3:]], [
            '324745d54a9c135ee93ab82ade1980abae3af78ddb09b80362be022f695e0654',
            '125afce7b31cc22ef2af679ad0f11e2282879f47dbf5fa696b4d94838f437926',
            '7b9432eae267cb9b89614cd553a30c3d6ee77e75043ce8b507439f4344f3e18a',
        ])
