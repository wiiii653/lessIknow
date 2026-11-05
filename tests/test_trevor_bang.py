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
        cpu=None
        for offset,letters in ((0,False),(16,True),(32,True),(80,True),(96,False),(112,False)):
            cpu=sequence.execute(27136+offset,cpu);m=cpu.memory
            self.assertEqual(m[0x83ed],2)
            self.assertEqual(m[0xd01b],0x11)
            self.assertEqual(m[0xd01d],3)
            self.assertEqual(m[0xd400],0x2e)
            self.assertEqual(m[0xd00c],0xff)
            self.assertEqual(m[0xd000:0xd004],[152,160,168,176])
            self.assertEqual(m[0xd004:0xd008],[152,160,168,176])
            self.assertTrue(any(m[0x980+36:0x980+68]))
            for plane in range(4):
                pixels=bytes(m[0xa00+plane*128+45:0xa00+plane*128+59])
                self.assertEqual(pixels,glyphs[plane] if letters else bytes(14))
            if letters:
                self.assertNotEqual(sequence.SequenceTests().raster(cpu,effects=True),sequence.SequenceTests().raster(cpu))
        cpu=sequence.execute(27264,cpu)
        self.assertEqual(cpu.memory[0xd01d],1)  # Back to ordinary glints.

    def test_bang_then_restart_restores_dance(self):
        cpu=sequence.execute(27152)
        sequence.execute(9163,cpu)
        missiles,players=pmg_art()
        self.assertEqual(bytes(cpu.memory[0x980:0xa00]),missiles)
        self.assertEqual(bytes(cpu.memory[0xa00:0xc00]),players)
        self.assertEqual(cpu.memory[0xd01b],1)
