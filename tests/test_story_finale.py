"""Approved overhead launch, broken backboard and last-shot star orbit."""
import json
import unittest
import test_sequence as sequence
from test_engine_cache import TrackedMemory
from test_tunnel_raster import BeamMemory
from basketball_hero import DUNK,DUNK_PHASE_TICKS,END as HERO_END,scene_frame,frames,shatter_stage,SHATTER_X,SHATTER_WIDTH,SHATTER_HEIGHT
from final_boy import START,END,FADE_START,artwork,fade_level,star_position


def raster(cpu):return sequence.SequenceTests().raster(cpu)
def active_pmg(m):
    base=(m[0xd407]&0xfc)<<8
    return bytes(m[base+0x180:base+0x400])


class StoryFinaleTests(unittest.TestCase):
    def test_backboard_breaks_on_contact_in_three_stages(self):
        cpu=None;seen=[]
        for phase in (74,75,80,81,86,87,93):
            tick=DUNK+phase*DUNK_PHASE_TICKS;cpu=sequence.execute(tick,cpu)
            p=scene_frame(tick,cpu.memory[0x83ec])
            self.assertEqual(raster(cpu),bytes(p[y*56//192*160+x] for y in range(192) for x in range(160)))
            self.assertEqual(cpu.memory[0x83e5],shatter_stage(phase))
            if phase in (75,81,87):seen.append(bytes(raster(cpu)))
            self.assertEqual(cpu.memory[0xd301],0xff)
        self.assertEqual(len(set(seen)),3)
        original=frames()[5]
        for phase in (75,81,87):
            p=scene_frame(DUNK+phase*DUNK_PHASE_TICKS,5)
            for i,value in enumerate(p):
                if i//160>=SHATTER_HEIGHT or i%160<SHATTER_X:
                    self.assertEqual(value,original[i])
        self.assertEqual(sequence.execute(HERO_END,cpu).memory[0x83e0],16)

    def test_glass_missiles_scatter_while_the_cracked_bitmap_is_held(self):
        from basketball_hero import helper,DATA,ENTRY,packed
        cpu=None;positions=set();pictures=set()
        for phase in range(75,81):
            cpu=sequence.execute(DUNK+phase*DUNK_PHASE_TICKS,cpu);m=cpu.memory
            positions.add(tuple(m[0xd004:0xd008]));pictures.add(bytes(raster(cpu)))
            self.assertTrue(all(any(v&(3<<(2*i)) for v in m[0x980:0xa00]) for i in range(4)))
        self.assertEqual(len(pictures),1)
        self.assertGreater(len(positions),3)
        self.assertLessEqual(ENTRY+len(helper()),DATA)
        self.assertLessEqual(DATA+len(packed()),0x8000)

    def test_overhead_flyer_approaches_as_court_and_bases_recede(self):
        from ribbon_dance import artwork
        pictures=[artwork(f)[0] for f in range(13,16)]
        # More of the central image is occupied by the approaching face/body.
        skin=[sum(v==3 for y in range(64) for v in p[y*160+40:y*160+120]) for p in pictures]
        self.assertEqual(skin,sorted(skin))
        self.assertGreater(skin[-1],skin[0]*1.8)
        self.assertEqual(len(set(pictures)),3)

    def test_final_shot_keeps_music_dlis_and_stays_black_after_end(self):
        cpu=sequence.execute(START-1)
        self.assertEqual(cpu.memory[0x83e0],6)
        cpu=sequence.execute(START,cpu);m=cpu.memory
        p=artwork();self.assertEqual(raster(cpu),bytes(p[y//3*160+x] for y in range(192) for x in range(160)))
        display=m[0xd402]|m[0xd403]<<8
        from outro_text import BITMAP_ROWS,BITMAP_DL
        self.assertEqual([y for y in range(BITMAP_ROWS) if m[display+BITMAP_DL+y*3]&128],[21,99])
        self.assertEqual(m[display],0x80)
        levels=[]
        for tick in range(FADE_START,END+1,16):
            cpu=sequence.execute(tick,cpu)
            levels.append(cpu.memory[0x83ec])
            self.assertEqual(cpu.memory[0x83ec],fade_level(tick))
        self.assertEqual(levels,sorted(levels,reverse=True))
        for tick in (END,END+1000,65536,0xffffff):
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            self.assertEqual(m[0x83e0],17)
            self.assertEqual(m[0xd016:0xd019],[0,0,0])
            self.assertEqual(m[0xd01d],0)
            self.assertEqual(m[0xd400],0x2e) # keep ANTIC + original music DLIs

    def test_four_stars_orbit_on_a_held_bitmap(self):
        cpu=None;positions=set();masks=set();p=None
        for phase in range(16):
            tick=(START+15)//16*16+phase*16
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            if p is None:p=bytes(raster(cpu))
            self.assertEqual(raster(cpu),p)
            self.assertEqual(m[0xd000:0xd004],[star_position(phase=(tick>>4)&15,plane=i)[0]+48 for i in range(4)])
            self.assertEqual(len(set(m[0xd012:0xd016])),4)
            positions.add(tuple(m[0xd000:0xd004]));masks.add(active_pmg(m))
        self.assertGreater(len(positions),12)
        self.assertGreater(len(masks),8)

    def test_final_alternates_original_melody_and_stars_without_trails(self):
        from final_boy import NOTE_SHAPES,STAR_SHAPE,notes_active
        from whistle_pmg import SHAPES
        self.assertEqual(NOTE_SHAPES,tuple(g[::2] for g in SHAPES))
        cpu=None
        for tick in range(START,START+1024,16):
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            base=(m[0xd407]&0xfc)<<8
            for plane in range(4):
                shape=NOTE_SHAPES[plane] if notes_active(tick) else STAR_SHAPE
                y=star_position((tick>>4)&15,plane)[1]-2
                expected=bytearray(128);expected[y:y+12]=bytes(shape)
                self.assertEqual(bytes(m[base+0x200+plane*128:base+0x280+plane*128]),bytes(expected))

    def test_final_glyphs_cycle_through_rainbow_hues(self):
        from final_boy import SHAPE_DATA
        from final_boy import install_control
        from trevor_polished import bank
        installed=install_control(bank(0,quiet=True),0x1234)
        colors=installed[SHAPE_DATA-0x4000+76:SHAPE_DATA-0x4000+95]
        self.assertEqual(len(colors),19)
        self.assertGreaterEqual(len(set(colors)),16)
        self.assertTrue(all((color&15)==15 or color in (0x1e,0x5e,0x9e) for color in colors))

    def test_final_updates_only_inactive_buffers_and_cleanly_restarts(self):
        cpu=sequence.MPU(memory=TrackedMemory(sequence.XEX.read_bytes()))
        sequence.execute(START-1,cpu)
        for tick in (START,START+16,START+48,FADE_START,END):
            m=cpu.memory;active=(m[0xd407]&0xfc)<<8
            bitmap=0x9000
            if tick==START:bitmap=0xb000  # transition fills the inactive picture first
            m.writes.clear();sequence.execute(tick,cpu)
            if tick!=START:self.assertFalse(any(active+0x180<=a<active+0x400 for a in m.writes))
            else:self.assertLess(m.writes.index(0xd01d),next(i for i,a in enumerate(m.writes) if active+0x180<=a<active+0x400))
            if tick!=START:self.assertFalse(any(bitmap<=a<bitmap+2560 for a in m.writes))
            self.assertEqual(m[0xd301],0xff)
        for tick in (96,9163,20942,27000,START):
            cpu=sequence.execute(tick,cpu);fresh=sequence.execute(tick)
            self.assertEqual(raster(cpu),raster(fresh))
            self.assertEqual(active_pmg(cpu.memory),active_pmg(fresh.memory))

    def test_final_star_registers_commit_only_in_early_blank(self):
        for line in (0,248,255,290,305,311):
            m=BeamMemory(sequence.XEX.read_bytes());cpu=sequence.MPU(memory=m)
            sequence.execute(START,cpu)
            cpu.processorCycles=0;m.start=line*114;m.cpu=cpu;m.events=[]
            cpu.pc=json.loads(sequence.METADATA.read_text())['callback'];cpu.sp=0xfd
            m[0x1fe:0x200]=[0xfe,0x7f]
            for _ in range(100000):
                if cpu.pc==0x7fff:break
                cpu.step()
            else:self.fail('final callback did not return')
            times=[t/114%312 for t,a,v in m.events if (0xd000<=a<=0xd01d and a not in (0xd017,0xd018)) or a==0xd400]
            self.assertTrue(times)
            self.assertGreaterEqual(min(times),248)
            self.assertLess(max(times),260)

    def test_final_copy_survives_original_music_nmi(self):
        m=sequence.RuntimeMemory(sequence.XEX.read_bytes());cpu=sequence.MPU(memory=m)
        m[0xd301]=m.values[3];m[0xd40b]=124
        for address in (0x232d,0x237d):
            cpu.pc=address;cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
            for _ in range(10000):
                if cpu.pc==0x7fff:break
                cpu.step()
            else:self.fail('music init did not return')
        for i in range(3):m[0x24a7+i]=START>>(8*i)&255
        m[0xd301]=0xff;cpu.pc=json.loads(sequence.METADATA.read_text())['callback'];cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
        deadline=cpu.processorCycles+2000;count=0
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
        else:self.fail('final callback did not finish')
        self.assertGreater(count,3)
        reference=sequence.execute(START)
        self.assertEqual(raster(cpu),raster(reference))
        self.assertEqual(active_pmg(m),active_pmg(reference.memory))
