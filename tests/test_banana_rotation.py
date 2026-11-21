"""Verify the original fixed texture through the whole camera cycle."""
from hashlib import sha256
import unittest

from mosaic import pixels


class BananaRotationTests(unittest.TestCase):
    def test_original_rotator_frames(self):
        # SHA-256 of the 32 decoded 160×96 playfields, in camera order,
        # captured separately for each motif from stereo release 119 (v381).
        references = {
            'gold': 'caa9d95b944e7583fb5e7318e8db6af1699b0c8dd6bc4882465361f695375bcf',
            'peeled': 'fd958c1045f3f752a1b454162921d7f02d967c1bd645c2f1c8501671ad2d301f',
        }
        for variant, (motif, digest) in enumerate(references.items()):
            with self.subTest(motif=motif):
                cycle = b''.join(pixels(frame, variant) for frame in range(32))
                self.assertEqual(sha256(cycle).hexdigest(), digest)
