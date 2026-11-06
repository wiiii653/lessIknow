#!/usr/bin/env python3
"""Continuous ANTIC E scenes, shared scanlines, double-buffered display lists."""

import argparse
import json
from pathlib import Path

from build_sequence import Code, text_pixels, dance_pixels, TITLE_TICK, DANCE_TICK, PALETTE, dance_group_pixels, DANCE_SECOND_TICK, DANCE_THIRD_TICK
from music_timing import tick_at_bar
from build_title import ROWS, gtia11_pixels
from title_mode import ENTRY as TITLE_MODE_ENTRY, helper as title_mode_helper
from title_plasma import build as plasma_build, artwork as plasma_artwork, SIZE as PLASMA_SIZE, FIRST_BANK as PLASMA_FIRST_BANK
from engine_effects import copy_helper, effects_helper, pmg_art, COPY_ORIGIN, EFFECT_ORIGIN, RUNTIME_ORIGIN, RUNTIME_END, DL_KEYS, runtime_helper
from dance_banks import FRAME_BASES, frame_address, frame_blob
from gym_practice import practice_pixels, PRACTICE_TICK, PRACTICE_SCENE, BALL_PATH, PRACTICE_CUTS
from build_visual_prototype import xex_segment
from extract_music import segments
from school_story import (story_frames, SCHOOL_PHASES, girl_front_pixels,
                          GIRL_PORTRAIT_SCENE, SCHOOL_PORTRAIT_TICK,
                          SCHOOL_PORTRAIT_END)
from school_portrait_bank import loader as school_bank_loader, BANK_VALUE
from mosaic import banks as mosaic_banks
from school_parallax import banks as school_pan_banks
from trevor_awakens import END as TREVOR_END, HIT as TREVOR_HIT, bank as trevor_bank
from trevor_polished import bank as polished_trevor_bank
from basketball_hero import START as HERO_START, END as HERO_END, ENTRY as HERO_ENTRY, BANK_VALUE as HERO_BANK, bank as hero_bank
from pompom_effects import ENTRY as POM_ENTRY, DATA as POM_DATA, helper as pom_helper
from rainbow_ball import ENTRY as BALL_ENTRY, RESTORE as BALL_RESTORE, helper as ball_helper
from os_ram import loader, image as os_image, run_stub, RUN

from crush_portraits import START as CRUSH_TICK, END as CRUSH_END, ENTRY as CRUSH_ENTRY, DATA as CRUSH_DATA, helper as crush_helper, packed as crush_packed, cleanup as crush_cleanup

KALEIDO_TICK = tick_at_bar(32)  # eight bars / 15 seconds after the dancer enters
SCHOOL_TICK = tick_at_bar(8)  # equal 7.5-second artist and title screens
ORIGIN = 0x1400
POOL_LOW = 0x1b50
TABLE_BASE = 0xd800
STATE = 0x83e0


def packed_rows(pixels):
    return [bytes(sum(pixels[y * 160 + x + dx] << (6 - 2 * dx)
                      for dx in range(4)) for x in range(0, 160, 4))
            for y in range(192)]


def build(output_path=Path('build/visual-prototype-dev.xex'), replace=False):
    if output_path.exists() and not replace:
        raise FileExistsError(f'Preserving existing XEX: {output_path}; choose --output with a new name')
    copy_code, copy_labels = copy_helper()
    effect_code = effects_helper()
    scenes = [bytes(160 * 192), bytes(160 * 192)]  # intro rendered into framebuffers
    # Keep every source scanline, especially the small facial features.
    dance_frames = [frame_blob(packed_rows(dance_group_pixels(frame, count)))
                    for count in (1, 2, 3) for frame in range(4)]
    # The bounded delta copy is valid for ANY pair of poses in a group.
    # Reject future art changes that move changing pixels outside these pages.
    for group in range(3):
        poses = dance_frames[group * 4:group * 4 + 4]
        for offset in list(range(0x400)) + list(range(0x1900, 0x1e10)):
            if len({pose[offset] for pose in poses}) != 1:
                raise ValueError('dance changes outside dirty pages 4–24')
    scenes += [bytes(160 * 192)] * 4
    scenes.append(bytes(160 * 192))  # mozaika: klatki w bankach rozszerzenia
    scenes += story_frames()
    scenes.append(bytes(160 * 192))  # practice uses the same banked framebuffers
    scenes.append(bytes(160 * 192))  # banked school portrait
    girl_frame = bytearray(frame_blob(packed_rows(girl_front_pixels())[::3] + [bytes(40)]*128)+bytes(8192))
    pom_code,pom_data=pom_helper()
    girl_frame[POM_ENTRY-0x4000:POM_ENTRY-0x4000+len(pom_code)]=pom_code
    girl_frame[POM_DATA-0x4000:POM_DATA-0x4000+len(pom_data)]=pom_data
    ball_code=ball_helper()
    girl_frame[BALL_ENTRY-0x4000:BALL_ENTRY-0x4000+len(ball_code)]=ball_code
    ball_restore=crush_cleanup(BALL_RESTORE)
    girl_frame[BALL_RESTORE-0x4000:BALL_RESTORE-0x4000+len(ball_restore)]=ball_restore
    portrait_code = crush_helper([])
    portrait_data = crush_packed()
    practice_frame = frame_blob(packed_rows(practice_pixels()))
    # Compact the vertical mapping without dropping a single image pixel.
    # Dance: full 192-line gym; kaleidoscope: 96 doubled lines; school: 64 tripled.
    sample_rows = [list(range(192)) if frame < 2 else
                   list(range(192)) if frame < 6 else
                   list(range(0, 192, 2)) if frame == 6 else list(range(0, 192, 3))
                   for frame in range(len(scenes))]
    sample_rows[GIRL_PORTRAIT_SCENE] = []
    sample_rows[PRACTICE_SCENE] = []  # runtime resolves the framebuffer tables
    table_end = TABLE_BASE + sum(len(indices) * 2 for indices in sample_rows)
    rows = [packed_rows(scene) for scene in scenes]
    unique = {}
    # Bitmap rows remain contiguous for ANTIC, but adjacent stored rows may
    # share identical suffix/prefix bytes (notably the dancer's black margins).
    # This is lossless and adds no work to the Atari's playback routine.
    regions = ((0x0400, 0x0800), (0x0900, 0x0980), (RUNTIME_END, RUN), (POOL_LOW, 0x2000), (0x3300, 0x3c00), (0x824a, 0x8300),
               (0x8340, 0x83e0), (0x864a, 0x9000),
               (EFFECT_ORIGIN + len(effect_code), 0xb000),
               (COPY_ORIGIN + len(copy_code), 0xd000),
               (table_end + PLASMA_SIZE, TITLE_MODE_ENTRY))
    region = 0
    blobs = [bytearray() for _ in regions]
    # Join rows with the strongest suffix/prefix overlaps first. Chains are
    # lossless and only affect asset placement, never playback or bank use.
    source_rows = sorted(set([bytes(40)] + [row for scene in rows for row in scene]))
    parent = list(range(len(source_rows)))
    next_row, previous_row = {}, {}

    def root(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    for length in range(39, 0, -1):
        starts = {}
        for index, row in enumerate(source_rows):
            if index not in previous_row:
                starts.setdefault(row[:length], []).append(index)
        for index, row in enumerate(source_rows):
            if index in next_row:
                continue
            for candidate in starts.get(row[-length:], ()):
                if candidate not in previous_row and root(index) != root(candidate):
                    next_row[index] = candidate
                    previous_row[candidate] = index
                    parent[root(candidate)] = root(index)
                    break
    ordered_rows = []
    for index in range(len(source_rows)):
        if index in previous_row:
            continue
        while True:
            ordered_rows.append(source_rows[index])
            if index not in next_row:
                break
            index = next_row[index]
    for row in ordered_rows:
        while True:
            start, end = regions[region]
            blob = blobs[region]
            cursor = start + len(blob)
            overlap = None
            for count in range(min(39, len(blob)), -1, -1):
                address = cursor - count
                if count and blob[-count:] != row[:count]:
                    continue
                if address + 40 <= end and address // 0x1000 == (address + 39) // 0x1000:
                    overlap = count
                    break
            if overlap is not None:
                unique[row] = address
                blob.extend(row[overlap:])
                break
            next_page = (cursor + 0xfff) & ~0xfff
            if next_page == cursor:
                next_page += 0x1000
            if next_page + 40 <= end:
                blob.extend(bytes(next_page - cursor))
            else:
                region += 1
                if region == len(regions):
                    raise ValueError(f'shared scanlines exceed unbanked RAM budget: {len(unique)} of {len(ordered_rows)} stored')
    chunks = [(regions[index][0], blob) for index, blob in enumerate(blobs) if blob]
    blank = unique[bytes(40)]
    plasma_code, plasma_labels = plasma_build(table_end, blank)
    effect_code = effects_helper(intro_color=plasma_labels['color'])
    addresses = [[unique[row] for row in scene] for scene in rows]
    for frame in range(2, 6):
        addresses[frame] = [frame_address(FRAME_BASES[frame & 1], y) for y in range(192)]
    tables = bytearray()
    table_pointers = []
    for scene, indices in zip(addresses, sample_rows):
        selected = [scene[index] for index in indices]
        lo = TABLE_BASE + len(tables)
        hi = lo + len(selected)
        table_pointers.append((lo, hi))
        tables.extend(a & 255 for a in selected)
        tables.extend(a >> 8 for a in selected)
    assert TABLE_BASE + len(tables) == table_end

    def display(base):
        result = bytearray((0x80, 0x70))
        for y in range(192):
            address = blank
            result.extend((0x4e | (0x80 if y + 9 in (78, 156) else 0),
                           address & 255, address >> 8))
        result.extend((0x70, 0x70, 0x70, 0x70, 0x90, 0x41, base & 255, base >> 8))
        assert (base & 0x3ff) + len(result) <= 0x400
        return result

    # Memory helpers: scene, shift, tick[3], row, back-buffer high, amplitude.
    SCENE, SHIFT, TICK, ROW, BACK, AMP = STATE, STATE + 1, STATE + 2, STATE + 5, STATE + 6, STATE + 7
    FRAMEID, TARGET = STATE + 15, STATE + 21
    NEWKEY, BUFKEYS = STATE + 23, STATE + 24
    LASTKEY, LASTSHIFT, LASTAMP, NEWAMP = STATE + 26, STATE + 27, STATE + 28, STATE + 29
    c = Code(ORIGIN)

    def absolute(op, address):
        c.emit(op, address & 255, address >> 8)

    def check_cached(tag):
        c.jump(0x20, 'cache_check')
        c.branch(0xd0, tag)
        c.jump(0x4c, 'effect_vblank')
        c.label(tag)

    def compare_tick(threshold, yes, no):
        # Local branch trampolines keep arbitrary scene dispatch within range.
        tag = f'cmp{threshold}'
        absolute(0xad, TICK + 2)
        c.branch(0xf0, tag + '_high')
        c.jump(0x4c, yes)
        c.label(tag + '_high')
        absolute(0xad, TICK + 1)
        c.emit(0xc9, threshold >> 8)
        c.branch(0x90, tag + '_no')
        c.branch(0xd0, tag + '_yes')
        absolute(0xad, TICK)
        c.emit(0xc9, threshold & 255)
        c.branch(0xb0, tag + '_yes')
        c.label(tag + '_no')
        c.jump(0x4c, no)
        c.label(tag + '_yes')
        c.jump(0x4c, yes)

    c.label('snapshot')
    for offset in (2, 1, 0):
        absolute(0xad, 0x24a7 + offset)
        absolute(0x8d, TICK + offset)
    for offset in (1, 2):
        absolute(0xad, 0x24a7 + offset)
        absolute(0xcd, TICK + offset)
        c.branch(0xd0, 'snapshot')
    absolute(0x20, plasma_labels['invalidate'])
    compare_tick(TREVOR_END, 'kaleido', 'before_hero_end')
    c.label('before_hero_end')
    compare_tick(CRUSH_END, 'hero', 'before_crush_end')
    c.label('hero')
    c.emit(0xa9,15)
    absolute(0x8d,SCENE)
    absolute(0xae,HERO_BANK)
    absolute(0xad,0xd301)
    c.emit(0x48)
    absolute(0x8e,0xd301)
    absolute(0x20,HERO_ENTRY)
    c.emit(0x68)
    absolute(0x8d,0xd301)
    c.emit(0x60)
    c.label('before_crush_end')
    compare_tick(CRUSH_TICK, 'crush', 'before_crush')
    c.label('crush')
    c.emit(0xa9, 14)
    absolute(0x8d, SCENE)
    c.emit(0xa9, 0)
    absolute(0x8d, SHIFT)
    absolute(0xad, 0xd301)
    c.emit(0x48)
    absolute(0xad, 0x2703)
    absolute(0x8d, 0xd301)
    absolute(0x20, CRUSH_ENTRY)
    c.emit(0x68)
    absolute(0x8d, 0xd301)
    c.emit(0x60)
    c.label('before_crush')
    compare_tick(KALEIDO_TICK, 'kaleido', 'before_kaleido')
    c.label('before_kaleido')
    compare_tick(DANCE_TICK, 'dance', 'before_dance')
    c.label('before_dance')
    compare_tick(SCHOOL_TICK, 'school', 'before_school')
    c.label('before_school')
    compare_tick(TITLE_TICK, 'title', 'artist')
    c.label('artist')
    c.emit(0xa9, 0)
    c.jump(0x4c, 'selected')
    c.label('title')
    c.emit(0xa9, 1)
    c.jump(0x4c, 'selected')
    c.label('school')
    # Here the tick is already known to be below DANCE_TICK: 16 bits suffice.
    for threshold, frame in reversed(SCHOOL_PHASES[1:]):
        tag=f'school_before_{threshold}'
        yes=f'school_at_{threshold}'
        absolute(0xad,TICK+1)
        c.emit(0xc9,threshold>>8)
        c.branch(0x90,tag)
        c.branch(0xd0,yes)
        absolute(0xad,TICK)
        c.emit(0xc9,threshold&255)
        c.branch(0x90,tag)
        c.label(yes)
        c.emit(0xa9,frame)
        c.jump(0x4c,'selected')
        c.label(tag)
    c.emit(0xa9,SCHOOL_PHASES[0][1])
    c.jump(0x4c,'selected')
    c.label('dance')
    absolute(0xad, TICK)
    c.emit(0x4a, 0x4a, 0x4a, 0x4a, 0x29, 3, 0x18, 0x69, 2)
    c.jump(0x4c, 'selected')
    c.label('kaleido')
    c.emit(0xa9, 6)
    c.label('selected')
    c.emit(0x48)
    absolute(0xad, SCENE)
    c.emit(0xc9,6)
    c.branch(0xd0,'cleanup_regular')
    c.emit(0x68,0x48,0xc9,6)
    c.branch(0xf0,'portrait_cleanup_done')
    c.jump(0x4c,'cleanup_required')
    c.label('cleanup_regular')
    c.emit(0xc9,14)
    c.branch(0x90,'portrait_cleanup_done')
    c.label('cleanup_required')
    absolute(0xad,0xd301)
    c.emit(0x48)
    absolute(0xad,BANK_VALUE)
    absolute(0x8d,0xd301)
    absolute(0x20,BALL_RESTORE)
    c.emit(0x68)
    absolute(0x8d,0xd301)
    c.label('portrait_cleanup_done')
    c.emit(0x68)
    absolute(0x8d, SCENE)
    c.emit(0xc9,6)
    c.branch(0xd0,'not_mosaic')
    c.jump(0x4c,'mosaic')
    c.label('not_mosaic')
    absolute(0xad,SCENE)
    # Artist and title have identical scanline entrance animations.
    c.branch(0xf0, 'artist_delta')
    c.emit(0xc9, 6)
    c.branch(0xb0, 'no_slide')
    c.emit(0xc9, 1)
    c.branch(0xd0, 'dance_delta')
    c.emit(0xa2, TITLE_TICK & 255, 0xa0, TITLE_TICK >> 8)
    c.jump(0x4c, 'delta')
    c.label('artist_delta')
    c.emit(0xa2, 0, 0xa0, 0)
    c.jump(0x4c, 'delta')
    c.label('dance_delta')
    c.emit(0xa2, DANCE_TICK & 255, 0xa0, DANCE_TICK >> 8)
    c.label('delta')
    absolute(0x8e, STATE + 8)
    absolute(0x8c, STATE + 9)
    c.emit(0x38)
    absolute(0xad, TICK)
    absolute(0xed, STATE + 8)
    c.emit(0xaa)
    absolute(0xad, TICK + 1)
    absolute(0xed, STATE + 9)
    c.branch(0xd0, 'no_slide')
    absolute(0xad, TICK + 2)
    c.branch(0xd0, 'no_slide')
    c.emit(0x8a, 0xc9, 96)
    c.branch(0xb0, 'no_slide')
    c.emit(0x0a, 0x49, 0xff, 0x18, 0x69, 193)
    c.jump(0x4c, 'slide')
    c.label('no_slide')
    c.emit(0xa9, 0)
    c.label('slide')
    absolute(0x8d, SHIFT)
    c.emit(0xa9, 0)
    absolute(0x8d, NEWAMP)
    c.label('amplitude_ready')
    # Resolve each scene's low/high pointer tables for the row lookup opcodes.
    # Copy the complete next dance raster into the inactive framebuffer.
    # ANTIC keeps reading the current unbanked buffer throughout the copy.
    absolute(0xad, SCENE)
    c.emit(0xc9, 2)
    c.branch(0xb0, 'copy_check_high')
    c.jump(0x4c, 'regular_lookup')
    c.label('copy_check_high')
    c.emit(0xc9, 6)
    c.branch(0xb0, 'copy_still_check')
    c.jump(0x4c, 'copy_begin')
    c.label('copy_still_check')
    c.emit(0xc9, GIRL_PORTRAIT_SCENE)
    c.branch(0xf0, 'copy_girl')
    c.emit(0xc9, PRACTICE_SCENE)
    c.branch(0xf0, 'copy_practice')
    c.jump(0x4c, 'regular_lookup')
    c.label('copy_girl')
    absolute(0xad,TICK);c.emit(0x38,0xe9,SCHOOL_PORTRAIT_TICK&255);absolute(0x8d,STATE+13)
    absolute(0xad,TICK+1);c.emit(0xe9,SCHOOL_PORTRAIT_TICK>>8)
    for _ in range(5):c.emit(0x4a);absolute(0x6e,STATE+13)
    absolute(0xad,STATE+13);c.emit(0x4a,0x4a,0xaa)
    absolute(0xad,0xd301);c.emit(0x48)
    absolute(0xbd,0x08d3);absolute(0x8d,0xd301);absolute(0x20,0x7000)
    c.emit(0x68);absolute(0x8d,0xd301);c.emit(0x60)
    c.label('copy_practice')
    compare_tick(PRACTICE_CUTS[2], 'practice_third', 'practice_before_third')
    c.label('practice_before_third')
    compare_tick(PRACTICE_CUTS[1], 'practice_second', 'practice_first')
    c.label('practice_third')
    c.emit(0xa9, 128)
    c.jump(0x4c, 'practice_offset')
    c.label('practice_second')
    c.emit(0xa9, 64)
    c.jump(0x4c, 'practice_offset')
    c.label('practice_first')
    c.emit(0xa9, 0)
    c.label('practice_offset')
    absolute(0x8d, STATE + 22)
    c.emit(0x4a, 0x4a, 0x4a, 0x4a, 0x4a, 0x4a, 0x18, 0x69, 12)
    absolute(0x8d, NEWKEY)
    c.emit(0xa9, 12)
    absolute(0x8d, FRAMEID)
    check_cached('practice_changed')
    c.emit(0xa9, 1, 0x48, 0xa2, 7)  # bank 8, second 8 KiB half
    c.jump(0x4c, 'copy_bank_select')
    c.label('copy_begin')
    c.emit(0x38, 0xe9, 2)
    absolute(0x8d, STATE + 10)
    compare_tick(DANCE_THIRD_TICK, 'copy_trio', 'copy_before_trio')
    c.label('copy_before_trio')
    compare_tick(DANCE_SECOND_TICK, 'copy_duo', 'copy_solo')
    c.label('copy_trio')
    c.emit(0xa9, 8)
    c.jump(0x4c, 'copy_group')
    c.label('copy_duo')
    c.emit(0xa9, 4)
    c.jump(0x4c, 'copy_group')
    c.label('copy_solo')
    c.emit(0xa9, 0)
    c.label('copy_group')
    c.emit(0x18)
    absolute(0x6d, STATE + 10)
    absolute(0x8d, FRAMEID)
    absolute(0x8d, NEWKEY)
    check_cached('dance_changed')
    absolute(0xad, FRAMEID)
    c.emit(0x48, 0x4a, 0x18, 0x69, 8, 0xaa)
    c.label('copy_bank_select')
    absolute(0xad, 0xd301)
    absolute(0x8d, STATE + 11)
    absolute(0xbd, 0x26fc)
    absolute(0x8d, 0xd301)
    c.emit(0x68, 0x29, 1, 0x0a, 0x0a, 0x0a, 0x0a, 0x0a, 0x18, 0x69, 0x40)
    c.label('copy_source_ready')
    absolute(0x8d, STATE + 12)
    absolute(0xad, BACK)
    c.emit(0x29, 4, 0x0a, 0x0a, 0x0a, 0x49, 0xb0)
    absolute(0x8d, STATE + 13)
    absolute(0xad, BACK)
    c.emit(0x29, 4, 0x4a, 0x4a, 0x49, 1, 0xaa)
    absolute(0x8d, TARGET)
    absolute(0xbd, BUFKEYS)
    absolute(0xcd, FRAMEID)
    c.branch(0xd0, 'pixels_changed')
    c.jump(0x4c, 'copy_done')
    c.label('pixels_changed')
    absolute(0x4d, FRAMEID)
    c.emit(0x29, 0xfc)
    c.branch(0xf0, 'dirty_copy')
    c.emit(0xa9, copy_labels['tail'] & 255)
    absolute(0x8d, copy_labels['gate'] + 1)
    c.emit(0xa9, copy_labels['pixels'] & 255)
    c.jump(0x4c, 'copy_entry')
    c.label('dirty_copy')
    c.emit(0xa9, copy_labels['end'] & 255)
    absolute(0x8d, copy_labels['gate'] + 1)
    c.emit(0xa9, copy_labels['dirty_pixels'] & 255)
    c.label('copy_entry')
    absolute(0x8d, copy_labels['repeat'] + 1)
    c.jump(0x8d, 'copy_call')
    c.emit(0xa0, 0)
    c.label('patch_copy')
    absolute(0xad, STATE + 12)
    source_patch = len(c.data)
    c.emit(0x99, 0, 0)
    absolute(0xee, STATE + 12)
    absolute(0xad, STATE + 13)
    target_patch = len(c.data)
    c.emit(0x99, 0, 0)
    absolute(0xee, STATE + 13)
    c.emit(0xc8, 0xc8, 0xc8, 0xc8, 0xc8, 0xc8, 0xc0, 150)
    c.branch(0xd0, 'patch_next')
    c.emit(0xc8, 0xc8, 0xc8)  # jump gate after page 24
    c.label('patch_next')
    c.emit(0xc0, 189)
    c.branch(0xd0, 'patch_copy')
    c.emit(0xa2, 0)
    c.labels['copy_call'] = c.origin + len(c.data) + 1
    absolute(0x20, COPY_ORIGIN)
    c.label('copy_done')
    absolute(0xae, TARGET)
    absolute(0xad, FRAMEID)
    absolute(0x9d, BUFKEYS)
    absolute(0xad, STATE + 11)
    absolute(0x8d, 0xd301)
    absolute(0xad, BACK)
    c.emit(0x29, 4, 0x4a, 0x4a, 0x49, 1, 0x18, 0x69, 2, 0xaa)
    c.jump(0x4c, 'resolve_lookup')
    c.label('regular_lookup')
    # Initialize both display lists while the ordinary intro/school scene is
    # active; banked effects then run without a per-frame timing surcharge.
    absolute(0x20, TITLE_MODE_ENTRY)
    absolute(0x20, plasma_labels['prepare'])
    c.branch(0xf0, 'regular_static')
    check_cached('plasma_changed')
    absolute(0x20, plasma_labels['draw'])
    c.jump(0x4c, 'resolve_lookup')
    c.label('regular_static')
    absolute(0xad, SCENE)
    c.emit(0x09, 0x20)
    absolute(0x8d, NEWKEY)
    check_cached('static_changed')
    absolute(0xae, SCENE)
    c.label('resolve_lookup')
    c.emit(0xa9, 0)
    absolute(0x8d, DL_KEYS)
    absolute(0x8d, DL_KEYS + 1)
    lookup_fixups = []
    for table, part in ((0x8300, 1), (0x8310, 2), (0x8320, 1), (0x8330, 2)):
        absolute(0xbd, table)
        for block in range(3):
            name = f'lookup{block}_{"lo" if table < 0x8320 else "hi"}'
            c.emit(0x8d, 0, 0)
            lookup_fixups.append((len(c.data) - 2, name, part))
    absolute(0xad, TICK)
    c.emit(0x4a, 0x4a, 0x4a, 0x29, 7)
    absolute(0x8d, AMP)

    # Build only the inactive display list while music NMIs remain enabled.
    # Three 64-row loops avoid a 6502 index wrapping across 256 bytes.
    for block in range(3):
        c.emit(0xa9, block * 64)
        absolute(0x8d, ROW)
        absolute(0xad, BACK)
        c.emit(0x18, 0x69, ((3 + block * 192) >> 8))
        c.emit(0x8d, 0, 0)
        store_lo_fix = len(c.data) - 2
        absolute(0xad, BACK)
        c.emit(0x18, 0x69, ((4 + block * 192) >> 8))
        c.emit(0x8d, 0, 0)
        store_hi_fix = len(c.data) - 2
        c.emit(0xa2, 0)
        c.label(f'loop{block}')
        absolute(0xad, ROW)
        c.emit(0x38)
        absolute(0xed, SHIFT)
        c.branch(0x90, f'blank{block}')
        c.emit(0xa8)
        absolute(0xad, SCENE)
        c.emit(0xc9, GIRL_PORTRAIT_SCENE)
        c.branch(0xf0, f'banked_still{block}')
        c.emit(0xc9, PRACTICE_SCENE)
        c.branch(0xd0, f'not_practice{block}')
        c.label(f'banked_still{block}')
        c.emit(0xb9, 0, 8, 0x18)
        absolute(0x6d, STATE + 22)
        c.emit(0xa8)
        c.jump(0x4c, f'lookup{block}_lo')
        c.label(f'not_practice{block}')
        c.emit(0xc9, 7)
        c.branch(0xb0, f'school_row{block}')
        c.emit(0xc9, 2)
        c.branch(0xb0, f'lookup{block}_lo')
        c.emit(0xb9, 0, 8, 0xa8)  # intro uses 64 rows, each tripled
        c.jump(0x4c, f'lookup{block}_lo')
        c.label(f'school_row{block}')
        c.emit(0xb9, 0, 8, 0xa8)
        c.jump(0x4c, f'lookup{block}_lo')
        c.label(f'lookup{block}_lo')
        c.emit(0xb9, 0, 8)
        c.jump(0x4c, f'store_lo{block}')
        c.label(f'blank{block}')
        c.emit(0xa0, 0xff, 0xa9, blank & 255)
        c.label(f'store_lo{block}')
        c.emit(0x9d, (3 + block * 192) & 255, 0x84 + ((3 + block * 192) >> 8))
        store_lo_addr = c.origin + len(c.data) - 1
        c.emit(0xc0, 0xff)
        c.branch(0xf0, f'blank_hi{block}')
        c.label(f'lookup{block}_hi')
        c.emit(0xb9, 0xc0, 8)
        c.jump(0x4c, f'store_hi{block}')
        c.label(f'blank_hi{block}')
        c.emit(0xa9, blank >> 8)
        c.label(f'store_hi{block}')
        c.emit(0x9d, (4 + block * 192) & 255, 0x84 + ((4 + block * 192) >> 8))
        store_hi_addr = c.origin + len(c.data) - 1
        for pos, address in ((store_lo_fix, store_lo_addr), (store_hi_fix, store_hi_addr)):
            c.data[pos:pos + 2] = address.to_bytes(2, 'little')
        absolute(0xee, ROW)
        c.emit(0xe8, 0xe8, 0xe8, 0xe0, 192)
        c.branch(0xd0, f'loop{block}')
    c.label('vblank')
    absolute(0xad, 0xd40b)
    c.emit(0xc9, 0x7c)
    c.branch(0x90, 'vblank')
    c.emit(0xa9, 0)
    absolute(0x8d, 0xd402)
    absolute(0xad, BACK)
    absolute(0x8d, 0xd403)
    c.emit(0x49, 4)
    absolute(0x8d, BACK)
    c.label('colors')
    c.emit(0xa9, 0)
    absolute(0x8d, 0xd01a)
    c.emit(0xa9, 0x48)
    absolute(0x8d, 0xd016)
    absolute(0xad, SCENE)
    c.emit(0xc9, 2)
    c.branch(0x90, 'text_colors')
    c.emit(0xc9, 6)
    c.branch(0xf0, 'text_colors')
    c.emit(0xa9, 0x9a)
    absolute(0x8d, 0xd017)
    c.emit(0xa9, 0x2c)
    c.jump(0x4c, 'last_color')
    c.label('text_colors')
    absolute(0xad, TICK)
    c.emit(0x29, 0xf0, 0x09, 0x0e)
    absolute(0x8d, 0xd017)
    c.emit(0x49, 0x80)
    c.label('last_color')
    absolute(0x8d, 0xd018)
    # The backdrop is part of every solo/duo/trio frame; no reveal masks.
    c.emit(0xa9, 0)
    absolute(0x8d, 0xd01d)
    c.emit(0xa9, 0x22)
    absolute(0x8d, 0xd400)
    absolute(0xad, SCENE)
    c.emit(0xc9, PRACTICE_SCENE)
    c.branch(0xf0, 'practice_players')
    c.emit(0xc9, 2)
    c.branch(0x90, 'scene_done')
    c.emit(0xc9, 6)
    c.branch(0xb0, 'scene_done')
    c.emit(0xa9, 0x82)
    absolute(0x8d, 0xd01a)
    c.jump(0x4c, 'scene_done')
    c.label('practice_players')
    c.emit(0xa9, 0)
    absolute(0x8d, 0xd01a)
    c.label('scene_done')
    absolute(0xad, SCENE)
    c.emit(0xc9, 2)
    c.branch(0x90, 'dance_palette_done')
    c.emit(0xc9, 6)
    c.branch(0xb0, 'dance_palette_done')
    for address, color in ((0xd016, 0x5a), (0xd017, 0xac), (0xd018, 0x2e)):
        c.emit(0xa9, color)
        absolute(0x8d, address)
    c.label('dance_palette_done')
    c.jump(0x4c, 'banked_effects')
    c.label('effect_vblank')
    absolute(0xad, 0xd40b)
    c.emit(0xc9, 0x7c)
    c.branch(0x90, 'effect_vblank')
    c.jump(0x4c, 'colors')
    c.label('cache_check')
    for new, old in ((NEWKEY, LASTKEY), (SHIFT, LASTSHIFT), (NEWAMP, LASTAMP)):
        absolute(0xad, new)
        absolute(0xcd, old)
        c.branch(0xd0, 'cache_changed')
    c.emit(0xa9, 0, 0x60)
    c.label('cache_changed')
    for new, old in ((NEWKEY, LASTKEY), (SHIFT, LASTSHIFT), (NEWAMP, LASTAMP)):
        absolute(0xad, new)
        absolute(0x8d, old)
    c.emit(0xa9, 1, 0x60)
    # Preserve foreground video-bank ownership across all music NMIs.
    # This wrapper reproduces the original entry including its WSYNC.
    c.label('mosaic')
    c.emit(0xa9,0);absolute(0x8d,SHIFT)
    absolute(0xad,TICK+1);c.emit(0x29,1,0x0a,0x0a,0x0a,0x0a);absolute(0x8d,STATE+13)
    absolute(0xad,TICK);c.emit(0x4a,0x4a,0x4a,0x4a);absolute(0x0d,STATE+13);absolute(0x8d,STATE+13)
    absolute(0xad,TICK+1);c.emit(0x29,4,0x0a,0x0a,0x0a);absolute(0x0d,STATE+13);absolute(0x8d,STATE+13)
    c.emit(0x4a,0x4a,0xaa)
    absolute(0xad,0xd301);c.emit(0x48)
    absolute(0xbd,0x08c3);absolute(0x8d,0xd301);absolute(0x20,0x7c00)
    absolute(0xad,0x24b5);absolute(0x8d,0xd301);absolute(0x20,0x7800)
    c.emit(0x68);absolute(0x8d,0xd301);c.emit(0x60)
    c.label('banked_effects')
    absolute(0xad,0xd301)
    c.emit(0x48)
    absolute(0xad,BANK_VALUE)
    absolute(0x8d,0xd301)
    absolute(0x20,BALL_ENTRY)
    c.emit(0x68)
    absolute(0x8d,0xd301)
    c.emit(0x60)
    c.labels['effect_bank_operand']=c.labels['banked_effects']+5
    c.label('music_entry')
    c.emit(0x48, 0x8a, 0x48, 0x98, 0x48)
    absolute(0x8d, 0xd40a)
    absolute(0xad, 0xd301)
    absolute(0x8d, STATE + 14)
    absolute(0xac, 0x24a5)
    absolute(0xb9, 0x26fc)
    absolute(0x8d, 0xd301)
    c.emit(0x4c, 0x18, 0x22)
    c.label('music_exit')
    absolute(0xad, STATE + 14)
    absolute(0x8d, 0xd301)
    c.emit(0x68, 0xa8, 0x68, 0xaa, 0x68, 0x40)
    code = c.finish()
    portrait_code = crush_helper(effects_address=c.labels['banked_effects'])
    for pos, offset in ((source_patch + 1, 2), (target_patch + 1, 5)):
        code[pos:pos + 2] = (copy_labels['pixels'] + offset).to_bytes(2, 'little')
    for pos, name, part in lookup_fixups:
        code[pos:pos + 2] = (c.labels[name] + part).to_bytes(2, 'little')
    if ORIGIN + len(code) > POOL_LOW:
        raise ValueError(f'code exceeds low-memory budget: {len(code)} bytes')
    descriptors = bytearray(0x100)
    for frame, (lo, hi) in enumerate(table_pointers):
        for offset, value in ((0, lo & 255), (16, lo >> 8), (32, hi & 255), (48, hi >> 8)):
            descriptors[offset + frame] = value
    descriptors[BACK - 0x8300] = 0x84
    for address in (BUFKEYS, BUFKEYS + 1, LASTKEY, LASTSHIFT, LASTAMP):
        descriptors[address - 0x8300] = 255

    missiles, players = pmg_art()
    inserts = [(RUNTIME_ORIGIN, runtime_helper()), (0x0800, bytes(y // 3 for y in range(192))), (0x0980, missiles),
               (0x0a00, players), (TABLE_BASE, tables), (ORIGIN, code), (RUN, run_stub()),
               (EFFECT_ORIGIN, effect_code), (COPY_ORIGIN, copy_code),
               (0x8000, display(0x8000)),
               (0x8300, descriptors[:0x3f]), (STATE, descriptors[0xe0:]),
               (0x8400, display(0x8400)), (TITLE_MODE_ENTRY, title_mode_helper()),
               (table_end, plasma_code)] + chunks
    # Reject every overlap, including accidental code/data growth.
    ordered = sorted(inserts)
    for (start, data), (next_start, _) in zip(ordered, ordered[1:]):
        if start + len(data) > next_start:
            raise ValueError(f'memory overlap at ${next_start:04X}')
    rom_chunks = [(address, data) for address, data in inserts if address >= 0xc000]
    rom = bytearray(os_image(rom_chunks))
    rom[-6:-4] = c.labels['music_entry'].to_bytes(2, 'little')
    # Framebuffers are cleared only at load time.
    inserts += [(base, bytes(0x1f00)) for base in FRAME_BASES]
    output = bytearray(b'\xff\xff')
    patched = inserted = False
    bank_number = 0
    for start, end, payload in segments(Path('less-i-know-release-v035.xex').read_bytes()):
        if start in (0x3000, 0x3100):
            # The original countdown writes five screen digits from its NMI.
            # Keep its instruction timing but move the digits out of video RAM.
            payload = bytearray(payload)
            operands = ((0x302f, 0x3036, 0x303e, 0x3041, 0x3048, 0x3050,
                         0x3053, 0x305a, 0x3062, 0x3065, 0x3068, 0x306b,
                         0x306e, 0x3071) if start == 0x3000 else
                        (0x311c, 0x3121, 0x3126, 0x312b, 0x3130))
            for operand in operands:
                offset = operand - start
                old = int.from_bytes(payload[offset:offset + 2], 'little')
                if not 0x34da <= old <= 0x34de:
                    raise ValueError('unexpected v035 countdown screen operand')
                payload[offset:offset + 2] = (STATE + 16 + old - 0x34da).to_bytes(2, 'little')
        if (start, end) == (0x8000, 0xbfff):
            bank_number += 1
            if bank_number == 8:
                if any(byte != 255 for byte in payload[0x2000:]):
                    raise ValueError('practice frame overlaps music in bank 8')
                payload = bytearray(payload[:0x2000] + practice_frame)
                if any(b != 255 for b in payload[CRUSH_ENTRY-0x4000:0x2000]):
                    raise ValueError('portraits overlap music')
                payload[CRUSH_ENTRY-0x4000:CRUSH_ENTRY-0x4000+len(portrait_code)] = portrait_code
                payload[0x0f00:0x0f00+len(crush_cleanup())] = crush_cleanup()
                payload[CRUSH_DATA-0x4000:0x2000] = portrait_data
            if bank_number >= 9:
                if any(byte != 255 for byte in payload):
                    raise ValueError('video bank is not unused v035 padding')
                offset = (bank_number - 9) * 2
                payload = dance_frames[offset] + dance_frames[offset + 1]
        if (start, end) == (0x2000, 0x24b2):
            payload = bytearray(payload)
            offset = 0x21bc - start
            if payload[offset:offset + 10] != bytes.fromhex('a9 00 8d 02 d4 a9 33 8d 03 d4'):
                raise ValueError('unexpected v035 display setup')
            payload[offset + 6] = 0x80
            ui = 0x220a - start
            if payload[ui:ui + 3] != bytes.fromhex('20 cd 23'):
                raise ValueError('unexpected v035 main-loop callback')
            payload[ui:ui + 3] = bytes((0x20, ORIGIN & 255, ORIGIN >> 8))
            if payload[0x218f - start:0x2192 - start] != bytes.fromhex('20 00 2d'):
                raise ValueError('unexpected v035 font initialization')
            payload[0x218f - start:0x2192 - start] = bytes((0xea,)) * 3
            exit_offset = 0x2312 - start
            if payload[exit_offset:exit_offset + 6] != bytes.fromhex('68 a8 68 aa 68 40'):
                raise ValueError('unexpected v035 interrupt epilogue')
            payload[exit_offset:exit_offset + 6] = bytes((0x4c,)) + c.labels['music_exit'].to_bytes(2, 'little') + bytes((0xea,)) * 3
            patched = True
        if (start, end) == (0x02e0, 0x02e1):
            output.extend(school_bank_loader(girl_frame))
            output.extend(school_bank_loader(hero_bank(c.labels['banked_effects'],c.labels['banked_effects']+5),index=1))
            output.extend(school_bank_loader(trevor_bank(),index=2))
            for index, frame in enumerate(mosaic_banks(),3):
                output.extend(school_bank_loader(frame,index=index))
            for index, frame in enumerate(school_pan_banks(),19):
                output.extend(school_bank_loader(frame,index=index))
            for phase in range(16):
                output.extend(school_bank_loader(polished_trevor_bank(phase),index=24+phase))
            for index, bank in enumerate(plasma_artwork(), PLASMA_FIRST_BANK):
                output.extend(school_bank_loader(bank, index=index))
            output.extend(school_bank_loader(polished_trevor_bank(0, quiet=True), index=49))
            output.extend(loader(rom))
            for address, data in inserts:
                if address < 0xc000:
                    output.extend(xex_segment(address, data))
            payload = RUN.to_bytes(2, 'little')
            inserted = True
        output.extend(xex_segment(start, payload))
    if not patched or not inserted:
        raise ValueError('missing v035 code or RUN vector')
    with output_path.open('wb' if replace else 'xb') as stream:
        stream.write(output)
    output_path.with_suffix('.json').write_text(json.dumps({
        'title_tick': TITLE_TICK, 'school_tick': SCHOOL_TICK,
        'school_phases': SCHOOL_PHASES, 'table_base': TABLE_BASE,
        'dance_tick': DANCE_TICK, 'dance_second_tick': DANCE_SECOND_TICK,
        'dance_third_tick': DANCE_THIRD_TICK, 'kaleido_tick': KALEIDO_TICK,
        'school_portrait_tick': SCHOOL_PORTRAIT_TICK, 'school_portrait_end': SCHOOL_PORTRAIT_END,
        'trevor_start': HERO_END, 'trevor_hit':TREVOR_HIT, 'trevor_end':TREVOR_END,
        'hero_start': HERO_START, 'hero_end': HERO_END, 'hero_bank': HERO_BANK,
        'crush_tick': CRUSH_TICK, 'crush_end': CRUSH_END,
        'crush_entry': CRUSH_ENTRY, 'crush_data': CRUSH_DATA,
        'table_bytes': len(tables),
        'blank_row': blank,
        'callback': ORIGIN, 'state': STATE, 'code_size': len(code),
        'unique_rows': len(unique), 'row_addresses': addresses,
        'row_storage_bytes': sum(len(blob) for blob in blobs),
        'row_unpacked_bytes': len(unique) * 40,
        'runtime_helper': RUNTIME_ORIGIN, 'runtime_end': RUNTIME_END,
        'display_layout_keys': DL_KEYS,
        'cache_keys': BUFKEYS, 'last_visual_key': LASTKEY,
        'copy_helper': COPY_ORIGIN, 'effects_helper': EFFECT_ORIGIN,
        'dirty_pages': [4, 24], 'full_copy_bytes': 7936, 'dirty_copy_bytes': 5376,
        'practice_cuts': PRACTICE_CUTS,
        'practice_tick': PRACTICE_TICK, 'practice_scene': PRACTICE_SCENE,
        'practice_bank_index': 7,
        'dance_framebuffers': FRAME_BASES, 'music_entry': c.labels['music_entry'],
        'music_exit': c.labels['music_exit'], 'video_bank_indices': list(range(8, 14)),
        'display_lists': [0x8000, 0x8400]}, indent=2) + '\n')
    print(f'Built continuous sequence: {len(unique)} shared rows, {len(code)} code bytes')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('build/visual-prototype-dev.xex'))
    parser.add_argument('--replace', action='store_true', help='replace a working build; omit for archived releases')
    args = parser.parse_args()
    build(args.output, replace=args.replace)
