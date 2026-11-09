"""Display-list colour split restores skin colours without a fifth music tick."""
import json
import unittest
import test_sequence as seq
from trevor_awakens import START,HIT

class OutroPaletteTests(unittest.TestCase):
    def interrupt(self,cpu,line):
        m=cpu.memory;m[0xd40b]=line//2
        cpu.sp=0xfa;m[0x1fb:0x1fe]=[0x20,0,7]
        cpu.pc=json.loads(seq.METADATA.read_text())['music_entry']
        for _ in range(10000):
            if cpu.pc==0x700:return
            cpu.step()
        self.fail('NMI did not return')

    def test_extra_dli_does_not_change_music_or_skin_palette(self):
        cpu=seq.execute(54000);m=cpu.memory
        before=bytes(m[0x24a7:0x24aa]);skin=m[0xd018];shirt=m[0xd017]
        self.interrupt(cpu,64)
        self.assertEqual(bytes(m[0x24a7:0x24aa]),before)
        self.assertEqual((m[0xd016],m[0xd017],m[0xd018]),(0x4c,shirt,skin))
        self.assertEqual(m[0xd301],0xff)

    def test_first_dli_sets_green_ink_without_colouring_the_background(self):
        cpu=seq.execute(54000);m=cpu.memory
        # Exit immediately after the router's regular-music RTS to isolate palette work.
        from outro_palette import ENTRY
        cpu.pc=ENTRY;cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f];m[0xd40b]=4
        old_skin=m[0xd018]
        for _ in range(1000):
            if cpu.pc==0x7fff:break
            cpu.step()
        self.assertEqual(m[0xd016],0xce)
        self.assertEqual(m[0xd01a],0)
        self.assertEqual(m[0xd018],old_skin)

    def test_trevor_entrance_has_the_fighting_base_palette(self):
        cpu=None
        for tick in (START,START+500,HIT-1):
            cpu=seq.execute(tick,cpu)
            self.assertEqual(cpu.memory[0xd016:0xd019],[0x48,0x68,0x2a])
