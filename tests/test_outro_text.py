"""Late loading, real ANTIC text pointers and final-shot restoration."""
import unittest
import test_sequence as seq
import outro_text as text
import outro_loader as loader
from ribbon_inbetweens import decompress

class OutroTests(unittest.TestCase):
    def test_foot_taps_on_alternate_kicks_and_changes_only_the_shoe_patch(self):
        import credits_foot as foot
        from build_audio_revision import music_packets
        from build_hardware_xex import with_approved_music
        from final_boy import BITMAP_BANK, packed
        from school_portrait_bank import bank_value

        xex = seq.XEX.read_bytes()
        packets = music_packets(with_approved_music(xex, release_122=True))
        kicks = tuple(tick for tick in range(text.START-1, text.END)
                      if packets[tick][4] == 18 and packets[tick][5] & 15 >= 6
                      and packets[tick-1][4] != 18)
        self.assertEqual(kicks[0], 41883)
        self.assertEqual(foot.ATTACKS, kicks[::2])

        rest = packed()
        raised = bytearray(rest)
        _, patch = foot.patches(rest)
        for row in range(len(foot.LIFTED)):
            dest = (foot.TOP+row)*40 + foot.LEFT//4
            start = row*foot.ROW_BYTES
            raised[dest:dest+foot.ROW_BYTES] = patch[start:start+foot.ROW_BYTES]

        class LateFootMemory(seq.RuntimeMemory):
            late = False
            next_packet = None

            def __getitem__(self, address):
                if (self.ram[0xd301] == self.ram[bank_value(BITMAP_BANK)]
                        and foot.ENTRY <= cpu.pc < foot.BANK_LIMIT):
                    if address == 0xd40b and self.late:
                        return 132
                    if self.next_packet is not None and address in (0x24a7, 0x24a8):
                        return self.next_packet >> (8*(address-0x24a7)) & 255
                return super().__getitem__(address)

        memory = LateFootMemory(xex)
        cpu = seq.MPU(memory=memory)
        first, second = foot.ATTACKS[:2]
        last = foot.ATTACKS[-1]
        seq.execute(text.PREP_START-1,cpu)
        self.assertEqual(memory[0x83e0], 6)
        for tick in (text.PREP_START, foot.LIFTS[0]-2):
            seq.execute(tick,cpu)
            self.assertEqual(memory[text.STATE_FLAG], 1)
            self.assertNotEqual(memory[0xd403], 0xbc)
            self.assertEqual(memory[0xd016:0xd019], [0,0,0])
        seq.execute(foot.LIFTS[0]-1,cpu)
        self.assertEqual(memory[0xd403], 0xbc)
        self.assertEqual(bytes(memory[foot.PORTRAIT:foot.PORTRAIT+len(rest)]), raised)
        # The value at $24A7 in blanking is the first of the two packets that
        # will play before the shoe is drawn.
        for tick, expected, late in (
            (first-2, raised, False), (first-1, rest, False),
            (text.START, rest, False),
            (kicks[1]-1, rest, False), (foot.LIFTS[1]-2, rest, False),
            (foot.LIFTS[1]-1, rest, True), (foot.LIFTS[1]-1, raised, False),
            (second-2, raised, False), (second-1, rest, False),
            (last-2, raised, False), (last-1, rest, False), (text.END, rest, False),
            (0, None, False), (text.START, rest, False),
        ):
            with self.subTest(tick=tick, late=late):
                memory.late = late
                seq.execute(tick, cpu)
                self.assertEqual(memory[0xd301], 0xff)
                if expected is not None:
                    actual = bytes(memory[foot.PORTRAIT:foot.PORTRAIT+len(rest)])
                    self.assertEqual(actual, expected)

        # A late publication must not introduce a downstroke off the beat.
        seq.execute(0,cpu)
        memory.next_packet = first+57
        seq.execute(text.START,cpu)
        self.assertEqual(bytes(memory[foot.PORTRAIT:foot.PORTRAIT+len(rest)]), rest)
        self.assertEqual(memory[0xd403], 0xbc)

    def test_both_restored_display_lists_loop_to_their_own_page(self):
        cpu=seq.execute(text.START)
        memory=cpu.memory
        seq.execute(0,cpu)
        for base in (0x8000,0x8400):
            jvb=base+text.BITMAP_JVB_HIGH-2
            self.assertEqual(bytes(memory[jvb:jvb+3]),bytes((0x41,0,base>>8)))

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

    def test_live_overlay_keeps_one_framing_and_retains_text_until_ending_card(self):
        from final_boy import END as CARD_START, FADE_START, artwork

        cpu=seq.execute(text.START);m=cpu.memory
        self.assertEqual(bytes(m[0xc800:0xcf00]),loader.resources()[0][0x800:])
        self.assertEqual(m[0xd409],text.COLOR_FONT>>8)
        bitmap_mapping=None
        for tick in (text.START,text.START+1000,text.START+3000,
                     text.END-1000,text.END-1):
            cpu=seq.execute(tick,cpu)
            display=m[0xd402]|m[0xd403]<<8
            if bitmap_mapping is None:bitmap_mapping=bytes(m[display+text.BITMAP_DL:display+text.FOOTER_DL])
            self.assertEqual(bytes(m[display+text.BITMAP_DL:display+text.FOOTER_DL]),bitmap_mapping)
            for row in range(text.HISTORY_ROWS):
                at=display+text.TEXT_DL+row*3
                self.assertEqual(m[at],0xc4)
                address=m[at+1]|m[at+2]<<8
                self.assertTrue(0xbf00<=address<0xbf00+text.HISTORY_ROWS*40)
            self.assertEqual(m[0xd301],0xff)
        final_lines = text.typing_lines()[-text.HISTORY_ROWS:]
        for tick in (text.END, FADE_START-1, *range(FADE_START, CARD_START, 16), CARD_START-1):
            seq.execute(tick,cpu)
            display=m[0xd402]|m[0xd403]<<8
            self.assertEqual(display,0xbc00)
            self.assertEqual(bytes(m[display+text.BITMAP_DL:display+text.FOOTER_DL]),bitmap_mapping)
            for row,line in enumerate(final_lines):
                at=display+text.TEXT_DL+1+row*3
                address=m[at]|m[at+1]<<8
                self.assertEqual(bytes(m[address:address+40]),(text.PROMPT+line.encode()).ljust(40))
        p=artwork()
        self.assertEqual(seq.SequenceTests().raster(cpu),bytes(p[y//3*160+x] for y in range(192) for x in range(160)))
        seq.execute(CARD_START,cpu)
        self.assertEqual(m[0xd402]|m[0xd403]<<8,text.FINAL_CARD_DL)

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
            if mode and op&64:pc+=2
        self.assertEqual(events,[1,9,19,27,35,43,51,59,67,79,157,235])
        self.assertEqual(line,235)
        self.assertLessEqual((start&0x3ff)+(pc-start)+2,0x400)

    def test_first_publication_is_already_the_lower_frame(self):
        class PublicationMemory(seq.RuntimeMemory):
            def __init__(self,data):
                self.publications=[]
                self.staging_colors=[]
                self.published_colors=[]
                super().__init__(data)
            def __setitem__(self,address,value):
                if address==0xb000:
                    self.staging_colors.append(tuple(self[0xd016:0xd01b]) + (self[0xd01d],))
                if address==0xd403:
                    self.publications.append(value)
                    if value==0xbc:
                        self.published_colors.append(tuple(self[0xd016:0xd019]))
                super().__setitem__(address,value)
        memory=PublicationMemory(seq.XEX.read_bytes())
        cpu=seq.MPU(memory=memory)
        seq.execute(text.PREP_START-1,cpu);memory.publications.clear()
        seq.execute(text.START,cpu)
        self.assertEqual(memory.publications,[0xbc])
        self.assertTrue(memory.staging_colors)
        self.assertTrue(all(colors==(0,)*6 for colors in memory.staging_colors))
        self.assertEqual(memory.published_colors,[(0x4c,0x9c,0x2c)])
        memory.publications.clear()
        seq.execute(text.END,cpu)
        self.assertFalse(memory.publications)
