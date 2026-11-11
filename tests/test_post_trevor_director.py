"""Post-fight beat montage reuses textures and keeps the ball over the hole."""
import unittest
import test_sequence as seq
import post_trevor_director as d

class PostTrevorDirectorTests(unittest.TestCase):
    def test_music_aligned_cuts_and_fixed_outro_entry(self):
        from music_timing import tick_at_bar
        cuts=d.cuts()
        self.assertEqual(cuts[0][0],37984)
        self.assertEqual(d.END,49850)
        self.assertEqual(len(cuts),72)
        self.assertTrue(all(tick<d.END for tick,mode in cuts))
        self.assertEqual(cuts,tuple(sorted(cuts)))
        allowed={tick_at_bar(n,4)-4000 for n in range(112*4,144*4)}|{37984}
        self.assertTrue(all(t in allowed for t,m in cuts))
        self.assertLessEqual(len(d.helper()),d.SIZE)

    def test_live_frames_at_cuts_and_ball_hole_coverage(self):
        cpu=None;seen=set()
        samples=sorted({d.START,d.END-1}|{t+delta for t,m in d.cuts() for delta in (-1,0,16) if d.START<=t+delta<d.END})
        for tick in samples:
            cpu=seq.execute(tick,cpu);m=cpu.memory
            self.assertEqual(m[0x83ed],d.frame_at(tick),tick)
            self.assertEqual(m[0xd301],0xff)
            self.assertEqual(m[0xd01d],3)
            if m[0x83ed]<32:continue
            seen.add(m[0x83ed]&48)
            for y in range(88,105):
                for x in range(75,86):
                    if (x-79.5)**2+((y//2-47.5)*1.66)**2>=25:continue
                    covered=False
                    for plane in range(4):
                        col=(x-(m[0xd000+plane]-48))//2
                        if 0<=col<8 and m[0xa00+plane*128+(y+17)//2]&(128>>col):covered=True
                    self.assertTrue(covered,(tick,x,y))
        self.assertEqual(seen,{32,48})
        self.assertEqual(seq.execute(d.END,cpu).memory[0x83e0],17)

    def test_banana_windows_and_earlier_clock_are_preserved(self):
        for tick in range(11967,d.END,17):
            clock=tick+(4000 if tick>=d.MONTAGE_START else 0)
            original=((clock>>4)&31)|((clock>>5)&32)
            if tick<d.START or original<32:
                self.assertEqual(d.frame_at(tick),original,tick)
