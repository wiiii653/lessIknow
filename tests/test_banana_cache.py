"""The raw banana banks and title resources remain available on replay."""
import unittest

import test_sequence as seq
import banana_variants as variants
from test_banana_variants import banana_raster, live_banana_frames
from test_engine_cache import TrackedMemory


class BananaCacheTests(unittest.TestCase):
    def test_all_raw_frames_fit_in_existing_physical_banks(self):
        memory = seq.RuntimeMemory(seq.XEX.read_bytes())
        self.assertEqual(len(memory.banks), 64)
        for peeled, first_bank in ((False, 3), (True, 41)):
            for frame in range(32):
                bank = memory.banks[14 + first_bank + frame // 4]
                offset = (frame % 4) * 3840
                self.assertEqual(bank[offset:offset + 3840], variants.packed(frame, peeled))

    def test_both_motifs_match_tunnel_playback_cost(self):
        cpu = seq.MPU(memory=TrackedMemory(seq.XEX.read_bytes()))
        for index, (tick, frame, variant) in enumerate(live_banana_frames()):
            before = cpu.processorCycles
            seq.execute(tick, cpu)
            self.assertEqual(seq.SequenceTests().raster(cpu), banana_raster(frame, variant))
            self.assertLess(cpu.processorCycles - before, 60000 if index < 2 else 49000)

    def test_title_can_render_after_the_banana_montage(self):
        def title_frame(cpu):
            memory = cpu.memory
            display = memory[0xd403] << 8
            base = memory[display + 3] | memory[display + 4] << 8
            return bytes(memory[base:base + 2560])

        reference = seq.execute(1664)
        cpu = seq.execute(3072)
        for tick, _, _ in live_banana_frames()[::8]:
            seq.execute(tick, cpu)
        seq.execute(1664, cpu)
        self.assertEqual(title_frame(cpu), title_frame(reference))
        self.assertEqual(cpu.memory[0xd301], 0xff)
