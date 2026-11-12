"""PMG/bitmap ownership, safe commits and music bank restoration for ribbons."""
import json
import unittest
import test_sequence as sequence
from test_tunnel_raster import BeamMemory
from test_engine_cache import TrackedMemory
from ribbon_dance import START, SIDE_START, SIDE_END, STEPS, FIREWORK_START, LAUNCH_START, artwork, frame_at, scene_artwork


class RibbonBufferTests(unittest.TestCase):
    def test_front_solo_ribbons_have_independent_phases_and_keep_their_grips(self):
        from ribbon_dance import CUTS, ribbon_streams
        streams=ribbon_streams()
        for tick in (CUTS[1]+64,CUTS[1]+80,CUTS[1]+96,CUTS[2]-16):
            cpu=sequence.execute(tick);m=cpu.memory
            _,hands=scene_artwork(tick)
            phase=(tick>>3)&15
            phases=(phase,((phase^15)+3)&15,(phase*2+8)&15,((phase^15)+11)&15)
            base=(m[0xd407]&0xfc)<<8
            for plane,(x,y) in enumerate(hands):
                self.assertEqual(m[0xd000+plane],x+34,(tick,plane))
                origin=((y*3+17)//2-32)&255
                expected=bytearray(128)
                shape=streams[plane*1024+phases[plane]*64:plane*1024+(phases[plane]+1)*64]
                for row,value in enumerate(shape):
                    if origin+row<128:expected[origin+row]=value
                start=base+0x200+plane*128
                self.assertEqual(bytes(m[start:start+128]),bytes(expected),(tick,plane))

    def test_side_dancer_and_all_pmg_move_right_together_without_phase_wrap(self):
        cpu=None
        for tick in (SIDE_START,SIDE_START+128,SIDE_START+1024,SIDE_END-1):
            cpu=sequence.execute(tick,cpu)
            pixels,anchors=scene_artwork(tick)
            expected=bytes(pixels[y//3*160+x] for y in range(192) for x in range(160))
            self.assertEqual(sequence.SequenceTests().raster(cpu),expected)
            self.assertEqual(cpu.memory[0xd000:0xd004],
                             [(x+34)&255 for x,y in anchors])
        # Position changes before the next bitmap/PMG phase. A frame-only
        # cache would leave the girl behind while moving her ribbons.
        a=sequence.execute(SIDE_START+127)
        before=tuple(a.memory[0xd000:0xd008])
        previous=bytes(sequence.SequenceTests().raster(a))
        a=sequence.execute(SIDE_START+128,a)
        self.assertEqual(tuple(a.memory[0xd000:0xd008]),tuple((x+4)&255 for x in before))
        self.assertNotEqual(sequence.SequenceTests().raster(a),previous)

    def test_rainbow_raster_bands_cycle_without_touching_banks_or_framebuffers(self):
        from ribbon_dance import rainbow_palette
        address=json.loads(sequence.METADATA.read_text())['ribbon_palette']
        colours=set()
        cpu=sequence.MPU(memory=TrackedMemory(sequence.XEX.read_bytes()))
        for tick in (START,START+32,START+64,START+128):
            for band in range(4):
                m=cpu.memory;m[0x83e2]=tick&255;m[0xd40b]=band*32
                m[0xd301]=m.values[30];saved=m[0xd301]
                m.writes.clear();cpu.pc=address;cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f]
                for _ in range(100):
                    if cpu.pc==0x7fff:break
                    cpu.step()
                else:self.fail('palette helper did not return')
                actual=tuple(m[a] for a in (0xd012,0xd013,0xd014,0xd015,0xd019))
                self.assertEqual(actual,rainbow_palette(tick,band))
                colours.update(actual)
                self.assertEqual(m[0xd301],saved)
                self.assertEqual(cpu.sp,0xff)
                self.assertTrue(all(0x100<=a<0x200 or a in (0xd012,0xd013,0xd014,0xd015,0xd019) for a in m.writes))
        self.assertGreater(len({c>>4 for c in colours}),12)

    def test_sparks_change_positions_and_masks_on_a_held_body_pose(self):
        cpu=None;positions=set();masks=set();pictures=set()
        from ribbon_dance import frame_at, CUTS
        for delta in (t-START for t in range(START,CUTS[1],8) if frame_at(t)==0):
            cpu=sequence.execute(START+delta,cpu);m=cpu.memory
            pictures.add(bytes(sequence.SequenceTests().raster(cpu)))
            positions.add(tuple(m[0xd004:0xd008]))
            base=(m[0xd407]&0xfc)<<8
            masks.add(bytes(m[base+0x180:base+0x200]))
            self.assertTrue(any(m[base+0x180:base+0x200]))
        self.assertEqual(len(pictures),1)
        self.assertGreater(len(positions),8)
        self.assertGreater(len(masks),8)

    def test_active_pmg_and_bitmap_are_never_written(self):
        cpu=sequence.MPU(memory=TrackedMemory(sequence.XEX.read_bytes()))
        for tick in (SIDE_START,SIDE_START+16,SIDE_START+64,START,START+8,START+16,(STEPS[0]+STEPS[1])//2,STEPS[1],STEPS[32],(STEPS[33]+STEPS[34])//2,STEPS[64],STEPS[122],SIDE_START):
            memory=cpu.memory
            active=0x8800 if memory[0xd407]&0x80 else 0x800
            active_dl=memory[0xd403]<<8
            active_bitmap=0x9000 if active_dl==0x8400 else 0xb000
            memory.writes.clear()
            sequence.execute(tick,cpu)
            from ribbon_dance import PALETTE
            self.assertEqual(memory[0xd016:0xd019],list(PALETTE[1:]),tick)
            self.assertFalse(any(active+0x180<=a<active+0x400 for a in memory.writes),tick)
            self.assertFalse(any(active_bitmap<=a<active_bitmap+2560 for a in memory.writes),tick)
            self.assertIn(memory[0xd407],(8,0x88))
            self.assertEqual(memory[0xd301],0xff)

    def test_late_raster_retains_old_pmg_until_safe_commit(self):
        for tick in (START,(STEPS[0]+STEPS[1])//2,FIREWORK_START+32):
            with self.subTest(tick=tick):
                self.check_late_raster_retains_old_pmg_until_safe_commit(tick)

    def check_late_raster_retains_old_pmg_until_safe_commit(self,tick):
        for start in (0,248,255,290,305,306,311):
            memory=BeamMemory(sequence.XEX.read_bytes());cpu=sequence.MPU(memory=memory)
            sequence.execute(tick,cpu)
            cpu.processorCycles=0;memory.start=start*114;memory.cpu=cpu;memory.events=[]
            cpu.pc=json.loads(sequence.METADATA.read_text())['callback'];cpu.sp=0xfd
            memory[0x1fe:0x200]=[0xfe,0x7f]
            for _ in range(100000):
                if cpu.pc==0x7fff:break
                cpu.step()
            else:self.fail('callback did not return')
            registers=[(t,a,v) for t,a,v in memory.events if 0xd000<=a<=0xd01d or a==0xd400]
            self.assertTrue(registers)
            lines=[t/114%312 for t,_,_ in registers]
            self.assertGreaterEqual(min(lines),248)
            self.assertLess(max(lines),260)
            self.assertFalse(any(a==0xd01d and v!=3 for _,a,v in registers))

    def test_banked_frame_copy_survives_music_nmi(self):
        for tick in (SIDE_START+48,(STEPS[0]+STEPS[1])//2,(STEPS[34]+STEPS[35])//2,LAUNCH_START,STEPS[122]):
            with self.subTest(tick=tick):
                self.check_banked_frame_copy_survives_music_nmi(tick)

    def check_banked_frame_copy_survives_music_nmi(self,tick):
        memory=sequence.RuntimeMemory(sequence.XEX.read_bytes());cpu=sequence.MPU(memory=memory)
        memory[0xd301]=memory.values[3];memory[0xd40b]=124
        for address in (0x232d,0x237d):
            cpu.pc=address;cpu.sp=0xfd;memory[0x1fe:0x200]=[0xfe,0x7f]
            for _ in range(10000):
                if cpu.pc==0x7fff:break
                cpu.step()
            else:self.fail('music init did not return')
        for i in range(3):memory[0x24a7+i]=tick>>(8*i)&255
        memory[0xd301]=0xff
        cpu.pc=json.loads(sequence.METADATA.read_text())['callback'];cpu.sp=0xfd
        memory[0x1fe:0x200]=[0xfe,0x7f]
        next_nmi=cpu.processorCycles+2000;count=0
        for _ in range(100000):
            if cpu.pc==0x7fff:break
            if cpu.processorCycles>=next_nmi:
                bank,pc=memory[0xd301],cpu.pc
                cpu.nmi()
                for _ in range(10000):
                    cpu.step()
                    if cpu.pc==pc:break
                else:self.fail('NMI did not return')
                self.assertEqual(memory[0xd301],bank)
                count+=1;next_nmi=cpu.processorCycles+8880
            cpu.step()
        else:self.fail('callback did not finish')
        self.assertGreater(count,3)
        pixels,_=scene_artwork(tick)
        expected=bytes(pixels[y//3*160+x] for y in range(192) for x in range(160))
        self.assertEqual(sequence.SequenceTests().raster(cpu),expected)


    def test_all_ribbon_phases_have_no_missing_rows_or_disconnected_segments(self):
        from ribbon_dance import ribbon_streams
        data=ribbon_streams();self.assertEqual(len(data),5120)
        for plane in range(4):
            for phase in range(16):
                rows=data[plane*1024+phase*64:plane*1024+(phase+1)*64]
                points={(x,y) for y,v in enumerate(rows) for x in range(8) if v&(0x80>>x)}
                ys={y for x,y in points}
                self.assertEqual(ys,set(range(min(ys),max(ys)+1)),(plane,phase))
                reached={next(iter(points))};todo=list(reached)
                while todo:
                    x,y=todo.pop()
                    for dx in (-1,0,1):
                        for dy in (-1,0,1):
                            q=(x+dx,y+dy)
                            if q in points and q not in reached:reached.add(q);todo.append(q)
                self.assertEqual(reached,points,(plane,phase))
