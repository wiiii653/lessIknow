"""Exercise warm caches, per-buffer ownership, partial copies and PMG accents."""
from artifact import XEX, METADATA
from pathlib import Path
import unittest

import test_sequence as sequence
from build_sequence import dance_group_pixels
from gym_practice import practice_shot
from mosaic import KALEIDO_START

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
        return sequence.MPU(memory=TrackedMemory(XEX.read_bytes()))

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
        for tick in (4496, 6000, 6500, 8000):
            cpu = self.cpu()
            self.step(cpu, tick)
            pixels = self.pixels(cpu)
            # A mode change initializes both alternating display lists once.
            self.step(cpu, tick + 4)
            cycles = self.step(cpu, tick + 8)
            # The practice overlay prepares PMG even when the bitmap holds.
            self.assertLess(cycles, 8000 if tick>=6000 else 2000)
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

    def test_side_pose_copies_only_its_compact_frame(self):
        from ribbon_dance import scene_artwork
        cpu=self.cpu()
        for tick, copies in ((9216,3512),(9232,3512),(9248,3512),
                             (9264,3512),(9268,0),(9280,3512),(9856,3512)):
            active=0x9000 if cpu.memory[0xd403]==0x84 else 0xb000
            self.step(cpu,tick)
            self.assertEqual(self.copied(cpu),copies)
            self.assertFalse(any(active<=a<active+2560 for a in cpu.memory.writes))
            art,_=scene_artwork(tick)
            self.assertEqual(self.pixels(cpu),bytes(art[y//3*160+x] for y in range(192) for x in range(160)))

    def test_nonsequential_side_phases_reconstruct_the_whole_frame(self):
        from ribbon_dance import scene_artwork
        cpu=self.cpu()
        for frame in (0,12,1,3,15,8,3,1,0):
            tick=9216+frame*16;self.step(cpu,tick)
            art,_=scene_artwork(tick)
            self.assertEqual(self.pixels(cpu),bytes(art[y//3*160+x] for y in range(192) for x in range(160)))

    def test_side_ribbons_keep_animating_on_a_held_pose(self):
        cpu=self.cpu();self.step(cpu,9216)
        raw=self.pixels(cpu);decorated=self.pixels(cpu,True)
        self.step(cpu,9224)
        self.assertEqual(self.pixels(cpu),raw)
        self.assertEqual(self.copied(cpu),0)
        self.assertNotEqual(self.pixels(cpu,True),decorated)
        self.assertEqual(cpu.memory[0xd01d],3)

    def test_reclaimed_trevor_slots_hold_only_allocated_scene_data(self):
        from school_portrait_bank import bank_value
        from ribbon_inbetweens import payloads
        from title_plasma import mask_pages
        title_pages, _ = mask_pages()
        cpu=self.cpu();m=cpu.memory
        for index in range(24,40):
            m[0xd301]=m[bank_value(index)]
            if index<32:
                self.assertEqual(bytes(m[0x5200:0x5400]),bytes(512))
            elif index<39:
                streams=sorted((source,data) for bank,source,data in payloads() if bank==index)
                end=0x4a00
                for source,data in streams:
                    self.assertEqual(source,end)
                    self.assertEqual(bytes(m[source:source+len(data)]),data)
                    end=source+len(data)
                expected = bytearray(0x5400 - end)
                for data, (bank, page) in title_pages.items():
                    if bank == index:
                        offset = (page << 8) - end
                        self.assertGreaterEqual(offset, 0)
                        expected[offset:offset+256] = data
                self.assertEqual(bytes(m[end:0x5400]), expected)
            else:
                from final_boy import packed
                self.assertEqual(bytes(m[0x4a00:0x5400]),packed())
