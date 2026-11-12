"""Static artwork checks for full 360-degree tile orientation."""
import unittest
import math
import mosaic


class BananaRotationTests(unittest.TestCase):
    def test_four_cardinal_orientations_complete_one_turn(self):
        # Independent 0/90/180/270-degree sample transforms. The old
        # quarter-turn generator fails at frame 8 and subsequent quadrants.
        for frame,co,si,scale in ((0,1,0,1.08),(8,0,1,.78),
                                   (16,-1,0,.48),(24,0,-1,.78)):
            p=mosaic.pixels(frame);tile=mosaic.banana_tile()
            for y in (12,33,54,78):
                for x in (20,49,79,100,128):
                    xx,yy=x-79.5,(y-47.5)*1.66
                    u=int(scale*(co*xx-si*yy)+32)%64
                    v=int(scale*(si*xx+co*yy)+32)%64
                    self.assertEqual(p[y*160+x],tile[v*64+u],(frame,x,y))

    def test_last_to_first_frame_is_an_ordinary_step(self):
        frames=[mosaic.pixels(i) for i in range(32)]
        differences=[sum(a!=b for a,b in zip(frames[i],frames[(i+1)%32])) for i in range(32)]
        # Zoom is fastest/largest around the seam, so compare against the
        # strongest regular step rather than the smaller mid-zoom median.
        self.assertLess(differences[-1],max(differences[:-1])*1.15)
