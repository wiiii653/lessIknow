"""Hardware display-list constraints that protect the music interrupt cadence."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from build_visual_prototype import xex_segment
from extract_music import segments

ROOT = Path(__file__).resolve().parents[1]


class DisplayListTests(unittest.TestCase):
    def inspect(self, path, address):
        return subprocess.check_output(
            [sys.executable, str(ROOT / 'tools/inspect_display_list.py'),
             str(path), '--address', hex(address)], text=True)

    def test_jump_operands_wrap_inside_one_kib(self):
        memory = bytearray(1024)
        memory[:2] = b'\x00\x90'
        memory[-1] = 0x41
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'wrap.xex'
            path.write_bytes(b'\xff\xff' + xex_segment(0x8000, memory))
            self.assertIn('JVB $9000', self.inspect(path, 0x83ff))

    def test_each_animation_phase_preserves_music_dlis(self):
        path = ROOT / 'build/kaleidoscope.xex'
        for address in (0xb000, 0xb400, 0xb800, 0xbc00):
            with self.subTest(address=hex(address)):
                output = self.inspect(path, address)
                lines = [int(row.rsplit(' ', 1)[1]) for row in output.splitlines()
                         if 'DLI on line' in row]
                self.assertEqual(lines, [0, 78, 156, 234])
                self.assertIn('Total display-list scanlines: 235', output)
                self.assertIn(f'JVB ${address:04X}', output)

    def test_sequence_preserves_music_dlis(self):
        output = self.inspect(ROOT / 'build/visual-prototype-v051.xex', 0x8000)
        lines = [int(row.rsplit(' ', 1)[1]) for row in output.splitlines()
                 if 'DLI on line' in row]
        self.assertEqual(lines, [0, 78, 156, 234])
        self.assertIn('Total display-list scanlines: 235', output)

    def test_visible_image_has_no_blank_dli_seams(self):
        for address in (0x8000, 0x8400):
            output = self.inspect(ROOT / 'build/visual-prototype-v051.xex', address)
            visible = [line for line in output.splitlines() if ': mode E,' in line]
            self.assertEqual(len(visible), 192)
            for row, line in enumerate(visible):
                self.assertIn(f'lines {row + 9}-{row + 9}', line)

    def test_music_payload_preserved_and_unused_banks_reclaimed(self):
        def banks(name):
            return [data for start, end, data in segments((ROOT / name).read_bytes())
                    if (start, end) == (0x8000, 0xbfff)]
        original = banks('less-i-know-release-v035.xex')
        demo = banks('build/visual-prototype-v051.xex')
        self.assertEqual(original[:7], demo[:7])
        self.assertEqual(original[7][:0x0b10], demo[7][:0x0b10])
        self.assertEqual(set(original[7][0x2000:]), {255})
        self.assertNotEqual(original[7][0x2000:], demo[7][0x2000:])
        self.assertTrue(all(set(bank) == {255} for bank in original[8:]))
        self.assertTrue(all(set(bank) != {255} for bank in demo[8:]))


if __name__ == '__main__':
    unittest.main()
