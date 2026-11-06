"""PMG comic splash phases, visible lettering and safe scene handoffs."""
import unittest
import test_sequence as sequence
from trevor_polished import bang_art, HITS, HANDS
from engine_effects import pmg_art

@unittest.skipIf(sequence.MPU is None,'py65 required')
class TrevorBangTests(unittest.TestCase):
    def test_impact_expands_prints_and_scatters(self):
        burst,glyphs=bang_art();self.assertEqual(len(burst),96)
        self.assertEqual(len(set((burst[:32],burst[32:64],burst[64:]))),3)
        self.assertLess(sum(x.bit_count() for x in burst[:32]),sum(x.bit_count() for x in burst[32:64]))
        self.assertLess(sum(x.bit_count() for x in burst[32:64]),sum(x.bit_count() for x in burst[64:]))
        self.assertGreater(len(set(burst[72:88])),1)
        self.assertTrue(all((row & 0x03)==0 for row in glyphs[3]))
        cpu=None
        for offset,letters in ((0,False),(8,True),(16,True),(24,True),(40,True),(79,True),(80,False),(96,False),(103,False)):
            cpu=sequence.execute(HITS[0]+offset,cpu);m=cpu.memory
            dx,dy=0,0  # first punch is right-handed
            self.assertEqual(m[0x83ed],2)
            self.assertEqual(m[0xd01b],0x11)
            self.assertEqual(m[0xd01d],3)
            self.assertEqual(m[0xd400],0x2e)
            self.assertEqual(m[0xd00c],0xff)
            self.assertEqual(m[0xd000:0xd004],[152+dx,160+dx,168+dx,176+dx])
            self.assertEqual(m[0xd004:0xd008],[152+dx,160+dx,168+dx,176+dx])
            self.assertTrue(any(m[0x980+36+dy:0x980+68+dy]))
            for plane in range(4):
                pixels=bytes(m[0xa00+plane*128+45+dy:0xa00+plane*128+59+dy])
                self.assertEqual(pixels,glyphs[plane] if letters else bytes(14))
            if letters:
                self.assertNotEqual(sequence.SequenceTests().raster(cpu,effects=True),sequence.SequenceTests().raster(cpu))
        starts=[]; rows=[]
        for offset in (104,108,112,120,128,135):
            cpu=sequence.execute(HITS[0]+offset,cpu);m=cpu.memory
            self.assertEqual(m[0xd01b],1)
            self.assertEqual(m[0xd01d],1)
            self.assertEqual(m[0xd00c],0x55)
            starts.append(tuple(m[0xd004:0xd008]))
            rows.append(tuple(next(row for row,b in enumerate(m[0x980:0xa00]) if b & (3 << (2*i))) for i in range(4)))
            for i in range(4):
                self.assertTrue(any(b & (3 << (2*i)) for b in m[0x980:0xa00]))
        self.assertLess(starts[-1][0],starts[0][0])
        self.assertLess(starts[-1][1],starts[0][1])
        self.assertGreater(starts[-1][2],starts[0][2])
        self.assertGreater(starts[-1][3],starts[0][3])
        for i in (0,2): self.assertLess(rows[-1][i],rows[0][i])
        for i in (1,3): self.assertGreater(rows[-1][i],rows[0][i])
        for tick in (HITS[0]+136,HITS[0]+137,HITS[0]+138,HITS[0]+139):
            cpu=sequence.execute(tick,cpu)
            self.assertEqual(cpu.memory[0xd01d],0)
            self.assertEqual(cpu.memory[0xd400],0x22)

    def test_punch_position_varies_as_one_composition(self):
        positions=set()
        for tick in (t+16 for t in HITS[:8]):
            cpu=sequence.execute(tick);m=cpu.memory
            self.assertIn(m[0x83ed], (2,4))
            positions.add((m[0xd000],m[0x83ef]))
            self.assertEqual(m[0xd000:0xd004],m[0xd004:0xd008])
            for plane,glyph in enumerate(bang_art()[1]):
                dy=m[0x83ef] if m[0x83ef]<128 else m[0x83ef]-256
                self.assertEqual(bytes(m[0xa00+plane*128+45+dy:0xa00+plane*128+59+dy]),glyph)
        self.assertGreater(len(positions),1)

    def test_scatter_starts_at_bang_for_both_hands(self):
        for tick in HITS[:8]:
            with self.subTest(tick=tick):
                cpu=sequence.execute(tick+100)
                m=cpu.memory
                bubble_x = (m[0xd000] + m[0xd003] + 8) // 2
                dy = m[0x83ef] if m[0x83ef] < 128 else m[0x83ef]-256
                bubble_y = 52 + dy
                sequence.execute(tick+104,cpu)
                xs=m[0xd004:0xd008]
                ys=[next(row for row,b in enumerate(m[0x980:0xa00]) if b & (3 << (2*i))) for i in range(4)]
                self.assertLessEqual(max(abs(x-bubble_x) for x in xs), 6)
                self.assertLessEqual(max(abs(y-bubble_y) for y in ys), 1)
                sequence.execute(tick+132,cpu)
                self.assertLess(m[0xd004], xs[0])
                self.assertGreater(m[0xd007], xs[3])

    def test_bang_then_restart_restores_dance(self):
        cpu=sequence.execute(HITS[0]+16)
        sequence.execute(9163,cpu)
        missiles,players=pmg_art()
        self.assertEqual(bytes(cpu.memory[0x980:0xa00]),missiles)
        self.assertEqual(bytes(cpu.memory[0xa00:0xc00]),players)
        self.assertEqual(cpu.memory[0xd01b],1)
