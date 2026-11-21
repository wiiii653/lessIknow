#!/usr/bin/env python3
"""Dump the demo's runtime planes exactly as stored and as shown on screen.

Requires py65 (see requirements-dev.txt). Every plane is captured by running
the real 6502 scene callback for a selected player tick:

* playfield bitmap read through the display list (ANTIC), without PMG,
* each PMG player P0-P3 and missile M0-M3: raw 128-byte page plus the
  screen-space plane rebuilt from HPOSP/HPOSM/SIZEP/SIZEM/COLOR registers,
* CPU bitmap overlays that exist as separate stored planes (side dancer),
* stored overlay planes around the same moment (portraits, title masks).

Only genuine runtime planes are written. Characters baked into the playfield
bitmap are listed as such in PLANES.md; they have no separate plane in the XEX.
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

from pmg_preview import atari_rgb, player_masks
from scene_palettes import SCHOOL_PALETTE, GYM_PALETTE
from build_sequence import PALETTE

try:
    from py65.devices.mpu6502 import MPU
    from scene_memory import RuntimeMemory
except ModuleNotFoundError as error:  # pragma: no cover - environment guard
    raise SystemExit('py65 is required: use the venv that installed requirements-dev.txt') from error

DATE = '2026-11-21'
BUILD = ROOT / 'build/visual-prototype-dev.xex'
BUILD_JSON = ROOT / 'build/visual-prototype-dev.json'
REFERENCE = ROOT / 'releases/less-i-know-demo-release-126-stereo.xex'

PLAYER_SCALE = (1, 2, 1, 4)


@dataclass
class Moment:
    slug: str
    tick: int
    note: str


def moments(info):
    return [
        Moment('01-artist-plasma', 96, 'plazma artysty; PMG fajerwerki'),
        Moment('02-title-plasma', 1592, 'plazma tytułu + maski liter; PMG fajerwerki'),
        Moment('03-school', info['school_tick'], 'chłopiec i tło w bitmapie; brak PMG'),
        Moment('04-portrait', info['school_portrait_tick'] + 100,
               'zbliżenie dziewczyny; PMG gwizdka nieaktywne'),
        Moment('05-whistle', 4882, 'nuty gwizdka na P0-P3 + iskry na missiles'),
        Moment('06-practice', info['practice_cuts'][1] + 100,
               'trening; tęczowa piłka na PMG'),
        Moment('07-dance-side', info['ribbon_side_start'] + 625,
               'bok tancerki: gym + bitmapowy overlay z maską + akcenty PMG'),
        Moment('08-dance-front', 15200, 'grupa/solówka; portrety jako overlay'),
        Moment('09-kaleidoscope', info['kaleido_tick'] + 33, 'mozaika/tunel; piłka PMG'),
        Moment('10-dance-group', 19000, 'taniec grupowy z portretami; akcenty PMG'),
        Moment('11-kiss', 20700, 'serce z ust na PMG; sala w bitmapie'),
        Moment('12-hero', info['hero_start'] + 410,
               'hero w bitmapie; piłka/satelity na PMG'),
        Moment('13-trevor-bang', info['trevor_hit'] + 40,
               'BUM/BAM na players + missiles; Trevor w bitmapie'),
        Moment('14-bananas', 39000, 'bananowy rotator; świecące kiście na PMG'),
        Moment('15-final', 51500,
               'karta finałowa; chłopiec w bitmapie, linie tekstowe pominięte'),
    ]


# --------------------------------------------------------------- capture

class Capture:
    def __init__(self, data: bytes, info: dict):
        self.data = data
        self.info = info

    def run(self, tick: int):
        cpu = MPU(memory=RuntimeMemory(self.data))
        memory = cpu.memory
        memory[0x23cd] = 0x60
        memory[0xd40b] = 124
        for offset in range(3):
            memory[0x24a7 + offset] = (tick >> (8 * offset)) & 255
        cpu.sp = 0xfd
        memory[0x1fe:0x200] = [0xfe, 0x7f]
        cpu.pc = self.info['callback']
        for _ in range(120000):
            if cpu.pc == 0x7fff:
                break
            cpu.step()
        else:
            raise RuntimeError('scene callback did not return')
        return memory

    @staticmethod
    def playfield(memory):
        pc = memory[0xd402] | memory[0xd403] << 8

        def fetch():
            nonlocal pc
            value = memory[pc]
            pc = (pc & 0xfc00) | ((pc + 1) & 0x3ff)
            return value

        indices = bytearray()
        for _ in range(1024):
            op = fetch()
            mode = op & 15
            if mode == 1:
                target = fetch() | fetch() << 8
                if op & 0x40:
                    break
                pc = target
            elif mode == 0:
                indices.extend(bytes(160 * (((op >> 4) & 7) + 1)))
            elif mode in (2, 3, 4, 5) and op & 0x40:
                # Character mode: the bytes are glyph codes, not pixels.
                # The font itself is out of scope, so keep alignment only.
                fetch(); fetch()
                indices.extend(bytes(160) * {2: 8, 3: 10, 4: 8, 5: 16}[mode])
            elif mode in (14, 15) and op & 0x40:
                address = fetch() | fetch() << 8
                for byte in memory[address:address + 40]:
                    if mode == 15:
                        indices.extend((byte >> 4, byte >> 4, byte & 15, byte & 15))
                    else:
                        for shift in (6, 4, 2, 0):
                            indices.append((byte >> shift) & 3)
            else:
                raise ValueError(f'unsupported display-list mode ${op:02X}')
        else:
            raise ValueError('display list did not terminate')
        return bytes(indices), len(indices) // 160

    @staticmethod
    def palette(memory):
        gtia11 = (memory[0xd01b] & 0xc0) == 0xc0
        if gtia11:
            return [(atari_rgb((hue << 4) | (memory[0xd01a] & 15)) if hue else
                     atari_rgb(memory[0xd01a])) for hue in range(16)], True
        scene = memory[0x83e0]
        original = {0: PALETTE[0], 0x82: (12, 24, 48)}
        if scene in (7, 8, 9, 10, 11, 12, 14):
            original.update({0x38: SCHOOL_PALETTE[1], 0x88: SCHOOL_PALETTE[2],
                             0x2c: SCHOOL_PALETTE[3]})
        elif scene in (2, 3, 4, 5, 13, 15):
            original.update({0x38: GYM_PALETTE[1], 0x68: GYM_PALETTE[2],
                             0x2a: GYM_PALETTE[3]})
        if scene == 16:
            original = {}
        palette = [original.get(color, atari_rgb(color)) for color in
                   (memory[0xd01a], memory[0xd016], memory[0xd017], memory[0xd018])]
        return palette, False


# --------------------------------------------------------------- PMG planes

def pmg_state(memory):
    single = bool(memory[0xd400] & 16)
    base = (memory[0xd407] & (0xf8 if single else 0xfc)) << 8
    players = [base + (0x400 + index * 0x100 if single else 0x200 + index * 0x80)
               for index in range(4)]
    missiles = base + (0x300 if single else 0x180)
    return single, base, players, missiles


def page_bytes(memory, address, size):
    return bytes(memory[address:address + size])


def plane_mask(value, bits):
    return [bool(value & (1 << (bits - bit - 1))) for bit in range(bits)]


def rainbow_color(memory, y, plane):
    """Per-scanline colour for the ribbon scenes, matching the preview."""
    if memory[0x83e0] != 14:
        return None
    try:
        from ribbon_dance import rainbow_palette
    except Exception:
        return None
    band = min(3, (y + 9) // 78)
    palette = rainbow_palette(memory[0x83e2], band,
                              airflow=12 <= memory[0x83ed] < 16,
                              kiss=memory[0x83e0] == 14 and memory[0x83ed] == 15)
    return atari_rgb(palette[plane])


def render_player(memory, index, height, single, address, raster_start=8):
    position = memory[0xd000 + index]
    size = memory[0xd008 + index] & 3
    color = atari_rgb(memory[0xd012 + index])
    return render_bits(memory, address, height, position, size, 8, color,
                       single, raster_start,
                       color_at=lambda y: rainbow_color(memory, y, index))


def render_missile(memory, index, height, single, address, raster_start=8):
    position = memory[0xd004 + index]
    size = (memory[0xd00c] >> (2 * index)) & 3
    color_byte = (memory[0xd019] if memory[0xd01b] & 0x10
                  else memory[0xd012 + index])
    color = atari_rgb(color_byte)
    return render_bits(memory, address, height, position, size, 2, color,
                       single, raster_start, missile_index=index,
                       color_at=lambda y: rainbow_color(memory, y, 4))


def render_bits(memory, address, height, position, size, bits, color,
                single, raster_start, missile_index=None, color_at=None):
    image = Image.new('RGBA', (160, height), (0, 0, 0, 0))
    pixels = image.load()
    if position == 0:
        return image
    scale = PLAYER_SCALE[size]
    left = position - 48
    for y in range(height):
        ink = color_at(y) if color_at is not None else color
        if ink is None:
            ink = color
        line = y + raster_start
        value = memory[address + (line if single else line // 2)]
        if missile_index is not None:
            value = (value >> (2 * missile_index)) & 3
        for bit in range(bits):
            if value & (1 << (bits - bit - 1)):
                for dx in range(scale):
                    x = left + bit * scale + dx
                    if 0 <= x < 160:
                        pixels[x, y] = (*ink, 255)
    return image


def render_store(memory, address, size, color=(255, 255, 255)):
    image = Image.new('RGBA', (8, size), (0, 0, 0, 0))
    pixels = image.load()
    for row in range(size):
        value = memory[address + row]
        for bit in range(8):
            if value & (1 << (7 - bit)):
                pixels[bit, row] = (*color, 255)
    return image


def rgba_plane_to_indexed(image, palette):
    """Convert an RGBA PMG plane to a 1-bit indexed PNG plus a colour note."""
    mask = Image.new('P', image.size, 0)
    mask.putpalette([0, 0, 0] + list(palette) + [0] * (768 - 6))
    source = image.load()
    target = mask.load()
    for y in range(image.height):
        for x in range(image.width):
            if source[x, y][3]:
                target[x, y] = 1
    return mask


# ------------------------------------------------------------- source banks

def xex_segments(data: bytes):
    assert data[:2] == b'\xff\xff'
    offset = 2
    while offset + 4 <= len(data):
        if data[offset:offset + 2] == b'\xff\xff':
            break
        start = int.from_bytes(data[offset:offset + 2], 'little')
        end = int.from_bytes(data[offset + 2:offset + 4], 'little')
        size = end - start + 1
        yield start, data[offset + 4:offset + 4 + size]
        offset += 4 + size


def demo_banks(data: bytes):
    banks = [payload for start, payload in xex_segments(data)
             if start == 0x8000 and len(payload) == 16384]
    if len(banks) != 64:
        raise SystemExit(f'expected 64 banks, got {len(banks)}')
    return banks


def unpack2(data: bytes):
    out = bytearray()
    for value in data:
        out.extend(((value >> 6) & 3, (value >> 4) & 3, (value >> 2) & 3, value & 3))
    return bytes(out)


def side_actor(banks, pose):
    # Bank 24+pose holds 952 bytes of pixels and a 952-byte mask at $4A00/$4E00.
    payload = banks[38 + pose][0x0a00:0x0a00 + 2048]
    pixels = bytearray()
    mask = bytearray()
    for row in range(56):
        pixels.extend(unpack2(payload[row * 17:(row + 1) * 17])[:68])
        keep = unpack2(payload[1024 + row * 17:1024 + (row + 1) * 17])[:68]
        mask.extend(1 if value == 0 else 0 for value in keep)  # stored 0 = opaque
    return bytes(pixels), bytes(mask)


# ------------------------------------------------------------------- writing

def indexed_image(width, height, pixels, palette):
    image = Image.frombytes('P', (width, height), bytes(pixels))
    flat = [channel for rgb in palette for channel in rgb]
    flat += [0] * (768 - len(flat))
    image.putpalette(flat)
    return image


def save_indexed(path, width, height, pixels, palette):
    path.parent.mkdir(parents=True, exist_ok=True)
    indexed_image(width, height, pixels, palette).save(path, optimize=True)


def save_rgba(path, image):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def save_scaled(path, image, scale=4):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.resize((image.width * scale, image.height * scale),
                 Image.Resampling.NEAREST).save(path, optimize=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=BUILD)
    parser.add_argument('--output', type=Path,
                        default=ROOT / f'dumps/{DATE}-planes')
    parser.add_argument('--replace', action='store_true')
    parser.add_argument('--scale', type=int, default=4)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()) and not args.replace:
        raise SystemExit(f'{output} is not empty; pick a new directory or --replace')
    source = args.source.resolve()
    if not source.exists():
        raise SystemExit(f'missing {source}')
    info = json.loads(BUILD_JSON.read_text())
    data = source.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    reference_sha = hashlib.sha256(REFERENCE.read_bytes()).hexdigest()

    capture = Capture(data, info)
    banks = demo_banks(data)
    scale = args.scale
    report = []

    for moment in moments(info):
        memory = capture.run(moment.tick)
        indices, height = capture.playfield(memory)
        palette, gtia11 = capture.palette(memory)
        single, base, players, missiles = pmg_state(memory)
        folder = output / 'runtime' / moment.slug
        folder.mkdir(parents=True, exist_ok=True)

        # Playfield exactly as displayed before PMG (may contain CPU overlays).
        save_indexed(folder / 'playfield.png', 160, height, indices, palette)
        save_scaled(folder / 'playfield@4x.png',
                    indexed_image(160, height, indices, palette).convert('RGB'), scale)

        # Composite using the same approximation as the existing previews.
        composited = player_masks(bytearray(indices), memory, height,
                                  raster_start=8,
                                  rainbow_bands=memory[0x83e0] == 14,
                                  pmg_color_offset=16 if gtia11 else 4)
        rgb = Image.new('RGB', (160, height))
        rgb.putdata([(atari_rgb((index - 16) * 2) if index >= 16 else
                      (atari_rgb((index << 4) | (memory[0xd01a] & 15))
                       if gtia11 and index else
                       (palette[index] if index < 4 else atari_rgb((index - 4) * 2))))
                     for index in composited])
        save_rgba(folder / 'composite.png', rgb)
        save_scaled(folder / f'composite@{scale}x.png', rgb, scale)

        state = {
            'tick': moment.tick,
            'note': moment.note,
            'scene': memory[0x83e0],
            'frame': memory[0x83ed],
            'playfield': {'width': 160, 'height': height,
                          'bits_per_pixel': 4 if gtia11 else 2,
                          'display_list': f'${(memory[0xd402] | memory[0xd403] << 8):04X}'},
            'pmg': {
                'base': f'${base:04X}',
                'single_line': single,
                'page_bytes': 256 if single else 128,
                'prior': f'${memory[0xd01b]:02X}',
                'd400': f'${memory[0xd400]:02X}',
                'players_enabled': bool(memory[0xd01d] & 2 and memory[0xd400] & 8),
                'missiles_enabled': bool(memory[0xd01d] & 1 and memory[0xd400] & 4),
                'players': [], 'missiles': [],
            },
            'baked_into_playfield': [],
        }

        players_enabled = state['pmg']['players_enabled']
        missiles_enabled = state['pmg']['missiles_enabled']
        for index in range(4):
            if not players_enabled:
                break
            address = players[index]
            size_bytes = 256 if single else 128
            raw = page_bytes(memory, address, size_bytes)
            (folder / 'pmg' / 'raw').mkdir(parents=True, exist_ok=True)
            (folder / 'pmg' / 'raw' / f'p{index}.bin').write_bytes(raw)
            plane = render_player(memory, index, height, single, address)
            save_rgba(folder / 'pmg' / f'p{index}.png', plane)
            save_scaled(folder / 'pmg' / f'p{index}@{scale}x.png', plane, scale)
            save_rgba(folder / 'pmg' / f'p{index}-stored.png',
                      render_store(memory, address, size_bytes,
                                   atari_rgb(memory[0xd012 + index])))
            state['pmg']['players'].append({
                'plane': index,
                'address': f'${address:04X}',
                'bytes': size_bytes,
                'position': memory[0xd000 + index],
                'size_bits': memory[0xd008 + index] & 3,
                'scale': PLAYER_SCALE[memory[0xd008 + index] & 3],
                'color': f'${memory[0xd012 + index]:02X}',
                'visible': bool(memory[0xd01d] & 2 and memory[0xd400] & 8
                                and memory[0xd000 + index]),
            })

        size_bytes = 256 if single else 128
        if missiles_enabled:
            raw = page_bytes(memory, missiles, size_bytes)
            (folder / 'pmg' / 'raw' / 'missiles.bin').write_bytes(raw)
        for index in range(4 if missiles_enabled else 0):
            plane = render_missile(memory, index, height, single, missiles)
            save_rgba(folder / 'pmg' / f'm{index}.png', plane)
            save_scaled(folder / 'pmg' / f'm{index}@{scale}x.png', plane, scale)
            state['pmg']['missiles'].append({
                'plane': index,
                'address': f'${missiles:04X}',
                'bytes': size_bytes,
                'position': memory[0xd004 + index],
                'size_bits': (memory[0xd00c] >> (2 * index)) & 3,
                'color': f'${(memory[0xd019] if memory[0xd01b] & 0x10 else memory[0xd012 + index]):02X}',
                'visible': bool(memory[0xd01d] & 1 and memory[0xd400] & 4
                                and memory[0xd004 + index]),
            })

        # Side dancer overlay: separate stored bitmap + mask, fixed placement.
        if memory[0x83e0] == 14 and 16 <= memory[0x83ed] < 32:
            # The clean gym backdrop is a separate stored frame; the captured
            # playfield already has the actor composited into it by the NMI.
            frame = memory[0x83ed]
            bank = 8 + frame // 6
            offset = (frame % 6) * 2560
            backdrop = unpack2(banks[bank][offset:offset + 2560])
            save_indexed(folder / 'background' / f'gym-{frame:02d}.png',
                         160, 64, backdrop, palette)
            save_scaled(folder / 'background' / f'gym-{frame:02d}@4x.png',
                        indexed_image(160, 64, backdrop, palette).convert('RGB'),
                        scale)
            pose = (memory[0x83ed] - 16) // 2
            pixels, mask = side_actor(banks, pose)
            overlay = Image.new('RGBA', (68, 56))
            overlay.putdata([(*(PALETTE[value] if value else (0, 0, 0)),
                              255 if keep else 0)
                             for value, keep in zip(pixels, mask)])
            save_rgba(folder / 'overlay' / f'side-{pose}-pixels.png', overlay)
            alpha = Image.new('L', (68, 56))
            alpha.putdata([255 if keep else 0 for keep in mask])
            save_rgba(folder / 'overlay' / f'side-{pose}-mask.png', alpha)
            state['overlay'] = {
                'kind': 'side-dancer',
                'pose': pose,
                'bank': 24 + pose,
                'address': '$4A00 pixels, $4E00 mask',
                'placement': {'x': 4, 'y': 8, 'width': 68, 'height': 56},
                'storage': '952 B 2bpp pixels + 952 B mask, row stride 17 B',
            }
            state['baked_into_playfield'].append('gym backdrop (banked frame)')

        # Title: plasma frames are stored separately from the letter masks.
        if memory[0x83e0] in (0, 1):
            for index in range(16):
                raw = banks[54 + index // 4][(index % 4) * 2560:(index % 4 + 1) * 2560]
                pixels = bytearray()
                for value in raw:
                    pixels.extend((value >> 4, value & 15))
                save_indexed(folder / 'background' / f'plasma-{index:02d}.png',
                             80, 64, pixels,
                             [atari_rgb((hue << 4) | 0x0e) if hue else (0, 0, 0)
                              for hue in range(16)])
            masks = banks[58]
            for index in range(6):
                raw = masks[index * 2560:(index + 1) * 2560]
                pixels = bytearray()
                for value in raw:
                    pixels.extend((value >> 4, value & 15))
                save_indexed(folder / 'overlay' / f'title-mask-{index}.png',
                             80, 64, pixels,
                             [(0, 0, 0)] * 8 + [atari_rgb((hue << 4) | 0x0e)
                                                for hue in range(8)])
            state['overlay'] = {'kind': 'title-letter-masks', 'bank': 44,
                                'count': 6, 'storage': '6 x 2560 B 4bpp masks'}

        (folder / 'state.json').write_text(json.dumps(state, indent=1) + '\n')
        report.append(state)
        print(f'{moment.slug}: scene {state["scene"]} frame {state["frame"]} '
              f'{height} linii, PMG @ {state["pmg"]["base"]}')

    # Stored rectangle overlays: 4 crush portraits (published on cuts).
    try:
        from crush_portraits import portraits
        target = output / 'stored-overlays' / 'portraits'
        for index, pixels in enumerate(portraits()):
            image = Image.new('RGBA', (80, 52))
            image.putdata([(*(PALETTE[value] if value else (0, 0, 0)), 255)
                           for value in pixels])
            save_rgba(target / f'portrait-{index}.png', image)
            save_scaled(target / f'portrait-{index}@4x.png', image, scale)
    except Exception as error:  # module may be mid-edit
        print(f'portraits skipped: {type(error).__name__}: {error}')

    summary = {
        'generated': DATE,
        'source': {'xex': str(source.relative_to(ROOT)), 'sha256': sha,
                   'release': str(REFERENCE.relative_to(ROOT)),
                   'release_sha256': reference_sha},
        'format': {
            'playfield': 'indexed 1:1, ANTIC pixel values; PMG not composited',
            'pmg-plane': 'RGBA screen-space plane rebuilt from GTIA registers',
            'pmg-stored': '8 px wide, one row per stored page byte',
            'pmg-raw': 'exact bytes read at the PMG base address',
            'composite': 'approximate preview: playfield + PMG priority',
        },
        'moments': report,
        'baked': {
            '03-school': 'chłopiec, dziewczyna i tło są w jednej bitmapie 160x192',
            '04-portrait': 'twarz dziewczyny w bitmapie; brak osobnej płaszczyzny',
            '06-practice': 'ilustracja treningu w bitmapie; osobna jest tylko piłka PMG',
            '07-dance-side': 'tło gym i tancerka to osobne płaszczyzny (bitmapa + maska)',
            '08-dance-front': 'tancerka w bitmapie; portrety to osobne, publikowane overlaye',
            '12-hero': 'bohater i arena w jednej bitmapie 160x56; PMG to piłka/satelity',
            '13-trevor-bang': 'Trevor i tunel w bitmapie; PMG to BUM/BAM i iskry',
            '15-final': 'chłopiec w bitmapie; PMG to gwiazdy i nuty',
        },
    }
    (output / 'manifest.json').write_text(json.dumps(summary, indent=1) + '\n')
    print(f'\n{len(report)} momentów w {output}')


if __name__ == '__main__':
    main()
