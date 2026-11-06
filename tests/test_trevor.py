"""Trevor staging, hardware sprites and safe allocation of the seventeenth bank."""
from artifact import XEX, METADATA
import unittest
import test_sequence as sequence
from trevor_awakens import START,MIDPOINT,HIT,END
from trevor_polished import frames, helper, tunnel_frames, POLYGONS, CUTOUTS, inside, HITS, HANDS, bank, entrance_mask

@unittest.skipIf(sequence.MPU is None,'py65 required')
class TrevorTests(unittest.TestCase):
    def test_entrance_uses_one_gym_and_preserves_face(self):
        far, near = frames()[:2]
        mask = entrance_mask()
        for pos, keep in enumerate(mask):
            if not keep:
                self.assertEqual(near[pos], far[pos], pos)
        # Doorway/wall must survive outside the actor, including underarms.
        self.assertGreater(sum(not keep and far[pos] != 0 for pos, keep in enumerate(mask)), 1000)
        # The face stays drawn in front of the original gym.
        self.assertGreater(sum(near[y*160+x] == 3 for y in range(20,32) for x in range(69,91)), 80)

    def test_unused_pose_slots_are_available(self):
        quiet = bank(0, quiet=True)
        self.assertTrue(all(quiet[start:start+0xa00] == bytes(0xa00)
                            for start in (0x1400, 0x2a00, 0x3400)))
        for phase in range(16):
            self.assertEqual(bank(phase)[0xa00:0x1400], bytes(0xa00))

    def test_illustrations_boundaries_and_missiles(self):
        art=frames();cpu=None;seen=set()
        for tick in (START,START+512,MIDPOINT-1,MIDPOINT,HIT-1,*HITS[:5],HITS[1]-4,HITS[3]-4,END-1):
            cpu=sequence.execute(tick,cpu)
            self.assertEqual(cpu.memory[0x83e0],16)
            pose=cpu.memory[0x83ed];seen.add(pose)
            source=art[pose] if pose<2 else tunnel_frames(0 if tick < HIT else (tick>>4)&15)[pose-2]
            expected=bytes(source[y//3*160+x] for y in range(192) for x in range(160))
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected)
            age = tick - max((t for t in HITS if t <= tick), default=tick)
            active=pose in (2,4) and age<120
            self.assertEqual(cpu.memory[0xd01d],(3 if age<72 else 1) if active else 0)
            if active:
                self.assertTrue(any(cpu.memory[0x980:0xa00]))
                self.assertNotEqual(sequence.SequenceTests().raster(cpu,effects=True),expected)
        self.assertEqual(seen,{0,1,2,3,4,5})
        self.assertEqual(sequence.execute(END,cpu).memory[0x83e0],6)
        self.assertLess(len(helper()),2560)

    def test_tunnel_moves_while_trevor_is_preserved(self):
        pictures=[]
        for phase in range(16):
            tick=HITS[0]+phase*32
            cpu=sequence.execute(tick)
            pose=cpu.memory[0x83ed]
            source=tunnel_frames((tick>>4)&15)[pose-2]
            expected=bytes(source[y//3*160+x] for y in range(192) for x in range(160))
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected)
            pictures.append(source)
        self.assertGreaterEqual(len(set(pictures)),8)
        cpu=sequence.execute(HITS[3]+32)
        raw=sequence.SequenceTests().raster(cpu);before=cpu.processorCycles
        sequence.execute(HITS[3]+36,cpu)
        self.assertLess(cpu.processorCycles-before,12500)
        self.assertEqual(sequence.SequenceTests().raster(cpu),raw)

    def test_original_trevor_pixels_preserved_while_background_moves(self):
        original=frames()
        for stage in (2,3):
            a=tunnel_frames(4)[stage-2];b=tunnel_frames(8)[stage-2]
            kept=changed=0
            for y in range(64):
                for x in range(160):
                    gap=any(inside(x+.5,y+.5,cutout) for cutout in CUTOUTS[stage-2])
                    pos=y*160+x
                    if not gap and inside(x+0.5,y+0.5,POLYGONS[stage-2]):
                        self.assertEqual((a[pos],b[pos]),(original[stage][pos],)*2)
                        kept+=1
                    elif a[pos]!=b[pos]:changed+=1
            self.assertGreater(kept,2000)
            self.assertGreater(changed,1000)

    def test_combination_changes_hands_and_tempo(self):
        self.assertEqual(HANDS[:5], (2,4,4,2,4))
        gaps = [b-a for a,b in zip(HITS,HITS[1:])]
        self.assertTrue(all(140 <= gap <= 188 for gap in gaps))
        self.assertGreater(max(gaps), min(gaps) + 40)
        self.assertEqual([sequence.execute(t).memory[0x83ed] for t in HITS[:8]], list(HANDS[:8]))
        for index in (0, 1, 2, 7, 8, 19, 20, 30, 38, 39):
            cpu = sequence.execute(HITS[index])
            self.assertEqual(cpu.memory[0x83ed], HANDS[index], index)
            self.assertEqual(cpu.memory[0xd01d], 3, index)
            self.assertEqual(cpu.memory[0xd301], 0xff, index)
        original = tunnel_frames(4)[0]
        mirrored = tunnel_frames(4)[2]
        for y in range(64):
            for x in range(160):
                if inside(x + .5, y + .5, POLYGONS[0]) and not any(inside(x+.5,y+.5,c) for c in CUTOUTS[0]):
                    self.assertEqual(original[y*160+x], mirrored[y*160+159-x])

    def test_correct_hand_rises_before_each_impact(self):
        cpu=None
        for impact, punch in zip(HITS[:9], HANDS[:9]):
            cpu=sequence.execute(impact-4,cpu)
            self.assertEqual(cpu.memory[0x83ed], punch+1)
            self.assertEqual(cpu.memory[0xd01d], 0)
            source=tunnel_frames(((impact-4)>>4)&15)[punch-1]
            expected=bytes(source[y//3*160+x] for y in range(192) for x in range(160))
            self.assertEqual(sequence.SequenceTests().raster(cpu), expected)
            cpu=sequence.execute(impact,cpu)
            self.assertEqual(cpu.memory[0x83ed], punch)
            self.assertEqual(cpu.memory[0xd01d], 3)
            self.assertEqual(cpu.memory[0xd301], 0xff)

    def test_all_action_poses_keep_consistent_brightness(self):
        poses=set()
        for tick in (HIT+16, HITS[0]+8, HITS[1]-8, HITS[1]+8,
                     HITS[2]+64, HITS[3]-8, HITS[3]+8):
            cpu=sequence.execute(tick)
            poses.add(cpu.memory[0x83ed])
            self.assertEqual(cpu.memory[0xd016]&15, 8)
            self.assertIn(cpu.memory[0xd017]&15, (6,8))
            self.assertEqual(cpu.memory[0xd018], 0x2a)
        self.assertEqual(poses,{2,3,4,5})

    def test_entrance_never_raises_a_fist(self):
        cpu=None
        for tick in (MIDPOINT, HIT-64, HIT-32, HIT-16, HIT-4, HIT-1):
            cpu=sequence.execute(tick,cpu)
            self.assertEqual(cpu.memory[0x83ed],1,tick)
            self.assertEqual(cpu.memory[0xd01d],0,tick)
        cpu=sequence.execute(HIT,cpu)
        self.assertEqual(cpu.memory[0x83ed],3)
        self.assertEqual(cpu.memory[0xd01d],0)
        cpu=sequence.execute(HITS[0],cpu)
        self.assertEqual(cpu.memory[0x83ed],2)
        self.assertEqual(cpu.memory[0xd01d],3)

    def test_first_windup_follows_the_live_tunnel_phase(self):
        # Before the first impact the same animated phase bank must be used;
        # falling back to phase zero causes a visibly stray tunnel frame.
        for tick in (HIT, HIT+16, HITS[0]-4):
            with self.subTest(tick=tick):
                cpu = sequence.execute(tick)
                self.assertEqual(cpu.memory[0x83ed], 3)
                source = tunnel_frames((tick >> 4) & 15)[1]
                expected = bytes(source[y//3*160+x] for y in range(192) for x in range(160))
                self.assertEqual(sequence.SequenceTests().raster(cpu), expected)

    def test_body_is_registered_across_all_tunnel_phases(self):
        art=frames()
        for phase in range(16):
            shot=tunnel_frames(phase)
            for stage in (2,3,4,5):
                original=2 if stage in (2,4) else 3
                poly=POLYGONS[0 if original==2 else 1]
                for y in range(64):
                    for x in range(160):
                        source_x=159-x if stage in (4,5) else x
                        gap=any(inside(source_x+.5,y+.5,c) for c in CUTOUTS[original-2])
                        if not gap and inside(source_x+.5,y+.5,poly):
                            self.assertEqual(shot[stage-2][y*160+x],art[original][y*160+source_x])

    def test_all_impacts_show_the_correct_pose_in_live_buffers(self):
        allowed={pose:set() for pose in (2,3,4,5)}
        for phase in range(16):
            for pose,pixels in enumerate(tunnel_frames(phase),2):
                allowed[pose].add(bytes(sum(pixels[y*160+x+k]<<(6-2*k) for k in range(4))
                                        for y in range(64) for x in range(0,160,4)))
        cpu=None
        for index,impact in enumerate(HITS):
            for age in (-4,0,8,80,103,104,116,120,132,136):
                tick=impact+age
                cpu=sequence.execute(tick,cpu)
                pose=(HANDS[index]+1 if age<0 else HANDS[index] if age<120 or index==len(HITS)-1 else HANDS[index+1]+1)
                self.assertEqual(cpu.memory[0x83ed],pose,(index,age))
                expected_pm=0 if age<0 or age>=136 else 3 if age<104 else 1
                self.assertEqual(cpu.memory[0xd01d],expected_pm,(index,age))
                m=cpu.memory;display=m[0xd402]|m[0xd403]<<8
                actual=b''.join(bytes(m[(m[display+3+y*9]|m[display+4+y*9]<<8):
                                        (m[display+3+y*9]|m[display+4+y*9]<<8)+40]) for y in range(64))
                self.assertIn(actual,allowed[pose],(index,age))

    def test_bank_probe_preserves_all_sixteen_loaded_banks(self):
        from school_portrait_bank import loader
        from extract_music import segments
        from scene_memory import RuntimeMemory
        from pathlib import Path
        m=RuntimeMemory(XEX.read_bytes())
        m.banks[0][0]=0x55 # The second marker must disambiguate this coincidence.
        saved=[bytes(bank) for bank in m.banks[:16]]
        frame=bytes((i*17+i//256)&255 for i in range(16384))
        for lo,hi,payload in segments(b'\xff\xff'+loader(frame,index=2)):
            if lo!=0x02e2:m[lo:hi+1]=payload
        m[0xd301]=0xff
        cpu=sequence.MPU(memory=m);cpu.pc=0x1000;cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
        for _ in range(200000):
            if cpu.pc==0x7fff:break
            cpu.step()
        else:self.fail('bank probe / loader did not return')
        self.assertEqual(m[0x24b5],0xc0)
        self.assertEqual([bytes(bank) for bank in m.banks[:16]],saved)
        self.assertEqual(bytes(m.banks[16]),frame)
        self.assertEqual(m[0xd301],0xff)
