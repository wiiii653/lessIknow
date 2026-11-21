"""Alternating appearances, full stored cycles, bank ownership and NMI."""
import unittest
import json
import test_sequence as seq
import banana_variants as variants
import mosaic
from girl_eyes import frame_at as eye_frame_at
from post_trevor_director import START, END, frame_at
from test_engine_cache import TrackedMemory


def live_banana_frames():
    """One real montage tick for each stored phase of both motifs."""
    first_ticks={}
    for tick in range(START,END,8):
        frame=eye_frame_at(tick,frame_at(tick))
        if frame<32:first_ticks.setdefault((frame,variants.variant_at(tick)),tick)
    return sorted((tick,frame,variant) for (frame,variant),tick in first_ticks.items())


def banana_raster(frame,variant):
    pixels=mosaic.pixels(frame,variant)
    return b''.join(pixels[y:y+160]*2 for y in range(0,len(pixels),160))


class BananaVariantTests(unittest.TestCase):
    def test_all_64_camera_views_compose_into_the_inactive_buffer(self):
        cpu=seq.MPU(memory=TrackedMemory(seq.XEX.read_bytes()))
        samples=live_banana_frames()
        self.assertEqual(len(samples),64)
        for tick,frame,variant in samples:
            m=cpu.memory;front=0x9000 if m[0xd403]==0x84 else 0xb000
            m.writes.clear();before=cpu.processorCycles
            seq.execute(tick,cpu)
            self.assertLess(cpu.processorCycles-before,90000,(variant,frame))
            self.assertEqual(seq.SequenceTests().raster(cpu),banana_raster(frame,variant))
            self.assertFalse(any(front<=a<front+3840 for a in m.writes),(variant,frame))
            self.assertEqual(m[0xd301],0xff)
            self.assertEqual(m[0x83fa],0xff)

    def test_decoder_survives_original_music_nmi_and_restores_portb(self):
        samples=live_banana_frames()
        for tick,frame,variant in (samples[0],next(s for s in samples if s[2]==1),samples[-1]):
            m=seq.RuntimeMemory(seq.XEX.read_bytes());cpu=seq.MPU(memory=m)
            m[0xd301]=m.values[3];m[0xd40b]=124
            for address in (0x232d,0x237d):
                cpu.pc=address;cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
                for _ in range(10000):
                    if cpu.pc==0x7fff:break
                    cpu.step()
                else:self.fail('music init did not return')
            for i in range(3):m[0x24a7+i]=tick>>(8*i)&255
            m[0xd301]=0xff;cpu.pc=json.loads(seq.METADATA.read_text())['callback'];cpu.sp=0xfd
            m[0x1fe:0x200]=[0xfe,0x7f];deadline=cpu.processorCycles+1000;count=0
            for _ in range(100000):
                if cpu.pc==0x7fff:break
                if cpu.processorCycles>=deadline:
                    bank,pc=m[0xd301],cpu.pc;cpu.nmi()
                    for _ in range(10000):
                        cpu.step()
                        if cpu.pc==pc:break
                    else:self.fail('NMI did not return')
                    self.assertEqual(m[0xd301],bank);count+=1;deadline=cpu.processorCycles+8880
                cpu.step()
            else:self.fail('callback did not return')
            self.assertGreater(count,4)
            self.assertEqual(seq.SequenceTests().raster(cpu),banana_raster(frame,variant))
            self.assertEqual(m[0xd301],0xff)
