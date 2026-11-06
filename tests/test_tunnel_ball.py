"""Tunnel ball stays in PMG RAM, spins, sparks and restores dance art."""
import unittest
import test_sequence as sequence
from tunnel_ball import masks, tunnel_offsets
from engine_effects import pmg_art
from mosaic import KALEIDO_START

@unittest.skipIf(sequence.MPU is None,'py65 required')
class TunnelBallTests(unittest.TestCase):
    def test_all_rotations_and_four_missiles(self):
        frames=masks();self.assertEqual(len({b''.join(f) for f in frames}),8)
        areas = [sum(byte.bit_count() for plane in frame for byte in plane) for frame in frames]
        self.assertGreater(max(areas), min(areas) * 2)
        # Each physical half can contain both inks, so the boundary follows
        # the curved seam rather than a fixed player edge.
        self.assertTrue(any(any(f[0]) and any(f[2]) for f in frames))
        self.assertTrue(any(any(f[1]) and any(f[3]) for f in frames))
        for frame in frames:
            for y in range(32):
                self.assertEqual(frame[0][y]&frame[2][y],0)
                self.assertEqual(frame[1][y]&frame[3][y],0)
        pictures=set()
        for tick in range(KALEIDO_START,KALEIDO_START+256,32):
            cpu=sequence.execute(tick);m=cpu.memory
            self.assertEqual(m[0xd01b],0x11)
            self.assertEqual(m[0xd01d],3)
            dx,dy=tunnel_offsets()[(tick>>4)&31]
            self.assertEqual(m[0xd000:0xd004],[112+dx,128+dx,112+dx,128+dx])
            for i in range(4):self.assertTrue(any(b&(3<<(2*i)) for b in m[0x980:0xa00]))
            raw=sequence.SequenceTests().raster(cpu)
            painted=sequence.SequenceTests().raster(cpu,effects=True)
            self.assertNotEqual(raw,painted)
            pictures.add(bytes(m[0xa00:0xc00]))
        self.assertEqual(len(pictures),8)

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
        missiles,players=pmg_art()
        self.assertEqual(bytes(cpu.memory[0x980:0xa00]),missiles)
        self.assertEqual(bytes(cpu.memory[0xa00:0xc00]),players)
        self.assertEqual(cpu.memory[0xd01b],1)
        self.assertEqual(sequence.SequenceTests().raster(cpu,effects=True),
                         sequence.SequenceTests().raster(sequence.execute(9163),effects=True))

    def test_rainbow_panels_and_satellites_keep_distinct_bright_hues(self):
        colors=set()
        for tick in range(KALEIDO_START,KALEIDO_START+256,32):
            m=sequence.execute(tick).memory
            palette=tuple(m[a] for a in (0xd012,0xd014,0xd019))
            self.assertEqual(len({c>>4 for c in palette}),3)
            self.assertTrue(all(c&15>=12 for c in palette))
            self.assertEqual(m[0xd012],m[0xd013])
            self.assertEqual(m[0xd014],m[0xd015])
            self.assertEqual(m[0xd00c],0xff)
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
        for i in range(64):
            tick=12288+i*16
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            self.assertEqual(m[0xd01d],3)
            self.assertEqual(m[0xd000],112+offsets[i])
            self.assertEqual(m[0xd001],128+offsets[i])
            self.assertEqual(m[0x83e9], vertical[i] & 255)
            self.assertTrue(any(m[0x980:0xa00]))
            for j in range(4):
                self.assertLess(abs(m[0xd004+j]-(128+offsets[i])),32)
        self.assertLessEqual(abs(offsets[-1]),4)
        cpu=sequence.execute(13312,cpu)
        self.assertEqual(cpu.memory[0xd000],112)
        self.assertEqual(cpu.memory[0xd001],128)
        self.assertEqual(cpu.memory[0xd01d],3)

    def test_tunnel_bob_covers_central_hole_at_every_phase(self):
        cpu=None;positions=set()
        for i in range(32):
            tick=13312+i*16
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            dx,dy=tunnel_offsets()[i];positions.add((dx,dy))
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
        self.assertEqual(tunnel_offsets()[0],(0,0))
