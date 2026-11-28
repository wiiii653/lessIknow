"""Real extra poses, unchanged musical accents and fast banked decompression."""
import unittest
import test_sequence as seq
import ribbon_dance as d
import ribbon_inbetweens as mid
from test_engine_cache import TrackedMemory


class RibbonInbetweenTests(unittest.TestCase):
    def test_every_original_accent_and_camera_cut_keeps_its_pose(self):
        for step,tick in enumerate(d.STEPS):
            self.assertEqual(d.frame_at(tick),d.frame_for_step(step))
        for tick in range(d.LAUNCH_PREP,d.END,4):
            step=max(i for i,t in enumerate(d.STEPS) if t<=tick)
            self.assertEqual(d.frame_at(tick),d.frame_for_step(step))
        for tick in range(d.SIDE_START,d.SIDE_END,16):
            self.assertEqual(d.frame_at(tick),16+((tick>>4)&15))

    def test_midpoints_are_exactly_halfway_and_never_bridge_camera_cuts(self):
        seen=set()
        for step in range(117):
            tick=(d.STEPS[step]+d.STEPS[step+1])//2
            self.assertIn(tick-d.STEPS[step],(23,24))
            index=mid.step_midpoint(step)
            if index is None:
                self.assertEqual(d.frame_at(tick),d.frame_for_step(step))
            else:
                self.assertEqual(d.frame_at(tick-1),d.frame_for_step(step))
                selected=37+index
                self.assertEqual(d.frame_at(tick),selected)
                self.assertEqual(d.frame_at(d.STEPS[step+1]-1),selected)
                seen.add(index)
        self.assertEqual(seen,set(range(14)))
        self.assertIsNone(mid.step_midpoint(31));self.assertIsNone(mid.step_midpoint(63))

    def test_all_fourteen_new_frames_decode_and_have_new_body_and_hand_shapes(self):
        for index,(a,b) in enumerate(mid.PAIRS):
            pixels,hands=mid.artwork(index)
            self.assertNotEqual(pixels,d.artwork(a)[0])
            self.assertNotEqual(pixels,d.artwork(b)[0])
            self.assertEqual(len(hands),4)
            encoded=mid.payloads()[index][2]
            self.assertEqual(mid.decompress(encoded),mid.packed(index))
        self.assertEqual(len(set(mid.POSES)),9)
        for index in range(14,18):
            bank,source,encoded=mid.payloads()[index]
            self.assertEqual(bank,32+index-14)
            self.assertEqual(source,mid.payloads()[index-7][1]+len(mid.payloads()[index-7][2]))
            self.assertEqual(mid.decompress(encoded),mid.packed(index))
        self.assertLess(sum(len(data) for bank,source,data in mid.payloads()),22000)

    def test_live_solo_midpoints_decode_from_banks_with_the_decoder_installed(self):
        cpu=None;seen=set();costs=[]
        for step in range(32,64):
            index=mid.step_midpoint(step)
            if index not in range(6,10) or index in seen:continue
            seen.add(index)
            start=d.STEPS[step];tick=(start+d.STEPS[step+1])//2
            cpu=seq.execute(start,cpu);before=cpu.processorCycles
            cpu=seq.execute(tick,cpu);costs.append(cpu.processorCycles-before)
            pixels,hands=mid.artwork(index)
            expected=bytes(pixels[y//3*160+x] for y in range(192) for x in range(160))
            m=cpu.memory
            self.assertEqual(seq.SequenceTests().raster(cpu),expected,(step,index))
            self.assertEqual(m[0xd000:0xd004],[max(0,min(255,x+34)) for x,y in hands])
            self.assertEqual(m[0xd301],0xff)
            self.assertEqual(m[0x83e5],128)
        self.assertEqual(seen,set(range(6,10)))
        self.assertLess(max(costs),120000)

    def test_live_midpoints_match_all_new_compositions_and_restore_endpoint_anchors(self):
        cpu=None;seen=set();costs=[]
        for step in range(117):
            index=mid.step_midpoint(step)
            if index is None or index in seen:continue
            seen.add(index)
            start=d.STEPS[step];tick=(start+d.STEPS[step+1])//2
            cpu=seq.execute(start,cpu);before=cpu.processorCycles
            cpu=seq.execute(tick,cpu);costs.append(cpu.processorCycles-before)
            m=cpu.memory
            pixels,hands=d.scene_artwork(tick)
            expected=bytes(pixels[y//3*160+x] for y in range(192) for x in range(160))
            self.assertEqual(seq.SequenceTests().raster(cpu),expected,(step,index))
            self.assertEqual(m[0xd000:0xd004],[max(0,min(255,x+34)) for x,y in hands])
            self.assertEqual(m[0xd301],0xff)
            self.assertEqual(m[0x83e5],128)
            # A subsequent original accent must restore its own hand anchors.
            cpu=seq.execute(d.STEPS[step+1],cpu)
            hands=d.scene_artwork(d.STEPS[step+1])[1]
            self.assertEqual(m[0xd000:0xd004],[max(0,min(255,x+34)) for x,y in hands])
            self.assertEqual(m[0x83e5],0)
        self.assertEqual(seen,set(range(14)))
        # CPU costs, not real DMA/FPS: retain headroom inside a 23-tick interval.
        self.assertLess(max(costs),120000)

    def test_held_midpoint_uses_the_bitmap_cache_and_only_prepares_back_pmg(self):
        tick=(d.STEPS[0]+d.STEPS[1])//2
        memory=TrackedMemory(seq.XEX.read_bytes());cpu=seq.MPU(memory=memory)
        seq.execute(tick,cpu);previous=bytes(seq.SequenceTests().raster(cpu))
        memory.writes.clear();before=cpu.processorCycles
        seq.execute(tick+4,cpu)
        self.assertEqual(seq.SequenceTests().raster(cpu),previous)
        self.assertFalse(any(0x9000<=a<0x9a00 or 0xb000<=a<0xba00 for a in memory.writes))
        self.assertLess(cpu.processorCycles-before,25000)
