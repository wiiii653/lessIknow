"""Late loading, real ANTIC text pointers and final-shot restoration."""
import unittest
import test_sequence as seq
import outro_text as text
import outro_loader as loader
from ribbon_inbetweens import decompress

class OutroTests(unittest.TestCase):
    def test_early_outro_never_restores_the_old_frame_between_callbacks(self):
        from test_engine_cache import TrackedMemory
        memory=TrackedMemory(seq.XEX.read_bytes());cpu=seq.MPU(memory=memory)
        seq.execute(text.START,cpu)
        saved=bytes(memory[0xbc00+text.BITMAP_DL:0xbc00+text.FOOTER_DL])
        for tick in range(text.START+4,text.END,16):
            memory.writes.clear();seq.execute(tick,cpu)
            self.assertEqual(memory[0xdd0],2,tick)
            self.assertEqual(memory[0xd403],0xbc,tick)
            self.assertFalse(0xd403 in memory.writes,tick)
            self.assertFalse(any(0x8000<=a<0x824a or 0x8400<=a<0x864a for a in memory.writes),tick)
            self.assertEqual(bytes(memory[0xbc00+text.BITMAP_DL:0xbc00+text.FOOTER_DL]),saved,tick)

    def test_staged_payload_roundtrip_and_boundaries(self):
        raw,packed,chunks=loader.resources()
        self.assertEqual(decompress(packed),raw)
        self.assertLessEqual(loader.ENTRY+len(loader.bootstrap()),0x4000)
        self.assertTrue(all(any(lo<=a<a+len(b)<=hi for lo,hi in loader.GAPS)
                            for a,b,d in chunks))
        from terminal_typing import TIMES,schedule
        from outro_palette import ENTRY as PALETTE
        for address,data,_ in chunks:
            self.assertFalse(address<TIMES+2*len(schedule()) and TIMES<address+len(data))
            self.assertFalse(address<0x249c and PALETTE<address+len(data))

    def test_live_overlay_keeps_one_framing_and_blanks_text_at_finale(self):
        cpu=seq.execute(text.START);m=cpu.memory
        self.assertEqual(bytes(m[0xc800:0xcf00]),loader.resources()[0][0x800:])
        self.assertEqual(m[0xd409],0xc8)
        bitmap_mapping=None
        for tick in (text.START,text.START+1000,text.START+3000,
                     text.END-1000,text.END-1):
            cpu=seq.execute(tick,cpu)
            display=m[0xd402]|m[0xd403]<<8
            if bitmap_mapping is None:bitmap_mapping=bytes(m[display+text.BITMAP_DL:display+text.FOOTER_DL])
            self.assertEqual(bytes(m[display+text.BITMAP_DL:display+text.FOOTER_DL]),bitmap_mapping)
            for row in range(text.HISTORY_ROWS):
                at=display+4+row*3
                self.assertEqual(m[at],0xc4 if row==text.HISTORY_ROWS-1 else 0x44)
                address=m[at+1]|m[at+2]<<8
                self.assertTrue(0xbf00<=address<0xbf00+text.HISTORY_ROWS*40)
            self.assertEqual(m[0xd301],0xff)
        cpu=seq.execute(text.END,cpu)
        display=m[0xd402]|m[0xd403]<<8
        self.assertEqual(display,0xbc00)
        self.assertEqual(bytes(m[display+text.BITMAP_DL:display+text.FOOTER_DL]),bitmap_mapping)
        for row in range(text.HISTORY_ROWS):
            at=display+5+row*3
            address=m[at]|m[at+1]<<8
            self.assertEqual(bytes(m[address:address+40]),b' '*40)
        p=__import__('final_boy').artwork()
        self.assertEqual(seq.SequenceTests().raster(cpu),bytes(p[y//3*160+x] for y in range(192) for x in range(160)))

    def test_music_dli_spacing_and_static_scanline_storage_survive_outro(self):
        cpu=seq.execute(text.START-1);m=cpu.memory
        spans=((0x824a,0x8300),(0x8340,0x83e0),(0x864a,0x8980))
        saved=[bytes(m[a:b]) for a,b in spans]
        for tick in (text.START,text.START+3000,text.END):
            seq.execute(tick,cpu)
            self.assertEqual([bytes(m[a:b]) for a,b in spans],saved)
        seq.execute(text.START,cpu)
        pc=m[0xd402]|m[0xd403]<<8;start=pc;line=0;events=[]
        for _ in range(210):
            op=m[pc];pc+=1;mode=op&15
            if mode==1:break
            line+=((op>>4)&7)+1 if mode==0 else 8 if mode in (2,4) else 1
            if op&128:events.append(line)
            if op&64:pc+=2
        self.assertEqual(events,[1,57,79,157,235])
        self.assertEqual(line,235)
        self.assertLessEqual((start&0x3ff)+(pc-start)+2,0x400)

    def test_first_publication_is_already_the_lower_frame(self):
        class PublicationMemory(seq.RuntimeMemory):
            def __init__(self,data):
                self.publications=[]
                super().__init__(data)
            def __setitem__(self,address,value):
                if address==0xd403:self.publications.append(value)
                super().__setitem__(address,value)
        memory=PublicationMemory(seq.XEX.read_bytes())
        cpu=seq.MPU(memory=memory)
        seq.execute(text.START-1,cpu);memory.publications.clear()
        seq.execute(text.START,cpu)
        self.assertEqual(memory.publications,[0xbc])
        memory.publications.clear()
        seq.execute(text.END,cpu)
        self.assertFalse(memory.publications)
