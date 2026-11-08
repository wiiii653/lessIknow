"""Post-Trevor effect order, complete PMG data and active-effect hole coverage."""
import unittest
import test_sequence as s
from pmg_showcase import START,NAMES,frame_index,frame,primary
from test_engine_cache import TrackedMemory

class ShowcaseTests(unittest.TestCase):
    def test_all_effects_cycle_in_order_with_complete_masks_and_covered_hole(self):
        cpu=None;seen=set()
        for mode in range(8):
            for phase in range(8):
                tick=START+mode*512+phase*16
                cpu=s.execute(tick,cpu);m=cpu.memory;index=frame_index(tick)
                self.assertEqual(index,mode*8+phase);seen.add(NAMES[mode])
                data,meta=frame(index);base=(m[0xd407]&0xfc)<<8
                main,main_meta=primary(index)
                self.assertEqual(bytes(m[base+0x200+main_meta[1]:base+0x200+main_meta[1]+32]),main)
                self.assertEqual(m[0xd000],main_meta[0]);self.assertEqual(m[0xd008],main_meta[2])
                for p in range(4):
                    address=base+(0x280+p*128 if p<3 else 0x180)+meta[7+p]
                    self.assertEqual(bytes(m[address:address+32]),data[p*32:(p+1)*32],(mode,phase,p))
                for y in range(88,105):
                    for x in range(75,86):
                        if (x-79.5)**2+((y//2-47.5)*1.66)**2>=25:continue
                        covered=False
                        for player in range(4):
                            scale=(1,2,1,4)[m[0xd008+player]]
                            col=(x-(m[0xd000+player]-48))//scale
                            if 0<=col<8 and m[base+0x200+player*128+(y+17)//2]&(0x80>>col):covered=True
                        self.assertTrue(covered,(mode,phase,x,y))
                self.assertEqual(m[0xd301],0xff)
                self.assertEqual(m[0xd01d],3)
        self.assertEqual(len(seen),8)
        self.assertNotIn('ribbons',seen)
        self.assertFalse(any('firework' in n for n in seen))
        self.assertIn('beating_heart',seen)
        self.assertEqual(frame_index(START+4096),0)

    def test_cycle_never_writes_the_active_pmg_and_hands_back_to_earlier_scenes(self):
        cpu=s.MPU(memory=TrackedMemory(s.XEX.read_bytes()))
        s.execute(START,cpu)
        for mode in range(8):
            m=cpu.memory;active=(m[0xd407]&0xfc)<<8;m.writes.clear()
            s.execute(START+mode*512+64,cpu)
            self.assertFalse(any(active+0x180<=a<active+0x400 for a in m.writes))
        for tick in (12000,20942,9504,START,59085,START):
            cpu=s.execute(tick,cpu);fresh=s.execute(tick).memory;m=cpu.memory
            base=(m[0xd407]&0xfc)<<8;other=(fresh[0xd407]&0xfc)<<8
            self.assertEqual(bytes(m[base+0x180:base+0x400]),bytes(fresh[other+0x180:other+0x400]),tick)
            regs=[a for a in range(0xd000,0xd020) if a!=0xd019 or m[0xd01b]&16]
            self.assertEqual([m[a] for a in regs],[fresh[a] for a in regs],tick)


    def test_preparation_survives_real_music_nmi(self):
        import json
        m=s.RuntimeMemory(s.XEX.read_bytes());cpu=s.MPU(memory=m)
        m[0xd301]=m.values[3];m[0xd40b]=124
        for entry in (0x232d,0x237d):
            cpu.pc=entry;cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
            for _ in range(10000):
                if cpu.pc==0x7fff:break
                cpu.step()
            else:self.fail('music init did not return')
        tick=START+7*512+96
        for i in range(3):m[0x24a7+i]=tick>>(8*i)&255
        cpu.pc=json.loads(s.METADATA.read_text())['callback'];cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f];m[0xd301]=0xff
        deadline=cpu.processorCycles+2000;count=0
        for _ in range(100000):
            if cpu.pc==0x7fff:break
            if cpu.processorCycles>=deadline:
                pc,bank=cpu.pc,m[0xd301];cpu.nmi()
                for _ in range(10000):
                    cpu.step()
                    if cpu.pc==pc:break
                else:self.fail('NMI did not return')
                self.assertEqual(m[0xd301],bank);count+=1;deadline=cpu.processorCycles+8880
            cpu.step()
        else:self.fail('callback did not return')
        self.assertGreater(count,3)
        fresh=s.execute(tick).memory
        base=(m[0xd407]&0xfc)<<8;other=(fresh[0xd407]&0xfc)<<8
        self.assertEqual(bytes(m[base+0x180:base+0x400]),bytes(fresh[other+0x180:other+0x400]))
        self.assertEqual(m[0xd000:0xd020],fresh[0xd000:0xd020])


    def test_heart_has_two_pulses_and_is_not_a_fixed_guard_silhouette(self):
        from pmg_showcase import full_frame
        areas=[];shapes=set()
        for phase in range(8):
            data,meta,main,mm=full_frame(16+phase)
            planes=[main,data[:32],data[32:64],data[64:96]]
            areas.append(sum(v.bit_count() for p in planes for v in p))
            shapes.add(b''.join(planes))
            self.assertEqual(mm,(112,40,1))
        self.assertGreater(areas[1],areas[0]);self.assertGreater(areas[5],areas[4])
        self.assertGreater(len(shapes),4)


    def test_comic_letters_are_above_their_bubble_in_hardware_and_preview(self):
        from pmg_preview import player_masks
        m=s.execute(START+3*512).memory;base=(m[0xd407]&0xfc)<<8
        self.assertEqual(m[0xd013],0)
        self.assertNotEqual(m[0xd015],0)
        self.assertTrue(m[base+0x280+49]&0x80)
        self.assertTrue(m[base+0x380+49]&0x80)
        self.assertEqual(player_masks(bytes(160*192),m,192)[81*160+64],0)
