"""Actual banked heart masks, face expressions, ownership and cut cleanup."""
import unittest
import launch_kiss as k
import ribbon_dance as d
import test_sequence as s
from test_engine_cache import TrackedMemory


class LaunchKissTests(unittest.TestCase):
    def test_tail_budget_and_single_expression_sequence(self):
        self.assertLessEqual(len(k.helper()),1024)
        self.assertLessEqual(len(k.trampoline()),64)
        self.assertEqual(d.frame_at(d.STEPS[121]),14)
        self.assertEqual(d.frame_at(k.START),15)
        self.assertEqual(k.START,d.STEPS[122])
        self.assertEqual(d.END,20942)
        self.assertEqual(k.MOUTH,(82,67))

    def test_all_heart_phases_match_live_pmg_and_cover_no_active_memory(self):
        cpu=s.MPU(memory=TrackedMemory(s.XEX.read_bytes()))
        s.execute(d.STEPS[121],cpu)
        pictures=set();masks=set()
        for phase in range(8):
            tick=k.START+phase*32;m=cpu.memory
            active=(m[0xd407]&0xfc)<<8
            active_bitmap=0x9000 if m[0xd403]==0x84 else 0xb000
            m.writes.clear();s.execute(tick,cpu)
            self.assertFalse(any(active+0x180<=a<active+0x400 for a in m.writes),tick)
            self.assertFalse(any(active_bitmap<=a<active_bitmap+2560 for a in m.writes),tick)
            left,y,size,width,height=k.geometry(phase)
            scale=1 if size==0 else 2
            self.assertEqual(m[0xd000:0xd004],[left+48,left+48+8*scale]*2)
            self.assertEqual(m[0xd008:0xd00c],[size]*4)
            self.assertEqual(tuple(m[0xd012:0xd016]),k.COLORS)
            base=(m[0xd407]&0xfc)<<8
            for plane,shape in enumerate(k.masks(phase)):
                expected=bytearray(128)
                rows=bytes(v for v in shape for _ in range(scale))
                expected[y:y+len(rows)]=rows
                self.assertEqual(bytes(m[base+0x200+plane*128:base+0x280+plane*128]),bytes(expected),(phase,plane))
            self.assertEqual(m[0xd301],0xff)
            self.assertEqual(m[0xd01d],3)
            # Missiles retain the launch's separate air/spark trails.
            for plane in range(4):self.assertTrue(any(v&(3<<(plane*2)) for v in m[base+0x180:base+0x200]))
            masks.add(bytes(m[base+0x200:base+0x400]));pictures.add(bytes(s.SequenceTests().raster(cpu)))
        self.assertEqual(len(masks),8)
        self.assertEqual(len(pictures),1)  # facial kiss held, PMG moves independently
        s.execute(d.END,cpu)
        self.assertNotEqual(cpu.memory[0x83e0],14)
        s.execute(d.START,cpu)
        self.assertEqual(cpu.memory[0xd008:0xd00c],[3]*4)

    def test_side_sparks_trace_curved_paths_every_pal_frame(self):
        cpu = None
        positions = [set() for _ in range(4)]
        for tick in range(k.START, k.START+128, 4):
            cpu = s.execute(tick, cpu)
            m = cpu.memory
            base = (m[0xd407] & 0xfc) << 8
            for plane, offset in enumerate((0, 11, 7, 23)):
                x, y = d.launch_spark_path(((tick >> 2)+offset) & 31)
                expected_x = x if plane < 2 else 160-x
                self.assertEqual(m[0xd004+plane], expected_x+48)
                expected_y = y + (39 if plane & 1 else 0)
                mask = 3 << (plane*2)
                rows = m[base+0x180:base+0x200]
                self.assertEqual(next(i for i, bits in enumerate(rows) if bits & mask), expected_y)
                positions[plane].add((expected_x, expected_y))
        self.assertTrue(all(len(path) > 24 for path in positions))

    def test_shading_has_a_white_specular_and_two_distinct_lobes(self):
        planes=k.masks(5)
        self.assertTrue(any(planes[2]))
        rows=[((planes[0][y]|planes[2][y])<<8)|(planes[1][y]|planes[3][y]) for y in range(16)]
        top=next(v for v in rows if v)
        occupied=[x for x in range(16) if top&(0x8000>>x)]
        self.assertTrue(any(not top&(0x8000>>x) for x in range(min(occupied),max(occupied)+1)))

    def test_burst_particles_scatter_outward(self):
        def points(phase):
            result = set()
            for plane, rows in enumerate(k.masks(phase)):
                for y, row in enumerate(rows):
                    for x in range(8):
                        if row & (0x80 >> x):
                            result.add((x + (8 if plane & 1 else 0), y))
            return result
        early, late = points(6), points(7)
        self.assertGreaterEqual(len(early), 10)
        self.assertGreaterEqual(len(late), 10)
        self.assertGreater(sum((x-7.5)**2+(y-7.5)**2 for x,y in late)/len(late),
                           sum((x-7.5)**2+(y-7.5)**2 for x,y in early)/len(early))
        self.assertTrue(all(any(p) for p in k.masks(7)))

    def test_late_raster_commits_and_original_music_nmi_during_heart(self):
        from test_ribbon_buffers import RibbonBufferTests
        checks=RibbonBufferTests()
        for tick in (k.START,k.START+128,k.START+224):
            checks.check_late_raster_retains_old_pmg_until_safe_commit(tick)
            checks.check_banked_frame_copy_survives_music_nmi(tick)
