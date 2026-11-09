"""Full 360-degree tile orientation and a continuous live 32-frame cycle."""
import unittest
import math
import test_sequence as seq
import mosaic
from music_timing import tick_at_bar


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

    def test_act5_visits_all_32_phases_without_half_turn_resets(self):
        cpu=None;seen=set();previous=None
        for tick in range(tick_at_bar(88),tick_at_bar(96),16):
            cpu=seq.execute(tick,cpu);frame=cpu.memory[0x83ed]
            self.assertEqual(frame,(tick>>4)&31,tick)
            if previous is not None:self.assertEqual(frame,(previous+1)&31,tick)
            self.assertEqual(cpu.memory[0xd301],0xff)
            seen.add(frame);previous=frame
        self.assertEqual(seen,set(range(32)))
        # Bar 92 must not jump from the first half to an unrelated frame.
        for tick in (33023,33024,34403,34404,34415,34416):
            cpu=seq.execute(tick,cpu)
            self.assertEqual(cpu.memory[0x83ed],(tick>>4)&31,tick)
        self.assertGreaterEqual(seq.execute(tick_at_bar(96),cpu).memory[0x83ed],32)
