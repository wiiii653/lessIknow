"""Compare optimized callbacks against the archived v126 executable."""
import unittest
import random

import test_sequence as sequence
from test_engine_cache import TrackedMemory


@unittest.skipIf(sequence.MPU is None, 'py65 required')
class OptimizationTests(unittest.TestCase):
    def pair(self):
        old = sequence.ROOT / 'build/visual-prototype-v126.xex'
        new = sequence.XEX
        return [sequence.MPU(memory=TrackedMemory(path.read_bytes())) for path in (old, new)]

    def assert_equivalent(self, pair, tick):
        for cpu in pair:
            sequence.execute(tick, cpu)
        for cpu in pair:
            self.assertEqual(cpu.memory[0xd301], 0xff)
        scene = pair[1].memory[0x83e0]
        # V128 intentionally revises dance art/palette and Trevor silhouettes.
        if scene not in (2, 3, 4, 5, 16):
            self.assertEqual(sequence.SequenceTests().raster(pair[0]),
                             sequence.SequenceTests().raster(pair[1]), tick)
        old_gtia = pair[0].memory[0xd000:0xd020]
        new_gtia = pair[1].memory[0xd000:0xd020]
        if scene in (2, 3, 4, 5):
            self.assertEqual(new_gtia[0x16:0x19], [0x5a, 0xac, 0x2e])
            old_gtia[0x16:0x19] = new_gtia[0x16:0x19]
        self.assertEqual(old_gtia, new_gtia, tick)
        self.assertEqual(pair[0].memory[0x0980:0x0c00], pair[1].memory[0x0980:0x0c00], tick)

    def test_scene_handoffs_restarts_and_nonsequential_frames_match_v126(self):
        pair = self.pair()
        ticks = [0, 1496, 2992, 3553, 3681, 4114, 5984, 8975, 9723,
                 10471, 11967, 14959, 16455, 17950, 19446, 20942,
                 22438, 23934, 26925, 32909, 59000, 96, 3553, 59000]
        # Exercise cache ownership with arbitrary scene and animation jumps.
        rng = random.Random(127)
        ticks.extend(rng.randrange(59834) for _ in range(40))
        for tick in ticks:
            self.assert_equivalent(pair, tick)

    def test_palette_division_preserves_beat_edges(self):
        pair = self.pair()
        # Both bases, including clamped negative deltas and the late palette.
        ticks = [11967, 11968, 32909, 32911, 32912, 65535]
        for base, stop in ((11968, 14959), (32912, 59834)):
            for tick in range(base, stop, 187):
                ticks.extend((tick, tick + 23, tick + 24, tick + 186))
        for tick in ticks:
            for cpu in pair:
                sequence.execute(tick, cpu)
            self.assertEqual(pair[0].memory[0xd016:0xd019],
                             pair[1].memory[0xd016:0xd019], tick)

    def test_warm_layouts_skip_lms_writes_and_reduce_update_cycles(self):
        for start in (3553, 12000, 18000, 21000, 27000, 59000):
            pair = self.pair()
            savings = []
            skipped = 0
            for tick in range(start, start + 160, 4):
                costs = []
                for cpu in pair:
                    cpu.memory.writes.clear()
                    before = cpu.processorCycles
                    sequence.execute(tick, cpu)
                    costs.append(cpu.processorCycles - before)
                savings.append(costs[0] - costs[1])
                writes = pair[1].memory.writes
                if any(0x9000 <= a < 0x9f00 or 0xb000 <= a < 0xbf00 for a in writes):
                    if not any(0x8003 <= a < 0x8243 or 0x8403 <= a < 0x8643 for a in writes):
                        skipped += 1
            self.assertGreater(sum(savings), 0, start)
            if start not in (18000, 21000):
                self.assertGreater(skipped, 0, start)
