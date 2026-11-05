#!/usr/bin/env python3
"""Audit staged music banks; optionally trace the original v035 decoder (py65)."""

import argparse
import json
from pathlib import Path

from extract_music import segments


def trace(entries, banks, protected_ranges=()):
    from py65.devices.mpu6502 import MPU

    # Distinct expansion-bank values from the player's first detection table.
    values = (0x81, 0x83, 0x85, 0x87, 0x89, 0x8b, 0x8d,
              0x8f, 0xa1, 0xa3, 0xa5, 0xa7, 0xa9, 0xab)
    if len(banks) != len(values):
        raise ValueError('trace expects fourteen v035 staging banks')

    class Memory:
        def __init__(self):
            self.ram = [0] * 65536
            self.bank = 0
            self.reads = [set() for _ in banks]

        def __getitem__(self, address):
            if isinstance(address, slice):
                return self.ram[address]
            if any(lo <= address < hi for lo, hi in protected_ranges):
                raise ValueError(f'music reads video RAM at ${address:04X}')
            if 0x4000 <= address < 0x8000:
                offset = address - 0x4000
                self.reads[self.bank].add(offset)
                return banks[self.bank][offset]
            return self.ram[address]

        def __setitem__(self, address, value):
            if any(lo <= address < hi for lo, hi in protected_ranges):
                raise ValueError(f'music writes video RAM at ${address:04X}')
            self.ram[address] = value
            if address == 0xd301:
                self.bank = values.index(value)

    memory = Memory()
    for start, end, payload in entries:
        if (start, end) != (0x8000, 0xbfff):
            memory.ram[start:end + 1] = payload
    for address, expected in ((0x2210, bytes.fromhex('48 8a 48 98 48')),
                              (0x2351, bytes.fromhex('a0 00 b1 a0')),
                              (0x3180, bytes.fromhex('a9 00 8d c8 24'))):
        if bytes(memory.ram[address:address + len(expected)]) != expected:
            raise ValueError(f'unexpected v035 routine at ${address:04X}')
    memory.ram[0x26fc:0x270a] = values
    cpu = MPU(memory=memory)

    def run_until(return_address):
        for _ in range(10000):
            if cpu.pc == return_address:
                return
            cpu.step()
        raise ValueError(f'player did not return: PC=${cpu.pc:04X}')

    def call(address):
        cpu.pc, cpu.sp = address, 0xfd
        memory.ram[0x1fe:0x200] = [0xfe, 0x7f]
        run_until(0x7fff)

    call(0x232d)  # real v035 restart/clock initialization
    call(0x237d)  # prime first register packet, as RUN does
    for tick in range(70000):
        if memory.ram[0x24c8]:
            break
        # NMI return stack: saved P, low PC, high PC. Execute the real handler.
        cpu.sp = 0xfa
        memory.ram[0x1fb:0x1fe] = [0x20, 0, 7]
        cpu.pc = 0x2210
        run_until(0x0700)
    else:
        raise ValueError('no end marker within 70,000 music updates')
    return tick, memory.reads


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xex', type=Path, nargs='?', default=Path('less-i-know-release-v035.xex'))
    parser.add_argument('--trace', action='store_true', help='execute the v035 decoder with py65')
    parser.add_argument('--json', type=Path, help='write machine-readable report')
    args = parser.parse_args()
    entries = list(segments(args.xex.read_bytes()))
    banks = [payload for start, end, payload in entries if (start, end) == (0x8000, 0xbfff)]
    if not banks:
        parser.error('no staging banks at $8000–$BFFF')
    ticks, reads = trace(entries, banks) if args.trace else (None, None)
    report = {'source': args.xex.name, 'bank_size': 16384, 'bank_count': len(banks),
              'decoder_updates_to_end': ticks, 'banks': []}
    for index, bank in enumerate(banks):
        last = next((i for i in range(len(bank) - 1, -1, -1) if bank[i] != 0xff), -1)
        row = {'bank': index + 1, 'all_ff': last == -1, 'trailing_ff_bytes': len(bank) - last - 1}
        if reads is not None:
            used = reads[index]
            row.update(read_bytes=len(used), unread_bytes=len(bank) - len(used),
                       highest_read_offset=max(used) if used else None)
            if used and used != set(range(max(used) + 1)):
                raise ValueError('noncontiguous bank reads; inspect before reclaiming gaps')
        report['banks'].append(row)
        print(f"Bank {index + 1:2}: trailing FF {row['trailing_ff_bytes']:5} bytes"
              + (f"; decoder read {len(reads[index]):5} bytes" if reads is not None else ''))
    if reads is not None:
        report['reserved_bytes'] = sum(map(len, banks))
        report['read_bytes'] = sum(map(len, reads))
        report['unread_bytes'] = report['reserved_bytes'] - report['read_bytes']
        print(f"Total reserved {report['reserved_bytes']:,}; read {report['read_bytes']:,}; "
              f"unread {report['unread_bytes']:,} bytes; {ticks:,} updates to end.")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
