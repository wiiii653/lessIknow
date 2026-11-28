"""Real ANTIC PMBASE is write-only; visible PMG must never be repainted."""
import unittest
import test_sequence as seq
from test_engine_cache import TrackedMemory
from final_boy import START,STAR_SHAPE,NOTE_SHAPES,notes_active
from final_orbits import PHASE_MASK, PHASE_SHIFT, animated_position as orbit_position
from test_story_finale import ORBIT_GLYPH_TOP_OFFSET, orbit_amount

class FinalPMGPublishTests(unittest.TestCase):
    def test_one_clean_glyph_per_plane_with_write_only_pmbase(self):
        class HardwareMemory(TrackedMemory):
            def __getitem__(self,address):
                if address==0xd407:return 0xff
                return super().__getitem__(address)
        m=HardwareMemory(seq.XEX.read_bytes());cpu=seq.MPU(memory=m)
        previous=None
        for tick in range(START,START+768,16):
            old=(m.ram[0xd407]&0xfc)<<8
            m.writes.clear();seq.execute(tick,cpu)
            base=(m.ram[0xd407]&0xfc)<<8
            if previous is not None:
                self.assertNotEqual(base,old)
                self.assertFalse(any(old+0x180<=a<old+0x400 for a in m.writes))
            publication=m.writes.index(0xd407)
            self.assertFalse(any(0x980<=a<0xc00 or 0x8980<=a<0x8c00 for a in m.writes[publication+1:]))
            for plane in range(4):
                shape=NOTE_SHAPES[plane] if notes_active(tick) else STAR_SHAPE
                expected=bytearray(128)
                y=orbit_position((tick>>PHASE_SHIFT)&PHASE_MASK,orbit_amount(m),plane)[1]-ORBIT_GLYPH_TOP_OFFSET
                expected[y:y+12]=bytes(shape)
                self.assertEqual(bytes(m[base+0x200+plane*128:base+0x280+plane*128]),expected)
            previous=base
