"""Prevent static assets from silently overwriting double-buffered video RAM."""
import unittest
from build_bitmap_sequence import validate_allocations


class MemoryAllocationTests(unittest.TestCase):
    def test_os_shadow_asset_cannot_overlap_second_framebuffer(self):
        with self.assertRaisesRegex(ValueError, r"memory overlap at \$C000"):
            validate_allocations([(0xb000, bytes(0x1f00)), (0xc000, bytes(375))])

    def test_copy_helper_starts_immediately_after_second_framebuffer(self):
        validate_allocations([(0xb000, bytes(0x1f00)), (0xcf00, bytes(0x100))])
