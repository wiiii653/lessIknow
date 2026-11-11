"""Compare playback against the available, structurally identical v198 anchor."""
import random
import unittest
import test_sequence as sequence
from test_engine_cache import TrackedMemory

BASELINE = sequence.ROOT / 'build/visual-prototype-v198.xex'


@unittest.skipIf(sequence.MPU is None, 'py65 required')
@unittest.skipUnless(BASELINE.exists(), 'archived v198 XEX required for comparison')
class OptimizationTests(unittest.TestCase):
    def pair(self):
        return [sequence.MPU(memory=TrackedMemory(path.read_bytes()))
                for path in (BASELINE, sequence.XEX)]

    def assert_equivalent(self, pair, tick):
        for cpu in pair:
            sequence.execute(tick, cpu)
            self.assertEqual(cpu.memory[0xd301], 0xff)
        from final_boy import START as OUTRO_START
        from trevor_awakens import END as MONTAGE_START
        if tick>=MONTAGE_START:return  # V248 translates the whole later sequence.
        if tick>=OUTRO_START:return  # Fixed lower framing, v240 starts 10 s earlier.
        if 41984<=tick<OUTRO_START and ((tick>>5)&32):return  # V231 tunnel-only beat direction/speed
        if 20615<=tick<20942:return  # V233 overhead wink/kiss and PMG heart
        # v252 reuses tunnel frames 60–63 for the eye close-up.
        if pair[1].memory[0x83e0]==6 and 60<=pair[0].memory[0x83ed]<64:return
        banana=pair[1].memory[0x83e0]==6 and pair[1].memory[0x83ed]<32
        if not banana:
            self.assertEqual(sequence.SequenceTests().raster(pair[0]),
                             sequence.SequenceTests().raster(pair[1]), tick)
        elif pair[0].memory[0x83ed]!=pair[1].memory[0x83ed]:
            return  # V236 continuous 32-phase banana/ball clock in Act 5
        if pair[1].memory[0x83e0]==14:return  # revised grip anchors/streams, bitmap checked above
        from trevor_awakens import HIT, END
        if HIT<=tick<END:return  # V247 replaces Trevor's PMG, bitmap checked above.
        for lo, hi in ((0xd000,0xd020),):
            old_values=pair[0].memory[lo:hi];new_values=pair[1].memory[lo:hi]
            if lo==0xd000 and pair[1].memory[0x83e0]<2:
                old_values[0x19]=new_values[0x19]  # stale missile colour after a seek
            if lo==0xd000 and not old_values[0x1d] and not new_values[0x1d]:
                # Disabled PMG registers retain values from the preceding scene.
                old_values[:0x16]=new_values[:0x16]
                old_values[0x19]=new_values[0x19]
            from banana_variants import variant_at
            if banana and variant_at(tick):
                self.assertEqual((new_values[0x16],new_values[0x18]),(0x1a,0x0e))
                old_values[0x16]=new_values[0x16];old_values[0x18]=new_values[0x18]
            from trevor_awakens import START,HIT
            if lo==0xd000 and START<=tick<HIT:
                self.assertEqual(new_values[0x16:0x19],[0x48,0x68,0x2a])
                old_values[0x16:0x19]=new_values[0x16:0x19]
            self.assertEqual(old_values,new_values,tick)
        old_base=(pair[0].memory[0xd407]&0xfc)<<8
        new_base=(pair[1].memory[0xd407]&0xfc)<<8
        # Disabled PMG RAM is scratch, not observable scene output.
        enabled=pair[1].memory[0xd01d]
        for bit,lo,hi in ((1,0x180,0x200),(2,0x200,0x400)):
            if enabled&bit:
                self.assertEqual(pair[0].memory[old_base+lo:old_base+hi],
                                 pair[1].memory[new_base+lo:new_base+hi],tick)

    def test_scene_handoffs_restarts_and_nonsequential_frames_match_v198(self):
        pair = self.pair()
        ticks = [0,1496,2992,3553,4862,5236,5984,8975,11967,14959,
                 17950,20942,23934,26925,32909,35900,41884,41984,
                 53850,56842,59085,59833,96,3553,59000]
        rng = random.Random(198)
        ticks.extend(rng.randrange(59834) for _ in range(12))
        for tick in ticks:
            self.assert_equivalent(pair,tick)

    def test_palette_and_orbit_edges_match_v198(self):
        pair = self.pair()
        for tick in (11967,11968,32909,32911,32912,53850,54015,54016,
                     56841,56842,59084,59085,59705,59833,65535):
            self.assert_equivalent(pair,tick)

    def test_held_callbacks_do_not_exceed_reference_cpu_cost(self):
        for start in (3553,12000,18000,21000,27000):
            pair = self.pair()
            for tick in range(start,start+32,4):
                costs=[]
                for cpu in pair:
                    before=cpu.processorCycles
                    sequence.execute(tick,cpu)
                    costs.append(cpu.processorCycles-before)
                self.assertLessEqual(costs[1],costs[0]+400,(start,tick))
