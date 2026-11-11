"""Story cutaways use the live banked renderer without disturbing handoffs."""
import unittest
import json
from test_tunnel_raster import BeamMemory
import test_sequence as seq
from test_engine_cache import TrackedMemory
from story_montage import WINDOWS,selected,frames
from girl_eyes import frame_at
import post_trevor_director as director

@unittest.skipIf(seq.MPU is None,'py65 required')
class StoryMontageTests(unittest.TestCase):
    def test_actual_art_follows_story_windows_and_restores_effect(self):
        cpu=seq.MPU(memory=TrackedMemory(seq.XEX.read_bytes()))
        for start,end,index in WINDOWS:
            tick=next(t for t in range(start,end) if selected(t)==index)
            cpu=seq.execute(tick-1,cpu)
            active=0x9000 if cpu.memory[0xd403]==0x84 else 0xb000
            cpu.memory.writes.clear();cpu=seq.execute(tick,cpu);m=cpu.memory
            self.assertEqual(m[0x83ed],index)
            self.assertEqual(m[0xd301],0xff)
            self.assertEqual(m[0xd01d],0)
            self.assertEqual(m[0xd016:0xd019],[0x48,0x68,0x2c])
            art=frames()[index-56]
            self.assertEqual(seq.SequenceTests().raster(cpu),bytes(art[y//2*160+x] for y in range(192) for x in range(160)))
            self.assertFalse(any(active<=addr<active+3840 for addr in m.writes))
            next_t=next(t for t in range(tick+1,end) if selected(t) is None)
            seq.execute(next_t,cpu)
            self.assertEqual(cpu.memory[0x83ed],frame_at(next_t,director.frame_at(next_t)))
            self.assertEqual(cpu.memory[0xd01d],3)
        self.assertEqual(len(set(frames())),4)

    def test_story_publication_waits_for_safe_blanking(self):
        for tick in (37888,38144):
            for start in (248,255,290,305,311):
                m=BeamMemory(seq.XEX.read_bytes());cpu=seq.MPU(memory=m)
                seq.execute(tick,cpu);cpu.processorCycles=0;m.start=start*114;m.cpu=cpu;m.events=[]
                cpu.pc=json.loads(seq.METADATA.read_text())['callback'];cpu.sp=0xfd
                m[0x1fe:0x200]=[0xfe,0x7f]
                for _ in range(100000):
                    if cpu.pc==0x7fff:break
                    cpu.step()
                else:self.fail('story callback did not return')
                commits=[t/114%312 for t,a,v in m.events if a==0xd01d]
                self.assertTrue(commits)
                if selected(tick) is not None:
                    self.assertGreaterEqual(min(commits),248)
                    self.assertLess(max(commits),260)
                else:
                    # Existing tunnel-ball routine enables PMG after its
                    # bounded blanking preparation, before the sprites.
                    self.assertTrue(all(line>=248 or line<48 for line in commits))

    def test_story_selection_survives_music_interrupts(self):
        tick=38000
        m=seq.RuntimeMemory(seq.XEX.read_bytes());cpu=seq.MPU(memory=m)
        m[0xd301]=m.values[3];m[0xd40b]=124
        for address in (0x232d,0x237d):
            cpu.pc=address;cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
            for _ in range(10000):
                if cpu.pc==0x7fff:break
                cpu.step()
            else:self.fail('music init did not return')
        for i in range(3):m[0x24a7+i]=tick>>(8*i)&255
        cpu.pc=json.loads(seq.METADATA.read_text())['callback'];cpu.sp=0xfd
        m[0x1fe:0x200]=[0xfe,0x7f];m[0xd301]=0xff
        next_nmi=cpu.processorCycles+2000;count=0
        for _ in range(120000):
            if cpu.pc==0x7fff:break
            if cpu.processorCycles>=next_nmi:
                bank,pc=m[0xd301],cpu.pc;cpu.nmi()
                for _ in range(10000):
                    cpu.step()
                    if cpu.pc==pc:break
                else:self.fail('NMI did not return')
                self.assertEqual(m[0xd301],bank)
                count+=1;next_nmi=cpu.processorCycles+8880
            cpu.step()
        else:self.fail('story callback did not return')
        self.assertGreater(count,3)
        baseline=seq.execute(tick).memory
        self.assertEqual(m[0x83ed],baseline[0x83ed])
        self.assertEqual(seq.SequenceTests().raster(cpu),seq.SequenceTests().raster(seq.execute(tick)))
        self.assertEqual(m[0xd016:0xd01e],baseline[0xd016:0xd01e])

    def test_original_eyes_and_outro_remain(self):
        for tick in (39379,39411,39443,39475):
            m=seq.execute(tick).memory
            self.assertGreaterEqual(m[0x83ed],60)
            self.assertEqual(m[0xd01d],3)
        self.assertEqual(seq.execute(49850).memory[0x83e0],17)
