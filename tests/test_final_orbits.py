"""Every typed line retargets the orbit without a position jump."""
import bisect
import unittest
import test_sequence as seq
import final_orbits as orbit
import outro_text


def state(m,address):
    return m.banks[m.values.index(m[0x08f1])][address-0x4000]


class FinalOrbitTests(unittest.TestCase):
    def test_adjacent_orbit_shapes_move_each_particle_at_most_one_pixel(self):
        for phase in range(16):
            for plane in range(4):
                for amount in range(7):
                    before=orbit.position(phase,amount,plane)
                    after=orbit.position(phase,amount+1,plane)
                    self.assertTrue(all(abs(a-b)<=1 for a,b in zip(before,after)),(phase,plane,amount))

    def test_every_line_eases_one_step_and_duplicate_callbacks_hold(self):
        events=orbit.events()
        self.assertEqual(len(events),sum(map(len,outro_text.pages())))
        self.assertTrue(all(a<b for a,b in zip(events,events[1:])))
        self.assertTrue(all(orbit.target_for(i)!=orbit.target_for(i+1) for i in range(len(events)-1)))
        cpu=None;amount=None;target=None;last_index=None;shapes=set()
        for tick in range(outro_text.START,outro_text.END,16):
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
            self.assertEqual(m[0xd000:0xd004],[orbit.position((tick>>4)&15,amount,p)[0] for p in range(4)],tick)
            shapes.add(amount)
            last_index=index
            if index and tick-events[index]<16:
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
                         [orbit.position((outro_text.START>>4)&15,orbit.target_for(0),p)[0] for p in range(4)])
