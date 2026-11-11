"""Tunnel ball stays in PMG RAM, spins, sparks and restores dance art."""
import unittest
import math
import test_sequence as sequence
from tunnel_ball import masks, tunnel_offsets
from engine_effects import pmg_art
from mosaic import KALEIDO_START

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
            dx,dy=tunnel_offsets()[m[0x83ed]&31]
            self.assertEqual(m[0xd000:0xd004],[112+dx,128+dx,112+dx,128+dx])
            for i in range(4):self.assertTrue(any(b&(3<<(2*i)) for b in m[0x980:0xa00]))
            origin=40+(m[0x83e9] if m[0x83e9]<128 else m[0x83e9]-256)
            expected=frames[(tick>>4)&15]
            for plane in range(4):
                self.assertEqual(bytes(m[0xa00+plane*128+origin:0xa00+plane*128+origin+32]),expected[plane],(tick,plane))
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
        for i in range(64):
            tick=12288+i*16
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            self.assertEqual(m[0xd01d],3)
            self.assertEqual(m[0xd000],112+offsets[i])
            self.assertEqual(m[0xd001],128+offsets[i])
            self.assertEqual(m[0x83e9], vertical[i] & 255)
            self.assertTrue(any(m[0x980:0xa00]))
            for j in range(4):
                self.assertLessEqual(abs(m[0xd004+j]-(128+offsets[i])),44)
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
            # The eye scene reuses four mosaic slots, so those phases repeat.
            phase=(20+(i&3) if i>=24 else i)
            dx,dy=tunnel_offsets()[phase];positions.add((dx,dy))
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

    def test_two_paired_missile_stars_follow_different_ellipses(self):
        cpu=None
        for j in range(32):
            cpu=sequence.execute(12288+j*8,cpu);m=cpu.memory
            dx=m[0x83e8] if m[0x83e8]<128 else m[0x83e8]-256
            dy=m[0x83e9] if m[0x83e9]<128 else m[0x83e9]-256
            for i in range(4):
                rx,ry=((25,14) if i<2 else (40,23))
                angle=(j+(0 if i<2 else 8))*math.tau/32
                half_offset=-4 if i%2==0 else 0
                self.assertEqual(m[0xd004+i],128+half_offset+round(rx*math.cos(angle))+dx)
                first=55+round(ry*math.sin(angle))+dy
                rows=[y for y in range(128) if m[0x980+y] & (3 << (2*i))]
                self.assertEqual(rows,list(range(first,first+5)))

    def test_reused_cycle_memory_and_original_tunnel_covering_are_separate(self):
        cpu=None
        for i in range(32):
            cpu=sequence.execute(34912+i*16,cpu);m=cpu.memory
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
