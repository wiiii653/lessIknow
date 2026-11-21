"""Portrait cuts, banked execution and PMG overlays on held frames."""
import unittest
import test_sequence as sequence
from crush_portraits import START, END

@unittest.skipIf(sequence.MPU is None,'py65 required')
class CrushTests(unittest.TestCase):
    def test_three_ribbon_shots_and_half_beat_frames(self):
        from ribbon_dance import STEPS, FRONT_PREP_STEPS, frame_at, artwork, CUTS as RIBBON_CUTS
        cpu=None
        self.assertEqual(len(RIBBON_CUTS),3)
        for tick in STEPS:
            cpu=sequence.execute(tick,cpu)
            pixels,_=artwork(frame_at(tick))
            expected=bytes(pixels[y//3*160+x] for y in range(192) for x in range(160))
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected,tick)
            self.assertEqual(cpu.memory[0xd301],0xff)
            self.assertEqual(cpu.memory[0xd01d],3)
        self.assertEqual(sequence.execute(FRONT_PREP_STEPS[0]-1).memory[0x83e0],6)
        self.assertEqual(sequence.execute(END-1,cpu).memory[0x83e0],14)
        self.assertEqual(sequence.execute(END,cpu).memory[0x83e0],6)  # tunnel cutaway after the unchanged throw

    def test_held_pose_animates_ribbons_without_copying_bitmap(self):
        from ribbon_dance import START
        cpu=sequence.execute(START)
        raw=sequence.SequenceTests().raster(cpu)
        painted=sequence.SequenceTests().raster(cpu,effects=True)
        display=cpu.memory[0xd403]
        before=cpu.processorCycles
        cpu=sequence.execute(START+16,cpu)
        self.assertEqual(sequence.SequenceTests().raster(cpu),raw)
        self.assertEqual(cpu.memory[0xd403],display)
        self.assertNotEqual(sequence.SequenceTests().raster(cpu,effects=True),painted)
        self.assertLess(cpu.processorCycles-before,25000)

    def test_nonsequential_ribbon_shots_and_launch(self):
        from ribbon_dance import STEPS, frame_at, artwork
        cpu=None
        for step in (126,0,33,66,120,122,124,127,0):
            tick=STEPS[step]
            cpu=sequence.execute(tick,cpu)
            pixels,_=artwork(frame_at(tick))
            expected=bytes(pixels[y//3*160+x] for y in range(192) for x in range(160))
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected,step)

    def test_restart_replaces_ribbon_pmg_with_title_fireworks(self):
        cpu=sequence.execute(15088)
        cpu=sequence.execute(96,cpu)
        fresh=sequence.execute(96)
        def active_pmg(m):
            base=(m[0xd407]&0xfc)<<8
            return bytes(m[base+0x180:base+0x400])
        self.assertEqual(active_pmg(cpu.memory),active_pmg(fresh.memory))
        self.assertEqual(cpu.memory[0xd01b],0xc1)
        self.assertEqual(cpu.memory[0xd012:0xd016],fresh.memory[0xd012:0xd016])

    def test_school_portrait_cut_and_return_preserve_scene_order(self):
        from school_story import girl_front_pixels, story_frames
        boy=story_frames()[1]
        girl=girl_front_pixels()
        cpu=None
        from school_parallax import frames
        pan=frames()
        def picture(i): return bytes(pan[i][y//3*160+x] for y in range(192) for x in range(160))
        for tick,expected in ((2992,boy),(3552,boy),(3553,picture(0)),(4113,picture(17)),(4114,boy),(4487,boy)):
            cpu=sequence.execute(tick,cpu)
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected,tick)
        for tick,scene in ((4488,9),(4862,10),(5236,11),(5610,12),(5984,13)):
            cpu=sequence.execute(tick,cpu)
            self.assertEqual(cpu.memory[0x83e0],scene,tick)
