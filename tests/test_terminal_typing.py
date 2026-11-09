"""Real 6502 typewriter progression, Enter/scroll and flashing cursor."""
import unittest
import test_sequence as seq
import outro_text as text
import terminal_typing as typing

class TerminalTypingTests(unittest.TestCase):
    def row(self,cpu,row):return bytes(cpu.memory[0xbf00+row*40:0xbf00+(row+1)*40])
    def test_prompt_waits_then_types_and_enters_the_next_line(self):
        cpu=seq.execute(text.START)
        self.assertTrue(self.row(cpu,0).startswith(b'>_'))
        self.assertEqual(self.row(cpu,1),b' '*40)
        cpu=seq.execute(text.START+16,cpu)
        self.assertEqual(self.row(cpu,0)[:13],b'>'+text.CREDITS[0][0][:12].encode())
        self.assertEqual(self.row(cpu,0)[13],0x5f)
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
        self.assertEqual(bytes(cpu.memory[text.FONT+95*8:text.FONT+96*8]),bytes([0]*6+[0x54,0]))

    def test_cursor_also_blinks_while_the_line_is_being_written(self):
        start=text.page_starts()[1]
        cpu=seq.execute(start+8)
        earlier=self.row(cpu,0)
        self.assertNotIn(0x5f,earlier)
        cpu=seq.execute(start+16,cpu)
        later=self.row(cpu,0)
        self.assertIn(0x5f,later)
        self.assertEqual(earlier[:5],later[:5])
        self.assertGreater(len(later.rstrip()),len(earlier.rstrip()))

    def test_all_pages_write_quickly_then_hold_for_reading(self):
        cpu=None;starts=text.page_starts()
        for start,end,page in zip(starts,(*starts[1:],text.END),text.pages()):
            writes=typing.schedule()[(starts.index(start))*text.HISTORY_ROWS:][:len(page)]
            finish=writes[-1]+typing.PROMPT_DELAY+len(page[-1])
            self.assertLess(finish-start,220)
            self.assertGreater(end-finish,600)
            cpu=seq.execute(start+300,cpu)
            for row,line in enumerate(page):
                self.assertTrue(self.row(cpu,row).startswith(b'>'+line.encode()),(start,row))
            for row in range(len(page),text.HISTORY_ROWS):self.assertEqual(self.row(cpu,row),b' '*40)
            before=[self.row(cpu,row).replace(b'_',b' ') for row in range(text.HISTORY_ROWS)]
            cpu=seq.execute(end-1,cpu)
            self.assertEqual([self.row(cpu,row).replace(b'_',b' ') for row in range(text.HISTORY_ROWS)],before)
        cpu=seq.execute(text.END,cpu)
        self.assertTrue(all(self.row(cpu,r)==b' '*40 for r in range(text.HISTORY_ROWS)))

    def test_paragraphs_get_separate_pages_without_losing_any_greeting(self):
        self.assertEqual(tuple(line for page in text.pages() for line in page),tuple(line for line in text.all_lines() if line))
        cpu=seq.execute(text.page_starts()[6]+300)
        self.assertIn(b'VIRUS / FOORMAN / MAQ',self.row(cpu,0))
        self.assertIn(b'ATARIONLINE.PL / PTODT',self.row(cpu,1))
        cpu=seq.execute(text.page_starts()[7],cpu)
        self.assertTrue(all(self.row(cpu,r)==b' '*40 for r in range(1,text.HISTORY_ROWS)))
        cpu=seq.execute(text.END-1,cpu)
        self.assertEqual(text.HISTORY_ROWS,6)
        self.assertIn(b'PERSONALLY',self.row(cpu,3))
        self.assertEqual(cpu.memory[0xd403],0xbc)
        self.assertEqual(len(self.row(cpu,5)),40)

    def test_ai_and_llm_creation_lines_are_typed_in_the_existing_pages(self):
        cpu=seq.execute(text.START+300)
        self.assertIn(b'HUMAN VISION / LLM CODE',self.row(cpu,5))
        cpu=seq.execute(text.page_starts()[2]+300,cpu)
        self.assertIn(b'AI TOOLS / ATARI SOUL',self.row(cpu,3))
        self.assertEqual(cpu.memory[0xd403],0xbc)

    def test_terminal_and_boy_start_ten_seconds_earlier_with_the_same_ending(self):
        import final_boy
        self.assertEqual(text.START,53850-2000)
        self.assertEqual(final_boy.START,text.START)
        self.assertEqual(text.END,59085)
        cpu=seq.execute(text.START-1)
        self.assertEqual(cpu.memory[0x83e0],6)
        cpu=seq.execute(text.START,cpu)
        self.assertEqual(cpu.memory[0x83e0],17)
