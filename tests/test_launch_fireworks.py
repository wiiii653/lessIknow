"""Quiet overhead composition and isolated launch fireworks, v146."""
import unittest
import test_sequence as sequence
from ribbon_dance import STEPS,START,CUTS,FIREWORK_START,FIREWORK_CENTRES,LAUNCH_PREP,LAUNCH_START,OVERHEAD_START,firework_shapes
from test_engine_cache import TrackedMemory


def active_planes(m):
    base=(m[0xd407]&0xfc)<<8
    return bytes(m[base+0x180:base+0x400])


class LaunchFireworksTests(unittest.TestCase):
    def test_dance_fills_time_before_one_fast_two_angle_launch(self):
        from ribbon_dance import END
        cpu=None;changes=[]
        for tick in range(CUTS[2],LAUNCH_PREP,16):
            cpu=sequence.execute(tick,cpu)
            frame=cpu.memory[0x83ed]
            if not changes or changes[-1]!=frame:changes.append(frame)
        self.assertGreater(len(changes),35)
        self.assertEqual(set(changes),{8,9,35,10})
        changes=[]
        for tick in range(LAUNCH_PREP,END,8):
            cpu=sequence.execute(tick,cpu);frame=cpu.memory[0x83ed]
            if not changes or changes[-1]!=frame:changes.append(frame)
        self.assertEqual(len(changes),len(set(changes)),changes)
        self.assertEqual(changes,[11,12,13,14,15])
        self.assertLess(STEPS[122]-LAUNCH_PREP,200) # under one second to close-up
        self.assertEqual(sequence.execute(LAUNCH_START).memory[0x83ed],12)
        self.assertEqual(sequence.execute(OVERHEAD_START).memory[0x83ed],13)
        for tick in range(STEPS[122],END,8):
            cpu=sequence.execute(tick,cpu)
            self.assertEqual(cpu.memory[0x83ed],15)

    def test_overhead_background_has_no_grid(self):
        from ribbon_dance import artwork
        for frame in range(12,16):
            p,_=artwork(frame)
            # Dancers remain, all outer ground and old court/plank edges vanish.
            self.assertGreater(sum(v==3 for v in p),50)
            for x,y in ((8,3),(152,3),(8,60),(152,60)):
                self.assertEqual(p[y*160+x],0,(frame,x,y))

    def test_recovered_time_has_dance_and_ribbons(self):
        cpu=sequence.execute(START)
        self.assertTrue(any(active_planes(cpu.memory)))
        for tick in (CUTS[2],STEPS[70],STEPS[93],LAUNCH_PREP-1):
            cpu=sequence.execute(tick,cpu)
            self.assertTrue(any(active_planes(cpu.memory)),tick)
            self.assertEqual(cpu.memory[0xd008:0xd00c],[3]*4)
            self.assertEqual(cpu.memory[0xd00c],0x55)
            self.assertEqual(cpu.memory[0xd301],0xff)

    def test_fireworks_are_discrete_bursts_outside_the_central_face(self):
        cpu=None;masks=set()
        self.assertEqual(len(firework_shapes()),128)
        for phase in range(8):
            cpu=sequence.execute(FIREWORK_START+phase*16,cpu);m=cpu.memory
            self.assertEqual(m[0xd000:0xd004],[x+40 for x,y in FIREWORK_CENTRES])
            self.assertEqual(m[0xd008:0xd00c],[1]*4)
            self.assertEqual(m[0xd00c],0)
            self.assertEqual((m[0xd012],m[0xd015]),(0x0e,0x9e))
            base=(m[0xd407]&0xfc)<<8
            for plane in range(4):
                occupied=[y for y in range(128) if m[base+0x200+plane*128+y]]
                self.assertTrue(occupied)
                self.assertLessEqual(len(occupied),16)
                left=m[0xd000+plane]-48
                self.assertTrue(left+16<=40 or left>=120)
            self.assertTrue(any(m[base+0x180:base+0x200]))
            masks.add(active_planes(m))
        self.assertEqual(len(masks),8)

    def test_both_launch_views_have_player_wind_and_moving_missile_trails(self):
        for tick in (LAUNCH_START,OVERHEAD_START):
            cpu=sequence.execute(tick);m=cpu.memory
            raw=bytes(sequence.SequenceTests().raster(cpu));before=active_planes(m)
            base=(m[0xd407]&0xfc)<<8
            for plane in range(4):
                rows=[y for y,v in enumerate(m[base+0x180:base+0x200]) if v&(3<<(2*plane))]
                self.assertGreaterEqual(len(rows),4)
            cpu=sequence.execute(tick+4,cpu)
            self.assertEqual(sequence.SequenceTests().raster(cpu),raw)
            self.assertNotEqual(active_planes(cpu.memory),before)

    def test_fireworks_prepare_offscreen_and_old_ribbons_return_cleanly(self):
        cpu=sequence.MPU(memory=TrackedMemory(sequence.XEX.read_bytes()))
        sequence.execute(CUTS[2],cpu)
        for tick in (FIREWORK_START,FIREWORK_START+8,FIREWORK_START+32,STEPS[126],START,9163):
            m=cpu.memory;active=(m[0xd407]&0xfc)<<8
            m.writes.clear();sequence.execute(tick,cpu)
            commit = m.writes.index(0xd407)
            self.assertFalse(any(active+0x180<=a<active+0x400 for a in m.writes[:commit]))
            fresh=sequence.execute(tick).memory
            self.assertEqual(active_planes(m),active_planes(fresh))
            self.assertEqual(m[0xd008:0xd00c],[3]*4 if tick<FIREWORK_START else [1]*4)
            self.assertEqual(m[0xd301],0xff)
