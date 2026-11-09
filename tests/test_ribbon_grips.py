"""Every live front/trio/solo pose roots each PMG ribbon at actual skin."""
import unittest
import ribbon_dance as d

class RibbonGripTests(unittest.TestCase):
    def test_original_and_all_inbetween_hands_land_on_the_actor(self):
        for frame in list(range(12))+[32,33,34,35]+list(range(37,55)):
            pixels,hands=d.artwork(frame)
            for x,y in hands:
                self.assertEqual(pixels[y*160+x],3,(frame,x,y))
    def test_every_phase_has_an_unbroken_centre_grip(self):
        streams=d.ribbon_streams()
        for plane in range(4):
            for phase in range(16):
                glyph=streams[plane*1024+phase*64:plane*1024+phase*64+64]
                for row in (31,32,33):
                    self.assertEqual(glyph[row]&0x18,0x18,(plane,phase,row))
    def test_quarter_sheet_uses_its_own_hand_annotations(self):
        import ribbon_inbetweens as mid
        self.assertNotEqual(mid.QUARTER_HANDS,mid.HANDS[:4])
        for index in range(14,18):
            pixels,hands=mid.artwork(index)
            self.assertTrue(all(pixels[y*160+x]==3 for x,y in hands))
