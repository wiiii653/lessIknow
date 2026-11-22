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
    def test_rotator_words_preserve_punch_positions_on_replay(self):
        from music_timing import tick_at_bar
        from post_trevor_director import FIRST_ROTATOR

        punch = HITS[1]+20
        cpu = sequence.execute(punch)
        memory = cpu.memory
        expected = memory[0xd000:0xd008]
        sequence.execute(tick_at_bar(104)+16,cpu)
        sequence.execute(tick_at_bar(105)+16,cpu)
        sequence.execute(0,cpu)
        sequence.execute(FIRST_ROTATOR,cpu)
        sequence.execute(punch,cpu)
        self.assertEqual(memory[0xd000:0xd008],expected)

    def test_every_punch_has_arrival_impact_and_departure(self):
        from rainbow_ball import spin_masks
        from tunnel_ball import masks as large_masks
        from basketball_hero import satellite_orbits
        from trevor_ball_flight import IN_VECTORS,INCOMING_TICKS,displacement
        import math
        frames = spin_masks(); large=large_masks(); orbits=satellite_orbits()
        self.assertEqual(len(set(IN_VECTORS)),len(HITS))
        for index, hit in enumerate(HITS):
            for age in (-48,-36,-24,-16,-1,80,92,105,120,135):
                if index+1<len(HITS) and age>=HITS[index+1]-hit-INCOMING_TICKS:continue
                m = sequence.execute(hit+age).memory
                base = (m[0xd407]&0xfc)<<8
                ax,ay=__import__('trevor_polished').impact_anchor(index)
                incoming=age<0; distance=((-2*age+2)//3) if incoming else (age-80)//2
                vx,vy=IN_VECTORS[index] if incoming else (0,0)
                x=(160+ax+displacement(vx,distance))&255
                y=max(0,min(111,45+ay+displacement(vy,distance)))
                if incoming:x=(x-8)&255;y=max(0,min(96,y-8))
                else:y=y+2-distance//2
                puff=bytes((0x18,0x3c,0x6e,0xff,0xfb,0x76,0x3c,0x18))
                frame=large[((hit+age)>>4)&15] if incoming else (puff,)*4
                expected_x=([x,(x+16)&255,x,(x+16)&255] if incoming else
                            [(x-distance-3)&255,(x+distance+15)&255,
                             (x-distance-3)&255,(x+distance+15)&255])
                self.assertEqual(m[0xd000:0xd004],expected_x,(index,age))
                for plane in range(4):
                    length=32 if incoming else 8
                    row=y if incoming or plane<2 else y+8+2*(distance//2)
                    self.assertEqual(bytes(m[base+0x200+plane*128+row:base+0x200+plane*128+row+length]),bytes(frame[plane]),(index,age,plane))
                self.assertEqual(m[0xd008:0xd00c],[1]*4)
                self.assertEqual(m[0xd00c],0x55)
                self.assertEqual(m[0xd01b],0x11 if incoming else 1)
                fade_masks=(0xfe,0xfe,0xfc,0xfc,0xf8,0xf8,0xf0,0xf0)
                fade=fade_masks[max(0,distance-(25 if incoming else 20))]
                if incoming:
                    hues=(0x40,0x60,0x80,0xa0,0xc0,0xe0,0x20,0x30);phase_h=((hit+age)>>4)&7
                    palette=[hues[(phase_h+offset)%8]|luma for offset,luma in ((0,8),(1,10),(4,14),(5,12))]
                    self.assertEqual(m[0xd019],(hues[(phase_h+2)%8]|14)&fade)
                else:
                    color=(((hit+age)<<2)&0xf0)|10
                    palette=[]
                    for increment in (0x44,0x42,0x42,0):
                        color|=10;palette.append(color);color=(color+increment)&255
                self.assertEqual(m[0xd012:0xd016],[value&fade for value in palette],(index,age))
                if not incoming:
                    from trevor_polished import IMPACT_HUES
                    self.assertEqual(m[0xd019],(IMPACT_HUES[(((distance*2+80)>>3)+2)&15]|14)&fade)
                phase=((hit+age)>>3)&31
                expected_missiles=bytearray(128)
                for plane in range(4):
                    if incoming:
                        rx,ry=((25,14) if plane<2 else (40,23))
                        angle=(phase+(0 if plane<2 else 8))*math.tau/32
                        sx=(x+12+(4 if plane%2 else 0)+round(rx*math.cos(angle)))&255
                        sy=(y+15+round(ry*math.sin(angle)))&255
                        shape=(1,1,3,1,1) if plane%2==0 else (2,2,3,2,2)
                    else:
                        ox,oy=orbits[plane][phase];sx=(x+6+ox)&255;sy=(y+6+oy)&255
                        shape=(1,3,3,3,1)
                    self.assertEqual(m[0xd004+plane],sx,(index,age,plane))
                    if sy<123:
                        for row,bits in enumerate(shape):expected_missiles[sy+row]|=bits<<(2*plane)
                self.assertEqual(bytes(m[base+0x180:base+0x200]),bytes(expected_missiles),(index,age))
                self.assertEqual(m[0xd301],0xff)

    def test_flights_do_not_stick_to_vertical_clamps_and_fade_at_handoffs(self):
        from trevor_ball_flight import IN_VECTORS, INCOMING_TICKS, displacement
        from trevor_polished import impact_anchor
        for index, hit in enumerate(HITS):
            base_y=45+impact_anchor(index)[1]
            x_profile,y_profile=IN_VECTORS[index]
            self.assertNotEqual(displacement(x_profile,24),0,index)
            self.assertNotEqual(displacement(y_profile,24),0,index)
            self.assertTrue(all(8<=base_y+displacement(y_profile,d)<=104 for d in range(1,33)),index)
            for age in (-48,-42,-36,-24,-1,80,98,120,128,135):
                if age>=0 and index+1<len(HITS) and age>=HITS[index+1]-hit-INCOMING_TICKS:continue
                m=sequence.execute(hit+age).memory
                if age in (-48,135):
                    self.assertTrue(all((v&15)==0 for v in m[0xd012:0xd016]),(index,age))
                    self.assertEqual(m[0xd019]&15,0,(index,age))
                elif age in (-36,-24,-1,80,98,120):
                    self.assertTrue(any(v&15 for v in m[0xd012:0xd016]),(index,age))

    @unittest.skipUnless((sequence.ROOT/'build/visual-prototype-v288.xex').exists(), 'v288 comparison XEX required')
    def test_flight_preserves_front_buffer_and_trevor_graphics(self):
        reference = sequence.ROOT/'build/visual-prototype-v288.xex'
        cpu=sequence.MPU(memory=TrackedMemory(sequence.XEX.read_bytes()))
        old=sequence.MPU(memory=sequence.RuntimeMemory(reference.read_bytes()))
        sequence.execute(HITS[0]-33,cpu); sequence.execute(HITS[0]-33,old)
        for index in (0,1,2,4,7):
            for age in (-32,-16,-1,0,40,79,80,92,105):
                tick=HITS[index]+age; m=cpu.memory
                active=(m[0xd407]&0xfc)<<8
                enabled=m[0xd01d]&3
                m.writes.clear(); sequence.execute(tick,cpu); sequence.execute(tick,old)
                if enabled:self.assertFalse(any(active+0x180<=a<active+0x400 for a in m.writes),(index,age))
                current=sequence.SequenceTests().raster(cpu);previous=sequence.SequenceTests().raster(old)
                # v292 redraws Trevor's mouth, including mirrored punch poses.
                for y in range(192):
                    if 57<=y<75:
                        self.assertEqual(current[y*160:y*160+54],previous[y*160:y*160+54],(index,age,y))
                        self.assertEqual(current[y*160+106:(y+1)*160],previous[y*160+106:(y+1)*160],(index,age,y))
                    else:
                        self.assertEqual(current[y*160:(y+1)*160],previous[y*160:(y+1)*160],(index,age,y))

    def test_flight_registers_commit_in_early_blanking(self):
        for age in (-48,-36,-1,80,120,135,136):
            for start in (248,255,290,305,311):
                m=BeamMemory(sequence.XEX.read_bytes()); cpu=sequence.MPU(memory=m)
                sequence.execute(HITS[1]+age,cpu)
                cpu.processorCycles=0; m.start=start*114; m.cpu=cpu; m.events=[]
                cpu.pc=json.loads(sequence.METADATA.read_text())['callback']; cpu.sp=0xfd
                m[0x1fe:0x200]=[0xfe,0x7f]
                for _ in range(100000):
                    if cpu.pc==0x7fff: break
                    cpu.step()
                else:self.fail('flight callback did not return')
                commits=[t/114%312 for t,a,v in m.events if 0xd000<=a<=0xd015 or a==0xd01d]
                self.assertTrue(commits)
                self.assertGreaterEqual(min(commits),248)
                self.assertLess(max(commits),260)

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

    def test_both_ball_flights_survive_music_nmi(self):
        for tick in (HITS[3]-40,HITS[3]-16,HITS[3]+98):
            m=sequence.RuntimeMemory(sequence.XEX.read_bytes());cpu=sequence.MPU(memory=m)
            m[0xd301]=m.values[3];m[0xd40b]=124
            for address in (0x232d,0x237d):
                cpu.pc=address;cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
                for _ in range(10000):
                    if cpu.pc==0x7fff:break
                    cpu.step()
                else:self.fail('music init did not return')
            for i in range(3):m[0x24a7+i]=tick>>(8*i)&255
            cpu.pc=json.loads(sequence.METADATA.read_text())['callback'];cpu.sp=0xfd
            m[0x1fe:0x200]=[0xfe,0x7f];m[0xd301]=0xff
            next_nmi=cpu.processorCycles+2000;count=0
            for _ in range(100000):
                if cpu.pc==0x7fff:break
                if cpu.processorCycles>=next_nmi:
                    bank,pc=m[0xd301],cpu.pc;cpu.nmi()
                    for _ in range(10000):
                        cpu.step()
                        if cpu.pc==pc:break
                    else:self.fail('NMI did not return')
                    self.assertEqual(m[0xd301],bank)
                    count+=1;next_nmi=cpu.processorCycles+8880
                cpu.step()
            else:self.fail('ball-flight renderer did not return')
            self.assertGreater(count,3)
            baseline=sequence.execute(tick).memory
            def active(mem):
                base=(mem[0xd407]&0xfc)<<8
                return bytes(mem[base+0x180:base+0x400])
            self.assertEqual(active(m),active(baseline),tick)
            self.assertEqual(m[0xd000:0xd020],baseline[0xd000:0xd020],tick)

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



    def test_bang_then_restart_restores_dance(self):
        cpu=sequence.execute(HITS[0]+16)
        sequence.execute(9163,cpu)
        reference=sequence.execute(9163).memory
        def active(mem):
            base=(mem[0xd407]&0xfc)<<8
            return bytes(mem[base+0x180:base+0x400])
        self.assertEqual(active(cpu.memory),active(reference))
        self.assertEqual(cpu.memory[0xd01b],0x11)
