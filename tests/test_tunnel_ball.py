"""Tunnel ball stays in PMG RAM, spins, sparks and restores dance art."""
import unittest
import math
import test_sequence as sequence
from tunnel_ball import masks
from engine_effects import pmg_art
from mosaic import KALEIDO_START
from post_trevor_director import START, BUM_START, SHIFT, frame_at, timeline


def director_phase(tick, memory):
    # Position between two bitmap orientations, at the director's signed rate.
    mode = memory[0x0dda]
    rate = (-1 if mode & 128 else 1) * (2 if mode & 64 else 1)
    return 4*(memory[0x83ed] & 31) + rate*((tick >> 2) & 3)


def tunnel_drift(tick, memory):
    phase = director_phase(tick, memory)
    organic = memory[0x83ed] >= 48
    angle = (phase-64 if organic else phase)*math.tau/(48 if organic else 64)
    return round(5*math.sin(angle)), round(2*math.sin(2*angle))

@unittest.skipIf(sequence.MPU is None,'py65 required')
class TunnelBallTests(unittest.TestCase):
    def test_all_rotations_and_four_missiles(self):
        frames=masks();self.assertEqual(len({b''.join(f) for f in frames}),16)
        areas = [sum(byte.bit_count() for plane in frame for byte in plane) for frame in frames]
        self.assertEqual(len(set(areas)),1)
        self.assertGreater(areas[0],350)
        # Solid geometry stays fixed; only the panels and seams rotate.
        silhouettes={bytes(f[h][y]|f[h+2][y] for h in range(2) for y in range(32)) for f in frames}
        self.assertEqual(len(silhouettes),1)
        # Each physical half can contain both inks, so the boundary follows
        # the curved seam rather than a fixed player edge.
        self.assertTrue(any(any(f[0]) and any(f[2]) for f in frames))
        self.assertTrue(any(any(f[1]) and any(f[3]) for f in frames))
        for frame in frames:
            for y in range(32):
                self.assertEqual(frame[0][y]&frame[2][y],0)
                self.assertEqual(frame[1][y]&frame[3][y],0)
        pictures=set()
        for tick in range(KALEIDO_START,KALEIDO_START+256,16):
            cpu=sequence.execute(tick);m=cpu.memory
            self.assertEqual(m[0xd01b],0x11)
            self.assertEqual(m[0xd01d],3)
            dx,dy=tunnel_drift(tick, m)
            self.assertEqual(m[0xd000:0xd004],[112+dx,128+dx,112+dx,128+dx])
            for i in range(4):self.assertTrue(any(b&(3<<(2*i)) for b in m[0x980:0xa00]))
            origin=40+(m[0x83e9] if m[0x83e9]<128 else m[0x83e9]-256)
            key = (tick >> 4) & 15
            mix = (tick >> 2) & 3
            for plane in range(4):
                expected = bytes(frames[(key+(row % 4 < mix)) & 15][plane][row]
                                 for row in range(32))
                self.assertEqual(bytes(m[0xa00+plane*128+origin:0xa00+plane*128+origin+32]),expected,(tick,plane))
            raw=sequence.SequenceTests().raster(cpu)
            painted=sequence.SequenceTests().raster(cpu,effects=True)
            self.assertNotEqual(raw,painted)
            pictures.add(bytes(m[0xa00:0xc00]))
        self.assertEqual(len(pictures),16)

    def test_held_bitmap_and_clean_handoff(self):
        cpu=sequence.execute(11968)
        bitmap=sequence.SequenceTests().raster(cpu)
        sparks=cpu.memory[0x980:0xa00]
        before=cpu.processorCycles
        sequence.execute(11976,cpu)
        self.assertEqual(bitmap,sequence.SequenceTests().raster(cpu))
        self.assertNotEqual(sparks,cpu.memory[0x980:0xa00])
        self.assertLess(cpu.processorCycles-before,14000)
        sequence.execute(12288,cpu)
        self.assertEqual(cpu.memory[0xd01d],3)
        sequence.execute(9163,cpu)
        reference=sequence.execute(9163).memory
        def active(mem):
            base=(mem[0xd407]&0xfc)<<8
            return bytes(mem[base+0x180:base+0x400])
        self.assertEqual(active(cpu.memory),active(reference))
        self.assertEqual(cpu.memory[0xd01b],0x11)
        self.assertEqual(sequence.SequenceTests().raster(cpu,effects=True),
                         sequence.SequenceTests().raster(sequence.execute(9163),effects=True))

    def test_tunnel_ball_drift_wraps_at_pal_cadence_in_both_directions(self):
        passes = timeline()[:5]
        for (start, mode, _, _), (end, _, _, _) in zip(passes, passes[1:]):
            with self.subTest(mode=hex(mode)):
                cpu = previous = None
                low, high = (48, 59) if mode & 16 else (32, 47)
                wrap = (low, high) if mode & 128 else (high, low)
                wrapped = False
                for tick in range((start+3) & ~3, end, 4):
                    cpu = sequence.execute(tick, cpu)
                    memory = cpu.memory
                    frame = memory[0x83ed]
                    x, y = tunnel_drift(tick, memory)
                    self.assertEqual(memory[0xd000], 112+x)
                    self.assertEqual(memory[0x83e9], y & 255)
                    if previous is not None:
                        prev_frame, prev_x, prev_y = previous
                        wrapped |= (prev_frame, frame) == wrap
                        self.assertLessEqual(max(abs(x-prev_x), abs(y-prev_y)), 1, tick)
                    previous = frame, x, y
                self.assertTrue(wrapped)

    def test_rainbow_panels_and_satellites_keep_distinct_hues(self):
        colors=set()
        for tick in range(KALEIDO_START,KALEIDO_START+128,16):
            m=sequence.execute(tick).memory
            palette=tuple(m[a] for a in (0xd012,0xd013,0xd014,0xd015,0xd019))
            self.assertEqual(len({c>>4 for c in palette}),5)
            self.assertEqual(tuple(c&15 for c in palette[:4]),(8,10,14,12))
            self.assertEqual(palette[4]&15,14)
            self.assertEqual(m[0xd00c],0x55)
            colors.add(palette)
        self.assertEqual(len(colors),8)

    def test_rotator_ball_sweeps_both_sides_then_returns(self):
        from tunnel_ball import rotator_offsets, rotator_vertical_offsets
        offsets=rotator_offsets();self.assertEqual(offsets[0],0)
        vertical=rotator_vertical_offsets()
        self.assertGreater(max(vertical), 5)
        self.assertLess(min(vertical), -5)
        self.assertEqual(vertical[0], 0)
        self.assertEqual(vertical[32], 0)
        self.assertGreater(max(offsets),30);self.assertLess(min(offsets),-30)
        cpu=None
        ticks={}
        for tick in range(START,BUM_START,8):
            frame=frame_at(tick)
            if frame<32:ticks.setdefault(frame|(((tick+SHIFT)>>4)&32),tick)
        self.assertEqual(set(ticks),set(range(64)))
        for i,tick in sorted(ticks.items()):
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            self.assertEqual(m[0xd01d],3)
            angle = (director_phase(tick, m) + 4*(i & 32))*math.tau/256
            dx, dy = round(40*math.sin(angle)), round(8*math.sin(2*angle))
            self.assertEqual(m[0xd000],112+dx)
            self.assertEqual(m[0xd001],128+dx)
            self.assertEqual(m[0x83e9], dy & 255)
            self.assertTrue(any(m[0x980:0xa00]))
            for j in range(4):
                self.assertLessEqual(abs(m[0xd004+j]-(128+dx)),44)
        self.assertLessEqual(abs(offsets[-1]),4)
        centered=next(t for t in range(tick+1,BUM_START) if frame_at(t)==32)
        cpu=sequence.execute(centered,cpu)
        self.assertEqual(cpu.memory[0xd000],112)
        self.assertEqual(cpu.memory[0xd001],128)
        self.assertEqual(cpu.memory[0xd01d],3)

    def test_tunnel_bob_covers_central_hole_at_every_phase(self):
        from ribbon_dance import FRONT_PREP_STEPS
        cpu=None;positions=set()
        ticks={}
        for tick in range(KALEIDO_START,FRONT_PREP_STEPS[0],8):
            ticks.setdefault(frame_at(tick),tick)
        self.assertEqual(set(ticks),set(range(32,60)))
        for i,tick in sorted(ticks.items()):
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            # The eye frames occupy slots 60–63.
            dx,dy=tunnel_drift(tick, m);positions.add((dx,dy))
            self.assertEqual(m[0xd000],112+dx)
            self.assertEqual(m[0x83e9],dy&255)
            for x in range(75,86):
                for y in range(88,105):
                    if ((x-79.5)**2+((y//2-47.5)*1.66)**2)**0.5>=5:
                        continue
                    covered=False
                    for plane in range(4):
                        left=m[0xd000+plane]-48
                        col=(x-left)//2
                        if 0<=col<8 and m[0xa00+plane*128+(y+17)//2]&(0x80>>col):
                            covered=True;break
                    self.assertTrue(covered,(i,x,y))
        self.assertGreater(len(positions),12)

    def test_two_paired_missile_stars_follow_different_ellipses(self):
        cpu=None
        for j in range(64):
            cpu=sequence.execute(12288+j*4,cpu);m=cpu.memory
            dx=m[0x83e8] if m[0x83e8]<128 else m[0x83e8]-256
            dy=m[0x83e9] if m[0x83e9]<128 else m[0x83e9]-256
            for i in range(4):
                rx,ry=((25,14) if i<2 else (40,23))
                angle=(j+(0 if i<2 else 16))*math.tau/64
                half_offset=-4 if i%2==0 else 0
                self.assertEqual(m[0xd004+i],128+half_offset+round(rx*math.cos(angle))+dx)
                first=55+round(ry*math.sin(angle))+dy
                rows=[y for y in range(128) if m[0x980+y] & (3 << (2*i))]
                self.assertEqual(rows,list(range(first,first+5)))

    def test_eyes_ball_follows_figure_eight_at_pal_frame_cadence(self):
        from girl_eyes import START as EYES_START
        cpu = None
        positions = set()
        for tick in range(EYES_START+4, EYES_START+4+64, 4):
            cpu = sequence.execute(tick, cpu)
            frame = ((tick+SHIFT) >> 2) & 255
            dx = round(40*math.sin(math.tau*frame/256))
            dy = round(8*math.sin(math.tau*frame/128))
            self.assertEqual(cpu.memory[0xd000], 112 + dx)
            self.assertEqual(cpu.memory[0x83e9], dy & 255)
            positions.add((dx, dy))
        self.assertGreater(len(positions), 8)

    def test_reused_cycle_memory_and_original_tunnel_covering_are_separate(self):
        cpu=None
        for i in range(28):
            tick=next(t for t in range(START,BUM_START,8) if frame_at(t)==32+i)
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            # Extra loader bank 2 is actual RuntimeMemory bank 16.
            from tunnel_ball import rebound_helper,helper
            from ribbon_inbetweens import BANK_ENTRY,selector
            self.assertEqual(bytes(m.banks[16][:len(rebound_helper())]),rebound_helper())
            self.assertEqual(bytes(m.banks[16][BANK_ENTRY-0x4000:BANK_ENTRY-0x4000+len(selector())]),selector())
            # Its original PMG renderer is outside the new animation payload.
            # Self-modified indices/pointers are deliberately excluded here.
            self.assertEqual(bytes(m.banks[16][0x3c00:]),helper()[0x400:])
            for x in range(75,86):
                for y in range(88,105):
                    if (x-79.5)**2+((y//2-47.5)*1.66)**2>=25:continue
                    covered=False
                    for p in range(4):
                        col=(x-(m[0xd000+p]-48))//2
                        if 0<=col<8 and m[0xa00+p*128+(y+17)//2]&(0x80>>col):covered=True
                    self.assertTrue(covered,(i,x,y))
