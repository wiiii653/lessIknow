"""Centred BUM/BAM and bounded, per-hit placement at the striking hand."""
import unittest
import test_sequence as s
from trevor_polished import HITS,HANDS,impact_anchor

@unittest.skipIf(s.MPU is None,'py65 required')
class ImpactPlacementTests(unittest.TestCase):
    def test_both_words_are_centred_inside_the_bubble(self):
        for i in range(10):
            m=s.execute(HITS[i]+24).memory
            self.assertEqual(m[0xd000]+12,m[0xd004]+16,i)
            self.assertEqual(list(m[0xd000:0xd004]),[m[0xd004]+4+8*p for p in range(4)])

    def test_random_offsets_are_held_and_stay_close_to_correct_fist(self):
        positions={2:set(),4:set()};cpu=None
        for i,hit in enumerate(HITS):
            expected=impact_anchor(i)
            origin=(-2,-1) if HANDS[i]==2 else (-38,2)
            self.assertLessEqual(abs(expected[0]-origin[0]),6)
            self.assertLessEqual(abs(expected[1]-origin[1]),3)
            positions[HANDS[i]].add(expected)
            for age in (8,24,79):
                cpu=s.execute(hit+age,cpu);m=cpu.memory
                actual=tuple(v if v<128 else v-256 for v in (m[0x83ec],m[0x83ef]))
                self.assertEqual(actual,expected,(i,age))
                self.assertEqual(m[0xd004],152+expected[0])
        for hand in positions:self.assertGreaterEqual(len(positions[hand]),min(4,HANDS.count(hand)))

    def test_u_is_inverted_a_without_crossbar(self):
        from trevor_polished import impact_glyphs
        a=impact_glyphs(1)[1]
        expected=bytes(0xcc if row==0xfc else row for row in reversed(a))
        self.assertEqual(impact_glyphs(0)[1],expected)
        m=s.execute(HITS[0]+24).memory
        base=(m[0xd407]&0xfc)<<8
        dy=m[0x83ef] if m[0x83ef]<128 else m[0x83ef]-256
        self.assertEqual(bytes(m[base+0x280+45+dy:base+0x280+59+dy]),expected)
