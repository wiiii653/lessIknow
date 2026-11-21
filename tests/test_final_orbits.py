"""Every typed line retargets the orbit without a position jump."""
import bisect
import unittest
import test_sequence as seq
import final_orbits as orbit
import outro_text


def state(m,address):
    return m.banks[m.values.index(m[0x08f1])][address-0x4000]


class FinalOrbitTests(unittest.TestCase):
    def test_adjacent_orbit_shapes_ease_without_a_position_jump(self):
        for phase in range(16):
            for plane in range(4):
                for amount in range(7):
                    before=orbit.position(phase,amount,plane)
                    after=orbit.position(phase,amount+1,plane)
                    self.assertTrue(all(abs(a-b)<=4 for a,b in zip(before,after)),(phase,plane,amount))

    def test_extreme_orbits_are_visibly_tall_and_wide(self):
        tall=[orbit.position(p,0) for p in range(16)]
        wide=[orbit.position(p,7) for p in range(16)]
        extent=lambda pts,axis: max(p[axis] for p in pts)-min(p[axis] for p in pts)
        self.assertGreater(extent(tall,1),2*extent(wide,1))
        self.assertGreater(extent(wide,0),2*extent(tall,0))

    def test_line_selected_paths_have_distinct_ellipses(self):
        for phase in (0,4,8,12):
            self.assertNotEqual(orbit.position(phase,0),orbit.position(phase,4))

    def test_every_line_eases_one_step_and_duplicate_callbacks_hold(self):
        events=orbit.events()
        self.assertEqual(len(events),sum(map(len,outro_text.pages())))
        self.assertTrue(all(a<b for a,b in zip(events,events[1:])))
        self.assertTrue(all(orbit.target_for(i)!=orbit.target_for(i+1) for i in range(len(events)-1)))
        cpu=None;amount=None;target=None;last_index=None;shapes=set()
        for tick in range(outro_text.START,outro_text.END,8):
            cpu=seq.execute(tick,cpu);m=cpu.memory
            index=bisect.bisect_right(events,tick)-1
            if amount is None:
                target=orbit.target_for(max(0,index));amount=target
            else:
                if index!=last_index:
                    old_target=target
                    target=orbit.target_for(max(0,index))
                    if target==amount:target^=7
                    if target==old_target:
                        target=(target+1)&7
                        if target==amount:target=(target+1)&7
                    self.assertNotEqual(target,amount,tick)
                    self.assertNotEqual(target,old_target,tick)
                amount+=int(target>amount)-int(target<amount)
            self.assertEqual(state(m,orbit.AMOUNT),amount,tick)
            self.assertEqual(m[0xd000:0xd004],[orbit.animated_position((tick>>orbit.PHASE_SHIFT)&31,amount,p)[0] for p in range(4)],tick)
            shapes.add(amount)
            last_index=index
            if index and tick-events[index]<8:
                seq.execute(tick,cpu)
                self.assertEqual(state(m,orbit.AMOUNT),amount,tick)
        self.assertGreaterEqual(len(shapes),7)

    def test_state_and_original_position_are_valid_after_reentry(self):
        cpu=seq.execute(outro_text.START+2000)
        amount=state(cpu.memory,orbit.AMOUNT)
        self.assertIn(amount,range(8))
        seq.execute(9163,cpu)
        seq.execute(outro_text.START,cpu)
        self.assertEqual(state(cpu.memory,orbit.AMOUNT),orbit.target_for(0))
        self.assertEqual(cpu.memory[0xd000:0xd004],
                         [orbit.animated_position((outro_text.START>>orbit.PHASE_SHIFT)&31,orbit.target_for(0),p)[0] for p in range(4)])
