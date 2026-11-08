"""Moving PAL VCOUNT regression for the PMG frame-boundary race.

Instruction timing plus an optional synthetic CPU stall; not ANTIC emulation.
"""
import json
import unittest
import test_sequence as sequence
from scene_memory import RuntimeMemory


class BeamMemory(RuntimeMemory):
    def __init__(self, data):
        super().__init__(data)
        self.cpu = None
        self.start = 0
        self.events = []

    def __getitem__(self, address):
        if address == 0xd40b and self.cpu is not None:
            return ((self.start + self.cpu.processorCycles) // 114 % 312) // 2
        return super().__getitem__(address)

    def __setitem__(self, address, value):
        if self.cpu is not None and isinstance(address, int):
            if 0x980 <= address < 0xc00 or 0x8980 <= address < 0x8c00 or 0xd000 <= address <= 0xd01d or address == 0xd400:
                self.events.append((self.start + self.cpu.processorCycles, address, value))
        super().__setitem__(address, value)


class TunnelRasterTests(unittest.TestCase):
    def test_late_callbacks_keep_ball_enabled_and_finish_before_satellites(self):
        for tick in (33024, 33152, 34560, 38904):
            for start in (0, 248, 254, 255, 256, 290, 300, 305, 306, 307, 311):
                for stall in (0, 3500):
                    with self.subTest(tick=tick, line=start, stall=stall):
                        memory = BeamMemory(sequence.XEX.read_bytes())
                        cpu = sequence.MPU(memory=memory)
                        sequence.execute(tick, cpu)  # Fully initialized previous overlay.
                        active=(memory[0xd407]&0xfc)<<8
                        cpu.processorCycles = 0
                        memory.start = start * 114
                        memory.cpu = cpu
                        memory.events.clear()
                        cpu.pc = json.loads(sequence.METADATA.read_text())['callback']
                        cpu.sp = 0xfd
                        memory[0x1fe:0x200] = [0xfe, 0x7f]
                        paused = False
                        for _ in range(100000):
                            if cpu.pc == 0x7fff:
                                break
                            cpu.step()
                            if not paused and any(0x980 <= a < 0xc00 for _, a, _ in memory.events):
                                cpu.processorCycles += stall
                                paused = True
                        else:
                            self.fail('callback did not return')
                        writes = [(t, a, v) for t, a, v in memory.events if 0x980 <= a < 0xc00 or 0x8980 <= a < 0x8c00]
                        self.assertTrue(writes)
                        first_line = writes[0][0] / 114
                        self.assertGreaterEqual(first_line % 312, 248)
                        self.assertLess(first_line % 312, 257)
                        next_frame = (int(first_line) // 312 + 1) * 312
                        self.assertLess(memory.events[-1][0] / 114, next_frame + 48)
                        self.assertFalse(any(a == 0xd01d and v != 3 for _, a, v in memory.events))
                        self.assertFalse(any(a == 0xd400 and v != 0x2e for _, a, v in memory.events))
