"""Retired title banks cache full raw banana cycles before their first use."""
import unittest
import test_sequence as seq
import banana_cache as cache
import banana_variants as variants
from test_engine_cache import TrackedMemory


class BananaCacheTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cpu=seq.MPU(memory=TrackedMemory(seq.XEX.read_bytes()))
        m=cls.cpu.memory
        m[0xd301]=m.values[3];m[0xd40b]=124
        for address in (0x232d,0x237d):
            cls.cpu.pc=address;cls.cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
            for _ in range(10000):
                if cls.cpu.pc==0x7fff:break
                cls.cpu.step()
            else:raise AssertionError('music init did not return')
        m[0xd301]=0xff
        seq.execute(3072,cls.cpu)
        assert m[cache.FLAG]==1
        cls.before=[bytes(b) for b in m.banks]
        cls.costs=[];cls.nmis=0;deadline=cls.cpu.processorCycles+4000
        for job in range(1500):
            m.writes.clear();cls.cpu.pc=cache.ENTRY;cls.cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
            before=cls.cpu.processorCycles
            for _ in range(100000):
                if cls.cpu.pc==0x7fff:break
                if cls.cpu.processorCycles>=deadline:
                    bank,pc=m[0xd301],cls.cpu.pc;cls.cpu.nmi()
                    for _ in range(10000):
                        cls.cpu.step()
                        if cls.cpu.pc==pc:break
                    else:raise AssertionError('NMI did not return')
                    assert m[0xd301]==bank
                    cls.nmis+=1;deadline=cls.cpu.processorCycles+8880
                cls.cpu.step()
            else:raise AssertionError('cache job did not return')
            cls.costs.append(cls.cpu.processorCycles-before)
            assert m[0xd301]==0xff
            assert not any(0x9000<=a<0xcf00 or 0x0980<=a<0x0c00 or 0x8980<=a<0x8c00
                           or a in (0xd400,0xd402,0xd403,0xd407) for a in m.writes)
            if m[cache.FLAG]==2:break
        else:raise AssertionError('cache failed to finish before available callbacks')
        cls.jobs=job+1
        cls.after=[bytes(b) for b in m.banks]

    def test_all_raw_frames_and_helpers_fit_in_existing_physical_banks(self):
        self.assertEqual(len(self.after),64)
        changed={i for i,(a,b) in enumerate(zip(self.before,self.after)) if a!=b}
        self.assertEqual(changed,set(range(17,25))|set(range(54,63)))
        for variant in range(2):
            for frame in range(32):
                bank=self.after[14+(40 if variant else 3)+frame//4]
                self.assertEqual(bank[frame%4*3840:(frame%4+1)*3840],variants.packed(frame,variant))
        self.assertGreater(self.nmis,100)
        self.assertLess(self.jobs,1500)
        self.assertLess(max(self.costs),18000)  # includes original music NMI

    def test_both_prepared_motifs_match_tunnel_playback_cost(self):
        for variant,start in enumerate((12288,14336)):
            costs=[]
            for frame in range(32):
                before=self.cpu.processorCycles
                seq.execute(start+16*frame,self.cpu)
                costs.append(self.cpu.processorCycles-before)
                self.assertEqual(seq.SequenceTests().raster(self.cpu),
                                 variants_raster(frame,variant))
            self.assertLess(max(costs[2:]),48000)

    def test_large_development_seek_does_not_replace_live_title_code(self):
        cpu=seq.execute(768);before=cpu.memory.ram[cache.ENTRY:cache.BUFFER]
        seq.execute(9000,cpu)
        self.assertEqual(cpu.memory[cache.FLAG],0)
        self.assertEqual(cpu.memory.ram[cache.ENTRY:cache.BUFFER],before)
        seq.execute(768,cpu)


def variants_raster(frame,variant):
    import mosaic
    p=mosaic.pixels(frame,variant)
    return bytes(p[y//2*160+x] for y in range(192) for x in range(160))
