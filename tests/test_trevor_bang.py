"""PMG comic splash phases, visible lettering and safe scene handoffs."""
import unittest
import test_sequence as sequence
from trevor_polished import bang_art, impact_glyphs, impact_word, HITS, HANDS
from engine_effects import pmg_art
from test_engine_cache import TrackedMemory
from test_tunnel_raster import BeamMemory
import json

@unittest.skipIf(sequence.MPU is None,'py65 required')
class TrevorBangTests(unittest.TestCase):
    def test_rebound_does_not_read_write_only_gtia_positions(self):
        class CollisionMemory(sequence.RuntimeMemory):
            def __getitem__(self,address):
                if isinstance(address,int) and 0xd000<=address<=0xd007:
                    raise AssertionError('HPOS read returns collision latches on Atari')
                return super().__getitem__(address)
        for index in (2,5,8,11):
            memory=CollisionMemory(sequence.XEX.read_bytes())
            cpu=sequence.MPU(memory=memory)
            sequence.execute(HITS[index]+112,cpu)
            reference=sequence.execute(HITS[index]+112).memory
            self.assertEqual(memory.ram[0xd000:0xd008],reference[0xd000:0xd008])

    def test_fragment_rendering_survives_music_nmi(self):
        m=sequence.RuntimeMemory(sequence.XEX.read_bytes());cpu=sequence.MPU(memory=m)
        m[0xd301]=m.values[3];m[0xd40b]=124
        for address in (0x232d,0x237d):
            cpu.pc=address;cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
            for _ in range(10000):
                if cpu.pc==0x7fff:break
                cpu.step()
            else:self.fail('music init did not return')
        tick=HITS[2]+128
        for i in range(3):m[0x24a7+i]=tick>>(8*i)&255
        cpu.pc=json.loads(sequence.METADATA.read_text())['callback'];cpu.sp=0xfd
        m[0x1fe:0x200]=[0xfe,0x7f];m[0xd301]=0xff
        next_nmi=cpu.processorCycles+2000;count=0
        for _ in range(100000):
            if cpu.pc==0x7fff:break
            if cpu.processorCycles>=next_nmi:
                saved,pc=m[0xd301],cpu.pc;cpu.nmi()
                for _ in range(10000):
                    cpu.step()
                    if cpu.pc==pc:break
                else:self.fail('NMI did not return')
                self.assertEqual(m[0xd301],saved)
                count+=1;next_nmi=cpu.processorCycles+8880
            cpu.step()
        else:self.fail('impact renderer did not return')
        self.assertGreater(count,3)
        baseline=sequence.execute(tick).memory
        def active_pmg(mem):
            base=(mem[0xd407]&0xfc)<<8
            return bytes(mem[base+0x180:base+0x400])
        self.assertEqual(active_pmg(m),active_pmg(baseline))
        self.assertEqual(m[0xd000:0xd020],baseline[0xd000:0xd020])

    def test_pmg_is_prepared_offscreen_and_committed_in_early_blank(self):
        cpu=sequence.MPU(memory=TrackedMemory(sequence.XEX.read_bytes()))
        sequence.execute(HITS[0],cpu)
        for index,age in ((0,8),(0,80),(0,104),(0,128),(1,24),(1,120),(2,88),(2,128),(0,8)):
            m=cpu.memory;base=(m[0xd407]&0xfc)<<8
            m.writes.clear();sequence.execute(HITS[index]+age,cpu)
            if index!=2:self.assertFalse(any(base+0x180<=a<base+0x400 for a in m.writes))
            if index!=2:self.assertNotEqual((m[0xd407]&0xfc)<<8,base)
            self.assertEqual(m[0xd301],0xff)
        for age in (8,88,104,128):
            for start in (248,255,290,305,306,311):
                m=BeamMemory(sequence.XEX.read_bytes());cpu=sequence.MPU(memory=m)
                sequence.execute(HITS[2]+age,cpu)
                cpu.processorCycles=0;m.start=start*114;m.cpu=cpu;m.events=[]
                cpu.pc=json.loads(sequence.METADATA.read_text())['callback'];cpu.sp=0xfd
                m[0x1fe:0x200]=[0xfe,0x7f]
                for _ in range(100000):
                    if cpu.pc==0x7fff:break
                    cpu.step()
                else:self.fail('callback did not return')
                commits=[t/114%312 for t,a,v in m.events if 0xd000<=a<=0xd015 or a==0xd019 or a==0xd01d or a==0xd400]
                if age<80:
                    self.assertGreaterEqual(min(commits),248)
                    self.assertLess(max(commits),260)
                else:
                    writes=[t for t,a,v in m.events if 0x980<=a<0xc00]
                    first=writes[0]/114
                    self.assertGreaterEqual(first%312,248);self.assertLess(first%312,257)
                    next_frame=(int(first)//312+1)*312
                    self.assertLess(m.events[-1][0]/114,next_frame+48)
                self.assertFalse(any(a==0xd01d and v!=3 for t,a,v in m.events))

    def test_impact_expands_and_alternates_readable_words(self):
        burst,_=bang_art()
        self.assertEqual(len(burst),96)
        self.assertEqual(len({burst[:32],burst[32:64],burst[64:]}),3)
        words=[]
        for index,hit in enumerate(HITS[:8]):
            words.append(impact_word(index))
            for offset in (0,8,24,79):
                cpu=sequence.execute(hit+offset);m=cpu.memory
                base=(m[0xd407]&0xfc)<<8
                dy=m[0x83ef] if m[0x83ef]<128 else m[0x83ef]-256
                self.assertEqual(m[0xd01b],0x11)
                self.assertEqual(m[0xd01d],3)
                self.assertEqual(m[0xd00c],0xff)
                for plane,glyph in enumerate(impact_glyphs(index)):
                    actual=bytes(m[base+0x200+plane*128+45+dy:base+0x200+plane*128+59+dy])
                    self.assertEqual(actual,glyph if offset>=8 else bytes(14),(index,offset,plane))
                self.assertEqual(m[0xd012:0xd016],[0]*4)
                self.assertNotEqual(m[0xd019],0)
                if offset>=8:
                    self.assertNotEqual(sequence.SequenceTests().raster(cpu,effects=True),sequence.SequenceTests().raster(cpu))
        self.assertEqual(words,['BUM','BAM']*4)

    def test_cloud_players_spread_shrink_split_and_cycle_colours(self):
        cpu=None;positions=[];colours=set();pictures=set()
        for age in (80,88,96,103,104,112,119,120,128,135):
            cpu=sequence.execute(HITS[0]+age,cpu);m=cpu.memory
            base=(m[0xd407]&0xfc)<<8
            self.assertEqual(m[0xd01d],3)
            self.assertEqual(m[0xd400],0x2e)
            self.assertEqual(m[0xd01b],0x11 if age<104 else 1)
            self.assertEqual(m[0xd008:0xd00c],[1 if age<120 else 0]*4)
            self.assertEqual(m[0xd00c],0xff if age<104 else 0x55 if age<120 else 0)
            self.assertTrue(all(any(m[base+0x200+p*128:base+0x280+p*128]) for p in range(4)))
            palette=tuple(m[0xd012:0xd016])
            self.assertEqual(len({c>>4 for c in palette}),4)
            self.assertTrue(all(c&15>=12 for c in palette))
            colours.add(palette);positions.append(tuple(m[0xd000:0xd004]))
            pictures.add(bytes(m[base+0x180:base+0x400]))
        self.assertLess(positions[-1][0],positions[0][0])
        self.assertGreater(positions[-1][3],positions[0][3])
        self.assertGreater(len(colours),5)
        self.assertGreater(len(pictures),8)
        for age in (136,137,138,139):
            cpu=sequence.execute(HITS[0]+age,cpu)
            self.assertEqual(cpu.memory[0xd01d],0)

    def test_scatter_starts_at_bang_for_both_hands(self):
        for index,hit in enumerate(HITS[:8]):
            if index%3==2:continue  # These hits retain the actual orbiting satellites.
            cpu=sequence.execute(hit+100);m=cpu.memory
            bubble_x=(m[0xd004]+m[0xd007]+8)//2
            dy=m[0x83ef] if m[0x83ef]<128 else m[0x83ef]-256
            sequence.execute(hit+104,cpu)
            base=(m[0xd407]&0xfc)<<8
            xs=m[0xd004:0xd008]
            ys=[next(row for row,b in enumerate(m[base+0x180:base+0x200]) if b&(3<<(2*i))) for i in range(4)]
            self.assertLessEqual(max(abs(x-bubble_x) for x in xs),6)
            self.assertLessEqual(max(abs(y-(52+dy)) for y in ys),1)
            sequence.execute(hit+132,cpu)
            self.assertLess(m[0xd004],xs[0]);self.assertGreater(m[0xd007],xs[3])
            base=(m[0xd407]&0xfc)<<8
            for i in range(4):
                rows=[row for row,b in enumerate(m[base+0x180:base+0x200]) if b&(3<<(2*i))]
                self.assertTrue(any(b-a>1 for a,b in zip(rows,rows[1:])))

    def test_bang_then_restart_restores_dance(self):
        cpu=sequence.execute(HITS[0]+16)
        sequence.execute(9163,cpu)
        reference=sequence.execute(9163).memory
        def active(mem):
            base=(mem[0xd407]&0xfc)<<8
            return bytes(mem[base+0x180:base+0x400])
        self.assertEqual(active(cpu.memory),active(reference))
        self.assertEqual(cpu.memory[0xd01b],0x11)


    def test_every_third_hit_uses_complete_rotator_ball_and_both_satellites(self):
        from tunnel_ball import masks
        import math
        ball=masks();cpu=None
        for index in (2,5,8,11):
            for age in (80,88,96,112,128):
                tick=HITS[index]+age;cpu=sequence.execute(tick,cpu);m=cpu.memory
                base=(m[0xd407]&0xfc)<<8
                for p in range(4):
                    self.assertEqual(bytes(m[base+0x200+p*128+40:base+0x200+p*128+72]),ball[(tick>>4)&15][p])
                dx=(32+age-80)*(-1 if HANDS[index]==4 else 1)
                self.assertEqual(m[0xd000:0xd004],[(112+dx)&255,(128+dx)&255]*2)
                phase=(tick>>3)&31
                for p in range(4):
                    rx,ry=(25,14) if p<2 else (40,23)
                    angle=(phase+(0 if p<2 else 8))*math.tau/32
                    self.assertEqual(m[0xd004+p],(128+(-4 if p%2==0 else 0)+round(rx*math.cos(angle))+dx)&255)
                    y=55+round(ry*math.sin(angle))
                    self.assertTrue(all(m[base+0x180+y+d]&(3<<(2*p)) for d in range(5)))
                self.assertEqual(m[0xd008:0xd00c],[1]*4)
                self.assertEqual(m[0xd00c],0x55)
                self.assertEqual(m[0xd01b],0x11)
                self.assertEqual(m[0xd301],0xff)

    def test_ball_and_satellites_depart_towards_the_nearest_edge(self):
        for index in (2,5,8,11):
            xs=[sequence.execute(HITS[index]+age).memory[0xd000] for age in (80,96,112,128)]
            left=HANDS[index]==4
            self.assertEqual(xs,sorted(xs,reverse=left))
            self.assertEqual(max(xs)-min(xs),48)
            centre=xs[0]-48+16
            self.assertEqual(left,centre<80)
