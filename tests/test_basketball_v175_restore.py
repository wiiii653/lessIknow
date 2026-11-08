"""Verify restored keyframes and glass against the preserved executable."""
import json
from pathlib import Path
import unittest
import test_sequence as s
from extract_music import segments
from scene_memory import RuntimeMemory
from basketball_hero import START,DUNK,END,DATA,packed,ORBIT_DATA,helper,ENTRY

@unittest.skipIf(s.MPU is None,'py65 required')
class BasketballV175RestoreTests(unittest.TestCase):
    def test_packed_art_and_three_glass_patches_match_v175_exactly(self):
        banks=[p for a,b,p in segments(Path('build/visual-prototype-v175.xex').read_bytes())
               if (a,b)==(0x8000,0xbfff)]
        old=banks[15]
        self.assertEqual(packed(),old[DATA-ENTRY:DATA-ENTRY+len(packed())])
        self.assertLessEqual(ENTRY+len(helper()),DATA)
        self.assertLessEqual(DATA+len(packed()),ORBIT_DATA)

    def test_live_keyframes_and_ball_match_the_archived_release(self):
        old=Path('build/visual-prototype-v175.xex')
        self.assertEqual(json.loads(old.with_suffix('.json').read_text())['callback'],
                         json.loads(s.METADATA.read_text())['callback'])
        archived=s.MPU(memory=RuntimeMemory(old.read_bytes()));current=None
        for tick in (START,START+48,START+96,START+160,DUNK,DUNK+376,
                     DUNK+488,DUNK+600,DUNK+648,DUNK+696,END-1):
            archived=s.execute(tick,archived);current=s.execute(tick,current)
            self.assertEqual(s.SequenceTests().raster(current),s.SequenceTests().raster(archived),tick)
            self.assertEqual(current.memory[0x83ec],archived.memory[0x83ec],tick)
            self.assertEqual(current.memory[0x83e5],archived.memory[0x83e5],tick)
            self.assertEqual(current.memory[0xd000:0xd01e],archived.memory[0xd000:0xd01e],tick)
            for cpu in (current,archived):
                self.assertEqual(cpu.memory[0xd301],0xff)
