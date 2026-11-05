"""Exercise warm caches, per-buffer ownership, partial copies and PMG accents."""
from pathlib import Path
import unittest

import test_sequence as sequence
from build_sequence import dance_group_pixels
from gym_practice import practice_shot

if sequence.MPU is not None:
    from scene_memory import RuntimeMemory

    class TrackedMemory(RuntimeMemory):
        def __init__(self, data):
            super().__init__(data)
            self.writes = []

        def __setitem__(self, address, value):
            if isinstance(address, int):
                self.writes.append(address)
            super().__setitem__(address, value)


@unittest.skipIf(sequence.MPU is None, 'install requirements-dev.txt')
class CacheTests(unittest.TestCase):
    def cpu(self):
        return sequence.MPU(memory=TrackedMemory((sequence.ROOT / 'build/visual-prototype-v051.xex').read_bytes()))

    def step(self, cpu, tick):
        cpu.memory.writes.clear()
        before = cpu.processorCycles
        sequence.execute(tick, cpu)
        return cpu.processorCycles - before

    def pixels(self, cpu, effects=False):
        return sequence.SequenceTests().raster(cpu, effects=effects)

    def copied(self, cpu):
        return sum(0x9000 <= a < 0xaf00 or 0xb000 <= a < 0xcf00 for a in cpu.memory.writes)

    def test_static_picture_skips_framebuffer_and_display_list_writes(self):
        for tick in (1592, 4496, 6000, 6500, 8000):
            cpu = self.cpu()
            self.step(cpu, tick)
            pixels = self.pixels(cpu)
            cycles = self.step(cpu, tick + 4)
            self.assertLess(cycles, 2000)
            self.assertEqual(self.copied(cpu), 0)
            self.assertFalse(any(0x8000 <= a < 0x824a or 0x8400 <= a < 0x864a for a in cpu.memory.writes))
            self.assertEqual(self.pixels(cpu), pixels)

    def test_practice_atlas_is_loaded_once_per_buffer(self):
        cpu = self.cpu()
        for tick, copies in ((6000, 7936), (6004, 0), (6981, 7936),
                             (6985, 0), (7978, 0), (7982, 0), (6000, 0)):
            self.step(cpu, tick)
            self.assertEqual(self.copied(cpu), copies, tick)
            self.assertEqual(self.pixels(cpu), practice_shot(tick))

    def test_partial_copy_tracks_each_buffer_and_group(self):
        cpu = self.cpu()
        for tick, copies, count in ((6000, 7936, 0), (9152, 7936, 1),
                                    (9168, 7936, 1), (9184, 5376, 1),
                                    (9200, 5376, 1), (9204, 0, 1),
                                    (9216, 5376, 1), (9792, 7936, 2),
                                    (9808, 7936, 2), (9824, 5376, 2),
                                    (10560, 7936, 3), (10576, 7936, 3),
                                    (10592, 5376, 3)):
            previous_dl = cpu.memory[0xd403] << 8
            old_active = 0x9000 if previous_dl == 0x8400 else 0xb000
            cycles = self.step(cpu, tick)
            self.assertEqual(self.copied(cpu), copies, tick)
            if copies:
                self.assertFalse(any(old_active <= a < old_active + 0x1f00 for a in cpu.memory.writes), tick)
            if copies == 5376:
                self.assertLess(cycles, 75000)
            if count:
                self.assertEqual(self.pixels(cpu), dance_group_pixels((tick >> 4) & 3, count))

    def test_nonsequential_poses_still_reconstruct_the_whole_frame(self):
        cpu = self.cpu()
        for count, start in ((1, 9152), (2, 9792), (3, 10560)):
            expected = [dance_group_pixels(frame, count) for frame in range(4)]
            for frame in (0, 2, 1, 3, 2, 0, 3, 1, 0):
                self.step(cpu, start + frame * 16)
                self.assertEqual(self.pixels(cpu), expected[frame])

    def test_players_and_missiles_pulse_only_on_dance_beats(self):
        cpu = self.cpu()
        for tick in (9163, 9171, 9179):
            self.step(cpu, tick)
            self.assertEqual(cpu.memory[0xd01d], 3)
            self.assertEqual(cpu.memory[0xd400], 0x2e)
            raw, decorated = self.pixels(cpu), self.pixels(cpu, effects=True)
            self.assertNotEqual(raw, decorated)
            self.assertEqual(raw[30 * 160:], decorated[30 * 160:])
            # Missile streaks exist beside the star players, not in bitmap RAM.
            self.assertTrue(any(raw[y*160+29] != decorated[y*160+29] for y in range(30)))
        self.step(cpu, 9187)
        self.assertEqual(cpu.memory[0xd01d], 0)
        self.step(cpu, 11968)
        self.assertEqual(cpu.memory[0xd400], 0x2e)
        self.assertEqual(cpu.memory[0xd01d], 3)
        self.step(cpu, 12288)
        self.assertEqual(cpu.memory[0xd01d], 3)
