"""Alternating appearances, full stored cycles, bank ownership and NMI."""
import unittest
import test_sequence as seq
import banana_variants as variants
import mosaic
from test_engine_cache import TrackedMemory


class BananaVariantTests(unittest.TestCase):
    def expected(self,frame,variant):
        p=mosaic.pixels(frame,variant)
        return bytes(p[y//2*160+x] for y in range(192) for x in range(160))

    def test_alternation_is_per_appearance_and_act5_never_switches_mid_turn(self):
        cpu=None
        for index,tick in enumerate((12288,14336,32909,43008,45056,47104,49152,51200)):
            variant=index&1;self.assertEqual(variants.variant_at(tick),variant)
            cpu=seq.execute(tick,cpu);m=cpu.memory
            self.assertEqual(m[variants.KEY],0x80|(variant<<6))
            self.assertEqual(m[0x83ed],(tick>>4)&31)
            self.assertEqual(tuple(m[a] for a in (0xd016,0xd018)),(0x1a,0x0e) if variant else (0x18,0x1e))
        for tick in range(32909,35900):self.assertEqual(variants.variant_at(tick),0)
        report=variants.memory_report()
        self.assertEqual(report['banks'],8)
        self.assertEqual(report['frames_per_variant'],32)
        self.assertGreater(report['free_bytes'],0)
        self.assertTrue(all(n<=variants.CAPACITY for n in report['payload_bytes_per_bank']))

    def test_all_64_live_frames_decode_without_front_writes_or_cost_regression(self):
        cpu=seq.MPU(memory=TrackedMemory(seq.XEX.read_bytes()))
        for variant,start in enumerate((12288,14336)):
            for frame in range(32):
                m=cpu.memory;front=0x9000 if m[0xd403]==0x84 else 0xb000
                m.writes.clear();before=cpu.processorCycles
                seq.execute(start+16*frame,cpu)
                self.assertLess(cpu.processorCycles-before,90000 if frame<2 else 76000,(variant,frame))
                self.assertEqual(seq.SequenceTests().raster(cpu),self.expected(frame,variant))
                self.assertFalse(any(front<=a<front+3840 for a in m.writes),(variant,frame))
                self.assertEqual(m[0xd301],0xff)
                self.assertEqual(m[0x83fa],0xff)

    def test_same_phase_variant_seeks_and_other_renderers_do_not_share_cache_keys(self):
        cpu=None
        for tick in (14336,3553,14336,12288,14336,14983,14336,33280,43008,45056,59000,14336):
            cpu=seq.execute(tick,cpu)
            if tick in (3553,14983,59000):continue
            self.assertEqual(seq.SequenceTests().raster(cpu),self.expected((tick>>4)&31,variants.variant_at(tick)),tick)
            seq.execute(tick+1,cpu)
            self.assertEqual(seq.SequenceTests().raster(cpu),self.expected((tick>>4)&31,variants.variant_at(tick)),tick)

    def test_decoder_survives_original_music_nmi_and_restores_portb(self):
        for tick in (12304,14336,14832):
            m=seq.RuntimeMemory(seq.XEX.read_bytes());cpu=seq.MPU(memory=m)
            m[0xd301]=m.values[3];m[0xd40b]=124
            for address in (0x232d,0x237d):
                cpu.pc=address;cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
                for _ in range(10000):
                    if cpu.pc==0x7fff:break
                    cpu.step()
                else:self.fail('music init did not return')
            for i in range(3):m[0x24a7+i]=tick>>(8*i)&255
            import json
            m[0xd301]=0xff;cpu.pc=json.loads(seq.METADATA.read_text())['callback'];cpu.sp=0xfd
            m[0x1fe:0x200]=[0xfe,0x7f];deadline=cpu.processorCycles+1000;count=0
            for _ in range(100000):
                if cpu.pc==0x7fff:break
                if cpu.processorCycles>=deadline:
                    bank,pc=m[0xd301],cpu.pc;cpu.nmi()
                    for _ in range(10000):
                        cpu.step()
                        if cpu.pc==pc:break
                    else:self.fail('NMI did not return')
                    self.assertEqual(m[0xd301],bank);count+=1;deadline=cpu.processorCycles+8880
                cpu.step()
            else:self.fail('callback did not return')
            self.assertGreater(count,4)
            self.assertEqual(seq.SequenceTests().raster(cpu),self.expected((tick>>4)&31,variants.variant_at(tick)))
            self.assertEqual(m[0xd301],0xff)

    def test_dense_playback_is_cheaper_than_the_original_rle_decoder(self):
        # v240 worst warm callback: bunch 78748, peeled 78599 CPU cycles.
        # Keep a real improvement while retaining all 32 independent phases.
        for start,limit in ((12288,76000),(14336,74000)):
            cpu=None;costs=[]
            for frame in range(32):
                before=cpu.processorCycles if cpu else 0
                cpu=seq.execute(start+16*frame,cpu)
                if frame>=2:costs.append(cpu.processorCycles-before)
            self.assertLess(max(costs),limit)
        for variant in range(2):
            self.assertNotEqual(mosaic.pixels(0,variant),mosaic.pixels(16,variant))

    def test_dense_frames_match_the_pre_symmetry_release_exactly(self):
        from pathlib import Path
        old=seq.RuntimeMemory(Path('build/visual-prototype-v240.xex').read_bytes())
        for frame in range(32):
            bank=old.banks[17+frame//4]
            for variant in range(2):
                i=frame%4+4*variant
                p=(bank[0x3f80+i]|bank[0x3f88+i]<<8)-0x4000;raw=bytearray()
                while bank[p]:
                    count=bank[p];p+=1
                    if count<128:raw.extend(bank[p:p+count]);p+=count
                    else:raw.extend([bank[p]]*((count&127)+2));p+=1
                self.assertEqual(variants.packed(frame,variant),raw,(frame,variant))
