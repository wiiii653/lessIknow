"""Execute PMG code: lip sync, finite arcs, fading, safe buffers and cutoff."""
import unittest
import test_sequence as s
from school_story import boy_poses
from whistle_pmg import START,END,path,age_at,luminance

@unittest.skipIf(s.MPU is None,'py65 required')
class WhistleTests(unittest.TestCase):
    def test_melody_is_not_painted_on_building(self):
        _,turned,whistle=boy_poses()
        for y in range(192):
            self.assertEqual(turned[y*160:y*160+104],whistle[y*160:y*160+104])

    def test_first_note_and_puckered_lips_begin_together(self):
        turned,whistle=boy_poses()[1:]
        self.assertNotEqual(turned[99*160+119:99*160+123],whistle[99*160+119:99*160+123])
        cpu=s.execute(START-1)
        self.assertEqual(cpu.memory[0xd01d],0)
        for tick,pose in ((START,whistle),(END,turned)):
            cpu=s.execute(tick,cpu)
            pixels=s.SequenceTests().raster(cpu)
            for y in range(99,114):
                self.assertEqual(pixels[y*160+119:y*160+123],pose[y*160+119:y*160+123])
            self.assertEqual(cpu.memory[0xd01d],3 if tick==START else 0)
            if tick==START:
                self.assertEqual(cpu.memory[0xd000]-48,path(0)[0])
                self.assertEqual(list(cpu.memory[0xd001:0xd004]),[0,0,0])

    def test_two_staggered_waves_follow_distinct_upward_arcs(self):
        cpu=None
        for phase in (0,12,12.5,24,36,60,86,93):
            cpu=s.execute(START+int(phase*8),cpu)
            base=(cpu.memory[0xd407]&0xfc)<<8
            for p in range(4):
                age=age_at(phase,p)
                if age is None:
                    self.assertEqual(cpu.memory[0xd000+p],0,(phase,p));continue
                self.assertEqual(cpu.memory[0xd000+p],48+path(age,p)[0])
                rows=cpu.memory[base+0x200+p*128:base+0x280+p*128]
                self.assertEqual(next(i for i,v in enumerate(rows) if v),path(age,p)[1])
                self.assertEqual(cpu.memory[0xd012+p]&15,luminance(int(age)))
                self.assertTrue(any(cpu.memory[base+0x180:base+0x200]))
        self.assertNotEqual(path(24,0),path(24,3))
        for p in range(4):
            ys=[path(age,p)[1] for age in range(36)]
            self.assertEqual(ys,sorted(ys,reverse=True))

    def test_alternate_buffer_preserves_front_and_restores_bank(self):
        cpu=s.execute(START)
        old=cpu.memory[0xd407];bank=cpu.memory[0xd301]
        base=(old&0xfc)<<8;image=cpu.memory[base+0x180:base+0x400]
        cpu=s.execute(START+4,cpu)
        self.assertEqual(old^cpu.memory[0xd407],0x80)
        self.assertEqual(image,cpu.memory[base+0x180:base+0x400])
        self.assertEqual(bank,cpu.memory[0xd301])

    def test_final_wave_fades_before_doorway_and_does_not_leak(self):
        cpu=s.execute(START+89*8)
        self.assertGreater(cpu.memory[0xd003],0)
        self.assertLessEqual(cpu.memory[0xd015]&15,6)
        cpu=s.execute(END-1,cpu)
        self.assertEqual(list(cpu.memory[0xd000:0xd008]),[0]*8)
        for tick in (END,END+80,5983,5984):
            cpu=s.execute(tick,cpu)
            self.assertEqual(cpu.memory[0xd01d],0,tick)

    def test_notes_are_large_bright_and_missiles_are_widened(self):
        cpu=s.execute(START+12*8)
        base=(cpu.memory[0xd407]&0xfc)<<8
        for p in (0,1,2):
            self.assertGreater(cpu.memory[0xd000+p],0)
            self.assertEqual(cpu.memory[0xd008+p],1)  # 16 logical pixels
            rows=cpu.memory[base+0x200+p*128:base+0x280+p*128]
            lit=[y for y,bits in enumerate(rows) if bits]
            self.assertGreaterEqual(len(lit),16)
            self.assertGreaterEqual((max(lit)-min(lit)+1)*2,32)
            self.assertEqual(cpu.memory[0xd012+p]&15,14)
        self.assertEqual(cpu.memory[0xd00c],0x55)
