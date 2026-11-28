"""Real 6502 typewriter progression, Enter/scroll and flashing cursor."""
import unittest
import test_sequence as seq
import outro_text as text
import terminal_typing as typing

class TerminalTypingTests(unittest.TestCase):
    def test_terminal_opens_with_four_blank_rows_before_first_prompt(self):
        cpu = None
        for tick in (text.START, text.TYPE_START-1):
            cpu = seq.execute(tick, cpu)
            self.assertEqual(cpu.memory[0xd403], 0xbc)
            for row in range(text.HISTORY_ROWS):
                lms = 0xbc00 + text.TEXT_DL + 3*row + 1
                address = int.from_bytes(bytes(cpu.memory[lms:lms+2]), 'little')
                self.assertEqual(bytes(cpu.memory[address:address+40]), b' '*40)

    def test_credits_and_greetings_scroll_type_and_blink_continuously(self):
        starts = text.page_starts()
        ends = (*starts[1:], text.END)
        self.assertEqual(starts[0], text.TYPE_START)
        intervals = [end-start for start, end in zip(starts, ends)]
        self.assertLessEqual(max(intervals)-min(intervals), 1)

        credits = tuple(line for group in text.CREDITS for line in group)
        greetings = tuple(line for line in text.GREETZ if line)
        transcript = (b'', b'', b'',
                      *(b'>' + line.encode() for line in (text.STATUS_HEADER,) + credits + greetings))
        self.assertEqual(len(starts), len(transcript)-3)

        cpu = seq.execute(text.START-1)
        for index, (start, end) in enumerate(zip(starts, ends)):
            history = [line.ljust(40) for line in transcript[index:index+3]]
            line = transcript[index+3]
            typed = start + typing.PROMPT_DELAY + 8
            finished = start + typing.PROMPT_DELAY + len(line)-1
            blink_on = (finished + 2*typing.BLINK_MASK-1) & ~(2*typing.BLINK_MASK-1)
            blink_off = blink_on + typing.BLINK_MASK
            self.assertLess(blink_off, end)
            for tick, prefix in ((start, b'>'), (typed, line[:9]), (blink_on, line),
                                 (blink_off, line), (end-1, line)):
                cpu = seq.execute(tick, cpu)
                self.assertEqual(cpu.memory[0xd403], 0xbc)
                cursor = b'_' if tick & typing.BLINK_MASK == 0 else b''
                expected = [*history, (prefix + cursor).ljust(40)]
                for row, contents in enumerate(expected):
                    address = 0xbf00 + 40*row
                    lms = 0xbc00 + text.TEXT_DL + 3*row + 1
                    self.assertEqual(bytes(cpu.memory[lms:lms+2]), address.to_bytes(2, 'little'))
                    self.assertEqual(bytes(cpu.memory[address:address+40]), contents, (tick, row))

        self.assertEqual(bytes(cpu.memory[text.COLOR_FONT+95*8:text.COLOR_FONT+96*8]),
                         bytes([0]*7+[0x54]))

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
