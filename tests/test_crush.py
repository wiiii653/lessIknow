"""Portrait cuts, banked execution and PMG overlays on held frames."""
import unittest
import test_sequence as sequence
from crush_portraits import CUTS, portraits, START, END
from pompom_effects import variants, PALETTES

@unittest.skipIf(sequence.MPU is None,'py65 required')
class CrushTests(unittest.TestCase):
    def test_all_cuts_pixels_and_held_frames(self):
        cpu=None
        art=variants()
        for i,t in enumerate(CUTS):
            cpu=sequence.execute(t,cpu)
            expected=bytes(art[i][(t>>4)&3][y*52//192*80+x//2] for y in range(192) for x in range(160))
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected)
            before=cpu.processorCycles
            dl=cpu.memory[0xd403]
            cpu=sequence.execute(t+4,cpu)
            self.assertLess(cpu.processorCycles-before,9000)
            self.assertEqual(cpu.memory[0xd403],dl)
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected)
        self.assertEqual(sequence.execute(START-1).memory[0x83e0],6)
        self.assertEqual(sequence.execute(END-1,cpu).memory[0x83e0],14)
        self.assertEqual(sequence.execute(END,cpu).memory[0x83e0],15)

    def test_blink_preserved_with_animated_pompoms(self):
        cpu=sequence.execute(15088)
        raster=sequence.SequenceTests().raster(cpu)
        self.assertNotEqual(cpu.memory[0xd000],0)
        cpu=sequence.execute(15092,cpu)
        self.assertEqual(sequence.SequenceTests().raster(cpu),raster)
        self.assertNotEqual(sequence.SequenceTests().raster(cpu,effects=True),raster)
        cpu=sequence.execute(15104,cpu)
        self.assertEqual(cpu.memory[0xd000],0)

    def test_every_animation_phase_reconstructs_local_pixels(self):
        art=variants()
        cpu=None
        for i,t in enumerate(CUTS):
            for phase in (3,0,2,1,3,0):
                tick=t+((phase-((t>>4)&3))%4)*16
                cpu=sequence.execute(tick,cpu)
                expected=bytes(art[i][phase][y*52//192*80+x//2] for y in range(192) for x in range(160))
                self.assertEqual(sequence.SequenceTests().raster(cpu),expected,(i,phase))
                self.assertEqual(tuple(cpu.memory[0xd016:0xd019]),PALETTES[i])

    def test_restart_restores_dance_player_and_missile_art(self):
        cpu=sequence.execute(15088)
        cpu=sequence.execute(96,cpu)
        from engine_effects import pmg_art
        missiles,players=pmg_art()
        self.assertEqual(bytes(cpu.memory[0x0980:0x0a00]),missiles)
        self.assertEqual(bytes(cpu.memory[0x0a00:0x0c00]),players)

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

    def test_pompom_bank_layout_and_protected_skin(self):
        from pompom_effects import ENTRY,DATA,helper
        from rainbow_ball import ENTRY as BALL_ENTRY,helper as ball_helper,RESTORE
        from crush_portraits import cleanup
        code,data=helper()
        self.assertLessEqual(BALL_ENTRY+len(ball_helper()),ENTRY)
        self.assertLessEqual(ENTRY+len(code),RESTORE)
        self.assertLessEqual(RESTORE+len(cleanup(RESTORE)),DATA)
        self.assertLessEqual(DATA+len(data),0x8000)
        source=portraits()
        for shot,views in enumerate(variants()):
            for view in views:
                self.assertTrue(all(view[j]==3 for j,value in enumerate(source[shot]) if value==3))
            self.assertGreater(len(set(views)),2)
