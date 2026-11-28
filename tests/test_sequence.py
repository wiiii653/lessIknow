"""Execute scene callback with py65 to verify clocks and live LMS addresses."""
from artifact import XEX, METADATA

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
from music_timing import tick_at_bar, tick_at_beat
KALEIDO_TICK = tick_at_bar(32)
from pmg_preview import player_masks
if MPU is not None:
    from scene_memory import video_memory, RuntimeMemory
from school_story import story_frames, SCHOOL_PHASES, GIRL_PLACEMENTS
from school_story import JACKET_BADGE, JACKET_BADGE_ORIGIN, JACKET_THREAD_INKS, foreground_girl
from os_ram import image, loader, RUN
from gym_practice import PRACTICE_TICK, PRACTICE_SCENE, practice_pixels, BALL_PATH, practice_shot, PRACTICE_CUTS


def run_callback(cpu, address):
    cpu.sp = 0xfd
    cpu.memory[0x1fe:0x200] = [0xfe, 0x7f]
    cpu.pc = address
    for _ in range(100000):
        if cpu.pc == 0x7fff:
            return cpu
        cpu.step()
    raise AssertionError(f'callback did not return: PC=${cpu.pc:04X}')


def side_ribbon_interrupt(cpu, vcount):
    info = json.loads(METADATA.read_text())
    entry = info.get('side_ribbon_nmi')
    if entry:
        cpu.memory[0xd40b] = vcount
        if cpu.memory[0x83e0] == 14:
            run_callback(cpu, info['ribbon_palette'])
        run_callback(cpu, entry)


def publish_side_ribbons(cpu):
    from side_ribbons import ACTIVE_POSE, BACK, NMI_ENTRY, PENDING_POSE

    memory = cpu.memory
    if not (memory[PENDING_POSE] or memory[ACTIVE_POSE]):
        return
    # Some tests use execute() with a CPU loaded from an archived prototype.
    if memory[NMI_ENTRY:NMI_ENTRY+3] != [0xad, PENDING_POSE & 255, PENDING_POSE >> 8]:
        return
    if not memory[BACK]:
        side_ribbon_interrupt(cpu, 124)
    side_ribbon_interrupt(cpu, 43)
    side_ribbon_interrupt(cpu, 124)
    if memory[PENDING_POSE]:
        side_ribbon_interrupt(cpu, 43)
        side_ribbon_interrupt(cpu, 124)


def execute(tick, cpu=None, *, publish_side=True):
    if cpu is None:
        cpu = MPU(memory=RuntimeMemory(XEX.read_bytes()))
    cpu.memory[0x23cd] = 0x60  # UI callback isolated from the scene routine
    cpu.memory[0xd40b] = 124  # VCOUNT already in vertical blank
    for byte in range(3):
        cpu.memory[0x24a7 + byte] = (tick >> (8 * byte)) & 255
    run_callback(cpu, json.loads(METADATA.read_text())['callback'])
    if publish_side:
        publish_side_ribbons(cpu)
    return cpu


def bitmap_layout(memory,display):
    """Locate the bitmap after optional terminal rows in any saved build."""
    start=1
    lead=0
    while start<4 and memory[display+start]&15==0:
        lead+=((memory[display+start]>>4)&7)+1
        start+=1
    rows=0
    while memory[display+start+rows*3]&15 in (2,4):rows+=1
    return (start+rows*3,max(0,lead+(rows-5)*8)) if rows else (2,0)


@unittest.skipIf(MPU is None, 'install requirements-dev.txt for 6502 scene tests')
class SequenceTests(unittest.TestCase):
    def test_act5_motif_boundaries(self):
        # Act 5 uses banana phases 0–31, spiral phases 32–47 and twelve
        # organic phases 48–59; eye art owns IDs 60–63.
        from post_trevor_director import START, CYCLE_START, cuts
        from outro_text import PREP_START
        for tick in sorted({START-1,START,CYCLE_START-1,CYCLE_START,39379,
                            40126,PREP_START-1,PREP_START,*[t for t,_ in cuts() if t<PREP_START]}):
            cpu=execute(tick)
            if tick==START-1:
                self.assertEqual(cpu.memory[0x83e0],16)
            elif tick<PREP_START:
                self.assertEqual(cpu.memory[0x83e0],6)
                self.assertLess(cpu.memory[0x83ed],64)
            else:
                self.assertEqual(cpu.memory[0x83e0],17)

    def raster(self, cpu, effects=False):
        display = cpu.memory[0xd402] | cpu.memory[0xd403] << 8
        pixels = bytearray()
        bitmap,skipped=bitmap_layout(cpu.memory,display)
        for row in range(192):
            if row<skipped:
                pixels.extend(bytes(160));continue
            operand=display+bitmap+1+(row-skipped)*3
            address = cpu.memory[operand] | cpu.memory[operand + 1] << 8
            for byte in cpu.memory[address:address + 40]:
                pixels.extend((byte >> shift) & 3 for shift in (6, 4, 2, 0))
        return player_masks(pixels, cpu.memory, 192) if effects else pixels

    def test_arena_encounter_pixels_and_readable_atari_logo(self):
        frames = story_frames()
        for tick, scene in SCHOOL_PHASES[:-1]:
            if scene == 14:
                continue
            cpu = execute(tick)
            self.assertEqual(cpu.memory[0x83e0], scene)
            pixels = self.raster(cpu)
            self.assertEqual(pixels, frames[scene - 7])
            if scene == 9:
                left, top = JACKET_BADGE_ORIGIN
                for y, row in enumerate(JACKET_BADGE, top):
                    for x, ink in enumerate(row, left):
                        if ink in JACKET_THREAD_INKS:
                            self.assertEqual(pixels[y * 3 * 160 + x], JACKET_THREAD_INKS[ink])

    def test_first_girl_view_crops_at_waist(self):
        _, top, width, height = GIRL_PLACEMENTS[0]
        self.assertGreater(height + top, 64)
        inks, mask = foreground_girl()
        ending = (63 - top) * width
        self.assertTrue(mask[ending+46])
        self.assertIn(inks[ending+46], (0, 1, 2))
        self.assertTrue(any(mask[110*width:111*width]))

    def test_girl_stays_left_of_boy_and_recedes_to_school(self):
        frames = story_frames()
        last_area = float('inf')
        last_distance = float('inf')
        for index, (left, top, width, height) in enumerate(GIRL_PLACEMENTS):
            self.assertGreaterEqual(left, 0)
            self.assertLessEqual(left + width, 104)
            self.assertLess(width * height, last_area)
            last_area = width * height
            distance = (left + width / 2 - 82) ** 2 + (top + height - 52) ** 2
            self.assertLess(distance, last_distance)
            last_distance = distance
            cpu = execute(next(t for t,s in SCHOOL_PHASES if s==index+9))
            pixels = self.raster(cpu)
            from school_story import boy_poses
            portrait = boy_poses()[2 if index in (1,2) else 1]
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
        from outro_text import FINAL_MARK_FIRST_GLYPH, FINAL_MARK_ROWS, FINAL_MARK_WIDTH, final_mark
        from terminal_opening import (AUDC1, AUDF1, CURSOR, ENTRY, FADE_START, FONT, HOLD_FRAMES,
                                      KEY_TONE, ROW_BYTES, SCREEN, TEXT, TEXT_BYTES, TRANSCRIPT,
                                      TYPE_STEP)

        tiles, glyphs = final_mark(0)
        sampled_frames = {0, FADE_START, HOLD_FRAMES-1}
        key_frames = set()
        for start, line in TRANSCRIPT:
            end = start + TYPE_STEP*len(line)
            sampled_frames.update((start, start+1, start+TYPE_STEP, end, end+16))
            key_frames.update(range(start+TYPE_STEP, end+1, TYPE_STEP))

        class StartupMemory(RuntimeMemory):
            blank_edges = 0
            beam = 124
            dli_pending = False

            def __init__(self, data):
                super().__init__(data)
                self.frames = {}
                self.key_pulses = {}

            def __getitem__(self, address):
                if address == 0xd40b:
                    # Advance to the next sampled edge without spinning a full frame.
                    self.beam = 123 if self.beam == 124 else 124
                    self.blank_edges += self.beam == 124
                    return self.beam
                return super().__getitem__(address)

            def __setitem__(self, address, value):
                frame = self.blank_edges - 1
                if address == AUDC1 and 0 <= frame < HOLD_FRAMES:
                    self.key_pulses.setdefault(frame, []).append(value)
                if address == 0xd400 and value == 0x22:
                    self.dli_pending = True
                    if frame in sampled_frames:
                        glyph_start = FONT + FINAL_MARK_FIRST_GLYPH * 8
                        self.frames[frame] = (
                            bytes(self[SCREEN:TEXT+TEXT_BYTES]),
                            bytes(self[glyph_start:glyph_start+len(glyphs)]),
                            self[0xd016],
                        )
                super().__setitem__(address, value)

        memory = StartupMemory(XEX.read_bytes())
        from dance_banks import FRAME_BASES
        from os_ram import FRAMEBUFFER_SIZE

        back = FRAME_BASES[1]
        end = back + FRAMEBUFFER_SIZE
        memory[back:end] = b'\xa5' * FRAMEBUFFER_SIZE
        guard = bytes(memory[end:end+8])
        cpu = MPU(memory=memory)
        cpu.pc = RUN
        for _ in range(1000*HOLD_FRAMES):
            if cpu.pc == 0x2146:
                break
            if memory.dli_pending:
                memory.dli_pending = False
                cpu.nmi()
            cpu.step()
        self.assertEqual(cpu.pc, 0x2146)
        expected = bytearray(TEXT - SCREEN)
        for row in range(FINAL_MARK_ROWS):
            start = row * 40 + (40 - FINAL_MARK_WIDTH) // 2
            first_tile = row * FINAL_MARK_WIDTH
            expected[start:start+FINAL_MARK_WIDTH] = tiles[first_tile:first_tile+FINAL_MARK_WIDTH]
        first, first_glyphs, _ = memory.frames[0]
        self.assertEqual(first[:len(expected)], expected)
        self.assertEqual(first[len(expected):], b' '*TEXT_BYTES)
        self.assertEqual(first_glyphs, glyphs)
        first_enter = TRANSCRIPT[0][0]
        self.assertEqual(memory.frames[first_enter][1], final_mark(first_enter)[1])
        self.assertNotEqual(memory.frames[first_enter][1], first_glyphs)
        for frame in sampled_frames:
            visible = [line[:(frame-start)//TYPE_STEP].encode()
                       for start,line in TRANSCRIPT if start <= frame]
            if visible and frame & 16 == 0:
                visible[-1] += bytes([CURSOR])
            window = visible[-4:]
            rows = [b'']*(4-len(window)) + window
            self.assertEqual(memory.frames[frame][0][len(expected):],
                             b''.join(row.ljust(ROW_BYTES) for row in rows), frame)
        for frame in range(HOLD_FRAMES):
            self.assertEqual(memory.key_pulses[frame], [KEY_TONE, 0] if frame in key_frames else [0])
        self.assertEqual(memory.frames[HOLD_FRAMES-1][2], 0)
        self.assertEqual(memory.blank_edges, HOLD_FRAMES + 1)
        self.assertFalse(any(memory[FONT:ENTRY+0x400]))
        self.assertFalse(any(memory[back:end]))
        self.assertEqual(bytes(memory[end:end+8]), guard)
        self.assertEqual(cpu.memory[0xd301], 0xfe)
        self.assertEqual(cpu.memory[0xd40e], 0)
        self.assertEqual([cpu.memory[a] for a in (AUDF1, AUDC1)], [0, 0])
        self.assertEqual([cpu.memory[a] for a in (0xd400, 0xd01d, 0xd01a)], [0, 0, 0])

    def test_side_dancer_uses_all_sixteen_composed_frames(self):
        from ribbon_dance import scene_artwork
        cpu=None
        for tick in range(9216,9472,16):
            cpu=execute(tick,cpu)
            pixels,_=scene_artwork(tick)
            expected=bytes(pixels[y//3*160+x] for y in range(192) for x in range(160))
            self.assertEqual(self.raster(cpu),expected,tick)
            self.assertEqual(cpu.memory[0x83e0],14)

    def test_side_gym_scrolls_left_at_two_depth_speeds(self):
        from ribbon_dance import side_gym
        for phase in range(15):
            a,b=side_gym(phase),side_gym(phase+1)
            for y in range(42):
                self.assertEqual(b[y*160:y*160+156],a[y*160+4:(y+1)*160])
            for y in range(42,64):
                self.assertEqual(b[y*160:y*160+158],a[y*160+2:(y+1)*160])
        self.assertEqual(side_gym(0),side_gym(16))

    def test_ribbon_shot_retains_original_interval_boundaries(self):
        from ribbon_dance import frame_at
        for tick in (DANCE_TICK,DANCE_SECOND_TICK,DANCE_THIRD_TICK,KALEIDO_TICK-1):
            cpu=execute(tick)
            self.assertEqual(cpu.memory[0x83e0],14)
            self.assertEqual(cpu.memory[0x83ed],frame_at(tick))
        self.assertEqual(execute(KALEIDO_TICK).memory[0x83e0],6)

    def test_trio_uses_independent_pose_phases(self):
        from build_sequence import DANCE_LEFTS
        for frame in range(4):
            group = dance_group_pixels(frame, 3)
            for dancer, left in enumerate(DANCE_LEFTS):
                source = dance_pixels((frame + (0, 1, 3)[dancer]) & 3)
                for y in range(192):
                    for x in range(48):
                        color = source[y * 160 + 56 + x]
                        if color:
                            self.assertEqual(group[y * 160 + left + x], color)

    def test_banked_frame_copy_survives_music_interrupts(self):
        info = json.loads(METADATA.read_text())
        # Interrupt each dance bank and the practice bank's shared music tail.
        for pose in (12, 13, 14):
            count, frame = pose // 4 + 1, pose % 4
            tick = (11968 if pose == 13 else 34288) if pose > 12 else PRACTICE_TICK if pose == 12 else (9216, 9856, 10624)[count - 1] + frame * 16
            cpu = MPU(memory=RuntimeMemory(XEX.read_bytes()))
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

    def test_practice_replaces_departure_and_hands_off_to_dance_preparation(self):
        from ribbon_dance import SIDE_PREP_START
        self.assertEqual(PRACTICE_TICK, 5984)
        self.assertEqual(execute(PRACTICE_TICK - 1).memory[0x83e0], 12)
        for tick in (PRACTICE_TICK, 6016, 6144, 6400, 7000, SIDE_PREP_START-1):
            cpu = execute(tick)
            self.assertEqual(cpu.memory[0x83e0], PRACTICE_SCENE)
            self.assertEqual(cpu.memory[0x83e1], 0)
            self.assertEqual(cpu.memory[0xd01d], 3)
            self.assertEqual(cpu.memory[0xd400], 0x2e)
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
        cpu = execute(SIDE_PREP_START, execute(SIDE_PREP_START-1))
        self.assertEqual(cpu.memory[0x83e0], 14)
        self.assertEqual(cpu.memory[0x83e1], 0)
        self.assertEqual(cpu.memory[0xd01d], 3)
        info = json.loads(METADATA.read_text())
        self.assertEqual(info['dance_tick'], DANCE_TICK)
        self.assertEqual(info['dance_second_tick'], DANCE_SECOND_TICK)
        self.assertEqual(info['dance_third_tick'], DANCE_THIRD_TICK)

    def test_player_dma_enabled_for_both_mosaic_motifs(self):
        cpu = execute(KALEIDO_TICK-1)
        self.assertEqual(cpu.memory[0xd01d], 3)
        cpu = execute(KALEIDO_TICK, cpu)
        self.assertEqual(cpu.memory[0xd01d], 3)
        self.assertEqual(cpu.memory[0xd400], 0x2e)
        cpu = execute(12288, cpu)
        self.assertEqual(cpu.memory[0xd01d], 3)

    def test_intro_timing_and_matching_entrances(self):
        info = json.loads(METADATA.read_text())
        self.assertEqual(info['school_tick'], 2 * info['title_tick'])
        for elapsed in (0, 4, 24, 48, 92, 96):
            artist = execute(elapsed)
            title = execute(info['title_tick'] + elapsed)
            self.assertEqual(artist.memory[0x83e1], title.memory[0x83e1])

    def test_gtia11_intro_and_mode_restoration_keep_music_dlis(self):
        cpu = None
        for tick in (96, 1592, 2992, 2996, KALEIDO_TICK,
                     96, 2992, 2996, 20942, 96, 2992, 2996, 14959):
            cpu = execute(tick, cpu)
            m = cpu.memory
            display = m[0xd402] | m[0xd403] << 8
            opcodes = [m[display + 2 + row * 3] for row in range(192)]
            self.assertEqual({op & 15 for op in opcodes}, {15 if tick < 2992 else 14})
            self.assertEqual([i for i, op in enumerate(opcodes) if op & 0x80], [69, 147])
            if tick < 2992:
                self.assertEqual(m[0xd01b] & 0xc0, 0xc0)
                self.assertEqual(m[0xd01d], 3)
                colors = set()
                for row in range(192):
                    operand=display+3+row*3
                    address = m[operand] | m[operand + 1] << 8
                    for byte in m[address:address+40]:
                        colors.add(byte >> 4)
                        colors.add(byte & 15)
                if tick == 96:
                    self.assertIn(0, colors)
                self.assertGreaterEqual(len(colors), 6)
            else:
                self.assertEqual(m[0xd01b] & 0xc0, 0)

    def test_plasma_dither_mixes_adjacent_hues_and_preserves_text_bit(self):
        from collections import Counter
        from title_plasma import dither_hue
        # A field exactly at a hue boundary splits a full Bayer cell evenly.
        value = 3 * 5.1 / 6 - 2.55
        cell = [dither_hue(value, x, y) for y in range(4) for x in range(4)]
        self.assertEqual(Counter(cell), {4: 8, 5: 8})
        self.assertEqual([dither_hue(value, x + 4, y + 4)
                          for y in range(4) for x in range(4)], cell)
        for value in (-100, -2.55, -.425, 0, 2.55, 100):
            for y in range(4):
                for x in range(4):
                    hue = dither_hue(value, x, y)
                    self.assertGreaterEqual(hue, 2)
                    self.assertLessEqual(hue, 7)
                    self.assertFalse(hue & 8)

    def test_title_letter_masks_are_multicolored_and_evolve_by_word(self):
        from title_plasma import artwork, FRAME_BYTES, TITLE_GLYPHS
        self.assertNotEqual(TITLE_GLYPHS['T'], TITLE_GLYPHS['I'])
        self.assertNotEqual(TITLE_GLYPHS['N'], TITLE_GLYPHS['M'])
        bank = artwork()[4]
        first, second = bank[:FRAME_BYTES], bank[FRAME_BYTES:2*FRAME_BYTES]
        values = [nibble for byte in second for nibble in (byte >> 4, byte & 15)]
        colors = {n for n in values if n}
        self.assertGreaterEqual(len(colors), 4)
        self.assertTrue(all(n == 1 or n & 8 for n in colors))
        self.assertGreater(sum(n != 0 for n in second), sum(n != 0 for n in first))
        partial = artwork()[7][4*FRAME_BYTES:5*FRAME_BYTES]
        populated = lambda b: sum((v >> 4 != 0) + ((v & 15) != 0) for v in b)
        self.assertGreater(populated(partial), 0)
        self.assertLess(populated(partial), populated(first))

    def test_solid_letter_inks_remain_readable_over_every_plasma_hue(self):
        from title_plasma import compose_byte, LETTER_HUES
        for code in range(8,16):
            for bg in range(2,8):
                self.assertEqual(compose_byte(bg*17, code*17),LETTER_HUES[code&7]*17)
                self.assertEqual(compose_byte(bg*17, code<<4),LETTER_HUES[code&7]*16+bg)
        from title_plasma import artwork, FRAME_BYTES
        mask=artwork()[4][FRAME_BYTES:2*FRAME_BYTES]
        rows=[y for y in range(64) if any(mask[y*40:(y+1)*40])]
        # Two large, separate words, rather than the old small single line.
        self.assertGreaterEqual(len(rows),28)
        self.assertTrue(any(y<30 for y in rows))
        self.assertTrue(any(y>=16 for y in rows))
        self.assertTrue(all(y<32 for y in rows))

    def test_intro_letter_colors_follow_beat_with_live_cache(self):
        from title_plasma import artwork, FRAME_BYTES, compose_byte
        banks = artwork()
        cpu = None
        # Same plasma phase on either side of these beats: only the letters
        # should change, and the cached frame must be redrawn on the beat.
        for beat in (7, 9, 12, 20, 25):
            tick = tick_at_beat(beat)
            before = execute(tick - 1, cpu)
            old_key = before.memory[0x83fa]
            cpu = execute(tick, before)
            self.assertNotEqual(cpu.memory[0x83fa], old_key)
            self.assertEqual((cpu.memory[0x83fa] >> 1) & 3, beat & 3)

    def test_plasma_composites_hue_only_text_and_spatial_fades(self):
        from title_plasma import (artwork, FRAME_BYTES, PLASMA_STEP_TICKS, TRANSITION_START,
                                  compose_byte, fade_mask, procedural_frame)
        banks = artwork()
        def picture(cpu):
            m = cpu.memory
            display = m[0xd402] | m[0xd403] << 8
            base = m[display + 3] | m[display + 4] << 8
            return bytes(m[base:base + FRAME_BYTES])
        for start, card in ((0, 0), (1496, 1)):
            for elapsed in (32, 64, 96, 128, 160, 192, 256, 512, 768, 1024,
                            1280, 1312, 1344, 1376, 1408, 1440):
                with self.subTest(start=start, elapsed=elapsed):
                    cpu = execute(start + elapsed)
                    phase = elapsed // 32
                    frame = ((start + elapsed) // PLASMA_STEP_TICKS) & 127
                    background = procedural_frame(frame, start + elapsed)
                    tick = start + elapsed
                    stage = max(1, min(elapsed // 256, 3)) if card else min(2, max(0, elapsed // 256 - 1))
                    if TRANSITION_START <= tick < TRANSITION_START + 256:
                        step = (tick - TRANSITION_START) // 32
                        mask = banks[7 + step // 4][step % 4 * FRAME_BYTES:(step % 4 + 1) * FRAME_BYTES]
                    else:
                        reveal = ({(0,1): 0, (0,2): 1, (1,2): 2, (1,3): 3}.get((card, stage))
                                  if elapsed < 1024 and elapsed % 256 < 64 else None)
                        if reveal is not None:
                            bank = banks[7 + reveal // 2]
                            offset = (4 + reveal % 2) * FRAME_BYTES
                            mask = bank[offset:offset + FRAME_BYTES]
                        else:
                            mask = (bytes(FRAME_BYTES) if not stage else
                                    banks[4][(card * 3 + stage - 1) * FRAME_BYTES:(card * 3 + stage) * FRAME_BYTES])
                    beat = max(i for i in range(32) if tick_at_beat(i) <= tick)
                    expected = bytes(compose_byte(a, b, beat & 3) for a, b in zip(background, mask))
                    level = phase if card == 0 and phase < 7 else 46 - phase if card == 1 and phase >= 39 else 7
                    if 1 <= level <= 6:
                        fade = fade_mask(level)
                        expected = bytes(a & b for a, b in zip(expected, fade))
                    self.assertEqual(picture(cpu), expected)
                    self.assertEqual(cpu.memory[0xd301], 0xff)
            self.assertEqual(execute(start).memory[0xd01a] & 15, 0 if card == 0 else 6)
            self.assertEqual(execute(start + 1495).memory[0xd01a] & 15, 6 if card == 0 else 0)
        # Changing the opaque lettering must not reset background pixels
        # outside either silhouette or alter the shared luminance.
        before, after = execute(1495), execute(1496)
        self.assertEqual(before.memory[0xd01a], after.memory[0xd01a])
        old_mask = banks[4][FRAME_BYTES:2*FRAME_BYTES]
        new_mask = banks[7][:FRAME_BYTES]
        first,second=picture(before),picture(after)
        for index,(a,b) in enumerate(zip(old_mask,new_mask)):
            for shift in (4,0):
                if not ((a|b)>>shift)&15:
                    self.assertEqual((first[index]>>shift)&15,(second[index]>>shift)&15)
        cpu = execute(768)
        first = picture(cpu)
        execute(9000, cpu)
        self.assertEqual(picture(execute(768, cpu)), first)
        self.assertNotEqual(picture(execute(800, cpu)), first)

    def test_startup_picture_is_blank_before_artist_entrance(self):
        info = json.loads(METADATA.read_text())
        cpu = MPU(memory=RuntimeMemory(XEX.read_bytes()))
        for display in info['display_lists']:
            for row in range(192):
                operand=display+3+row*3
                address = cpu.memory[operand] | cpu.memory[operand + 1] << 8
                self.assertEqual(address, info['blank_row'])

    def test_scene_boundaries(self):
        from ribbon_dance import SIDE_PREP_START
        from outro_text import PREP_START
        for tick, frame, shift in ((0, 0, 0), (48, 0, 0), (96, 0, 0), (1495, 0, 0), (1496, 1, 0),
                                   (1544, 1, 0), (1592, 1, 0), (2991, 1, 0),
                                   (2992, 8, 0), (4487, 8, 0), (4488, 9, 0),
                                   (4862, 10, 0), (5236, 11, 0), (5610, 12, 0),
                                   (5984, 13, 0), (SIDE_PREP_START-1, 13, 0), (SIDE_PREP_START, 14, 0),
                                   (DANCE_TICK, 14, 0),
                                   (DANCE_TICK+48, 14, 0),
                                   (DANCE_TICK+96, 14, 0),
                                   (KALEIDO_TICK-1, 14, 0), (KALEIDO_TICK, 6, 0),
                                   (PREP_START-1, 6, 0), (PREP_START,17,0),
                                   (51231, 17, 0), (51232,17,0),
                                   (65536, 17, 0), (0xffffff, 17, 0)):
            with self.subTest(tick=tick):
                cpu = execute(tick)
                self.assertEqual(cpu.memory[0x83e0], frame)
                self.assertEqual(cpu.memory[0x83e1], shift)

    def test_live_scanlines_and_budget(self):
        info = json.loads(METADATA.read_text())
        blank = info['blank_row']
        for tick in (0, 48, 96, 1496, 1544, 1592, 2992, 4488, 4862, 5236, 5610, 5984,
                     DANCE_TICK-1, DANCE_TICK, DANCE_TICK+48, DANCE_TICK+96,
                     KALEIDO_TICK, KALEIDO_TICK+32, 65536):
            cpu = execute(tick)
            frame, shift = cpu.memory[0x83e0], cpu.memory[0x83e1]
            display = cpu.memory[0xd402] | cpu.memory[0xd403] << 8
            self.assertEqual(display, 0xbc00 if frame==17 else 0x8400)
            for row in range(192):
                bitmap,skipped=bitmap_layout(cpu.memory,display)
                if row<skipped:continue
                operand=display+bitmap+1+(row-skipped)*3
                actual = cpu.memory[operand] | cpu.memory[operand + 1] << 8
                source = row - shift
                if frame == PRACTICE_SCENE:
                    source = source // 3 + 64 * sum(tick >= cut for cut in PRACTICE_CUTS[1:])
                lookup = 2 if 2 <= frame < 6 or frame == PRACTICE_SCENE else frame
                expected = (0x9000+row//3*40 if frame in (14,17) else
                            blank if source < 0 else info['row_addresses'][lookup][source])
                if frame == 6:
                    expected = 0x9000 + row//2*40
                if frame < 2:
                    self.assertEqual(actual, 0x9000 + (row // 3) * 40)
                else:
                    self.assertEqual(actual, expected, (tick, row))
                self.assertEqual(actual // 4096, (actual + 39) // 4096)
            # Intro includes procedural background, dissolve and offscreen PMG.
            # This is a CPU regression ceiling, not a real-time frame deadline.
            # V187 whistle PMG: the current school path reaches 23,954 CPU
            # cycles; allow <5% headroom, without claiming an ANTIC deadline.
            limit = 110000 if 2 <= frame <= 6 or frame == PRACTICE_SCENE else 170000 if frame < 2 else 210000 if frame==17 else 110000 if frame==14 else 25000 if frame in (10,11) else 21000
            self.assertLess(cpu.processorCycles, limit)

    def test_inactive_buffer_is_updated_then_swapped(self):
        from title_water import BUFFER_PAIRS, FOOTER_OFFSET, TAIL_OFFSET

        cpu = execute(0)
        for tick, expected in ((1496, 0x8000), (1592, 0x8400), (2992, 0x8000),
                               (DANCE_TICK+96, 0x8400), (KALEIDO_TICK, 0x8000)):
            active = cpu.memory[0xd402] | cpu.memory[0xd403] << 8
            previous = cpu.memory[active:active + 586]
            cpu = execute(tick, cpu)
            if tick == 2992:
                water_tail = dict(BUFFER_PAIRS)[active] + TAIL_OFFSET
                self.assertEqual(previous[FOOTER_OFFSET:FOOTER_OFFSET + 3],
                                 [1, water_tail & 255, water_tail >> 8])
                # Title retirement restores the footer during blanking.
                previous[FOOTER_OFFSET:FOOTER_OFFSET + 3] = [0x70] * 3
            self.assertEqual(cpu.memory[active:active + 586], previous)
            self.assertEqual(cpu.memory[0xd402] | cpu.memory[0xd403] << 8, expected)

    def test_all_dance_frames_selected(self):
        self.assertEqual({execute(t).memory[0x83e0] for t in range(9216, 9280, 16)},
                         {14})


if __name__ == '__main__':
    unittest.main()
