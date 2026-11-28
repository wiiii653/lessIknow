"""Post-fight beat montage reuses textures and keeps the ball over the hole."""
import unittest
import test_sequence as seq
import post_trevor_director as d
from girl_eyes import frame_at as eye_frame_at
from outro_text import PREP_START

class PostTrevorDirectorTests(unittest.TestCase):
    def test_short_music_aligned_passes_and_fixed_outro_entry(self):
        from music_timing import tick_at_bar
        cuts=d.cuts()
        self.assertEqual(cuts[0][0],d.FIRST_ROTATOR)
        self.assertEqual(tuple(mode for _,mode in cuts[:4]),(0x00,0x10,0x80,0x90))
        self.assertEqual(cuts[10][0],d.START)
        self.assertEqual(cuts[10][1],0x20)
        self.assertEqual(cuts[11][0],tick_at_bar(80))
        self.assertEqual(d.START,29656)
        self.assertEqual(d.END,tick_at_bar(112))
        self.assertEqual(len(cuts),43)
        self.assertTrue(all(tick<d.END for tick,mode in cuts))
        self.assertEqual(cuts,tuple(sorted(cuts)))
        self.assertEqual([t for t,m in cuts[11:]],[tick_at_bar(207,2) if n==104 else tick_at_bar(n) for n in range(80,112)])
        lengths=[b[0]-a[0] for a,b in zip(cuts,(*cuts[1:],(d.END,0)))]
        self.assertEqual(lengths[10],d.CYCLE_START-d.START)
        shortened = 11+103-80
        self.assertEqual(lengths[shortened], d.LATE_BANANA_START-tick_at_bar(103))
        self.assertEqual(lengths[shortened+1], tick_at_bar(105)-d.LATE_BANANA_START)
        for index, length in enumerate(lengths[11:-1], 11):
            if index not in (shortened, shortened+1):
                self.assertIn(length, (373,374))
        self.assertGreater(lengths[-1],0)
        self.assertEqual([mode for _,mode in cuts[11:23]],list(d.PATTERN))
        self.assertEqual([mode for _,mode in cuts[23:35]],list(d.PATTERN))
        self.assertEqual(dict(cuts)[tick_at_bar(108)],0x20)
        self.assertEqual(dict(cuts)[tick_at_bar(109)],0xa0)
        for texture in (0,0x10,0x20):
            modes=[mode for _,mode in cuts if mode&0x30==texture]
            self.assertEqual({bool(mode&0x40) for mode in modes},
                             {False})
            self.assertEqual({bool(mode&0x80) for mode in modes},{False,True})
        self.assertLessEqual(len(d.helper()),d.SIZE)
        self.assertLessEqual(d.BANK_ENTRY+len(d.bank_helper()),0x7250)

    def test_short_passes_keep_phase_through_reversals_and_avoid_eye_slots(self):
        timeline=d.timeline()
        self.assertEqual(len(timeline),43)
        self.assertEqual(timeline[0][3],d.timeline()[0][3])
        for previous,current in zip(timeline,timeline[1:]):
            _,old_mode,old_q,old_base=previous
            tick,mode,q,base=current
            if tick==d.START:continue  # fresh entrance after the Trevor scene
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
        samples=sorted({d.START,PREP_START-1}|{t+delta for t,m in d.cuts() for delta in (-1,0,16) if d.START<=t+delta<PREP_START})
        for tick in samples:
            cpu=seq.execute(tick,cpu);m=cpu.memory
            self.assertEqual(m[0x83ed],eye_frame_at(tick,d.frame_at(tick)),tick)
            self.assertEqual(m[0xd301],0xff)
            self.assertEqual(m[0xd01d],3)
            if m[0x83ed]>=60:
                seen.add(48)
                continue  # the eye shot deliberately moves the ball on an eight
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

    def test_early_rotators_are_tunnels_and_bananas_enter_after_trevor(self):
        from music_timing import tick_at_bar

        self.assertTrue(all(32<=d.frame_at(tick)<60 for tick in range(d.FIRST_ROTATOR,d.START)))
        cpu=None
        for bar in range(32, 40):
            aligned = (tick_at_bar(bar) // 16) * 16 + 32
            period, base = (12,48) if bar % 2 else (16,32)
            direction = -1 if d.FIRST_TUNNELS[bar-32]&0x80 else 1
            cpu = seq.execute(aligned,cpu)
            phase = cpu.memory[0x83ed] - base
            cpu = seq.execute(aligned+15,cpu)
            self.assertEqual(cpu.memory[0x83ed],base+phase)
            cpu = seq.execute(aligned+16,cpu)
            self.assertEqual(cpu.memory[0x83ed],base+(phase+direction)%period)
        from ribbon_dance import FRONT_PREP_STEPS
        for bar in (*range(32,40),56,57):
            end = FRONT_PREP_STEPS[0] if bar == 39 else tick_at_bar(bar+1)
            for tick in (tick_at_bar(bar),tick_at_bar(bar)+32,end-1):
                cpu=seq.execute(tick,cpu)
                m=cpu.memory
                self.assertEqual(m[0x83e0],6,tick)
                self.assertEqual(m[0x83ed],d.frame_at(tick),tick)
                self.assertLess(m[0x83ed],60,tick)
                self.assertGreaterEqual(m[0x83ed],32,tick)
        cpu=seq.execute(d.START,cpu)
        self.assertLess(cpu.memory[0x83ed],32)

    def test_late_bananas_stay_yellow_with_a_cycling_backdrop(self):
        from girl_eyes import START, END
        from mosaic import palette_pairs
        from banana_variants import variant_at

        cpu = seq.execute(d.LATE_BANANA_START-1)
        self.assertGreaterEqual(cpu.memory[0x83ed], 32)
        for start, stop in ((d.LATE_BANANA_START, START), (END, END+500)):
            backdrops = set()
            for tick in range(start, min(start+500, stop), 16):
                cpu = seq.execute(tick, cpu)
                frame = cpu.memory[0x83ed]
                self.assertLess(frame, 32)
                expected = (palette_pairs()[(tick >> 6) & 15][0] << 4) | 10
                self.assertEqual(cpu.memory[0xd016], 0xea if variant_at(tick) else 0xec)
                self.assertEqual(cpu.memory[0xd017], expected)
                self.assertEqual(cpu.memory[0xd018], 0xee)
                backdrops.add(expected)
            self.assertGreater(len(backdrops), 2)

    def test_overlay_on_late_bananas_and_not_in_eye_shot(self):
        from girl_eyes import START as eyes_start, END as eyes_end
        from music_timing import tick_at_bar
        cpu=None
        for tick in (d.FIRST_ROTATOR,d.START,d.BUM_START-1,d.BUM_START,
                     tick_at_bar(104)+56,tick_at_bar(105)+56,eyes_start-1,
                     eyes_start,eyes_end-1,eyes_end,tick_at_bar(108)+56,
                     tick_at_bar(109)+56,tick_at_bar(110)):
            cpu=seq.execute(tick,cpu);m=cpu.memory
            self.assertEqual(bool(m[0x0dd2]),tick>=d.BUM_START and m[0x83ed]<32,tick)
            self.assertEqual(m[0xd301],0xff,tick)

    def test_both_late_banana_sections_include_word_and_satellites(self):
        from music_timing import tick_at_bar
        cpu=None;words=[]
        for bar in (104,105,108,109):
            start=tick_at_bar(bar)
            cpu=seq.execute(start+16,cpu);m=cpu.memory
            self.assertEqual(m[0x0dd2],1,bar);words.append(m[0x0dd1])
            cpu=seq.execute(start+56,cpu);m=cpu.memory
            base=(m[0xd407]&0xfc)<<8
            self.assertEqual(m[0xd008:0xd00c],[1]*4,bar)
            self.assertTrue(all(any(m[base+0x200+p*128:base+0x280+p*128]) for p in range(4)),bar)
        self.assertEqual(words[0]^words[1],1)
        self.assertEqual(words[2]^words[3],1)

    def test_banana_impact_fades_shrinks_and_travels_safely(self):
        from music_timing import tick_at_bar
        from test_engine_cache import TrackedMemory
        start=tick_at_bar(108)
        cpu=seq.MPU(memory=TrackedMemory(seq.XEX.read_bytes()))
        seq.execute(start,cpu)
        counts={};ink={};satellite_delta={}
        for age in (0,2,4,6,8,16,47,48,56,64,72,78,79,82,85,86,90,93):
            m=cpu.memory;old_base=(m[0xd407]&0xfc)<<8;m.writes.clear()
            seq.execute(start+age,cpu)
            self.assertFalse(any(old_base+0x180<=a<old_base+0x400 for a in m.writes),age)
            self.assertEqual(m[0xd301],0xff,age)
            base=(m[0xd407]&0xfc)<<8
            missiles=m[base+0x180:base+0x200]
            players=[m[base+0x200+i*128:base+0x280+i*128] for i in range(4)]
            counts[age]=sum(bool(v) for v in missiles);ink[age]=m[0xd019]&15
            if age<8 or age>=86:self.assertFalse(any(any(p) for p in players),age)
            if 48<=age<86:
                self.assertTrue(all(any(p) for p in players),age)
                satellite_delta[age]=(m[0xd000]-m[0xd004])&255
            if age>=86:self.assertEqual(counts[age],0)
        self.assertEqual([ink[a] for a in (0,2,4,6,8)],[0,4,8,12,14])
        self.assertEqual([ink[a] for a in (79,82,85,86)],[14,8,2,0])
        self.assertLess(counts[0],counts[8]);self.assertLess(counts[8],counts[16])
        self.assertLess(counts[72],counts[64]);self.assertLess(counts[64],counts[56])
        self.assertGreater(satellite_delta[48],satellite_delta[56])
        xs=[];tops=[]
        for tick in range(start,start+512,8):
            seq.execute(tick,cpu);m=cpu.memory;base=(m[0xd407]&0xfc)<<8
            xs.append(m[0xd004])
            rows=[i for i,v in enumerate(m[base+0x180:base+0x200]) if v]
            if rows:tops.append(rows[0])
        self.assertGreaterEqual(max(xs)-min(xs),115)
        self.assertLessEqual(max(abs(b-a) for a,b in zip(xs,xs[1:])),7)
        self.assertGreaterEqual(max(tops)-min(tops),55)
