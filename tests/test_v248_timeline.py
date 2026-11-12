"""Translated montage preserves v247 and restores the v239 ending."""
import unittest
import test_sequence as seq
from trevor_awakens import END as TREVOR_END
from trevor_polished import HITS
from outro_text import START as OUTRO_START, END as TEXT_END
from girl_eyes import START as EYE_START, END as EYE_END, frame_at as eye_frame_at
import post_trevor_director as director


class RetimedMontageTests(unittest.TestCase):
    def test_boundaries_and_complete_last_punch(self):
        self.assertEqual((TREVOR_END,OUTRO_START,TEXT_END),(29656,49850,59085))
        self.assertLessEqual(HITS[-1]+106,TREVOR_END)
        cpu=seq.execute(TREVOR_END-1)
        self.assertEqual(cpu.memory[0x83e0],16)
        seq.execute(TREVOR_END,cpu);self.assertEqual(cpu.memory[0x83e0],6)
        seq.execute(OUTRO_START-1,cpu);self.assertEqual(cpu.memory[0x83e0],6)
        seq.execute(OUTRO_START,cpu);self.assertEqual(cpu.memory[0x83e0],17)

    def test_long_rotator_timeline_and_eye_frame_mapping(self):
        cuts=director.cuts()
        samples=sorted({director.START,director.END-1,
                        *(tick+delta for tick,_ in cuts for delta in (-16,-1,0,1,16)
                          if director.START<=tick+delta<director.END),
                        EYE_START,EYE_START+16,EYE_END-16,EYE_END})
        for tick in samples:
            cpu=seq.execute(tick);frame=cpu.memory[0x83ed]
            expected=eye_frame_at(tick,director.frame_at(tick))
            self.assertEqual(frame,expected,tick)
            if frame>=60:
                self.assertTrue(EYE_START<=tick<EYE_END,tick)
            else:
                self.assertLess(frame,60,tick)
