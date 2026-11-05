"""Load video XEX segments and execute the under-ROM asset INIT for previews."""

from functools import lru_cache

from py65.devices.mpu6502 import MPU

from extract_music import segments


@lru_cache(maxsize=2)
def video_memory(data):
    cpu = MPU()
    cpu.memory[0xd301] = 0xff
    for start, end, payload in segments(data):
        cpu.memory[start:end + 1] = payload
        if (start, end) == (0x02e2, 0x02e3) and payload == b'\x00\x10':
            if cpu.memory[0x1000:0x1006] == list(bytes.fromhex('08 78 ad 01 d3 48')):
                continue  # Bank INIT is modeled by RuntimeMemory, not flat RAM.
            cpu.pc, cpu.sp = 0x1000, 0xfd
            cpu.memory[0x1fe:0x200] = [0xfe, 0x7f]
            for _ in range(100000):
                if cpu.pc == 0x7fff:
                    break
                cpu.step()
            else:
                raise ValueError('under-ROM asset INIT did not return')
    return tuple(cpu.memory)


class RuntimeMemory:
    """Unbanked CPU RAM plus the fourteen banks loaded by the v035 loader."""

    def __init__(self, data):
        self.ram = list(video_memory(data))
        self.banks = [bytearray(payload) for start, end, payload in segments(data)
                      if (start, end) == (0x8000, 0xbfff)]
        extra = [bytearray(payload) + bytearray(8192) for start,end,payload in segments(data)
                 if (start,end)==(0x8000,0x9fff)]
        self.banks.extend(extra)
        self.values = self.ram[0x26fc:0x270a]
        if len(set(self.values)) != 14:
            # The real loader fills this table during expansion detection.
            self.values = [0x80, 0x82, 0x84, 0x86, 0x88, 0x8a, 0x8c,
                           0x8e, 0xa0, 0xa2, 0xa4, 0xa6, 0xa8, 0xaa]
            self.ram[0x26fc:0x270a] = self.values
        for index in range(len(self.banks)-14):
            candidate=([b+i for b in (0x80,0xa0,0xc0,0xe0,0x00,0x20,0x40,0x60) for i in range(0,16,2)][14+index] if self.values[0]==0x80 else self.values[13]+(index+1)*4)
            self.values.append(candidate)
            self.ram[0x24b3+index if index<3 else 0x08c0+index]=candidate

    def __getitem__(self, address):
        if isinstance(address, slice):
            return [self[index] for index in range(*address.indices(65536))]
        value = self.ram[0xd301] & 0xfe
        if 0x4000 <= address < 0x8000 and value in self.values:
            return self.banks[self.values.index(value)][address - 0x4000]
        return self.ram[address]

    def __setitem__(self, address, value):
        if isinstance(address, slice):
            for index, byte in zip(range(*address.indices(65536)), value):
                self[index] = byte
            return
        selected = self.ram[0xd301] & 0xfe
        if 0x4000 <= address < 0x8000 and selected in self.values:
            self.banks[self.values.index(selected)][address - 0x4000] = value
        else:
            self.ram[address] = value
