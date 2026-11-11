"""Translated montage preserves v247 and restores the v239 ending."""
import unittest
from pathlib import Path
import test_sequence as seq
from trevor_awakens import END as TREVOR_END
from trevor_polished import HITS
from outro_text import START as OUTRO_START, END as TEXT_END
from girl_eyes import START as EYE_START, END as EYE_END, frame_at as eye_frame_at


class RetimedMontageTests(unittest.TestCase):
    def test_boundaries_and_complete_last_punch(self):
        self.assertEqual((TREVOR_END,OUTRO_START,TEXT_END),(28909,49850,59085))
        self.assertLessEqual(HITS[-1]+106,TREVOR_END)
        cpu=seq.execute(TREVOR_END-1)
        self.assertEqual(cpu.memory[0x83e0],16)
        seq.execute(TREVOR_END,cpu);self.assertEqual(cpu.memory[0x83e0],6)
        seq.execute(OUTRO_START-1,cpu);self.assertEqual(cpu.memory[0x83e0],6)
        seq.execute(OUTRO_START,cpu);self.assertEqual(cpu.memory[0x83e0],17)

    @unittest.skipUnless(all((seq.ROOT/'build'/f'visual-prototype-v{n}.xex').exists() for n in (239,247)),
                         'v239 and v247 comparison builds required')
    def test_translated_frames_and_restored_ending(self):
        for release,start,end in ((247,28909,47850),(239,47850,49850)):
            path=seq.ROOT/'build'/f'visual-prototype-v{release}.xex'
            old=seq.MPU(memory=seq.RuntimeMemory(path.read_bytes()));new=None
            for tick in range(start,end,137):
                old=seq.execute(tick+4000,old);new=seq.execute(tick,new)
                original=old.memory[0x83ed]
                self.assertEqual(eye_frame_at(tick,original),new.memory[0x83ed],tick)
                # Those samples intentionally use eye art or remapped tunnel phases.
                if EYE_START<=tick<EYE_END or original>=60: continue
                self.assertEqual(seq.SequenceTests().raster(old),seq.SequenceTests().raster(new),tick)
                self.assertEqual(old.memory[0xd000:0xd016],new.memory[0xd000:0xd016],tick)
                self.assertEqual(old.memory[0xd016:0xd01a],new.memory[0xd016:0xd01a],tick)
