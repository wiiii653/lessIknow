"""Act boundaries, banked frames, moving PMG ball and lighting of Act 3."""
from artifact import XEX, METADATA
import unittest
import test_sequence as sequence
from basketball_hero import CUTAWAY_START,START,DUNK,END,DUNK_PHASE_TICKS,dribble_phase,frames,helper,DATA,ENTRY,scene_frame,SHATTER_PATCH_BYTES
from engine_effects import pmg_art
from trevor_awakens import END as TREVOR_END

@unittest.skipIf(sequence.MPU is None,'py65 required')
class HeroTests(unittest.TestCase):
    def test_act_boundaries_and_all_eight_poses(self):
        art=frames();cpu=None;seen=set()
        self.assertEqual(sequence.execute(CUTAWAY_START-1).memory[0x83e0],14)
        for tick in (START,START+24,START+48,START+72,DUNK-1,DUNK,DUNK+376,DUNK+488,DUNK+600,END-1):
            cpu=sequence.execute(tick,cpu)
            self.assertEqual(cpu.memory[0x83e0],15)
            pose=cpu.memory[0x83ec];seen.add(pose)
            picture=scene_frame(tick,pose)
            expected=bytes(picture[y*56//192*160+x] for y in range(192) for x in range(160))
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected)
            self.assertEqual(cpu.memory[0xd01d],3)
            self.assertNotEqual(sequence.SequenceTests().raster(cpu,effects=True),expected)
        self.assertEqual(seen,set(range(8)))
        self.assertEqual(sequence.execute(END,cpu).memory[0x83e0],16)
        cpu=sequence.execute(TREVOR_END,cpu)
        self.assertEqual(cpu.memory[0xd01d],3)  # rainbow ball in the rotator
        cpu=sequence.execute(9163,cpu)
        baseline=sequence.execute(9163).memory
        def active_pmg(m):
            base=(m[0xd407]&0xfc)<<8
            return bytes(m[base+0x180:base+0x400])
        self.assertEqual(active_pmg(cpu.memory),active_pmg(baseline))
        self.assertEqual(cpu.memory[0xd01b],0x11)
        self.assertLessEqual(ENTRY+len(helper()),DATA)
        self.assertEqual(len(set(cpu.memory.values)),64)

    def test_unchanged_throw_then_two_bar_tunnel_and_short_dunk(self):
        from mosaic import pixels
        from girl_eyes import frame_at as eye_frame_at
        from music_timing import tick_at_bar
        self.assertEqual((CUTAWAY_START,START,DUNK,END),tuple(tick_at_bar(b) for b in (56,58,62,64)))
        self.assertEqual(DUNK_PHASE_TICKS,8)
        cpu=None
        for tick in (CUTAWAY_START-1,CUTAWAY_START,CUTAWAY_START+16,START-1,START,DUNK,END,CUTAWAY_START):
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            if CUTAWAY_START<=tick<START:
                self.assertEqual(m[0x83e0],6)
                self.assertEqual(m[0x83ed],eye_frame_at(tick,32|((tick>>4)&31)))
                p=pixels(m[0x83ed])
                self.assertEqual(sequence.SequenceTests().raster(cpu),bytes(p[y//2*160+x] for y in range(192) for x in range(160)))
                self.assertEqual(m[0xd01d],3)
                self.assertEqual(m[0xd01b],0x11)
            self.assertEqual(m[0xd301],0xff)

    def test_music_clock_drives_dribble_and_one_dunk(self):
        cpu=None;levels=set()
        for elapsed in (0,40,92,94,140,184,187,188,280,373,374,1122):
            cpu=sequence.execute(START+elapsed,cpu)
            self.assertEqual(cpu.memory[0x83ff],dribble_phase(elapsed))
            levels.add(bytes(cpu.memory[0xa00:0xc00]))
        self.assertGreater(len(levels),4)
        for elapsed in (0,128,256,384,512,624,747):
            cpu=sequence.execute(DUNK+elapsed,cpu)
            self.assertEqual(cpu.memory[0x83ff],elapsed//DUNK_PHASE_TICKS)
        cpu=sequence.execute(DUNK+656,cpu)
        self.assertEqual(cpu.memory[0xd017],14)
        cpu=sequence.execute(DUNK+680,cpu)
        self.assertEqual(cpu.memory[0xd017],0x9c)

    def test_held_pose_uses_cached_bitmap_and_restart_restores_pmg(self):
        cpu=sequence.execute(START)
        raw=sequence.SequenceTests().raster(cpu);before=cpu.processorCycles
        cpu=sequence.execute(START+4,cpu)
        self.assertEqual(sequence.SequenceTests().raster(cpu),raw)
        self.assertLess(cpu.processorCycles-before,9000)
        cpu=sequence.execute(96,cpu)
        missiles,players=pmg_art()
        self.assertEqual(bytes(cpu.memory[0x980:0xa00]),missiles)
        self.assertEqual(bytes(cpu.memory[0xa00:0xc00]),players)

    def test_dribble_reuses_background_and_only_updates_actor_patch(self):
        from basketball_hero import DRIBBLE_X, DRIBBLE_Y, DRIBBLE_WIDTH, DRIBBLE_HEIGHT, DRIBBLE_PATCH_BYTES, packed
        from test_engine_cache import TrackedMemory
        from scene_memory import RuntimeMemory
        data=XEX.read_bytes()
        cpu=sequence.MPU(memory=TrackedMemory(data))
        art=frames()
        self.assertEqual(len(packed()), 5*2240+3*DRIBBLE_PATCH_BYTES+3*SHATTER_PATCH_BYTES)
        for y in range(56):
            for x in range(160):
                if not (DRIBBLE_X <= x < DRIBBLE_X+DRIBBLE_WIDTH and DRIBBLE_Y <= y < DRIBBLE_Y+DRIBBLE_HEIGHT):
                    for pose in (1,6,7):
                        self.assertEqual(art[0][y*160+x],art[pose][y*160+x])
        for elapsed in (0,24,48,72,94,118,142,166):
            cpu.memory.writes.clear()
            sequence.execute(START+elapsed,cpu)
            if elapsed >=48:
                bitmap=[a for a in cpu.memory.writes if 0x9000<=a<0xaf00 or 0xb000<=a<0xcf00]
                self.assertEqual(len(bitmap),DRIBBLE_PATCH_BYTES)
                for addr in bitmap:
                    offset=addr-(0x9000 if addr<0xb000 else 0xb000)
                    self.assertTrue(DRIBBLE_Y <= offset//40 < DRIBBLE_Y+DRIBBLE_HEIGHT)
                    self.assertTrue(DRIBBLE_X//4 <= offset%40 < (DRIBBLE_X+DRIBBLE_WIDTH)//4)

    def test_four_distinct_arm_poses_follow_ball_phase(self):
        phases = ((0,0),(12,1),(24,6),(40,7))
        hand_rows = []
        art=frames()
        for phase,pose in phases:
            cpu=sequence.execute(START+phase*2)
            self.assertEqual(cpu.memory[0x83ec],pose)
            # Each pose has a visibly different palm in the moving-arm area.
            hand_rows.append(bytes(art[pose][y*160+x] for y in range(20,44) for x in range(88,104)))
        self.assertEqual(len(set(hand_rows)),4)

    def test_live_buffers_show_every_arm_phase_over_three_bounces(self):
        art=frames()
        expected={pose:bytes(art[pose][y*56//192*160+x] for y in range(192) for x in range(160))
                  for pose in (0,1,6,7)}
        cpu=None
        for elapsed in range(0,374,4):
            phase=dribble_phase(elapsed)
            pose=0 if phase<9 or phase>=42 else 1 if phase<18 else 6 if phase<32 else 7
            cpu=sequence.execute(START+elapsed,cpu)
            self.assertEqual(cpu.memory[0x83ec],pose,elapsed)
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected[pose],elapsed)

    def test_dunk_ball_follows_hand_until_release(self):
        cpu=None
        for phase,pose,center in ((0,2,(85,102)),(46,2,(85,102)),
                                  (47,3,(99,28)),(60,3,(99,28)),
                                  (61,4,(115,18)),(74,4,(115,18)),
                                  (75,5,(124,32)),(81,5,(124,32))):
            cpu=sequence.execute(DUNK+phase*DUNK_PHASE_TICKS,cpu)
            self.assertEqual(cpu.memory[0x83ec],pose)
            self.assertEqual(cpu.memory[0xd000]-40,center[0])
            # Double-line PMG Y rounds to the nearest two raster lines.
            self.assertLessEqual(abs((cpu.memory[0x83e9]*2-17+16)-center[1]),1)
        cpu=sequence.execute(DUNK+93*DUNK_PHASE_TICKS,cpu)
        self.assertGreater(cpu.memory[0x83e9]*2-17+16,100)

    def test_four_satellites_orbit_the_ball_on_distinct_counter_rotating_paths(self):
        from basketball_hero import satellite_orbits
        paths=satellite_orbits();actual=[[] for _ in range(4)];cpu=None
        for age in range(0,256,8):
            tick=DUNK+age;cpu=sequence.execute(tick,cpu);m=cpu.memory
            self.assertEqual(m[0xd00c],0x55)
            self.assertEqual(m[0xd301],0xff)
            for plane in range(4):
                rows=[row for row in range(128) if m[0x980+row]&(3<<(2*plane))]
                self.assertEqual(rows,list(range(rows[0],rows[0]+3)))
                self.assertEqual([(m[0x980+row]>>(2*plane))&3 for row in rows],[1,3,1])
                point=(m[0xd004+plane]-m[0x83e8]-46,rows[0]-m[0x83e9]-6)
                self.assertEqual(point,paths[plane][(tick>>3)&31])
                actual[plane].append(point)
        self.assertEqual(len({tuple(path) for path in actual}),4)
        areas=[sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(path,path[1:]+path[:1])) for path in actual]
        self.assertGreater(areas[0],0);self.assertLess(areas[1],0)
        self.assertGreater(areas[2],0);self.assertLess(areas[3],0)
        self.assertEqual(len(set(actual[2])),16)  # Twice the angular speed.
        self.assertEqual(len(set(actual[0])),32)

    def test_satellites_follow_airborne_ball_and_become_glass_on_first_crack(self):
        from basketball_hero import satellite_orbits
        paths=satellite_orbits();cpu=None
        for phase in (46,47,60,61,74):
            tick=DUNK+phase*DUNK_PHASE_TICKS
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            for plane in range(4):
                dx,dy=paths[plane][(tick>>3)&31]
                self.assertEqual(m[0xd004+plane],m[0x83e8]+46+dx)
                rows=[row for row in range(128) if m[0x980+row]&(3<<(2*plane))]
                self.assertEqual(rows[0],m[0x83e9]+6+dy)
                self.assertGreaterEqual(rows[0],0);self.assertLess(rows[-1],128)
        for phase in (75,76,81,87,93):
            cpu=sequence.execute(DUNK+phase*DUNK_PHASE_TICKS,cpu);m=cpu.memory
            self.assertEqual(m[0xd00c],0)
            for plane in range(4):
                self.assertEqual(m[0xd004+plane],round(130+(plane-1.5)*(5+(phase-75)*.7))+48)

    def test_late_dunk_updates_finish_before_the_next_frame_satellites(self):
        import json
        from test_tunnel_raster import BeamMemory
        for phase in (0,47,61,74):
            for line in (248,255,290,306,311):
                m=BeamMemory(XEX.read_bytes());cpu=sequence.MPU(memory=m)
                sequence.execute(DUNK+phase*DUNK_PHASE_TICKS,cpu)
                cpu.processorCycles=0;m.start=line*114;m.cpu=cpu;m.events=[]
                cpu.pc=json.loads(METADATA.read_text())['callback'];cpu.sp=0xfd
                m[0x1fe:0x200]=[0xfe,0x7f]
                for _ in range(100000):
                    if cpu.pc==0x7fff:break
                    cpu.step()
                else:self.fail('callback did not return')
                writes=[t for t,a,v in m.events if 0x980<=a<0xc00]
                first=writes[0]/114
                self.assertGreaterEqual(first%312,248)
                self.assertLess(first%312,257)
                earliest=min(row*2 for row in range(128) if m[0x980+row])
                deadline=(int(first)//312+1)*312+earliest
                self.assertLess(m.events[-1][0]/114,deadline)
