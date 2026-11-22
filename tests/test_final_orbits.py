"""The orbit morph stays continuous on the player clock."""
import unittest
import test_sequence as seq
import final_orbits as orbit
import outro_text


def state(m,address):
    return m.banks[m.values.index(m[0x08f1])][address-0x4000]


class FinalOrbitTests(unittest.TestCase):
    def test_adjacent_orbit_shapes_ease_without_a_position_jump(self):
        for phase in range(32):
            for plane in range(4):
                for amount in range(7):
                    before=orbit.position(phase,amount,plane)
                    after=orbit.position(phase,amount+1,plane)
                    self.assertTrue(all(abs(a-b)<=5 for a,b in zip(before,after)),(phase,plane,amount))

    def test_extreme_orbits_are_visibly_tall_and_wide(self):
        tall=[orbit.position(p,0) for p in range(32)]
        wide=[orbit.position(p,7) for p in range(32)]
        extent=lambda pts,axis: max(p[axis] for p in pts)-min(p[axis] for p in pts)
        self.assertGreater(extent(tall,1),2*extent(wide,1))
        self.assertGreater(extent(wide,0),2*extent(tall,0))

    def test_morph_has_distinct_endpoints(self):
        for phase in (0,4,8,12):
            self.assertNotEqual(orbit.position(phase,0),orbit.position(phase,4))

    def test_morph_and_positions_follow_the_clock(self):
        start = outro_text.START
        cpu = None
        amounts = set()
        for tick in range(start, start+1024, 4):
            cpu = seq.execute(tick, cpu)
            amount = orbit.morph_amount(tick)
            phase = (tick >> orbit.PHASE_SHIFT) & orbit.PHASE_MASK
            expected = [orbit.animated_position(phase, amount, p)[0] for p in range(4)]
            self.assertEqual(state(cpu.memory, orbit.AMOUNT), amount, tick)
            self.assertEqual(cpu.memory[0xd000:0xd004], expected, tick)
            amounts.add(amount)
        self.assertEqual(amounts, set(range(8)))
        for tick in (start+400, start+400, start+64):
            seq.execute(tick, cpu)
            self.assertEqual(state(cpu.memory, orbit.AMOUNT), orbit.morph_amount(tick))
