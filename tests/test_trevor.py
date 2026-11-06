"""Trevor staging, hardware sprites and safe allocation of the seventeenth bank."""
import unittest
import test_sequence as sequence
from trevor_awakens import START,MIDPOINT,HIT,END
from trevor_polished import frames, helper, tunnel_frames, POLYGONS, inside

@unittest.skipIf(sequence.MPU is None,'py65 required')
class TrevorTests(unittest.TestCase):
    def test_illustrations_boundaries_and_missiles(self):
        art=frames();cpu=None;seen=set()
        for tick in (START,START+512,MIDPOINT-1,MIDPOINT,HIT-1,HIT,HIT+256,HIT+512,END-1):
            cpu=sequence.execute(tick,cpu)
            self.assertEqual(cpu.memory[0x83e0],16)
            pose=cpu.memory[0x83ed];seen.add(pose)
            source=art[pose] if pose<2 else tunnel_frames((tick>>4)&15)[pose-2]
            expected=bytes(source[y//3*160+x] for y in range(192) for x in range(160))
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected)
            phase=tick&255
            active=pose==2 and phase<192
            self.assertEqual(cpu.memory[0xd01d],(3 if phase<96 else 1) if active else 0)
            if active:
                self.assertTrue(any(cpu.memory[0x980:0xa00]))
                self.assertNotEqual(sequence.SequenceTests().raster(cpu,effects=True),expected)
        self.assertEqual(seen,{0,1,2,3})
        self.assertEqual(sequence.execute(END,cpu).memory[0x83e0],6)
        self.assertLess(len(helper()),2560)

    def test_tunnel_moves_while_trevor_is_preserved(self):
        art=frames();pictures=[];cpu=None
        for phase in range(16):
            tick=27136+phase*16
            cpu=sequence.execute(tick,cpu)
            pose=cpu.memory[0x83ed]
            self.assertEqual(pose,2)
            source=tunnel_frames((tick>>4)&15)[pose-2]
            expected=bytes(source[y//3*160+x] for y in range(192) for x in range(160))
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected)
            pictures.append(source)
        self.assertEqual(len(set(pictures)),16)
        cpu=sequence.execute(27136,cpu)
        raw=sequence.SequenceTests().raster(cpu);before=cpu.processorCycles
        sequence.execute(27140,cpu)
        self.assertLess(cpu.processorCycles-before,12500)
        self.assertEqual(sequence.SequenceTests().raster(cpu),raw)

    def test_original_trevor_pixels_preserved_while_background_moves(self):
        original=frames()
        for stage in (2,3):
            a=tunnel_frames(0)[stage-2];b=tunnel_frames(8)[stage-2]
            kept=changed=0
            for y in range(64):
                for x in range(160):
                    gap=stage==3 and 92<=x<107 and 9<=y<20
                    pos=y*160+x
                    if not gap and inside(x+0.5,y+0.5,POLYGONS[stage-2]):
                        self.assertEqual((a[pos],b[pos]),(original[stage][pos],)*2)
                        kept+=1
                    elif a[pos]!=b[pos]:changed+=1
            self.assertGreater(kept,2000)
            self.assertGreater(changed,1000)

    def test_bank_probe_preserves_all_sixteen_loaded_banks(self):
        from school_portrait_bank import loader
        from extract_music import segments
        from scene_memory import RuntimeMemory
        from pathlib import Path
        m=RuntimeMemory((sequence.ROOT/'build/visual-prototype-v076.xex').read_bytes())
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
