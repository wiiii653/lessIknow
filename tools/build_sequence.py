#!/usr/bin/env python3
"""Shared scene artwork and NMOS 6502 code-emission helpers."""

from pathlib import Path

from build_title import render
from gym_background import dance_gym_pixels
from music_timing import tick_at_bar

TITLE_TICK = tick_at_bar(4)  # 4 bars = 7.5 seconds
DANCE_TICK = tick_at_bar(24)  # 24 bars = 45 seconds
PALETTE = ((0, 0, 0), (255, 50, 160), (0, 220, 255), (255, 190, 150))
DANCE_WIDTH, DANCE_HEIGHT = 48, 128
DANCE_SECOND_TICK = tick_at_bar(26)  # two bars later: 48.75 seconds
DANCE_THIRD_TICK = tick_at_bar(28)  # four bars later: 52.5 seconds
DANCE_LEFTS = (56, 4, 108)  # center first, then left, then right


class Code:
    """Small label/fixup emitter; every emitted instruction is NMOS 6502."""

    def __init__(self, origin):
        self.origin, self.data, self.labels, self.fixups = origin, bytearray(), {}, []

    def emit(self, *values):
        self.data.extend(values)

    def label(self, name):
        self.labels[name] = self.origin + len(self.data)

    def branch(self, opcode, name):
        self.emit(opcode, 0)
        self.fixups.append((len(self.data) - 1, name, True))

    def jump(self, opcode, name):
        self.emit(opcode, 0, 0)
        self.fixups.append((len(self.data) - 2, name, False))

    def finish(self):
        for pos, name, relative in self.fixups:
            address = self.labels[name]
            if relative:
                offset = address - (self.origin + pos + 1)
                if not -128 <= offset <= 127:
                    raise ValueError(f'branch out of range: {name}')
                self.data[pos] = offset & 255
            else:
                self.data[pos:pos + 2] = address.to_bytes(2, 'little')
        return self.data


def text_pixels(rows):
    return bytes(0 if v < 48 else 2 if v < 155 else 3 for v in render(rows))


def dance_pixels(frame):
    rgb = Path(f'build/dance-v056-{frame}.rgb').read_bytes()
    if len(rgb) != DANCE_WIDTH * DANCE_HEIGHT * 3:
        raise ValueError('expected 48x128 RGB dance frame')
    result = bytearray(160 * 192)
    for y in range(DANCE_HEIGHT):
        for x in range(DANCE_WIDTH):
            color = rgb[(y * DANCE_WIDTH + x) * 3:(y * DANCE_WIDTH + x) * 3 + 3]
            value = min(range(4), key=lambda i: sum(
                (color[c] - PALETTE[i][c]) ** 2 for c in range(3)))
            result[(y + 28) * 160 + x + 56] = value
    return result


def dance_group_pixels(frame, count=3):
    result = bytearray(dance_gym_pixels())
    # One-pixel dark outlines retain face details and separate the uniforms
    # from the lighter parquet. Exterior background remains transparent.
    for dancer, left in enumerate(DANCE_LEFTS[:count]):
        # A staggered chorus gives the group a readable wave of motion.
        pose = (frame + (0, 1, 3)[dancer]) & 3
        source = dance_pixels(pose)
        opaque = bytearray(160 * 192)
        for y in range(2, 190):
            for x in range(56, 104):
                at = y * 160 + x
                # Atari pixels are wide; a two-pixel expansion creates heavy
                # black legs. Keep just the immediate original outline there.
                neighbors = (0, -1, 1, -160, 160) if y >= 95 else (
                    0, -1, 1, -2, 2, -160, 160, -320, 320)
                opaque[at] = any(source[at + delta] for delta in neighbors)
        # Foot contacts move with each pose. The wide stance has two
        # separate shadows, while a raised foot leaves only one on the floor.
        contacts = (((25, 4),), ((23, 6),), ((18, 4),), ((8, 4), (37, 4)))
        for center, radius in contacts[pose]:
            for y in range(146, 150):
                for x in range(max(0, center-radius), min(48, center+radius+1)):
                    if ((x-center) / radius) ** 2 + ((y-147.5) / 2) ** 2 <= 1:
                        result[y * 160 + left + x] = 0
        for y in range(192):
            for x in range(48):
                at = y * 160 + 56 + x
                if opaque[at]:
                    result[y * 160 + left + x] = source[at]
    return result
