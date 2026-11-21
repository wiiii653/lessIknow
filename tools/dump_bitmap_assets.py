#!/usr/bin/env python3
"""Dump the demo's bitmap scenes and animation frames as editable PNGs.

Read-only with respect to the project: the built XEX and the deterministic
build modules are only read. Everything is written inside --output.

Each 1:1 PNG is palette-indexed and one byte per pixel; the PNG index is the
raw Atari pixel value (2 bpp ANTIC index or 4 bpp GTIA hue nibble). The 4x/
subtree contains nearest-neighbour viewing copies with the same indices.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / 'tools'))

from PIL import Image

from pmg_preview import atari_rgb
import title_plasma
import mosaic
import school_parallax
import school_story
import gym_practice
import ribbon_dance
import ribbon_inbetweens
import banana_variants
import girl_eyes
import trevor_polished
import trevor_awakens
import basketball_hero
import arena_art
import final_boy
from dance_banks import frame_address

REFERENCE_RELEASE = ROOT / 'releases/less-i-know-demo-release-126-stereo.xex'
REFERENCE_SHA256 = 'dc4e3b5d00456b3d46999b09d8cc010c943baa3cfd95e885f1434b45089a86bd'
BUILD_COPY = ROOT / 'build/visual-prototype-v388.xex'
DATE = '2026-11-21'


# ---------------------------------------------------------------- PNG helpers

def gtia(colors):
    return [atari_rgb(c) for c in colors]


PAL_PLASMA = [atari_rgb((hue << 4) | 0x0e) if hue else (0, 0, 0) for hue in range(16)]
PAL_MASK = [(0, 0, 0)] * 8 + [atari_rgb((hue << 4) | 0x0e)
                             for hue in title_plasma.LETTER_HUES]
PAL_SCHOOL = gtia([0x00, 0x38, 0x88, 0x2c])
PAL_GYM = gtia([0x00, 0x38, 0x68, 0x2a])
PAL_RIBBON = gtia([0x00, 0x38, 0x4a, 0x2c])
PAL_TREVOR = [tuple(color) for color in trevor_awakens.COLORS]
PAL_HERO = gtia([0x00, 0x38, 0x68, 0x2a])
PAL_FINAL = gtia([0x00, 0x0e, 0x9a, 0x2c])
PAL_BANANA = gtia([0x00, 0x1a, 0x4a, 0xee])
PAL_TUNNEL = gtia([0x00, 0x1a, 0x4a, 0x0e])

PALETTES = {
    'title-plasma-16': PAL_PLASMA,
    'title-mask': PAL_MASK,
    'school-4': PAL_SCHOOL,
    'gym-4': PAL_GYM,
    'ribbon-4': PAL_RIBBON,
    'trevor-4': PAL_TREVOR,
    'hero-4': PAL_HERO,
    'final-4': PAL_FINAL,
    'banana-4': PAL_BANANA,
    'tunnel-4': PAL_TUNNEL,
}

PALETTE_NOTES = {
    'title-plasma-16': 'GTIA 11 hue nibbles with luminance $0E; real luminance pulses at runtime',
    'title-mask': '0-7 = ordered shadow (black), 8-15 = letter hue 0-7',
    'school-4': 'COLBK $00, COLPF0 $38, COLPF1 $88, COLPF2 $2C',
    'gym-4': 'COLBK $00, COLPF0 $38, COLPF1 $68, COLPF2 $2A',
    'ribbon-4': 'base ribbon palette; the scene streams a rainbow palette at runtime',
    'trevor-4': 'quantisation colours from tools/trevor_awakens.py',
    'hero-4': 'COLBK $00, COLPF0 $38, COLPF1 $68, COLPF2 $2A',
    'final-4': 'COLBK $00, COLPF0 $0E, COLPF1 $9A, COLPF2 $2C',
    'banana-4': 'representative banana pulse; hue pairs follow the music',
    'tunnel-4': 'representative hue pair; served colours change every frame',
}


@dataclass
class Asset:
    group: str
    name: str
    width: int
    height: int
    bpp: int
    pixels: bytes
    palette: str
    source: str
    usage: str
    bank: int | None = None
    offset: int | None = None
    stored: str = 'raw'
    verified: bool = False
    note: str = ''
    segment: int | None = None

    def entry(self):
        path = Path(self.group) / f'{self.name}.png'
        result = {
            'path': str(path),
            'preview': str(Path('4x') / path),
            'width': self.width,
            'height': self.height,
            'bits_per_pixel': self.bpp,
            'palette': self.palette,
            'bytes_unpacked': self.width * self.height,
            'bytes_packed': self.width * self.height * self.bpp // 8,
            'source': self.source,
            'usage': self.usage,
            'verified_against_xex': self.verified,
            'stored_form': self.stored,
        }
        if self.bank is not None or self.segment is not None:
            result['bank'] = {
                'loader_index': self.bank,
                'xex_segment': self.segment,
                'offset': None if self.offset is None else f'${self.offset:04X}',
            }
        if self.note:
            result['note'] = self.note
        return result


# ------------------------------------------------------------- XEX extraction

def xex_segments(data: bytes):
    assert data[:2] == b'\xff\xff', 'not an XEX'
    offset = 2
    while offset + 4 <= len(data):
        if data[offset:offset + 2] == b'\xff\xff':
            break
        start = int.from_bytes(data[offset:offset + 2], 'little')
        end = int.from_bytes(data[offset + 2:offset + 4], 'little')
        size = end - start + 1
        assert size > 0, f'bad segment at {offset}'
        yield start, data[offset + 4:offset + 4 + size]
        offset += 4 + size


def segment_of(loader_index: int) -> int:
    """XEX segment holding a loader-emitted bank (segments 0-7 are v035 banks)."""
    if not 0 <= loader_index <= 49:
        raise ValueError(f'loader index {loader_index} outside 0..49')
    return loader_index + 14


def release_banks(path: Path):
    """Reassemble the 64 packed banks from a hardware XEX.

    The hardware loader wraps every bank in an INIT at $3900; the payload
    runs follow it. Groups 0-6 are the original v035 music banks, whose
    loader was replaced during packaging, so only 7-63 are used here.
    """
    segments = list(xex_segments(path.read_bytes()))
    starts = [index for index, (address, _) in enumerate(segments) if address == 0x3900]
    groups = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(segments)
        bank = bytearray(0x4000)
        for address, payload in segments[start:end]:
            if 0x8000 <= address < 0xc000:
                bank[address - 0x8000:address - 0x8000 + len(payload)] = payload
        groups.append(bytes(bank))
    return groups


def demo_banks(path: Path):
    banks = [payload for start, payload in xex_segments(path.read_bytes())
             if start == 0x8000 and len(payload) == 16384]
    if len(banks) != 64:
        raise SystemExit(f'{path}: expected 64 bank segments, found {len(banks)}')
    return banks


def unpack2(data: bytes):
    out = bytearray()
    for value in data:
        out.extend(((value >> 6) & 3, (value >> 4) & 3, (value >> 2) & 3, value & 3))
    return bytes(out)


def unpack4(data: bytes):
    out = bytearray()
    for value in data:
        out.extend((value >> 4, value & 15))
    return bytes(out)


def pack2(pixels: bytes):
    return bytes(sum(pixels[i + k] << (6 - 2 * k) for k in range(4))
                 for i in range(0, len(pixels), 4))


def packed_form(asset):
    if asset.bpp == 2:
        return pack2(asset.pixels)
    return bytes((asset.pixels[i] << 4) | asset.pixels[i + 1]
                 for i in range(0, len(asset.pixels), 2))


# --------------------------------------------------------------- construction

class Dump:
    def __init__(self, banks, source_path: Path):
        self.banks = banks
        self.source_path = source_path
        self.assets: list[Asset] = []
        self.groups: dict[str, dict] = {}
        self.failures: list[str] = []
        self.checks: list[dict] = []

    def group(self, gid, title, usage):
        self.groups.setdefault(gid, {'id': gid, 'title': title, 'usage': usage})

    def check(self, label, actual, expected, bank, offset):
        ok = actual == expected
        self.checks.append({'label': label, 'bank': bank, 'offset': f'${offset:04X}',
                            'bytes': len(expected), 'ok': ok})
        if not ok:
            mismatch = next((i for i, (a, b) in enumerate(zip(actual, expected)) if a != b),
                            min(len(actual), len(expected)))
            self.failures.append(
                f'{label}: bank {bank} +${offset:04X} differs at byte {mismatch}')

    def add(self, asset: Asset):
        if len(asset.pixels) != asset.width * asset.height:
            raise SystemExit(f'{asset.group}/{asset.name}: pixel buffer size mismatch')
        if asset.pixels and max(asset.pixels) >= 1 << asset.bpp:
            raise SystemExit(f'{asset.group}/{asset.name}: value exceeds {asset.bpp} bpp')
        if asset.segment is None and asset.bank is not None:
            asset.segment = segment_of(asset.bank)
        top = asset.group.split('/')[0]
        if top not in self.groups:
            raise SystemExit(f'{asset.group}/{asset.name}: group {top} not registered')
        self.assets.append(asset)

    def build(self):
        self.build_intro()
        self.build_school()
        self.build_dance()
        self.build_kaleidoscope()
        self.build_bananas()
        self.build_trevor()
        self.build_hero()
        self.build_final()
        if self.failures:
            print('VERIFICATION FAILED:', file=sys.stderr)
            for failure in self.failures:
                print('  ' + failure, file=sys.stderr)
            raise SystemExit(1)

    # -- 01 intro -----------------------------------------------------------

    def build_intro(self):
        gid = '01-intro'
        self.group(gid, 'Intro: plazma GTIA 11 i karty tytułu',
                   'sceny 0-2, ticki 0-2992; banki 40-48')
        plasma = title_plasma.artwork()
        for index in range(16):
            bank = 40 + index // 4
            offset = (index % 4) * title_plasma.FRAME_BYTES
            raw = self.banks[segment_of(bank)][offset:offset + title_plasma.FRAME_BYTES]
            expected = plasma[index // 4][offset:offset + title_plasma.FRAME_BYTES]
            self.check(f'plasma frame {index}', raw, expected, bank, offset)
            self.add(Asset(
                f'{gid}/plasma', f'plasma-{index:02d}', 80, 64, 4, unpack4(raw),
                'title-plasma-16', 'tools/title_plasma.py:artwork()',
                'tło plazmy, 16 faz; wyświetlane z potrojeniem wierszy',
                bank, offset, '4bpp, 2 px/byte', True,
                note='segment XEX %d' % segment_of(bank)))

        for index in range(6):
            offset = index * title_plasma.FRAME_BYTES
            raw = self.banks[segment_of(44)][offset:offset + title_plasma.FRAME_BYTES]
            self.check(f'title mask {index}', raw,
                       plasma[4][offset:offset + title_plasma.FRAME_BYTES],
                       segment_of(44), offset)
            self.add(Asset(
                f'{gid}/title-masks', f'title-mask-{index}', 80, 64, 4, unpack4(raw),
                'title-mask', 'tools/title_plasma.py:artwork() masks',
                'kumulacyjne maski liter: cień i kolejne linie', 44, offset,
                '4bpp mask codes (0 = background)', True,
                note='segment XEX %d' % segment_of(44)))

        for index, (bank, slot) in enumerate(((45, 0), (45, 1), (45, 2), (45, 3),
                                              (46, 0), (46, 1))):
            offset = slot * title_plasma.FRAME_BYTES
            raw = self.banks[segment_of(bank)][offset:offset + title_plasma.FRAME_BYTES]
            self.check(f'title fade {index}', raw,
                       plasma[5 + bank - 45][offset:offset + title_plasma.FRAME_BYTES],
                       segment_of(bank), offset)
            self.add(Asset(
                f'{gid}/fades', f'title-fade-{index}', 80, 64, 4, unpack4(raw),
                'title-mask', 'tools/title_plasma.py:artwork() fade frames',
                'maski wygaszania planszy artysty i tytułu', bank, offset,
                '4bpp ordered-dissolve mask', True,
                note='segment XEX %d' % segment_of(bank)))

        for index in range(8):
            bank = 47 + index // 4
            slot = index % 4
            offset = slot * title_plasma.FRAME_BYTES
            raw = self.banks[segment_of(bank)][offset:offset + title_plasma.FRAME_BYTES]
            self.check(f'title transition {index}', raw,
                       plasma[7 + bank - 47][offset:offset + title_plasma.FRAME_BYTES],
                       segment_of(bank), offset)
            self.add(Asset(
                f'{gid}/transitions', f'title-transition-{index}', 80, 64, 4,
                unpack4(raw), 'title-mask',
                'tools/title_plasma.py:artwork() transitions',
                'przejście artysta → tytuł, 8 kroków rastra', bank, offset,
                '4bpp mask codes', True,
                note='segment XEX %d' % segment_of(bank)))

        for index in range(4):
            bank = 47 + index // 2
            slot = index % 2
            offset = (4 + slot) * title_plasma.FRAME_BYTES
            raw = self.banks[segment_of(bank)][offset:offset + title_plasma.FRAME_BYTES]
            self.check(f'title reveal {index}', raw,
                       plasma[7 + bank - 47][4 * title_plasma.FRAME_BYTES +
                                             slot * title_plasma.FRAME_BYTES:
                                             4 * title_plasma.FRAME_BYTES +
                                             (slot + 1) * title_plasma.FRAME_BYTES],
                       segment_of(bank), offset)
            self.add(Asset(
                f'{gid}/transitions', f'title-reveal-{index}', 80, 64, 4,
                unpack4(raw), 'title-mask',
                'tools/title_plasma.py:artwork() reveal frames',
                'połowiczne odsłonięcie kolejnych wierszy napisu', bank, offset,
                '4bpp mask codes', True,
                note='segment XEX %d' % segment_of(bank)))

    # -- 02 school ----------------------------------------------------------

    def build_school(self):
        gid = '02-school'
        self.group(gid, 'Szkoła: pan, historia, portret i trening',
                   'sceny 3-6 i 13; banki 0, 7, 19-23 i wspólna pula wierszy')
        for index, pixels in enumerate(school_parallax.frames()):
            group, slot = divmod(index, 4)
            offset = slot * 2560
            self.check(f'school pan {index}', pack2(pixels),
                       self.banks[segment_of(19 + group)][offset:offset + 2560],
                       segment_of(19 + group), offset)
            self.add(Asset(
                f'{gid}/pan', f'pan-{index:02d}', 160, 64, 2, pixels,
                'school-4', 'tools/school_parallax.py:frames()',
                '18 klatek panu areny, 3 wiersze na linię', 19 + group, offset,
                '2bpp, 4 px/byte', True,
                note='segment XEX %d; ogon banku zajmują znaczniki finału'
                     % segment_of(19 + group)))

        for index, pixels in enumerate(school_story.story_frames()):
            self.add(Asset(
                f'{gid}/story', f'story-{index:02d}', 160, 192, 2, pixels,
                'school-4', 'tools/school_story.py:story_frames()',
                'klatki spotkania: chłopiec, dziewczyna, gwizd', None, None,
                '2bpp, 4 px/byte; wiersze w tabeli $D800', False,
                'pełny bufor 160x192, wyświetlany z potrojeniem wierszy'))

        portrait = school_story.girl_front_pixels()
        native = bytes(portrait[(y * 3) * 160 + x] for y in range(64) for x in range(160))
        blob = bytearray(0x2000)
        for y in range(64):
            offset = frame_address(0, y)
            blob[offset:offset + 40] = pack2(native[y * 160:(y + 1) * 160])
        # Only the first 64 stored rows are the portrait; the upper half of
        # the 8 KiB slot carries the pompom helper code.
        self.check('school portrait', bytes(blob[:0x0a00]),
                   self.banks[segment_of(0)][:0x0a00], segment_of(0), 0)
        self.add(Asset(
            f'{gid}/portrait', 'girl-portrait', 160, 64, 2, native,
            'school-4', 'tools/school_story.py:girl_front_pixels()[::3]',
            'portret dziewczyny przed szkołą; bank 0', 0, 0,
            '2bpp, 4 px/byte; zapisane co trzecie wiersze', True,
            note='segment XEX %d' % segment_of(0)))

        practice = gym_practice.practice_pixels()
        blob = bytearray(0x2000)
        for y in range(192):
            offset = frame_address(0, y)
            blob[offset:offset + 40] = pack2(practice[y * 160:(y + 1) * 160])
        self.check('practice storyboard', bytes(blob),
                   self.banks[7][0x2000:0x4000], 7, 0x2000)
        self.add(Asset(
            f'{gid}/practice', 'practice-storyboard', 160, 192, 2, practice,
            'gym-4', 'tools/gym_practice.py:practice_pixels()',
            'trzy ujęcia treningu; bank 7, górna połowa', None, 0x2000,
            '2bpp, 4 px/byte; wiersze w tabeli', True,
            note='segment XEX 7 (bank 7 to oryginalny bank v035)'))

    # -- 03 dance -----------------------------------------------------------

    def build_dance(self):
        gid = '03-dance'
        self.group(gid, 'Taniec: przód, bok i klatki pośrednie',
                   'sceny 4-5 i montaż; banki 8-14 oraz 24-39')
        for index in range(ribbon_dance.FRAME_COUNT):
            bank = ribbon_dance.FIRST_BANK + index // ribbon_dance.FRAMES_PER_BANK
            offset = (index % ribbon_dance.FRAMES_PER_BANK) * 2560
            raw = self.banks[bank][offset:offset + 2560]
            self.check(f'dance front {index}', raw,
                       ribbon_dance.packed_frame(index), bank, offset)
            self.add(Asset(
                f'{gid}/front', f'front-{index:02d}', 160, 64, 2, unpack2(raw),
                'ribbon-4', 'tools/ribbon_dance.py:packed_frame()',
                f'klatka tańca {index}; bank {bank}', None, offset,
                '2bpp, 4 px/byte', True,
                note=f'fizyczny bank {bank}, segment XEX {bank}',
                segment=bank))

        for index in range(8):
            bank = ribbon_dance.SIDE_BANK + index
            raw = self.banks[segment_of(bank)][0x0a00:0x1200]
            self.check(f'dance side {index}', raw,
                       ribbon_dance.side_actor_data(index), segment_of(bank), 0x0a00)
            pixels = bytearray()
            for row in range(56):
                pixels.extend(unpack2(raw[row * 17:(row + 1) * 17])[:68])
            self.add(Asset(
                f'{gid}/side', f'side-{index:02d}', 68, 56, 2, bytes(pixels),
                'ribbon-4', 'tools/ribbon_dance.py:side_actor_data()',
                'wycinek tancerki z boku; banki 24-31 (osiem wariantów)', bank, 0x0a00,
                '2bpp, 4 px/byte; osobna maska w banku', True,
                'kadr przycięty do x=4..71, y=8..63; segment XEX %d'
                % segment_of(bank)))

        for index, (owner, address, payload) in enumerate(ribbon_inbetweens.payloads()):
            offset = address - 0x4000
            self.check(f'dance inbetween {index}', payload,
                       self.banks[segment_of(owner)][offset:offset + len(payload)],
                       segment_of(owner), offset)
            raw = ribbon_inbetweens.decompress(payload)
            if len(raw) != 2560:
                raise SystemExit(f'inbetween {index}: unexpected size {len(raw)}')
            self.add(Asset(
                f'{gid}/inbetweens', f'inbetween-{index:02d}', 160, 64, 2,
                unpack2(raw), 'ribbon-4',
                'tools/ribbon_inbetweens.py:packed()/compress()',
                'klatka pośrednia między pozami tańca', owner, offset,
                '2bpp RLE w banku; PNG po rozpakowaniu', True,
                'w banku leży wersja skompresowana; segment XEX %d'
                % segment_of(owner)))

    # -- 04 kaleidoscope ----------------------------------------------------

    def build_kaleidoscope(self):
        gid = '04-kaleidoscope'
        self.group(gid, 'Mozaika, tunel i oczy',
                   'scena 6 i montaż; banki 11-18, klatki 32-63')
        for index in range(32):
            frame = 32 + index
            pixels = (girl_eyes.pixels(frame - 60) if frame >= 60
                      else mosaic.pixels(frame))
            group, slot = divmod(index, 4)
            offset = slot * 3840
            self.check(f'kaleidoscope {frame}', pack2(pixels),
                       self.banks[segment_of(11 + group)][offset:offset + 3840],
                       segment_of(11 + group), offset)
            usage = ('portret oczu' if frame >= 60 else
                     'organiczny tunel' if frame >= 48 else 'mozaika / tunel')
            self.add(Asset(
                f'{gid}/frames', f'kaleido-{index:02d}', 160, 96, 2, pixels,
                'tunnel-4', 'tools/mosaic.py:pixels()',
                f'klatka {frame}: {usage}', 11 + group, offset,
                '2bpp, 4 px/byte', True,
                note='segment XEX %d' % segment_of(11 + group)))

    # -- 05 bananas ---------------------------------------------------------

    def build_bananas(self):
        gid = '05-bananas'
        self.group(gid, 'Banany: oryginalny rotator',
                   'montaż po Trevrze, banki 3–10, 32 klatki na wariant')
        for index in range(8):
            owner = 3 + index
            segment = segment_of(owner)
            bank = self.banks[segment]
            offset = 0
            for slot, stream in enumerate(banana_variants.streams(index)):
                variant, phase = divmod(slot, 4)
                frame = 4 * index + phase
                self.check(f'banana {variant}/{frame}', stream,
                           bank[offset:offset + len(stream)], segment, offset)
                self.add(Asset(
                    f'{gid}/v{variant}', f'frame-{frame:02d}', 160, 96, 2,
                    mosaic.pixels(frame, variant), 'banana-4', 'tools/mosaic.py:pixels()',
                    f'wariant {variant}, faza kamery {frame}', owner, offset,
                    '2bpp RLE', True, segment=segment))
                offset += len(stream)

    # -- 06 Trevor ----------------------------------------------------------

    def build_trevor(self):
        gid = '06-trevor'
        self.group(gid, 'Trevor: panele, tunel i stare tło',
                   'sceny 7-10 i montaż; bank 1-2 oraz 24-39')
        for index, pixels in enumerate(trevor_polished.frames()):
            self.add(Asset(
                f'{gid}/panels', f'panel-{index}', 160, 64, 2, pixels,
                'trevor-4', 'tools/trevor_polished.py:frames()',
                'czysty panel Trevora, źródło tunelu i ciosów', None, None,
                '2bpp, 4 px/byte', False,
                'panel jest komponowany do banków tunelu; zgodność sprawdzana tam'))

        offsets = ((0x0000, 3), (0x1400, 0), (0x2a00, 1), (0x3400, 2))
        for phase in range(16):
            punches = trevor_polished.tunnel_frames(phase)
            for stage in range(4):
                offset = next(item[0] for item in offsets if item[1] == stage)
                bank = 24 + phase
                self.check(f'trevor tunnel {phase}/{stage}', pack2(punches[stage]),
                           self.banks[segment_of(bank)][offset:offset + 2560],
                           segment_of(bank), offset)
                self.add(Asset(
                    f'{gid}/tunnel', f'phase-{phase:02d}-stage-{stage}', 160, 64, 2,
                    punches[stage], 'trevor-4',
                    'tools/trevor_polished.py:tunnel_frames()',
                    f'faza tunelu {phase}, etap {stage}', bank, offset,
                    '2bpp, 4 px/byte', True,
                    note='segment XEX %d' % segment_of(bank)))

        for index, pixels in enumerate(trevor_awakens.backgrounds()):
            self.add(Asset(
                f'{gid}/legacy', f'legacy-{index}', 160, 64, 2, pixels,
                'trevor-4', 'tools/trevor_awakens.py:backgrounds()',
                'starsze tło Trevora zachowane w banku 2', None, None,
                '2bpp, 4 px/byte', False))

    # -- 07 hero ------------------------------------------------------------

    def build_hero(self):
        gid = '07-hero'
        self.group(gid, 'Koszykówka i arena',
                   'sceny 11-12 i montaż; bank 1 oraz plansze areny')
        expected = basketball_hero.packed()
        self.check('hero packed art', expected,
                   self.banks[segment_of(1)][0x0b80:0x0b80 + len(expected)],
                   segment_of(1), 0x0b80)
        for index, pixels in enumerate(basketball_hero.frames()):
            stored = index in (0, 2, 3, 4, 5)
            self.add(Asset(
                f'{gid}/poses', f'pose-{index}', 160, 56, 2, pixels,
                'hero-4', 'tools/basketball_hero.py:frames()',
                f'poza bohatera {index}', 1,
                0x0b80 + (index if index < 2 else index - 1) * 2240 if stored else None,
                '2bpp, 4 px/byte', stored,
                '' if stored else 'poza złożona z klatki 0 i poprawki dłoni'))
        for stage in (1, 2, 3):
            self.add(Asset(
                f'{gid}/shatter', f'shatter-{stage}', 160, 56, 2,
                basketball_hero.shattered_frame(stage), 'hero-4',
                'tools/basketball_hero.py:shattered_frame()',
                f'rozpad tablicy, etap {stage}', 1,
                0x0b80 + 5 * 2240 + 3 * 308 + (stage - 1) * 288,
                '2bpp, 4 px/byte; poprawka 48x24', False,
                'złożenie klatki 5 z łatką rozpadu'))

        self.add(Asset(
            f'{gid}/arena', 'arena-exterior', 200, 64, 2,
            arena_art.background(False), 'hero-4', 'tools/arena_art.py:background()',
            'zewnętrze Atari Arena, panorama 200 px', None, None,
            '2bpp, 4 px/byte', False))
        self.add(Asset(
            f'{gid}/arena', 'arena-interior', 160, 56, 2,
            arena_art.background(True), 'hero-4', 'tools/arena_art.py:background()',
            'wnętrze areny z trybuną', None, None,
            '2bpp, 4 px/byte', False))

    # -- 08 final -----------------------------------------------------------

    def build_final(self):
        gid = '08-final'
        self.group(gid, 'Finał: chłopiec na tle gwiazd',
                   'scena 15; bank 39')
        expected = final_boy.packed()
        self.check('final boy packed', expected,
                   self.banks[segment_of(39)][0x0a00:0x0a00 + len(expected)],
                   segment_of(39), 0x0a00)
        self.add(Asset(
            f'{gid}/scene', 'final-boy', 160, 64, 2, final_boy.artwork(),
            'final-4', 'tools/final_boy.py:artwork()',
            'chłopiec pod gwiazdami; pełny kadr finału', 39, 0x0a00,
            '2bpp, 4 px/byte', True,
            note='segment XEX %d' % segment_of(39)))


# ------------------------------------------------------------------- writing

def palette_image(asset: Asset):
    image = Image.frombytes('P', (asset.width, asset.height), asset.pixels)
    palette = PALETTES[asset.palette]
    flat = [channel for rgb in palette for channel in rgb]
    flat += [0] * (768 - len(flat))
    image.putpalette(flat)
    return image


def write_png(path: Path, asset: Asset):
    path.parent.mkdir(parents=True, exist_ok=True)
    palette_image(asset).save(path, optimize=True)


def write_preview(path: Path, asset: Asset):
    path.parent.mkdir(parents=True, exist_ok=True)
    image = palette_image(asset)
    image.resize((asset.width * 4, asset.height * 4),
                 Image.Resampling.NEAREST).save(path)


def write_contact(path: Path, assets: list[Asset]):
    scale, gap = 2, 6
    columns = min(8, len(assets))
    cell_w = max(asset.width for asset in assets) * scale
    cell_h = max(asset.height for asset in assets) * scale
    rows = (len(assets) + columns - 1) // columns
    sheet = Image.new('RGB', (columns * (cell_w + gap) + gap,
                              rows * (cell_h + gap) + gap), (24, 24, 24))
    for index, asset in enumerate(assets):
        image = palette_image(asset).convert('RGB').resize(
            (asset.width * scale, asset.height * scale), Image.Resampling.NEAREST)
        sheet.paste(image, (gap + (index % columns) * (cell_w + gap),
                            gap + (index // columns) * (cell_h + gap)))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path,
                        default=ROOT / 'build/visual-prototype-dev.xex')
    parser.add_argument('--output', type=Path,
                        default=ROOT / f'dumps/{DATE}')
    parser.add_argument('--replace', action='store_true',
                        help='write into a non-empty output directory')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()) and not args.replace:
        raise SystemExit(f'{output} is not empty; pick a new directory or pass --replace')
    source = args.source.resolve()
    if not source.exists():
        raise SystemExit(f'missing {source}; run make all first')

    sha = hashlib.sha256(source.read_bytes()).hexdigest()
    reference_sha = (hashlib.sha256(REFERENCE_RELEASE.read_bytes()).hexdigest()
                     if REFERENCE_RELEASE.exists() else None)
    if reference_sha and reference_sha != REFERENCE_SHA256:
        raise SystemExit('release 126 SHA-256 does not match PLAN_STATUS.md')
    build_sha = hashlib.sha256(BUILD_COPY.read_bytes()).hexdigest() if BUILD_COPY.exists() else None

    banks = demo_banks(source)
    parity = None
    if reference_sha:
        packed = release_banks(REFERENCE_RELEASE)
        if len(packed) < 64:
            raise SystemExit(f'release 126: only {len(packed)} bank groups')
        differing = [index for index in range(7, 64)
                     if index >= len(packed) or packed[index] != banks[index]]
        parity = {
            'release': str(REFERENCE_RELEASE.relative_to(ROOT)),
            'sha256': reference_sha,
            'banks_compared': list(range(7, 64)),
            'identical': [index for index in range(7, 64) if index not in differing],
            'differing': differing,
            'note': 'bank 7 różni się tylko ogonem muzycznym; region praktyki '
                    '$A000-$BFFF jest identyczny',
        }

    dump = Dump(banks, source)
    dump.build()

    # Check the dumped image data against the packaged release as well.
    parity_assets = parity_failures = 0
    if reference_sha:
        packed_banks = release_banks(REFERENCE_RELEASE)
        for asset in dump.assets:
            if (not asset.verified or asset.segment is None
                    or asset.offset is None or asset.group.startswith('05-bananas')
                    or 'RLE' in asset.stored):
                continue
            data = packed_form(asset)
            stored = packed_banks[asset.segment][asset.offset:
                                                  asset.offset + len(data)]
            parity_assets += 1
            if stored != data:
                parity_failures += 1
                dump.failures.append(f'{asset.group}/{asset.name}: release 126 mismatch')
        parity['assets_checked'] = parity_assets
        parity['assets_failed'] = parity_failures
        if dump.failures:
            print('RELEASE PARITY FAILED:', file=sys.stderr)
            for failure in dump.failures:
                print('  ' + failure, file=sys.stderr)
            raise SystemExit(1)

    output.mkdir(parents=True, exist_ok=True)
    folders: dict[Path, list[Asset]] = {}
    for asset in dump.assets:
        path = Path(asset.group) / f'{asset.name}.png'
        write_png(output / path, asset)
        write_preview(output / '4x' / path, asset)
        folders.setdefault(Path(asset.group), []).append(asset)
    for folder, assets in folders.items():
        write_contact(output / folder / '_contact-2x.png', assets)

    top: dict[str, list[Asset]] = {}
    for asset in dump.assets:
        top.setdefault(asset.group.split('/')[0], []).append(asset)

    manifest = {
        'generated': DATE,
        'source': {
            'xex': str(source.relative_to(ROOT)),
            'sha256': sha,
            'build_copy': str(BUILD_COPY.relative_to(ROOT)),
            'build_copy_sha256': build_sha,
            'candidate': 'v388 / stereo 126',
            'bank_segments': 64,
        },
        'release_parity': parity,
        'format': {
            'png': 'indexed, one byte per pixel; index = raw Atari pixel value',
            '2bpp': '4 pixels per byte, high bits first',
            '4bpp': '2 pixels per byte, high nibble first',
            'preview': '4x nearest neighbour, same palette indices',
            'contact_sheet': '2x composited RGB contact sheet in every folder',
        },
        'palettes': {name: {'rgb': PALETTES[name], 'note': PALETTE_NOTES[name]}
                     for name in PALETTES},
        'groups': [{'id': gid,
                    'title': dump.groups[gid]['title'],
                    'usage': dump.groups[gid]['usage'],
                    'assets': [asset.entry() for asset in assets]}
                   for gid, assets in top.items()],
        'verification': {
            'checks': len(dump.checks),
            'passed': sum(1 for check in dump.checks if check['ok']),
            'failed': [check for check in dump.checks if not check['ok']],
        },
        'excluded': [
            "sprite'y PMG (players/missiles) i ich maski",
            'fonty: terminal, credits/outro, final mark, duże napisy',
            'ekrany tekstowe ANTIC 2 (loading screen, terminal)',
            'tablice palet i kod 6502 w bankach',
        ],
    }
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')

    lines = [f'# Zrzut bitmap — {DATE}', '',
             f'Źródło: `{source.relative_to(ROOT)}` (SHA-256 `{sha}`).',
             f'Kandydat: v388 / stereo 126. Wydanie: '
             f'`{REFERENCE_RELEASE.relative_to(ROOT)}` (SHA-256 `{reference_sha}`).',
             f'Kopia builda: `{BUILD_COPY.relative_to(ROOT)}` '
             f'(SHA-256 `{build_sha}`).', '',
             'Pliki 1:1 są indeksowane: wartość piksela to surowy indeks Atari.',
             'Katalog `4x/` zawiera powiększenia nearest-neighbour, a w każdym',
             'folderze leży `_contact-2x.png` do szybkiego przeglądu.', '',
             '## Grupy', '']
    for gid, assets in top.items():
        lines.append(f'- **{gid}** — {dump.groups[gid]["title"]}: {len(assets)} plików')
        lines.append(f'  - użycie: {dump.groups[gid]["usage"]}')
    lines += ['', '## Weryfikacja', '',
              f'Sprawdzono {len(dump.checks)} fragmentów banków; '
              f'{sum(1 for check in dump.checks if check["ok"])} zgodnych.', '',
              f'Dodatkowo {parity_assets} plików porównano z wydaniem 126; '
              f'niezgodnych: {parity_failures}.', '',
              'Pliki z `verified_against_xex: true` porównano bajt w bajt z bankiem',
              'zbudowanego XEX po spakowaniu 2bpp/4bpp. Pozostałe pochodzą z tych',
              'samych funkcji builda, ale są komponowane w locie (np. panele Trevora',
              'są wejściem do banków tunelu, a storyboardy trafiają do wspólnej puli',
              'wierszy), więc nie mają własnego, ciągłego bloku w banku.', '',
              '## Poza zakresem', '']
    lines += [f'- {item}' for item in manifest['excluded']]
    lines += ['', '## Pliki', '']
    for gid, assets in top.items():
        lines.append(f'### {gid}')
        lines.append('')
        lines.append('| plik | wymiary | bank | offset | źródło |')
        lines.append('| --- | --- | --- | --- | --- |')
        for asset in assets:
            bank = '—' if asset.bank is None else str(asset.bank)
            offset = '—' if asset.offset is None else f'${asset.offset:04X}'
            lines.append(f'| `{asset.group}/{asset.name}.png` | '
                         f'{asset.width}×{asset.height} | {bank} | {offset} | '
                         f'`{asset.source}` |')
        lines.append('')
    (output / 'MANIFEST.md').write_text('\n'.join(lines) + '\n')

    print(f'{len(dump.assets)} obrazów w {output} ({len(folders)} folderów)')
    print(f'weryfikacja: {sum(1 for c in dump.checks if c["ok"])}/{len(dump.checks)} OK')


if __name__ == '__main__':
    main()
