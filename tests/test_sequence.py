"""Execute scene callback with py65 to verify clocks and live LMS addresses."""

import json
from pathlib import Path
import sys
import unittest

try:
    from py65.devices.mpu6502 import MPU
except ImportError:
    MPU = None

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from extract_music import segments
from build_sequence import (dance_pixels, dance_group_pixels, DANCE_TICK,
                            DANCE_SECOND_TICK, DANCE_THIRD_TICK)
from music_timing import tick_at_bar
KALEIDO_TICK = tick_at_bar(32)
from pmg_preview import player_masks
if MPU is not None:
    from scene_memory import video_memory, RuntimeMemory
from school_story import story_frames, SCHOOL_PHASES, GIRL_PLACEMENTS, NORTH, NORTH_ORIGIN, NORTH_ADVANCE
from os_ram import image, loader, RUN
from gym_practice import PRACTICE_TICK, PRACTICE_SCENE, practice_pixels, BALL_PATH, practice_shot, PRACTICE_CUTS


def execute(tick, cpu=None):
    if cpu is None:
        cpu = MPU(memory=RuntimeMemory((ROOT / 'build/visual-prototype-v053.xex').read_bytes()))
    cpu.memory[0x23cd] = 0x60  # UI callback isolated from the scene routine
    cpu.memory[0xd40b] = 124  # VCOUNT already in vertical blank
    for byte in range(3):
        cpu.memory[0x24a7 + byte] = (tick >> (8 * byte)) & 255
    cpu.sp = 0xfd
    cpu.memory[0x1fe:0x200] = [0xfe, 0x7f]
    cpu.pc = json.loads((ROOT / 'build/visual-prototype-v053.json').read_text())['callback']
    for _ in range(100000):
        if cpu.pc == 0x7fff:
            return cpu
        cpu.step()
    raise AssertionError(f'callback did not return: PC=${cpu.pc:04X}')


@unittest.skipIf(MPU is None, 'install requirements-dev.txt for 6502 scene tests')
class SequenceTests(unittest.TestCase):
    def raster(self, cpu, effects=False):
        display = cpu.memory[0xd402] | cpu.memory[0xd403] << 8
        pixels = bytearray()
        for row in range(192):
            operand = display + 3 + row * 3
            address = cpu.memory[operand] | cpu.memory[operand + 1] << 8
            for byte in cpu.memory[address:address + 40]:
                pixels.extend((byte >> shift) & 3 for shift in (6, 4, 2, 0))
        return player_masks(pixels, cpu.memory, 192) if effects else pixels

    def test_school_encounter_pixels_and_readable_north(self):
        frames = story_frames()
        for tick, scene in SCHOOL_PHASES[:-1]:
            if scene == 14:
                continue
            cpu = execute(tick)
            self.assertEqual(cpu.memory[0x83e0], scene)
            pixels = self.raster(cpu)
            self.assertEqual(pixels, frames[scene - 7])
            if scene == 9:  # lettering is fully legible in the foreground
                left, top, width, height = GIRL_PLACEMENTS[0]
                for index, letter in enumerate('NORTH'):
                    for y, row in enumerate(NORTH[letter]):
                        for x, bit in enumerate(row):
                            at = (top + (NORTH_ORIGIN[1] + y) * height // 64) * 3 * 160 + left + (NORTH_ORIGIN[0] + index * NORTH_ADVANCE + x) * width // 48
                            self.assertEqual(pixels[at], 3 if bit == '1' else 2)

    def test_first_girl_view_crops_at_waist(self):
        left, top, width, height = GIRL_PLACEMENTS[0]
        self.assertEqual((64 - top) * 64 // height, 32)
        self.assertGreater(height + top, 64)
        rgba = (ROOT / 'build/north-girl.rgba').read_bytes()
        for y in range(15, 19):
            for x in range(14, 33):
                offset = (y * 48 + x) * 4
                self.assertGreaterEqual(rgba[offset + 3], 160)
        # Every backing pixel was already teal jacket or its original lettering.
        from school_story import color
        for y in range(15, 19):
            for x in range(14, 33):
                offset = (y * 48 + x) * 4
                self.assertIn(color(rgba[offset:offset + 3]), (2, 3))

    def test_girl_stays_left_of_boy_and_recedes_to_school(self):
        frames = story_frames()
        last_area = float('inf')
        last_distance = float('inf')
        for index, (left, top, width, height) in enumerate(GIRL_PLACEMENTS):
            self.assertGreaterEqual(left, 0)
            self.assertLessEqual(left + width, 104)
            self.assertLess(width * height, last_area)
            last_area = width * height
            distance = (left + width / 2 - 66) ** 2 + (top + height - 46) ** 2
            self.assertLess(distance, last_distance)
            last_distance = distance
            cpu = execute(next(t for t,s in SCHOOL_PHASES if s==index+9))
            pixels = self.raster(cpu)
            portrait = frames[1 if index == 0 else 0]
            for y in range(192):
                self.assertEqual(pixels[y * 160 + 104:(y + 1) * 160],
                                 portrait[y * 160 + 104:(y + 1) * 160])

    def test_rom_asset_loader_and_rom_off_startup(self):
        bank_values = bytes(range(0x81, 0x9d, 2))
        from build_visual_prototype import xex_segment
        sample = image([(0xc000, b'ASSET'), (0xd800, b'TABLE')])
        memory = video_memory(b'\xff\xff' + xex_segment(0x26fc, bank_values) + loader(sample))
        self.assertEqual(bytes(memory[0xc000:0xc005]), b'ASSET')
        self.assertEqual(bytes(memory[0xd800:0xd805]), b'TABLE')
        self.assertEqual(bytes(memory[0xfffa:0xfffc]), b'\x10\x22')
        self.assertEqual(bytes(memory[0x26fc:0x270a]), bytes(v & 0xfe for v in bank_values))
        self.assertEqual(memory[0xd301], 0xff)  # OS restored before INIT returns
        cpu = MPU(memory=RuntimeMemory((ROOT / 'build/visual-prototype-v053.xex').read_bytes()))
        cpu.pc = RUN
        for _ in range(20):
            if cpu.pc == 0x2146:
                break
            cpu.step()
        self.assertEqual(cpu.pc, 0x2146)
        self.assertEqual(cpu.memory[0xd301] & 1, 0)
        self.assertEqual(cpu.memory[0xd40e], 0)

    def test_dancer_retains_every_source_pixel_in_all_four_poses(self):
        for frame in range(4):
            # These ticks select poses 0–3 after the entrance has completed.
            cpu = execute(9152 + frame * 16)
            actual = self.raster(cpu)
            source = dance_pixels(frame)
            for index, pixel in enumerate(source):
                if pixel:
                    self.assertEqual(actual[index], pixel, f'pose {frame}, pixel {index}')

    def test_gym_stays_visible_for_solo_duo_and_trio(self):
        from gym_background import gym_pixels
        gym = gym_pixels()
        for tick in (9152, 9808, 10560):
            pixels = self.raster(execute(tick))
            frame = execute(tick).memory[0x83e0] - 2
            count = 1 if tick < DANCE_SECOND_TICK else 2 if tick < DANCE_THIRD_TICK else 3
            self.assertEqual(pixels, dance_group_pixels(frame, count))
            self.assertEqual(pixels[:24 * 160], gym[:24 * 160])
            self.assertEqual(pixels[156 * 160:], gym[156 * 160:])
        self.assertEqual(gym[42 * 160 + 75], 3)
        self.assertEqual(gym[54 * 160 + 80], 1)
        self.assertEqual(gym[36 * 160 + 24], 2)
        self.assertEqual(gym[160 * 160 + 12], 3)

    def test_dancers_join_progressively_without_losing_detail(self):
        for tick, count in ((DANCE_SECOND_TICK-1, 1), (DANCE_SECOND_TICK, 2),
                            (DANCE_THIRD_TICK-1, 2), (DANCE_THIRD_TICK, 3),
                            (KALEIDO_TICK-1, 3)):
            cpu = execute(tick)
            frame = cpu.memory[0x83e0] - 2
            self.assertEqual(self.raster(cpu), dance_group_pixels(frame, count))
        for count, start in ((1, 9152), (2, 9792), (3, 10560)):
            for frame in range(4):
                cpu = execute(start + frame * 16)
                self.assertEqual(cpu.memory[0x83e0], 2 + frame)
                self.assertEqual(self.raster(cpu), dance_group_pixels(frame, count))

    def test_banked_frame_copy_survives_music_interrupts(self):
        info = json.loads((ROOT / 'build/visual-prototype-v053.json').read_text())
        # Interrupt each dance bank and the practice bank's shared music tail.
        for pose in (0, 2, 4, 6, 8, 10, 12, 13, 14):
            count, frame = pose // 4 + 1, pose % 4
            tick = (11968 if pose == 13 else 34288) if pose > 12 else PRACTICE_TICK if pose == 12 else (9152, 9792, 10560)[count - 1] + frame * 16
            cpu = MPU(memory=RuntimeMemory((ROOT / 'build/visual-prototype-v053.xex').read_bytes()))
            m = cpu.memory
            m[0xd40b] = 124
            m[0xd301] = m.values[3]
            # Initialize the real original music decoder as RUN does.
            for address in (0x232d, 0x237d):
                cpu.pc, cpu.sp = address, 0xfd
                m[0x1fe:0x200] = [0xfe, 0x7f]
                for _ in range(10000):
                    if cpu.pc == 0x7fff:
                        break
                    cpu.step()
                else:
                    self.fail('music initialization did not return')
            for byte in range(3):
                m[0x24a7 + byte] = tick >> (8 * byte) & 255
            cpu.pc, cpu.sp = info['callback'], 0xfd
            m[0x1fe:0x200] = [0xfe, 0x7f]
            next_interrupt, interruptions = 4000, 0
            for _ in range(50000):
                if cpu.pc == 0x7fff:
                    break
                if cpu.processorCycles >= next_interrupt:
                    saved_bank, saved_pc = m[0xd301], cpu.pc
                    cpu.nmi()
                    for _ in range(10000):
                        cpu.step()
                        if cpu.pc == saved_pc:
                            break
                    else:
                        self.fail('music NMI did not return')
                    self.assertEqual(m[0xd301], saved_bank)
                    interruptions += 1
                    next_interrupt = cpu.processorCycles + 8880
                cpu.step()
            else:
                self.fail('interrupted frame copy did not finish')
            self.assertGreater(interruptions, 5)
            expected = self.raster(execute(tick)) if pose >= 12 else dance_group_pixels(frame, count)
            self.assertEqual(self.raster(cpu), expected)

    def test_practice_replaces_departure_and_ends_at_original_dance_tick(self):
        self.assertEqual(PRACTICE_TICK, 5984)
        self.assertEqual(execute(PRACTICE_TICK - 1).memory[0x83e0], 12)
        for tick in (PRACTICE_TICK, 6016, 6144, 6400, 7000, DANCE_TICK-1):
            cpu = execute(tick)
            self.assertEqual(cpu.memory[0x83e0], PRACTICE_SCENE)
            self.assertEqual(cpu.memory[0x83e1], 0)
            self.assertEqual(cpu.memory[0xd01d], 3 if 6981<=tick<7978 else 0)
            self.assertEqual(cpu.memory[0xd400], 0x2e if 6981<=tick<7978 else 0x22)
            # The underlying bitmap contains both boys and both girls by bars.
            memory = cpu.memory
            display = memory[0xd402] | memory[0xd403] << 8
            raw = bytearray()
            for y in range(192):
                operand = display + 3 + y * 3
                address = memory[operand] | memory[operand + 1] << 8
                for byte in memory[address:address + 40]:
                    raw.extend((byte >> shift) & 3 for shift in (6, 4, 2, 0))
            self.assertEqual(raw, practice_shot(tick))
            self.assertEqual(self.raster(cpu), raw)
        for tick in (6980, 6981, 7977, 7978):
            self.assertEqual(self.raster(execute(tick)), practice_shot(tick))
        cpu = execute(DANCE_TICK, execute(DANCE_TICK-1))
        self.assertEqual(cpu.memory[0x83e0], 3)
        self.assertEqual(cpu.memory[0x83e1], 192)
        self.assertEqual(cpu.memory[0xd01d], 0)
        info = json.loads((ROOT / 'build/visual-prototype-v053.json').read_text())
        self.assertEqual(info['dance_tick'], DANCE_TICK)
        self.assertEqual(info['dance_second_tick'], DANCE_SECOND_TICK)
        self.assertEqual(info['dance_third_tick'], DANCE_THIRD_TICK)

    def test_player_dma_enabled_for_both_mosaic_motifs(self):
        cpu = execute(KALEIDO_TICK-1)
        self.assertEqual(cpu.memory[0xd01d], 0)
        cpu = execute(KALEIDO_TICK, cpu)
        self.assertEqual(cpu.memory[0xd01d], 3)
        self.assertEqual(cpu.memory[0xd400], 0x2e)
        cpu = execute(12288, cpu)
        self.assertEqual(cpu.memory[0xd01d], 3)

    def test_intro_timing_and_matching_entrances(self):
        info = json.loads((ROOT / 'build/visual-prototype-v053.json').read_text())
        self.assertEqual(info['school_tick'], 2 * info['title_tick'])
        for elapsed in (0, 4, 24, 48, 92, 96):
            artist = execute(elapsed)
            title = execute(info['title_tick'] + elapsed)
            self.assertEqual(artist.memory[0x83e1], title.memory[0x83e1])

    def test_startup_picture_is_blank_before_artist_entrance(self):
        info = json.loads((ROOT / 'build/visual-prototype-v053.json').read_text())
        cpu = MPU(memory=RuntimeMemory((ROOT / 'build/visual-prototype-v053.xex').read_bytes()))
        for display in info['display_lists']:
            for row in range(192):
                operand = display + 3 + row * 3
                address = cpu.memory[operand] | cpu.memory[operand + 1] << 8
                self.assertEqual(address, info['blank_row'])

    def test_scene_boundaries(self):
        for tick, frame, shift in ((0, 0, 192), (48, 0, 96), (96, 0, 0), (1495, 0, 0), (1496, 1, 192),
                                   (1544, 1, 96), (1592, 1, 0), (2991, 1, 0),
                                   (2992, 8, 0), (4487, 8, 0), (4488, 9, 0),
                                   (4862, 10, 0), (5236, 11, 0), (5610, 12, 0),
                                   (5984, 13, 0), (DANCE_TICK-1, 13, 0),
                                   (DANCE_TICK, 3, 192), (DANCE_TICK+48, 2, 96), (DANCE_TICK+96, 5, 0),
                                   (KALEIDO_TICK-1, 5, 0), (KALEIDO_TICK, 6, 0),
                                   (65536, 6, 0), (0xffffff, 6, 0)):
            with self.subTest(tick=tick):
                cpu = execute(tick)
                self.assertEqual(cpu.memory[0x83e0], frame)
                self.assertEqual(cpu.memory[0x83e1], shift)

    def test_live_scanlines_and_budget(self):
        info = json.loads((ROOT / 'build/visual-prototype-v053.json').read_text())
        blank = info['blank_row']
        for tick in (0, 48, 96, 1496, 1544, 1592, 2992, 4488, 4862, 5236, 5610, 5984,
                     DANCE_TICK-1, DANCE_TICK, DANCE_TICK+48, DANCE_TICK+96,
                     KALEIDO_TICK, KALEIDO_TICK+32, 65536):
            cpu = execute(tick)
            frame, shift = cpu.memory[0x83e0], cpu.memory[0x83e1]
            display = cpu.memory[0xd402] | cpu.memory[0xd403] << 8
            self.assertEqual(display, 0x8400)
            for row in range(192):
                operand = display + 3 + row * 3
                actual = cpu.memory[operand] | cpu.memory[operand + 1] << 8
                source = row - shift
                if frame == PRACTICE_SCENE:
                    source = source // 3 + 64 * sum(tick >= cut for cut in PRACTICE_CUTS[1:])
                lookup = 2 if 2 <= frame < 6 or frame == PRACTICE_SCENE else frame
                expected = blank if source < 0 else info['row_addresses'][lookup][source]
                if frame == 6:
                    expected = 0x9000 + row//2*40
                self.assertEqual(actual, expected, (tick, row))
                self.assertEqual(actual // 4096, (actual + 39) // 4096)
            self.assertLess(cpu.processorCycles, 110000 if 2 <= frame <= 6 or frame == PRACTICE_SCENE else 21000)

    def test_inactive_buffer_is_updated_then_swapped(self):
        cpu = execute(0)
        for tick, expected in ((1496, 0x8000), (1592, 0x8400), (2992, 0x8000),
                               (DANCE_TICK+96, 0x8400), (KALEIDO_TICK, 0x8000)):
            active = cpu.memory[0xd402] | cpu.memory[0xd403] << 8
            previous = cpu.memory[active:active + 586]
            cpu = execute(tick, cpu)
            self.assertEqual(cpu.memory[active:active + 586], previous)
            self.assertEqual(cpu.memory[0xd402] | cpu.memory[0xd403] << 8, expected)

    def test_all_dance_frames_selected(self):
        self.assertEqual({execute(t).memory[0x83e0] for t in range(9104, 9168)},
                         {2, 3, 4, 5})


if __name__ == '__main__':
    unittest.main()
