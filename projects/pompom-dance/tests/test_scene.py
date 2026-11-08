import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from py65.devices.mpu6502 import MPU
from scene_memory import RuntimeMemory
from extract_music import segments

XEX=Path('build/pompom-dance-dev.xex')
INFO=json.loads(XEX.with_suffix('.json').read_text())


def execute(tick,cpu=None):
    cpu=cpu or MPU(memory=RuntimeMemory(XEX.read_bytes()))
    m=cpu.memory;m[0xd40b]=124
    for i in range(3):m[0x24a7+i]=tick>>(8*i)&255
    cpu.pc=INFO['callback'];cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
    for _ in range(100000):
        if cpu.pc==0x7fff:return cpu
        cpu.step()
    raise AssertionError('callback did not return')


class SceneTests(unittest.TestCase):
    def test_art_is_identical_to_frozen_scene(self):
        self.assertEqual(Path('build/dance_frames.bin').read_bytes(),Path('reference/dance_frames_v141.bin').read_bytes())
        self.assertEqual(len(Path('build/dance_frames.bin').read_bytes()),98304)

    def test_all_groups_and_poses_display_from_the_selected_bank(self):
        frames=Path('reference/dance_frames_v141.bin').read_bytes();cpu=None;seen=set()
        for tick in (0,16,32,48,752,768,784,800,1504,1520,1536,1552,2992,6000,0):
            cpu=execute(tick,cpu);m=cpu.memory
            group=0 if tick%2992<748 else 1 if tick%2992<1496 else 2
            index=group*4+((tick>>4)&3);seen.add(index)
            display=m[0xd402]|m[0xd403]<<8
            art=frames[index*8192:(index+1)*8192]
            for y in range(192):
                ptr=m[display+3+y*3]|m[display+4+y*3]<<8
                offset=y*40 if y<102 else 4096+(y-102)*40
                self.assertEqual(bytes(m[ptr:ptr+40]),art[offset:offset+40],(tick,y))
            self.assertEqual(m[0xd301],0xff)
        self.assertEqual(len(seen),12)

    def test_original_music_banks_and_four_dli_spacing_are_preserved(self):
        def banks(path):return [p for a,b,p in segments(Path(path).read_bytes()) if (a,b)==(0x8000,0xbfff)]
        self.assertEqual(banks(XEX)[:8],banks('player/less-i-know-release-v035.xex')[:8])
        m=execute(0).memory
        for base in INFO['display_lists']:
            self.assertEqual([y+9 for y in range(192) if m[base+2+y*3]&128],[78,156])
            self.assertEqual(m[base],0x80)
            self.assertEqual(m[base+2+192*3+4],0x90)


if __name__=='__main__':unittest.main()
