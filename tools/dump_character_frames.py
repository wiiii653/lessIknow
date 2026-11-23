#!/usr/bin/env python3
"""Dump every character animation frame, removing exact duplicates.

Frames are grouped per character/role. Indexed 1:1 PNG keeps the raw Atari
pixel values; RGBA is used only for source sprites that carry a mask.
A manifest records the original frame indices and any aliases removed by
deduplication.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / 'tools'))

from PIL import Image

from pmg_preview import atari_rgb
from scene_palettes import ART_PALETTE, SCHOOL_PALETTE, GYM_PALETTE

import school_story
import school_parallax
import gym_practice
import ribbon_dance
import ribbon_inbetweens
import trevor_polished
import trevor_awakens
import basketball_hero
import final_boy
import crush_portraits
import pompom_effects
import girl_eyes

DATE = '2026-11-22'
BUILD = ROOT / 'build/visual-prototype-dev.xex'
REFERENCE = ROOT / 'releases/less-i-know-demo-release-133-stereo.xex'

SCHOOL = [(0, 0, 0), SCHOOL_PALETTE[1], SCHOOL_PALETTE[2], SCHOOL_PALETTE[3]]
GYM = [(0, 0, 0), GYM_PALETTE[1], GYM_PALETTE[2], GYM_PALETTE[3]]
RIBBON = [atari_rgb(c) for c in (0x00, 0x38, 0x4a, 0x2c)]
TREVOR = [tuple(c) for c in trevor_awakens.COLORS]
HERO = [atari_rgb(c) for c in (0x00, 0x38, 0x68, 0x2a)]
FINAL = [atari_rgb(c) for c in (0x00, 0x0e, 0x9a, 0x2c)]
ART = [tuple(c) for c in ART_PALETTE]
EYES = [atari_rgb(c) for c in (0x00, 0x1a, 0x4a, 0x0e)]


def unpack2(data: bytes):
    out = bytearray()
    for value in data:
        out.extend(((value >> 6) & 3, (value >> 4) & 3, (value >> 2) & 3, value & 3))
    return bytes(out)


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
    alpha = image.getchannel('A')
    alpha.save(path.with_name(path.stem + '-mask.png'), optimize=True)


def save_preview(path, image, scale=4):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert('RGB').resize((image.width * scale, image.height * scale),
                                Image.Resampling.NEAREST).save(path, optimize=True)


def contact(path, frames):
    scale, gap = 2, 6
    columns = min(8, len(frames))
    cell_w = max(frame.width for frame in frames) * scale
    cell_h = max(frame.height for frame in frames) * scale
    rows = (len(frames) + columns - 1) // columns
    sheet = Image.new('RGB', (columns * (cell_w + gap) + gap,
                              rows * (cell_h + gap) + gap), (24, 24, 24))
    for index, frame in enumerate(frames):
        tile = frame.convert('RGB').resize((frame.width * scale, frame.height * scale),
                                           Image.Resampling.NEAREST)
        sheet.paste(tile, (gap + (index % columns) * (cell_w + gap),
                           gap + (index // columns) * (cell_h + gap)))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=True)


def rgb_file(path, width, height):
    data = Path(path).read_bytes()
    if len(data) != width * height * 3:
        raise ValueError(f'{path}: expected {width}x{height} RGB')
    return Image.frombytes('RGB', (width, height), data)


def rgba_file(path, width, height):
    data = Path(path).read_bytes()
    if len(data) != width * height * 4:
        raise ValueError(f'{path}: expected {width}x{height} RGBA')
    return Image.frombytes('RGBA', (width, height), data)


class Group:
    def __init__(self, slug, title, source, palette=None):
        self.slug = slug
        self.title = title
        self.source = source
        self.palette = palette
        self.frames = []   # (name, width, height, pixels, rgba_image)
        self.aliases = {}

    def add_indexed(self, name, width, height, pixels):
        self.frames.append((name, width, height, bytes(pixels), None))

    def add_rgba(self, name, image):
        self.frames.append((name, image.width, image.height, None, image))

    def dedupe(self):
        seen = {}
        unique = []
        for index, frame in enumerate(self.frames):
            name, width, height, pixels, image = frame
            key = hashlib.sha256(pixels if pixels is not None else image.tobytes()).hexdigest()
            if key in seen:
                self.aliases.setdefault(seen[key], []).append(index)
            else:
                seen[key] = index
                unique.append((name, width, height, pixels, image))
        self.frames = unique
        return len(seen)


def build_groups():
    groups = []

    # -- school ---------------------------------------------------------
    boy = Group('school-boy', 'Chłopiec ze szkoły', 'school_story.boy_poses()', SCHOOL)
    poses = school_story.boy_poses()
    for index, name in enumerate(('neutral', 'turned', 'whistle')):
        boy.add_indexed(name, 160, 192, poses[index])
    groups.append(boy)

    story = Group('school-story', 'Klatki spotkania (chłopiec + dziewczyna)',
                  'school_story.story_frames()', SCHOOL)
    for index, pixels in enumerate(school_story.story_frames()):
        story.add_indexed(f'story-{index}', 160, 192, pixels)
    groups.append(story)

    girl = Group('school-girl', 'Dziewczyna: chód, portret, zbliżenie',
                 'build/*.rgba + school_story', SCHOOL)
    for index in range(4):
        girl.add_rgba(f'walk-{index}', rgba_file('build/girl-walk-cycle-v177.rgba',
                                                 96, 128).crop(
            ((index % 2) * 48, (index // 2) * 64,
             (index % 2 + 1) * 48, (index // 2 + 1) * 64)))
    girl.add_rgba('far', rgba_file('build/north-girl.rgba', 48, 64))
    girl.add_rgba('close', rgba_file('build/north-girl-close.rgba', 96, 128))
    girl.add_rgba('cutout', rgba_file('build/school-girl-cutout-v176.rgba', 160, 64))
    side_rgb = Path('build/school-girl-side-v033.rgb').read_bytes()
    girl.add_indexed('side', 160, 64,
                     bytes(school_story.color(side_rgb[i:i + 3])
                           for i in range(0, len(side_rgb), 3)))
    groups.append(girl)

    walk = Group('arena-walk-girl', 'Dziewczyna idąca przed Atari Arena (18 klatek)',
                 'school_parallax.frames()', SCHOOL)
    for index, pixels in enumerate(school_parallax.frames()):
        walk.add_indexed(f'walk-{index:02d}', 160, 64, pixels)
    groups.append(walk)

    practice = Group('school-practice', 'Trening: trzy ujęcia',
                     'gym_practice.practice_pixels()', GYM)
    pixels = gym_practice.practice_pixels()
    for index in range(3):
        practice.add_indexed(f'shot-{index}', 160, 64,
                             pixels[index * 64 * 160:(index + 1) * 64 * 160])
    groups.append(practice)

    # -- dance ----------------------------------------------------------
    cheer = Group('cheer-dance', 'Tancerka z pompomami (przód)',
                  'ribbon_dance.artwork()', RIBBON)
    for frame in range(36):
        if 16 <= frame < 32:
            continue  # gym-only backdrops, no character
        cheer.add_indexed(f'front-{frame:02d}', 160, 64,
                          ribbon_dance.artwork(frame)[0])
    groups.append(cheer)

    side = Group('ribbon-side', 'Tancerka z boku (overlay z maską)',
                 'ribbon_dance.side_actor_data()', None)
    for pose in range(8):
        raw = ribbon_dance.side_actor_data(pose)
        pixels = bytearray()
        mask = bytearray()
        for row in range(56):
            pixels.extend(unpack2(raw[row * 17:(row + 1) * 17])[:68])
            keep = unpack2(raw[1024 + row * 17:1024 + (row + 1) * 17])[:68]
            mask.extend(1 if value == 0 else 0 for value in keep)
        image = Image.new('RGBA', (68, 56))
        image.putdata([(*(RIBBON[value] if value else (0, 0, 0)),
                        255 if keep else 0) for value, keep in zip(pixels, mask)])
        side.add_rgba(f'side-{pose}', image)
    groups.append(side)

    between = Group('ribbon-inbetweens', 'Tancerka: klatki pośrednie',
                    'ribbon_inbetweens.payloads()', RIBBON)
    for index, (_, _, payload) in enumerate(ribbon_inbetweens.payloads()):
        between.add_indexed(f'inbetween-{index:02d}', 160, 64,
                            unpack2(ribbon_inbetweens.decompress(payload)))
    groups.append(between)

    # -- Trevor ---------------------------------------------------------
    panels = Group('trevor-panels', 'Trevor: cztery panele', 'trevor_polished.frames()', TREVOR)
    for index, pixels in enumerate(trevor_polished.frames()):
        panels.add_indexed(f'panel-{index}', 160, 64, pixels)
    groups.append(panels)

    tunnel = Group('trevor-tunnel', 'Trevor: tunel 16 faz x 4 etapy',
                   'trevor_polished.tunnel_frames()', TREVOR)
    for phase in range(16):
        punches = trevor_polished.tunnel_frames(phase)
        for stage in range(4):
            tunnel.add_indexed(f'phase-{phase:02d}-stage-{stage}', 160, 64,
                               punches[stage])
    groups.append(tunnel)

    # -- hero -----------------------------------------------------------
    hero = Group('hero-basketball', 'Koszykarz: pozy i rozpad tablicy',
                 'basketball_hero.frames()/shattered_frame()', HERO)
    for index, pixels in enumerate(basketball_hero.frames()):
        hero.add_indexed(f'pose-{index}', 160, 56, pixels)
    for stage in (1, 2, 3):
        hero.add_indexed(f'shatter-{stage}', 160, 56,
                         basketball_hero.shattered_frame(stage))
    groups.append(hero)

    # -- final ----------------------------------------------------------
    final = Group('final-boy', 'Chłopiec w finale', 'final_boy.artwork()', FINAL)
    final.add_indexed('final-boy', 160, 64, final_boy.artwork())
    groups.append(final)

    # -- portraits / eyes ----------------------------------------------
    portraits = Group('crush-portraits', 'Portrety dziewczyn (4 ujęcia)',
                      'crush_portraits.portraits()', ART)
    for index, pixels in enumerate(crush_portraits.portraits()):
        portraits.add_indexed(f'portrait-{index}', 80, 52, pixels)
    groups.append(portraits)

    pompoms = Group('crush-pompoms', 'Portrety z ruchomymi pompomami',
                    'pompom_effects.variants()', ART)
    for shot, phases in enumerate(pompom_effects.variants()):
        for phase, pixels in enumerate(phases):
            pompoms.add_indexed(f'shot-{shot}-phase-{phase}', 80, 52, pixels)
    groups.append(pompoms)

    eyes = Group('girl-eyes', 'Oczy dziewczyny (4 fazy)', 'girl_eyes.pixels()', EYES)
    for index in range(4):
        eyes.add_indexed(f'eyes-{index}', 160, 96, girl_eyes.pixels(index))
    groups.append(eyes)

    return groups


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=ROOT / f'dumps/{DATE}/characters')
    parser.add_argument('--replace', action='store_true')
    parser.add_argument('--scale', type=int, default=4)
    parser.add_argument('--group', action='append', default=None,
                        help='only these character slugs (repeatable)')
    parser.add_argument('--flat', action='store_true',
                        help='write a single selected group directly into --output')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()) and not args.replace:
        raise SystemExit(f'{output} is not empty; pick a new directory or --replace')

    build_sha = hashlib.sha256(BUILD.read_bytes()).hexdigest()
    reference_sha = hashlib.sha256(REFERENCE.read_bytes()).hexdigest()
    groups = build_groups()
    if args.group:
        wanted = set(args.group)
        groups = [group for group in groups if group.slug in wanted]
        missing = wanted - {group.slug for group in groups}
        if missing:
            raise SystemExit(f'unknown groups: {sorted(missing)}')
        if args.flat and len(groups) != 1:
            raise SystemExit('--flat requires exactly one --group')
    summary = []
    total_frames = total_unique = 0

    for group in groups:
        before = len(group.frames)
        unique = group.dedupe()
        total_frames += before
        total_unique += unique
        folder = output if args.flat else output / group.slug
        contact_frames = []
        for name, width, height, pixels, image in group.frames:
            if image is not None:
                frame = image
                save_rgba(folder / f'{name}.png', frame)
            else:
                save_indexed(folder / f'{name}.png', width, height, pixels, group.palette)
                frame = indexed_image(width, height, pixels, group.palette)
            save_preview(folder / '4x' / f'{name}.png', frame, args.scale)
            contact_frames.append(frame)
        contact(folder / '_contact-2x.png', contact_frames)
        summary.append({
            'slug': group.slug,
            'title': group.title,
            'source': group.source,
            'frames_input': before,
            'frames_unique': unique,
            'duplicates': group.aliases,
            'sizes': sorted({(frame[1], frame[2]) for frame in group.frames}),
            'palette': ([list(c) for c in group.palette] if group.palette else None),
        })
        print(f'{group.slug:20} {before:3} -> {unique:3} unikalnych')

    manifest = {
        'generated': DATE,
        'kind': 'character animation frames, exact duplicates removed',
        'source': {'build': str(BUILD.relative_to(ROOT)), 'sha256': build_sha,
                   'release': str(REFERENCE.relative_to(ROOT)),
                   'release_sha256': reference_sha},
        'format': {'indexed': '1:1 PNG, index = raw Atari pixel value',
                   'rgba': 'source sprite with alpha; mask stored separately',
                   'preview': '4x nearest neighbour',
                   'contact': '2x contact sheet per character'},
        'totals': {'frames': total_frames, 'unique': total_unique,
                   'removed': total_frames - total_unique},
        'groups': summary,
        'notes': [
            'Trevor/tunel: 64 klatki różnią się tłem tunelu; postać ma 4 etapy.',
            'Taniec: klatki 16-31 to samo tło sali bez tancerki, więc pominięte.',
            'Chłopiec szkolny i trening mają tło wpieczone w klatkę.',
            'Dziewczyna szkolna jest zapisana jako sprite z alfą (źródło builda).',
            'school-girl/walk-0..3 to arkusz girl-walk-cycle-v177; bieżący montaż go nie używa.',
            'Nieużywane arkusze (girl_back_art, walk_head_art, boy-whistle, hero-v177) pominięto.',
        ],
    }
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')

    lines = [f'# Klatki postaci — {DATE}', '',
             f'Źródło: `{BUILD.relative_to(ROOT)}` (SHA-256 `{build_sha}`).',
             f'Wydanie referencyjne: `{REFERENCE.relative_to(ROOT)}`.', '',
             f'Klatek wejściowych: {total_frames}; unikalnych: {total_unique}; '
             f'usunięto dokładnych duplikatów: {total_frames - total_unique}.', '',
             '| postać | klatek | unikalnych | rozmiary | źródło |',
             '| --- | ---: | ---: | --- | --- |']
    for item in summary:
        sizes = ', '.join(f'{w}×{h}' for w, h in item['sizes'])
        lines.append(f'| {item["slug"]} | {item["frames_input"]} | '
                     f'{item["frames_unique"]} | {sizes} | `{item["source"]}` |')
    lines += ['', '## Uwagi', '']
    lines += [f'- {note}' for note in manifest['notes']]
    lines += ['', 'Klatki 1:1 są indeksowane; sprite’y dziewczyny i boku tancerki',
              'mają kanał alfa oraz osobną maskę `*-mask.png`.', '']
    (output / 'CHARACTERS.md').write_text('\n'.join(lines) + '\n')
    print(f'\n{total_unique} unikalnych klatek w {output}')


if __name__ == '__main__':
    main()
