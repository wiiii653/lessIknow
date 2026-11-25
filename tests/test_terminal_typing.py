"""Real 6502 typewriter progression, Enter/scroll and flashing cursor."""
import unittest
import test_sequence as seq
import outro_text as text
import terminal_typing as typing

class TerminalTypingTests(unittest.TestCase):
    def row(self,cpu,row):return bytes(cpu.memory[0xbf00+row*40:0xbf00+(row+1)*40])
    def test_status_header_stays_fixed_across_music_tick_wrap(self):
        cpu=None
        first_wrap=(text.START+255)&~255
        for tick in (text.START,first_wrap-1,first_wrap,first_wrap+4,first_wrap+64):
            cpu=seq.execute(tick,cpu)
            memory=cpu.memory
            lms=0xbc00+text.TEXT_DL+1
            address=memory[lms]+256*memory[lms+1]
            self.assertEqual(bytes(memory[address:address+40]),
                             b'[XE-OS] LINK:ONLINE // SV2026 [OK]'.ljust(40))

    def test_prompt_waits_then_types_and_enters_the_next_line(self):
        cpu=seq.execute(text.START)
        self.assertEqual(self.row(cpu,0),b'>'.ljust(40))
        self.assertEqual(self.row(cpu,1),b' '*40)
        cpu=seq.execute(text.START+16,cpu)
        self.assertEqual(self.row(cpu,0)[:13],b'>'+text.CREDITS[0][0][:12].encode())
        self.assertEqual(self.row(cpu,0)[13],0x20)
        cpu=seq.execute(typing.schedule()[1],cpu)
        self.assertTrue(self.row(cpu,1).startswith(b'>'))
        self.assertNotIn(0x5f,self.row(cpu,0))
        self.assertEqual(self.row(cpu,2),b' '*40)
        self.assertEqual(cpu.memory[0xd403],0xbc)
    def test_cursor_flashes_without_erasing_the_typed_prefix(self):
        cpu=None
        states=[]
        for tick in (text.START+300,text.START+364):
            cpu=seq.execute(tick,cpu)
            states.append(self.row(cpu,len(text.CREDITS[0])-1))
        self.assertNotEqual(0x5f in states[0],0x5f in states[1])
        self.assertEqual(states[0].replace(b'_',b' '),states[1].replace(b'_',b' '))
        self.assertEqual(bytes(cpu.memory[text.COLOR_FONT+95*8:text.COLOR_FONT+96*8]),bytes([0]*7+[0x54]))

    def test_top_row_has_no_cursor_in_either_blink_phase(self):
        cpu=None
        for start in text.page_starts():
            for tick in (start+1,start+65):
                cpu=seq.execute(tick,cpu)
                self.assertNotIn(0x5f,self.row(cpu,0))

    def test_all_pages_write_quickly_then_hold_for_reading(self):
        cpu=None;starts=text.page_starts()
        for start,end,page in zip(starts,(*starts[1:],text.END),text.pages()):
            writes=typing.schedule()[(starts.index(start))*text.HISTORY_ROWS:][:len(page)]
            finish=writes[-1]+typing.PROMPT_DELAY+len(page[-1])
            self.assertLess(finish-start,220)
            self.assertGreater(end-finish,350)
            cpu=seq.execute(start+300,cpu)
            for row,line in enumerate(page):
                expected = b'>' + line.encode() if line else b' ' * 40
                self.assertTrue(self.row(cpu,row).startswith(expected),(start,row))
            for row in range(len(page),text.HISTORY_ROWS):self.assertEqual(self.row(cpu,row),b' '*40)
            before=[self.row(cpu,row).replace(b'_',b' ') for row in range(text.HISTORY_ROWS)]
            cpu=seq.execute(end-1,cpu)
            self.assertEqual([self.row(cpu,row).replace(b'_',b' ') for row in range(text.HISTORY_ROWS)],before)

    def test_paragraphs_get_separate_pages_without_losing_any_greeting(self):
        display_lines=tuple(line for page in text.pages() for line in page if line)
        expected=tuple(line for page in text.CREDITS for line in page if line)+tuple(line for line in text.GREETZ if line)
        self.assertEqual(display_lines,expected)
        cpu=seq.execute(text.page_starts()[9]+300)
        self.assertIn(b'VIRUS / FOORMAN / MAQ / KEY-G',self.row(cpu,2))
        self.assertIn(b'FALCON / ATARIONLINE.PL / PTODT',self.row(cpu,3))
        cpu=seq.execute(text.page_starts()[10],cpu)
        self.assertTrue(all(self.row(cpu,r)==b' '*40 for r in range(1,text.HISTORY_ROWS)))
        cpu=seq.execute(text.END-1,cpu)
        self.assertEqual(text.HISTORY_ROWS,4)
        self.assertIn(b'PERSONALLY',self.row(cpu,0))
        self.assertEqual(cpu.memory[0xd403],0xbc)
        self.assertEqual(len(self.row(cpu,3)),40)

    def test_ai_and_llm_creation_lines_are_typed_in_the_existing_pages(self):
        cpu=seq.execute(text.START+300)
        self.assertIn(b'I STARTED VIBECODING IN JULY 2026',self.row(cpu,3))
        self.assertIn(b'THIS IS MY FIRST WORK FOR ATARI',self.row(cpu,4))
        self.assertIn(b'MADE WITH OPENAI CODEX',self.row(cpu,5))
        cpu=seq.execute(text.page_starts()[2]+300,cpu)
        self.assertIn(b'AI TOOLS / ATARI SOUL',self.row(cpu,3))
        self.assertIn(b'HUMAN VISION / LLM CODE',self.row(cpu,4))
        self.assertEqual(cpu.memory[0xd403],0xbc)

    def test_terminal_keeps_read_time_and_finale_ends_on_bar_139(self):
        import final_boy
        from music_timing import tick_at_bar
        self.assertEqual(text.START,tick_at_bar(112))
        self.assertEqual(final_boy.START,text.START)
        self.assertEqual(text.END,tick_at_bar(137))
        self.assertEqual(final_boy.END,tick_at_bar(139))
        cpu=seq.execute(text.START-1)
        self.assertEqual(cpu.memory[0x83e0],6)
        cpu=seq.execute(text.START,cpu)
        self.assertEqual(cpu.memory[0x83e0],17)
