"""PMG comic splash phases, visible lettering and safe scene handoffs."""
import unittest
import test_sequence as sequence
from trevor_polished import bang_art
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
        for offset,letters in ((0,False),(16,True),(32,True),(80,True)):
            cpu=sequence.execute(27136+offset,cpu);m=cpu.memory
            dx,dy=4,2  # per-punch offset for tick 27136
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
        for offset in (96,112,124,144,160,188):
            cpu=sequence.execute(27136+offset,cpu);m=cpu.memory
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
        for tick in (27328,27360,27391,27392,27420):
            cpu=sequence.execute(tick,cpu)
            self.assertEqual(cpu.memory[0xd01d],0)
            self.assertEqual(cpu.memory[0xd400],0x22)

    def test_punch_position_varies_as_one_composition(self):
        positions=set()
        for tick in (27152,27664,28176,28688):
            cpu=sequence.execute(tick);m=cpu.memory
            self.assertEqual(m[0x83ed],2)
            positions.add((m[0xd000],m[0x83e9]))
            self.assertEqual(m[0xd000:0xd004],m[0xd004:0xd008])
            for plane,glyph in enumerate(bang_art()[1]):
                dy=m[0x83e9] if m[0x83e9]<128 else m[0x83e9]-256
                self.assertEqual(bytes(m[0xa00+plane*128+45+dy:0xa00+plane*128+59+dy]),glyph)
        self.assertGreater(len(positions),1)

    def test_bang_then_restart_restores_dance(self):
        cpu=sequence.execute(27152)
        sequence.execute(9163,cpu)
        missiles,players=pmg_art()
        self.assertEqual(bytes(cpu.memory[0x980:0xa00]),missiles)
        self.assertEqual(bytes(cpu.memory[0xa00:0xc00]),players)
        self.assertEqual(cpu.memory[0xd01b],1)
