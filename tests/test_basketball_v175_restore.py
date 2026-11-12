"""Verify restored keyframes and glass against the preserved executable."""
import json
from pathlib import Path
import unittest
import test_sequence as s
from extract_music import segments
from scene_memory import RuntimeMemory
from basketball_hero import START,DUNK,END,DATA,packed,ORBIT_DATA,helper,ENTRY,reference_art,unpack,scene_frame,DRIBBLE_PATCH_BYTES,DRIBBLE_WIDTH,DRIBBLE_X,DRIBBLE_Y
from hero_mask_cleanup import NEGATIVE_SPACE, SHOULDER_SPACE, KNEE_SKIN
from arena_art import background

@unittest.skipIf(s.MPU is None,'py65 required')
class BasketballV175RestoreTests(unittest.TestCase):
    def test_dribble_poses_and_ball_match_release001(self):
        from basketball_hero import frames
        for pose in (0,1,6,7):
            for x,y in KNEE_SKIN:
                self.assertEqual(frames()[pose][y*160+x],3,(pose,x,y))
        archived=s.MPU(memory=RuntimeMemory(Path('releases/less-i-know-demo-release-001.xex').read_bytes()))
        current=None
        for tick in range(START,DUNK,8):
            archived=s.execute(tick,archived);current=s.execute(tick,current)
            for addr in (0x83ec,0x83ff,0x83e8,0x83e9,0xd000):
                self.assertEqual(current.memory[addr],archived.memory[addr],(tick,hex(addr)))

    def test_release001_poses_change_only_in_background_masks(self):
        banks=[p for a,b,p in segments(Path('releases/less-i-know-demo-release-001.xex').read_bytes())
               if (a,b)==(0x8000,0xbfff)]
        old=banks[15]
        self.assertEqual(reference_art(),old[DATA-ENTRY:DATA-ENTRY+len(packed())])
        clean=packed();original=reference_art();plate=background(interior=True);total=0
        for pose in range(5):
            a=unpack(original[pose*2240:(pose+1)*2240]);b=unpack(clean[pose*2240:(pose+1)*2240])
            for i,(before,after) in enumerate(zip(a,b)):
                if before==after:continue
                x,y=i%160,i//160
                if pose==0 and (x,y) in KNEE_SKIN:
                    self.assertEqual(after,3)
                    continue
                if pose==0 and y in SHOULDER_SPACE and SHOULDER_SPACE[y][0]<=x<SHOULDER_SPACE[y][1] and before==3:
                    self.assertEqual(after,0)
                    total+=1
                    continue
                if pose==0 and 70<=x<76 and 17<=y<21 and before==1:
                    self.assertEqual(after,0)
                    total+=1
                    continue
                self.assertEqual(before,1)
                self.assertEqual(after,plate[i])
                self.assertTrue(any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in NEGATIVE_SPACE[pose]))
                total+=1
        self.assertGreater(total,100)
        for pose in range(3):
            begin=5*2240+pose*DRIBBLE_PATCH_BYTES;end=begin+DRIBBLE_PATCH_BYTES
            before=unpack(original[begin:end]);after=unpack(clean[begin:end])
            for i,(old_pixel,new_pixel) in enumerate(zip(before,after)):
                if old_pixel==new_pixel:continue
                x=DRIBBLE_X+i%DRIBBLE_WIDTH;y=DRIBBLE_Y+i//DRIBBLE_WIDTH
                if (x,y) in KNEE_SKIN:
                    self.assertEqual(new_pixel,3)
                    continue
                if 70<=x<76 and 17<=y<21 and old_pixel==1:
                    self.assertEqual(new_pixel,0)
                    continue
                self.assertEqual(old_pixel,1)
                self.assertEqual(new_pixel,plate[y*160+x])
                self.assertTrue(any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in NEGATIVE_SPACE[0]))
        self.assertEqual(clean[5*2240+3*DRIBBLE_PATCH_BYTES:],original[5*2240+3*DRIBBLE_PATCH_BYTES:])
        self.assertLessEqual(ENTRY+len(helper()),DATA)
        self.assertLessEqual(DATA+len(packed()),ORBIT_DATA)

    def test_dunk_keyframes_and_ball_match_the_archived_release(self):
        old=Path('releases/less-i-know-demo-release-001.xex')
        self.assertEqual(json.loads(old.with_suffix('.json').read_text())['callback'],
                         json.loads(s.METADATA.read_text())['callback'])
        archived=s.MPU(memory=RuntimeMemory(old.read_bytes()));current=None
        for tick in (DUNK,DUNK+376,
                     DUNK+488,DUNK+600,DUNK+648,DUNK+696,END-1):
            archived=s.execute(tick,archived);current=s.execute(tick,current)
            art=scene_frame(tick,current.memory[0x83ec])
            expected=bytes(art[y*56//192*160+x] for y in range(192) for x in range(160))
            self.assertEqual(s.SequenceTests().raster(current),expected,tick)
            self.assertEqual(current.memory[0x83ec],archived.memory[0x83ec],tick)
            self.assertEqual(current.memory[0x83e5],archived.memory[0x83e5],tick)
            actual=current.memory[0xd000:0xd01e];reference=archived.memory[0xd000:0xd01e]
            self.assertEqual(actual[0x16:0x19],[0x38,0x68,0x2a])
            reference[0x16:0x19]=actual[0x16:0x19]
            self.assertEqual(actual,reference,tick)
            for cpu in (current,archived):
                self.assertEqual(cpu.memory[0xd301],0xff)
