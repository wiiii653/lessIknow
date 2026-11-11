"""The load display is installed before the music and graphics bank copies."""
import unittest
from artifact import XEX
from extract_music import segments
import loading_screen as ls
import test_sequence as seq

@unittest.skipIf(seq.MPU is None, 'py65 required')
class LoadingScreenTests(unittest.TestCase):
    def test_loading_display_initializes_before_bank_loading(self):
        entries=list(segments(XEX.read_bytes()))
        i=next(i for i,(a,b,p) in enumerate(entries) if (a,b)==(0x02e2,0x02e3))
        self.assertEqual(entries[i][2],b'\x00\x20')
        self.assertEqual([a for a,b,p in entries[i+1:i+5]], [ls.SCREEN,ls.DLIST,ls.ENTRY,0x02e2])
        self.assertEqual(entries[i+4][2],ls.ENTRY.to_bytes(2,'little'))
        self.assertGreater(next(j for j,(a,b,p) in enumerate(entries) if a==0x8000),i+4)
        text=entries[i+1][2]
        self.assertEqual([bytes(c+32 for c in text[j:j+40]).decode().strip() for j in (0,40,80)],list(ls.LINES))
        # The first 14 original bank INITs must not turn off DMA again.
        code=next(p for a,b,p in entries if (a,b)==(0x2000,0x24b2))
        self.assertEqual(code[0x20f1-0x2000:0x20f4-0x2000],b'\xea'*3)
        cpu=seq.MPU();cpu.memory[ls.ENTRY:ls.ENTRY+len(entries[i+3][2])]=entries[i+3][2]
        cpu.pc=ls.ENTRY;cpu.sp=0xfd;cpu.memory[0x1fe:0x200]=[0xfe,0x7f]
        for _ in range(100):
            if cpu.pc==0x7fff:break
            cpu.step()
        else:self.fail('loading display initializer did not return')
        for addr,value in ((0x22f,0x22),(0x230,0),(0x231,7),(0xd400,0x22),
                           (0xd402,0),(0xd403,7),(0xd409,0xe0),(0xd017,0x0e)):
            self.assertEqual(cpu.memory[addr],value,hex(addr))
