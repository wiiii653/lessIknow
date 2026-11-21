#!/usr/bin/env python3
"""Dump build-time source layers: clean plates, character sprites and masks.

These are NOT runtime planes. They are the layers the build composites into
the playfield bitmaps that the demo actually stores. Kept separate for manual
art editing, with an explicit note in the manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / 'tools'))

from PIL import Image

DATE = '2026-11-21'


def rgb(path, width, height):
    data = Path(path).read_bytes()
    if len(data) != width * height * 3:
        raise ValueError(f'{path}: expected {width}x{height} RGB, got {len(data)} bytes')
    return Image.frombytes('RGB', (width, height), data)


def rgba(path, width, height):
    data = Path(path).read_bytes()
    if len(data) != width * height * 4:
        raise ValueError(f'{path}: expected {width}x{height} RGBA, got {len(data)} bytes')
    return Image.frombytes('RGBA', (width, height), data)


def save(image, path, mask=True):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)
    if mask and image.mode == 'RGBA':
        alpha = image.getchannel('A')
        alpha.save(path.with_name(path.stem + '-mask.png'), optimize=True)


def alpha_from_black(image):
    """Flood-fill near-black from the borders; keep interior black details."""
    image = image.convert('RGBA')
    width, height = image.size
    pixels = image.load()
    black = [[max(pixels[x, y][:3]) < 45 for x in range(width)] for y in range(height)]
    outside = [[False] * width for _ in range(height)]
    queue = deque()
    for x in range(width):
        for y in (0, height - 1):
            if black[y][x] and not outside[y][x]:
                outside[y][x] = True
                queue.append((x, y))
    for y in range(height):
        for x in (0, width - 1):
            if black[y][x] and not outside[y][x]:
                outside[y][x] = True
                queue.append((x, y))
    while queue:
        x, y = queue.popleft()
        for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= xx < width and 0 <= yy < height:
                if black[yy][xx] and not outside[yy][xx]:
                    outside[yy][xx] = True
                    queue.append((xx, yy))
    result = image.copy()
    target = result.load()
    for y in range(height):
        for x in range(width):
            if outside[y][x]:
                target[x, y] = (*target[x, y][:3], 0)
    return result


def crop_cells(image, cols, rows):
    width, height = image.size
    cell_w, cell_h = width // cols, height // rows
    result = []
    for row in range(rows):
        for col in range(cols):
            result.append(image.crop((col * cell_w, row * cell_h,
                                      (col + 1) * cell_w, (row + 1) * cell_h)))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=ROOT / f'dumps/{DATE}-planes/source')
    parser.add_argument('--replace', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()) and not args.replace:
        raise SystemExit(f'{output} is not empty; pick a new directory or --replace')

    entries = []

    def entry(name, path, kind, size, source, note=''):
        entries.append({'name': name, 'path': str(Path(kind) / path),
                        'kind': kind, 'size': size, 'source': source,
                        'note': note})

    # -- school ----------------------------------------------------------
    clean = Image.open('assets/art/source/act1_school_background_v034.png').convert('RGB')
    clean = clean.resize((160, 64), Image.Resampling.NEAREST)
    save(clean, output / 'school' / 'background-clean-160x64.png', mask=False)
    entry('background-clean', 'school/background-clean-160x64.png', 'school',
          (160, 64), 'assets/art/source/act1_school_background_v034.png',
          'czyste tło bez postaci; kadr 160x64 jak w prepare_school_pan')

    wide = rgb('build/school-wide-v034.rgb', 200, 64)
    save(wide, output / 'school' / 'background-wide-200x64.png', mask=False)
    entry('background-wide', 'school/background-wide-200x64.png', 'school',
          (200, 64), 'build/school-wide-v034.rgb',
          'szeroki pas tła 200x64 używany przez pan')

    cutout = rgba('build/school-girl-cutout-v176.rgba', 160, 64)
    save(cutout, output / 'school' / 'girl-cutout-160x64.png')
    entry('girl-cutout', 'school/girl-cutout-160x64.png', 'school', (160, 64),
          'build/school-girl-cutout-v176.rgba',
          'dziewczyna na przezroczystym tle; alfa = maska')

    north = rgba('build/north-girl.rgba', 48, 64)
    save(north, output / 'school' / 'north-girl-48x64.png')
    entry('north-girl', 'school/north-girl-48x64.png', 'school', (48, 64),
          'build/north-girl.rgba', 'dalsza dziewczyna z alfa (story)')

    close = rgba('build/north-girl-close.rgba', 96, 128)
    save(close, output / 'school' / 'north-girl-close-96x128.png')
    entry('north-girl-close', 'school/north-girl-close-96x128.png', 'school',
          (96, 128), 'build/north-girl-close.rgba', 'bliska dziewczyna z alfa')

    walk = rgba('build/girl-walk-cycle-v177.rgba', 96, 128)
    for index, cell in enumerate(crop_cells(walk, 2, 2)):
        save(cell, output / 'school' / f'girl-walk-{index}-48x64.png')
        entry(f'girl-walk-{index}', f'school/girl-walk-{index}-48x64.png', 'school',
              (48, 64), 'build/girl-walk-cycle-v177.rgba',
              'arkusz cyklu chodu; nieużywany przez bieżący montaż')

    boy = rgba('build/boy-whistle-v177.rgba', 160, 64)
    save(boy, output / 'school' / 'boy-whistle-160x64.png')
    entry('boy-whistle', 'school/boy-whistle-160x64.png', 'school', (160, 64),
          'build/boy-whistle-v177.rgba', 'chłopiec z alfa; nieużywany przez montaż')

    for name in ('school', 'school-neutral', 'school-front'):
        image = rgb(f'build/{name}.rgb', 160, 64)
        save(image, output / 'school' / f'{name}-160x64.png', mask=False)
        entry(name, f'school/{name}-160x64.png', 'school', (160, 64),
              f'build/{name}.rgb',
              'chłopiec wpieczony w tło; brak osobnej maski')

    # -- dance -----------------------------------------------------------
    gym = rgb('build/gym-v056.rgb', 160, 192)
    save(gym, output / 'dance' / 'gym-160x192.png', mask=False)
    entry('gym', 'dance/gym-160x192.png', 'dance', (160, 192),
          'build/gym-v056.rgb', 'czyste tło sali; tancerka jest osobno')

    cheer = Image.open('assets/art/source/act1_cheer_dance_v056.png').convert('RGB')
    for index, cell in enumerate(crop_cells(cheer, 2, 2)):
        cell = cell.resize((48, 128), Image.Resampling.NEAREST)
        cell = alpha_from_black(cell)
        save(cell, output / 'dance' / f'cheer-{index}-48x128.png')
        entry(f'cheer-{index}', f'dance/cheer-{index}-48x128.png', 'dance',
              (48, 128), 'assets/art/source/act1_cheer_dance_v056.png',
              'poza tancerki; czarne tło zamienione na alfę')

    for name, label in (('act2_ribbon_dancer_v136', 'ribbon-dancer'),
                        ('act2_ribbon_side_v142', 'ribbon-side'),
                        ('act2_ribbon_overhead_v145', 'ribbon-overhead'),
                        ('act2_ribbon_inbetweens_v166', 'ribbon-mid-v166'),
                        ('act2_ribbon_inbetweens_v171', 'ribbon-mid-v171'),
                        ('act2_ribbon_inbetweens_v173', 'ribbon-mid-v173')):
        source = Image.open(f'assets/art/source/{name}.png').convert('RGB')
        layered = alpha_from_black(source)
        save(layered, output / 'dance' / f'{label}-sheet.png')
        entry(label, f'dance/{label}-sheet.png', 'dance', layered.size,
              f'assets/art/source/{name}.png',
              'arkusz szarf; zewnętrzne czarne tło zamienione na alfę')

    # -- hero ------------------------------------------------------------
    hero = rgba('build/basketball-hero-v177.rgba', 960, 56)
    for index, cell in enumerate([hero.crop((i * 160, 0, (i + 1) * 160, 56))
                                  for i in range(6)]):
        save(cell, output / 'hero' / f'pose-{index}-160x56.png')
        entry(f'hero-pose-{index}', f'hero/pose-{index}-160x56.png', 'hero',
              (160, 56), 'build/basketball-hero-v177.rgba',
              'arkusz produkcyjny z alfa (montaż używa klatek v175)')
    interior = rgb('build/arena-interior-v151.rgb', 160, 56)
    save(interior, output / 'hero' / 'arena-interior-160x56.png', mask=False)
    entry('arena-interior', 'hero/arena-interior-160x56.png', 'hero', (160, 56),
          'build/arena-interior-v151.rgb', 'tło areny bez bohatera')
    exterior = rgb('build/arena-exterior-v151.rgb', 200, 64)
    save(exterior, output / 'hero' / 'arena-exterior-200x64.png', mask=False)
    entry('arena-exterior', 'hero/arena-exterior-200x64.png', 'hero', (200, 64),
          'build/arena-exterior-v151.rgb', 'panorama zewnętrza areny')

    sources = {}
    for item in entries:
        source = item['source']
        if source not in sources and Path(source).exists():
            sources[source] = hashlib.sha256(Path(source).read_bytes()).hexdigest()

    manifest = {
        'generated': DATE,
        'kind': 'source layers used by the build, not runtime planes',
        'sources': sources,
        'layers': entries,
        'baked': {
            'practice': 'pojedyncza ilustracja 160x192; brak czystego tła',
            'trevor': 'panele 160x64 z tłem; tunel generowany wokół sylwetki',
            'final': 'chłopiec i gwiazdy w jednej bitmapie 160x64',
            'school-boy': 'chłopiec wpieczony w school*.rgb; brak maski',
            'ribbon-runtime': 'w XEX klatki szarf są już złożone; arkusze powyżej to źródła',
        },
    }
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
    print(f'{len(entries)} warstw źródłowych w {output}')


if __name__ == '__main__':
    main()
