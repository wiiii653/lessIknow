"""Post-fight beat montage reuses textures and keeps the ball over the hole."""
import unittest
import test_sequence as seq
import post_trevor_director as d
from girl_eyes import frame_at as eye_frame_at

class PostTrevorDirectorTests(unittest.TestCase):
    def test_short_music_aligned_passes_and_fixed_outro_entry(self):
        from music_timing import tick_at_bar
        cuts=d.cuts()
        self.assertEqual(cuts[0][0],d.START)
        self.assertEqual(cuts[0][1],0x20)
        self.assertEqual(cuts[1][0],tick_at_bar(80))
        self.assertEqual(d.START,29656)
        self.assertEqual(d.END,tick_at_bar(112))
        self.assertEqual(len(cuts),33)
        self.assertTrue(all(tick<d.END for tick,mode in cuts))
        self.assertEqual(cuts,tuple(sorted(cuts)))
        self.assertEqual([t for t,m in cuts[1:]],[tick_at_bar(n) for n in range(80,112)])
        lengths=[b[0]-a[0] for a,b in zip(cuts,(*cuts[1:],(d.END,0)))]
        self.assertEqual(lengths[0],d.CYCLE_START-d.START)
        self.assertGreaterEqual(min(lengths[1:-1]),373)
        self.assertLessEqual(max(lengths[1:-1]),374)
        self.assertGreater(lengths[-1],0)
        self.assertEqual([mode for _,mode in cuts[1:13]],list(d.PATTERN))
        self.assertEqual([mode for _,mode in cuts[13:25]],list(d.PATTERN))
        for texture in (0,0x10,0x20):
            modes=[mode for _,mode in cuts if mode&0x30==texture]
            self.assertEqual({bool(mode&0x40) for mode in modes},{False,True})
            self.assertEqual({bool(mode&0x80) for mode in modes},{False,True})
        self.assertLessEqual(len(d.helper()),d.SIZE)
        self.assertLessEqual(d.BANK_ENTRY+len(d.bank_helper()),0x7250)

    def test_short_passes_keep_phase_through_reversals_and_avoid_eye_slots(self):
        timeline=d.timeline()
        self.assertEqual(len(timeline),33)
        self.assertEqual(timeline[0][3],d.timeline()[0][3])
        for previous,current in zip(timeline,timeline[1:]):
            _,old_mode,old_q,old_base=previous
            _,mode,q,base=current
            if (old_mode&0x30)!=(mode&0x30):
                self.assertEqual(base,0)
                continue
            period=32 if mode&32 else 12 if mode&16 else 16
            speed=2 if old_mode&64 else 1
            direction=-1 if old_mode&128 else 1
            self.assertEqual(base,(old_base+direction*speed*((q-old_q)&255))%period)
        from girl_eyes import START as eyes_start, END as eyes_end, frame_at as eye_frame_at
        for tick in range(d.START,d.END,16):
            frame=eye_frame_at(tick,d.frame_at(tick))
            if frame>=60:
                self.assertTrue(eyes_start<=tick<eyes_end,tick)
            else:
                self.assertLess(frame,60,tick)

    def test_live_frames_at_cuts_and_ball_hole_coverage(self):
        cpu=None;seen=set()
        samples=sorted({d.START,d.END-1}|{t+delta for t,m in d.cuts() for delta in (-1,0,16) if d.START<=t+delta<d.END})
        for tick in samples:
            cpu=seq.execute(tick,cpu);m=cpu.memory
            self.assertEqual(m[0x83ed],eye_frame_at(tick,d.frame_at(tick)),tick)
            self.assertEqual(m[0xd301],0xff)
            self.assertEqual(m[0xd01d],3)
            if m[0x83ed]<32:
                seen.add(0)
                continue
            seen.add(m[0x83ed]&48)
            for y in range(88,105):
                for x in range(75,86):
                    if (x-79.5)**2+((y//2-47.5)*1.66)**2>=25:continue
                    covered=False
                    for plane in range(4):
                        col=(x-(m[0xd000+plane]-48))//2
                        if 0<=col<8 and m[0xa00+plane*128+(y+17)//2]&(128>>col):covered=True
                    self.assertTrue(covered,(tick,x,y))
        self.assertTrue({0,32,48}<=seen,seen)
        self.assertEqual(seq.execute(d.END,cpu).memory[0x83e0],17)

    def test_banana_windows_and_earlier_clock_are_preserved(self):
        for tick in range(11967,d.END,17):
            clock=tick+(4000 if tick>=d.MONTAGE_START else 0)
            original=((clock>>4)&31)|((clock>>5)&32)
            if tick<d.START:
                self.assertEqual(d.frame_at(tick),original,tick)
