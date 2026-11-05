"""Hardware ball motion, colors, cache and restoration at shot boundaries."""
import unittest
import test_sequence as sequence
from engine_effects import pmg_art
from gym_practice import practice_shot
from rainbow_ball import paths

@unittest.skipIf(sequence.MPU is None,'py65 required')
class RainbowBallTests(unittest.TestCase):
    def test_motion_rainbow_and_spray_without_bitmap_updates(self):
        cpu=sequence.execute(6981)
        raw=sequence.SequenceTests().raster(cpu)
        self.assertEqual(raw,practice_shot(6981))
        colors=set();positions=set()
        for phase in (0,1,2,3,4,5,6,7,8,16,24,32,40,44,52,60):
            before=cpu.processorCycles
            cpu=sequence.execute(6981+4*phase,cpu)
            self.assertLess(cpu.processorCycles-before,8500)
            self.assertEqual(cpu.memory[0xd01d],3)
            self.assertEqual(cpu.memory[0xd400],0x2e)
            self.assertEqual(len(set(cpu.memory[0xd012:0xd016])),4)
            colors.update(cpu.memory[0xd012:0xd016]);positions.add(cpu.memory[0xd000])
            self.assertEqual(sequence.SequenceTests().raster(cpu),raw)
            self.assertNotEqual(sequence.SequenceTests().raster(cpu,effects=True),raw)
            self.assertTrue(all(any(v & (3<<(2*i)) for v in cpu.memory[0x980:0xa00]) for i in range(4)))
        self.assertGreater(len(colors),10)
        self.assertGreater(len(positions),4)
        p=paths();self.assertLess(p[24][1],p[8][1]);self.assertEqual(p[124][0],137)

    def test_effect_is_confined_to_shot_and_restores_dance_masks(self):
        cpu=sequence.execute(6980)
        self.assertEqual(cpu.memory[0xd01d],0)
        cpu=sequence.execute(6981,cpu)
        self.assertEqual(cpu.memory[0xd01d],3)
        cpu=sequence.execute(7978,cpu)
        self.assertEqual(cpu.memory[0xd01d],0)
        missiles,players=pmg_art()
        self.assertEqual(bytes(cpu.memory[0x980:0xa00]),missiles)
        self.assertEqual(bytes(cpu.memory[0xa00:0xc00]),players)
        cpu=sequence.execute(7000,cpu)
        cpu=sequence.execute(9163,cpu) # Seek directly into dance as well.
        self.assertEqual(bytes(cpu.memory[0x980:0xa00]),missiles)
        self.assertEqual(bytes(cpu.memory[0xa00:0xc00]),players)

    def test_single_flight_spans_whole_shot_without_low_byte_wrap(self):
        cpu=None
        xs=[]
        for elapsed in (0,128,256,384,512,640,768,896,996):
            cpu=sequence.execute(6981+elapsed,cpu)
            self.assertEqual(cpu.memory[0x83ff],elapsed//8)
            self.assertEqual(cpu.memory[0xd008:0xd00c],[1]*4)
            xs.append(cpu.memory[0xd000])
        self.assertEqual(xs,sorted(xs))
        self.assertGreater(xs[-1]-xs[0],40)
        self.assertEqual(cpu.memory[0x83ff],124)

    def test_spin_changes_geometry_as_well_as_color(self):
        from rainbow_ball import spin_masks
        frames=spin_masks()
        silhouettes=[]
        for planes in frames:
            silhouettes.append(bytes(planes[0][y]|planes[1][y]|planes[2][y]|planes[3][y] for y in range(16)))
        self.assertGreater(len(set(silhouettes)),4)
        self.assertTrue(all(any(plane) for frame in frames for plane in frame))
