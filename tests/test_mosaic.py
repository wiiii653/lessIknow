"""All 64 frames, buffer ownership, bank probing and music interrupt safety."""
import unittest
import test_sequence as sequence
from mosaic import pixels, KALEIDO_START, TREVOR_START
from crush_portraits import START as CRUSH_START
from test_engine_cache import TrackedMemory
from school_portrait_bank import loader, bank_value
from extract_music import segments

@unittest.skipIf(sequence.MPU is None, 'py65 required')
class MosaicTests(unittest.TestCase):
    def test_all_frames_and_inactive_buffer_ownership(self):
        cpu=sequence.MPU(memory=TrackedMemory((sequence.ROOT/'build/visual-prototype-v070.xex').read_bytes()))
        for frame in range(64):
            tick=33792+(frame&31)*16+(1024 if frame>=32 else 0)
            # Inverse of ((tick>>4)&31) | ((tick>>5)&32).
            frame_expected=((tick>>4)&31)|((tick>>5)&32)
            active=cpu.memory[0xd403]<<8
            old_frame=0x9000 if active==0x8400 else 0xb000
            cpu.memory.writes.clear();before=cpu.processorCycles
            sequence.execute(tick,cpu)
            art=pixels(frame_expected)
            expected=bytes(art[y//2*160+x] for y in range(192) for x in range(160))
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected,frame)
            self.assertFalse(any(old_frame<=a<old_frame+3840 for a in cpu.memory.writes),frame)
            self.assertLess(cpu.processorCycles-before,90000)
            self.assertEqual(cpu.memory[0xd301],0xff)
            cpu.memory.writes.clear()
            sequence.execute(tick+1,cpu)
            self.assertFalse(any(0x9000<=a<0xaf00 or 0xb000<=a<0xcf00 for a in cpu.memory.writes))

    def test_last_bank_probe_preserves_all_prior_banks(self):
        cpu=sequence.execute(KALEIDO_START);m=cpu.memory
        m.banks[0][0]=0x55
        saved=[bytes(b) for b in m.banks[:32]]
        payload=bytes((i*19+i//256)&255 for i in range(16384))
        for lo,hi,data in segments(b'\xff\xff'+loader(payload,index=18)):
            if lo!=0x02e2:m[lo:hi+1]=data
        m[0xd301]=0xff;cpu.pc=0x1000;cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
        for _ in range(300000):
            if cpu.pc==0x7fff:break
            cpu.step()
        else:self.fail('last bank loader did not return')
        self.assertEqual([bytes(b) for b in m.banks[:32]],saved)
        self.assertEqual(bytes(m.banks[32]),payload)
        self.assertEqual(m[bank_value(18)],m.values[32])
        self.assertEqual(m[0xd301],0xff)

    def test_scene_handoffs_and_restart(self):
        cpu=None
        for tick,scene in ((KALEIDO_START-1,2+(((KALEIDO_START-1)>>5)&3)),(KALEIDO_START,6),(CRUSH_START-1,6),(CRUSH_START,14),
                           (TREVOR_START-1,16),(TREVOR_START,6),(96,0),(9163,2+((9163>>5)&3)),(KALEIDO_START,6)):
            cpu=sequence.execute(tick,cpu)
            self.assertEqual(cpu.memory[0x83e0],scene)
            if scene==6:self.assertEqual(cpu.memory[0xd01d],3)
