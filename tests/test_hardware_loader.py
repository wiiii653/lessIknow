"""Protect the physical AVG loading protocol and all reconstructed bank bytes."""
import unittest
from artifact import XEX
from build_hardware_xex import build, REFERENCE, ROOT, LOW_ENDS
from build_hardware_xex import APPROVED_STEREO, with_approved_music
from build_visual_prototype import xex_segment
from extract_music import segments

try:
    from py65.devices.mpu6502 import MPU
except ImportError:
    MPU = None


class HardwareLoaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = XEX.read_bytes()
        cls.result = build(cls.source)
        cls.fast = build(cls.source, fast_clear=True)

    @unittest.skipUnless((ROOT / 'build/visual-prototype-v330.xex').exists(),
                         'archived raw v330 prototype required for round-trip check')
    def test_v330_reproduces_hardware_confirmed_058_byte_for_byte(self):
        self.assertEqual(build((ROOT / 'build/visual-prototype-v330.xex').read_bytes()),
                         REFERENCE.read_bytes())

    @unittest.skipUnless((ROOT / 'build/visual-prototype-v390.xex').exists(),
                         'archived raw v390 prototype required for round-trip check')
    def test_approved_music_reproduces_stereo_133_byte_for_byte(self):
        source = (ROOT / 'build/visual-prototype-v390.xex').read_bytes()
        self.assertEqual(build(with_approved_music(source)), APPROVED_STEREO.read_bytes())

    def test_training_mix_preserves_opening_and_hits_ahead_of_dance_cut(self):
        from build_audio_revision import music_packets
        from build_sequence import DANCE_TICK
        from gym_practice import PRACTICE_TICK
        from school_story import WHISTLE_END

        baseline = music_packets(with_approved_music(self.source))
        revised = music_packets(with_approved_music(self.source, earlier_percussion=True))
        self.assertEqual(revised[:WHISTLE_END], baseline[:WHISTLE_END])
        self.assertTrue(any(packet[14] & 15 for packet in revised[WHISTLE_END:PRACTICE_TICK]))
        attack = DANCE_TICK - 2
        self.assertEqual(revised[attack-1][5] & 15, 0)
        self.assertGreater(revised[attack][5] & 15, 0)
        for tick in (attack, DANCE_TICK):
            self.assertEqual((revised[tick][3] & 15, revised[tick][12] & 15), (15, 15))
        self.assertEqual(revised[DANCE_TICK+50:], baseline[DANCE_TICK+50:])

    def staging_images(self, result):
        images = []
        staging = None
        for a, b, p in segments(result):
            if a == 0x3a00:
                if staging is not None:
                    images.append(bytes(staging))
                staging = bytearray(16384)
            elif a == 0x2e2 and p == b'\x00\x39' and staging is not None:
                images.append(bytes(staging))
                staging = None
            elif staging is not None and 0x8000 <= a <= b <= 0xbfff:
                staging[a-0x8000:b-0x8000+1] = p
        return images

    def test_all_64_staging_images_match_raw_prototype(self):
        expected = [p for a, b, p in segments(self.source) if (a, b) == (0x8000, 0xbfff)]
        self.assertEqual(len(expected), 64)
        for result in (self.result, self.fast):
            self.assertEqual(self.staging_images(result), expected)

    def test_each_staging_clear_is_followed_by_bank_data(self):
        entries = list(segments(self.result))
        transfers = [entries[i+2] for i,(start, _, _) in enumerate(entries)
                     if start == 0x3a00]
        self.assertEqual(len(transfers),64)
        for start, end, _ in transfers:
            self.assertTrue(0x8000 <= start <= end <= 0xbfff)

    def test_fast_clear_changes_only_clear_segments(self):
        base = list(segments(self.result))
        fast = list(segments(self.fast))
        self.assertEqual(len(base), len(fast))
        changed = [(a, b) for a, b in zip(base, fast) if a != b]
        self.assertEqual(len(changed), 64)
        self.assertTrue(all(a[0] == b[0] == 0x3a00 for a, b in changed))

    @unittest.skipIf(MPU is None, 'py65 required')
    def test_fast_clear_preserves_state_and_clears_only_staging(self):
        cycles = []
        for result in (self.result, self.fast):
            code = next(p for a, _, p in segments(result) if a == 0x3a00)
            cpu = MPU()
            cpu.memory[0x3a00:0x3a00+len(code)] = code
            for marker in (0x7fff, 0xc000, 0xd301):
                cpu.memory[marker] = 0xa5
            cpu.memory[0x8000:0xc000] = [0xa5] * 16384
            cpu.a, cpu.x, cpu.y, cpu.p, cpu.sp = 0x2e, 0x3a, 0x18, 0xb9, 0xfd
            cpu.memory[0x1fe:0x200] = [0xfe, 0x3f]
            cpu.pc = 0x3a00
            for _ in range(60000):
                if cpu.pc == 0x3fff:
                    break
                cpu.step()
            else:
                self.fail('Staging clear did not return')
            self.assertFalse(any(cpu.memory[0x8000:0xc000]))
            self.assertTrue(all(cpu.memory[marker] == 0xa5 for marker in (0x7fff, 0xc000, 0xd301)))
            self.assertEqual((cpu.a, cpu.x, cpu.y, cpu.p, cpu.sp), (0x2e, 0x3a, 0x18, 0xb9, 0xff))
            cycles.append(cpu.processorCycles)
        self.assertLess(cycles[1], cycles[0] * 0.52)

    def test_unknown_bank_loader_change_is_rejected(self):
        out = bytearray(b'\xff\xff')
        changed = False
        for a, b, p in segments(self.source):
            if a == 0x1000 and not changed:
                p = bytes([p[0] ^ 1]) + p[1:]
                changed = True
            out.extend(xex_segment(a, p))
        with self.assertRaisesRegex(ValueError, 'Unexpected bank loader'):
            build(bytes(out))

    @unittest.skipIf(MPU is None, 'py65 required')
    def test_final_bootstrap_restores_runtime_bytes_and_enters_player_stub(self):
        entries = list(segments(self.result))
        cpu = MPU()
        for a, b, p in entries:
            if a in (0x4000, 0x4800):
                cpu.memory[a:b+1] = p
        cpu.memory[0x400:0xc00] = [0xa5] * 0x800
        cpu.pc = 0x4800
        for _ in range(30000):
            if cpu.pc == 0x13e0:
                break
            cpu.step()
        else:
            self.fail(f'Bootstrap did not enter player stub: ${cpu.pc:04X}')
        raw = list(segments(self.source))
        last = max(i for i, (a, b, p) in enumerate(raw) if a == 0x2e2)
        for a, b, p in raw[last+1:]:
            if a in LOW_ENDS:
                self.assertEqual(bytes(cpu.memory[a:b+1]), p)
        self.assertEqual(cpu.memory[0xd40e], 0)
        self.assertTrue(cpu.p & cpu.INTERRUPT)
