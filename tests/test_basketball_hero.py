"""Act boundaries, banked frames, moving PMG ball and lighting of Act 3."""
import unittest
import test_sequence as sequence
from basketball_hero import START,DUNK,END,frames,helper,DATA,ENTRY
from engine_effects import pmg_art
from trevor_awakens import END as TREVOR_END

@unittest.skipIf(sequence.MPU is None,'py65 required')
class HeroTests(unittest.TestCase):
    def test_act_boundaries_and_all_six_poses(self):
        art=frames();cpu=None;seen=set()
        self.assertEqual(sequence.execute(START-1).memory[0x83e0],14)
        for tick in (START,START+96,DUNK-1,DUNK,DUNK+752,DUNK+976,DUNK+1200,END-1):
            cpu=sequence.execute(tick,cpu)
            self.assertEqual(cpu.memory[0x83e0],15)
            pose=cpu.memory[0x83ec];seen.add(pose)
            expected=bytes(art[pose][y*56//192*160+x] for y in range(192) for x in range(160))
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected)
            self.assertEqual(cpu.memory[0xd01d],3)
            self.assertNotEqual(sequence.SequenceTests().raster(cpu,effects=True),expected)
        self.assertEqual(seen,set(range(6)))
        self.assertEqual(sequence.execute(END,cpu).memory[0x83e0],16)
        cpu=sequence.execute(TREVOR_END,cpu)
        self.assertEqual(cpu.memory[0xd01d],3)  # rainbow ball in the rotator
        cpu=sequence.execute(9163,cpu)
        missiles,players=pmg_art()
        self.assertEqual(bytes(cpu.memory[0x980:0xa00]),missiles)
        self.assertEqual(bytes(cpu.memory[0xa00:0xc00]),players)
        self.assertLessEqual(ENTRY+len(helper()),DATA)
        self.assertEqual(len(set(cpu.memory.values)),54)

    def test_music_clock_drives_dribble_and_one_dunk(self):
        cpu=None;levels=set()
        for elapsed in (0,40,92,140,184,187,374,1122):
            cpu=sequence.execute(START+elapsed,cpu)
            self.assertEqual(cpu.memory[0x83ff],(elapsed%187)//4)
            levels.add(bytes(cpu.memory[0xa00:0xc00]))
        self.assertGreater(len(levels),4)
        for elapsed in (0,256,512,768,1024,1248,1495):
            cpu=sequence.execute(DUNK+elapsed,cpu)
            self.assertEqual(cpu.memory[0x83ff],elapsed//16)
        cpu=sequence.execute(DUNK+1312,cpu)
        self.assertEqual(cpu.memory[0xd017],14)
        cpu=sequence.execute(DUNK+1360,cpu)
        self.assertEqual(cpu.memory[0xd017],0x9a)

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

    def test_dunk_ball_follows_hand_until_release(self):
        cpu=None
        for phase,pose,center in ((0,2,(85,102)),(46,2,(85,102)),
                                  (47,3,(99,28)),(60,3,(99,28)),
                                  (61,4,(115,18)),(74,4,(115,18)),
                                  (75,5,(124,32)),(81,5,(124,32))):
            cpu=sequence.execute(DUNK+phase*16,cpu)
            self.assertEqual(cpu.memory[0x83ec],pose)
            self.assertEqual(cpu.memory[0xd000]-40,center[0])
            # Double-line PMG Y rounds to the nearest two raster lines.
            self.assertLessEqual(abs((cpu.memory[0x83e9]*2-17+16)-center[1]),1)
        cpu=sequence.execute(DUNK+93*16,cpu)
        self.assertGreater(cpu.memory[0x83e9]*2-17+16,100)
