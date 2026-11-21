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

    def test_three_distant_views_show_the_small_bolt(self):
        self.assertEqual([sha256(frame).hexdigest() for frame in story_frames()[3:]], [
            '98acbc77f5123ade51a53df9c5059d8ca78b185e96891e28c34c24fc5f4ddaf9',
            '568c86f86cd900564b46c044b331445befae7fb7c0f6f665a0714d542132c428',
            '902ffb8de6e3daff1a25f569831388c42957668e442a174e7bbdb36720b8d46b',
        ])
