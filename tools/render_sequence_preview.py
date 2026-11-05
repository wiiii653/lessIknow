#!/usr/bin/env python3
"""Render live bitmap display-list scanlines after executing the 6502 callback.

Requires optional py65. Colors are approximate; vertical gaps are rendered,
not hidden, so DLI seam regressions are visible in these previews.
"""

import json
from pathlib import Path

from py65.devices.mpu6502 import MPU

from build_sequence import PALETTE
from scene_memory import video_memory, RuntimeMemory
from pmg_preview import player_masks, atari_rgb


def preview(tick, name):
    info = json.loads(Path('build/visual-prototype-v051.json').read_text())
    cpu = MPU(memory=RuntimeMemory(Path('build/visual-prototype-v051.xex').read_bytes()))
    cpu.memory[0x23cd] = 0x60
    cpu.memory[0xd40b] = 124
    for offset in range(3):
        cpu.memory[0x24a7 + offset] = (tick >> (8 * offset)) & 255
    cpu.sp = 0xfd
    cpu.memory[0x1fe:0x200] = [0xfe, 0x7f]
    cpu.pc = info['callback']
    for _ in range(100000):
        if cpu.pc == 0x7fff:
            break
        cpu.step()
    else:
        raise ValueError('scene callback did not return')
    memory = cpu.memory
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
        elif mode == 14 and op & 0x40:
            address = fetch() | fetch() << 8
            for byte in memory[address:address + 40]:
                for shift in (6, 4, 2, 0):
                    indices.append((byte >> shift) & 3)
        else:
            raise ValueError(f'unsupported preview mode: ${op:02X}')
    else:
        raise ValueError('display list did not terminate')
    height = len(indices) // 160
    indices = player_masks(indices, memory, height, raster_start=8)
    original={0:PALETTE[0],0x48:PALETTE[1],0x9a:PALETTE[2],0x2c:PALETTE[3],0x82:(12,24,48)}
    palette=tuple(original.get(color,atari_rgb(color)) for color in
                  (memory[0xd01a],memory[0xd016],memory[0xd017],memory[0xd018]))
    pixels = bytes(channel for index in indices for channel in (palette[index] if index<4 else atari_rgb((index-4)*2)))
    path = Path(f'build/{name}-raster.ppm')
    path.write_bytes(f'P6\n160 {height}\n255\n'.encode() + pixels)
    print(path)


if __name__ == '__main__':
    for tick, name in ((96, 'artist'), (1592, 'title'), (2992, 'school-front'), (4488, 'school-girl-left'),
                       (4862, 'school-girl-receding'), (5236, 'school-girl-near-school'),
                       (5610, 'school-girl-at-entrance'),
                       (5984, 'practice-closeup'), (6981, 'practice-shot'), (7978, 'practice-stretch'), (9152, 'dance-solo'),
                       (9808, 'dance-duo'), (10560, 'dance-trio'),
                       (11968, 'kaleidoscope')):
        preview(tick, name)
