"""Title reveal order, foreground fireworks and safe buffer ownership."""
import json
import unittest
import test_sequence as sequence
from test_engine_cache import TrackedMemory
from test_tunnel_raster import BeamMemory
from title_plasma import artwork, FRAME_BYTES
from title_fireworks import graphics, occupied, anchors, CENTRES, missile_fragments


class TitleFireworkTests(unittest.TestCase):
    def test_water_reflects_the_live_plasma_and_releases_both_lists(self):
        from main_act_terminal import SCHOOL_START
        from title_plasma import (
            CITY_REVEAL_START, PLASMA_STEP_TICKS, TRANSITION_START,
            city_reveal_level, procedural_frame,
        )
        from title_water import (
            BUFFER_PAIRS, FIRST_FADE_OUT_PHASE, FOOTER_OFFSET, LAST_FADE_OUT_PHASE,
            PIXELS_OFFSET, ROW_BYTES, ROW_COUNT,
            TAIL_OFFSET, TAIL_SIZE, reflection, tail,
        )

        memory = TrackedMemory(sequence.XEX.read_bytes())
        cpu = sequence.MPU(memory=memory)
        sequence.execute(CITY_REVEAL_START-1, cpu)
        for display, _ in BUFFER_PAIRS:
            self.assertEqual(memory[display+FOOTER_OFFSET:display+FOOTER_OFFSET+3],
                             [0x70]*3)

        visible = set()
        for tick in (1024, 1040, 1120, 1248, 1344, 1504, 2048, 2080, 2920, 2984):
            active = (memory[0xd403] << 8) | memory[0xd402]
            active_buffer = dict(BUFFER_PAIRS)[active]
            memory.writes.clear()
            sequence.execute(tick, cpu)
            display = (memory[0xd403] << 8) | memory[0xd402]
            framebuffer = dict(BUFFER_PAIRS)[display]
            address = framebuffer + PIXELS_OFFSET
            tail_address = framebuffer + TAIL_OFFSET
            jump = bytes((1, tail_address & 255, tail_address >> 8))
            self.assertEqual(bytes(memory[display+FOOTER_OFFSET:display+FOOTER_OFFSET+3]), jump)
            self.assertEqual(bytes(memory[tail_address:tail_address+TAIL_SIZE]), tail(display, framebuffer))
            phase = (tick // PLASMA_STEP_TICKS) & 127
            level = city_reveal_level(tick)
            fade = (tick - TRANSITION_START) // 32
            if fade >= FIRST_FADE_OUT_PHASE:
                level = LAST_FADE_OUT_PHASE - fade
            expected = reflection(level, phase, procedural_frame(phase, 0))
            self.assertEqual(bytes(memory[address:address+ROW_BYTES*ROW_COUNT]), expected)
            self.assertFalse(any(active_buffer+PIXELS_OFFSET <= a <
                                 active_buffer+TAIL_OFFSET+TAIL_SIZE for a in memory.writes))
            visible.add(display)
        self.assertEqual(visible, dict(BUFFER_PAIRS).keys())

        for next_tick in (SCHOOL_START, 0):
            sequence.execute(next_tick, cpu)
            for display, _ in BUFFER_PAIRS:
                self.assertEqual(memory[display+FOOTER_OFFSET:display+FOOTER_OFFSET+3],
                                 [0x70]*3)
            sequence.execute(1408, cpu)
            sequence.execute(1424, cpu)

    def test_opening_introduces_fireworks_one_at_a_time(self):
        cpu = None
        for tick, expected in ((767, 0), (768, 1), (1215, 1), (1216, 2),
                               (1407, 2), (1408, 3), (1855, 3), (1856, 4)):
            cpu = sequence.execute(tick, cpu)
            memory = cpu.memory
            base = (memory[0xd407] & 0xfc) << 8
            for plane in range(4):
                shape = memory[base + 0x200 + plane * 128:base + 0x280 + plane * 128]
                self.assertEqual(any(shape), plane < expected, (tick, plane))
            if tick < 2048:
                self.assertFalse(any(memory[base + 0x180:base + 0x200]))

    def test_city_reveal_survives_music_interrupts(self):
        import json
        from title_plasma import FRAME_BYTES, PLASMA_ENTRY, SKYLINE_FIRST_PAGE

        cpu = sequence.MPU(memory=sequence.RuntimeMemory(sequence.XEX.read_bytes()))
        memory = cpu.memory
        tick = 2400
        memory[0xd40b] = 124
        memory[0xd301] = memory.values[3]
        for address in (0x232d, 0x237d):
            cpu.pc = address
            cpu.sp = 0xfd
            memory[0x1fe:0x200] = [0xfe, 0x7f]
            for _ in range(10000):
                if cpu.pc == 0x7fff:
                    break
                cpu.step()
            else:
                self.fail('music init did not return')
        memory[0xd301] = 0xff
        memory[0x24a7:0x24aa] = tick.to_bytes(3, 'little')
        cpu.pc = json.loads(sequence.METADATA.read_text())['callback']
        cpu.sp = 0xfd
        memory[0x1fe:0x200] = [0xfe, 0x7f]
        interrupts = 0
        for _ in range(100000):
            if cpu.pc == 0x7fff:
                break
            # Interrupt while the city groups are being composited. The music
            # NMI stores PORTB in $83EE, formerly shared with the reveal rank.
            opcode = memory[cpu.pc]
            if PLASMA_ENTRY <= cpu.pc < 0x4400 and opcode == 0xbe:
                resume = cpu.pc
                bank = memory[0xd301]
                cpu.nmi()
                for _ in range(10000):
                    cpu.step()
                    if cpu.pc == resume:
                        break
                else:
                    self.fail('music NMI did not return')
                self.assertEqual(memory[0xd301], bank)
                interrupts += 1
                # One interruption is enough to expose a shared rank.
                cpu.step()
                break
            cpu.step()
        self.assertEqual(interrupts, 1)
        for _ in range(100000):
            if cpu.pc == 0x7fff:
                break
            cpu.step()
        else:
            self.fail('title callback did not return')

        reference = sequence.execute(tick)
        actual, expected = memory, reference.memory
        actual_dl = actual[0xd403] << 8
        expected_dl = expected[0xd403] << 8
        actual_base = actual[actual_dl+3] | actual[actual_dl+4] << 8
        expected_base = expected[expected_dl+3] | expected[expected_dl+4] << 8
        offset = SKYLINE_FIRST_PAGE * 256
        self.assertEqual(bytes(actual[actual_base+offset:actual_base+FRAME_BYTES]),
                         bytes(expected[expected_base+offset:expected_base+FRAME_BYTES]))

    def test_live_fireworks_are_complete_at_full_intensity(self):
        from pmg_preview import player_masks
        from title_plasma import zuraw_hue
        data=graphics(bytes(FRAME_BYTES));cpu=None;overlaps=[0,0]
        for tick in range(2048, 2560, 32):
            cpu=sequence.execute(tick,cpu);m=cpu.memory
            phase=(m[0x83e2]>>4)&15;base=(m[0xd407]&0xfc)<<8
            for p in range(5):
                start=p*512+phase*32 if p<4 else 2048+phase*64
                size=32 if p<4 else 64
                target=base+(0x200+p*128 if p<4 else 0x180)+anchors((tick>>2)&63)[p]
                self.assertEqual(bytes(m[target:target+size]),data[start:start+size],(tick,p))
            mask=bytes(m[0xa000:0xaa00])
            composite=player_masks(bytes(160*192),m,192,raster_start=8,pmg_color_offset=16)
            for y in range(192):
                for x in range(160):
                    if composite[y*160+x]<16:continue
                    overlaps[0]+=occupied(mask,x,y)
                    overlaps[1]+=zuraw_hue(x//2,y//3) is not None
            self.assertEqual(m[0xd01b],0xc1)
        self.assertTrue(all(overlaps),overlaps)

    def test_raised_title_enters_middle_then_bottom_then_top(self):
        masks=artwork()[4]
        stages=[masks[i*FRAME_BYTES:(i+1)*FRAME_BYTES] for i in (3,4,5)]
        def rows(mask,start,end):return any(mask[start*40:end*40])
        self.assertFalse(rows(stages[0],0,11))
        self.assertTrue(rows(stages[0],11,21))
        self.assertFalse(rows(stages[0],21,64))
        self.assertFalse(rows(stages[1],0,11))
        self.assertTrue(rows(stages[1],22,32))
        self.assertTrue(rows(stages[2],0,11))
        self.assertEqual(stages[0][11*40:21*40],stages[2][11*40:21*40])
        self.assertEqual(stages[1][22*40:],stages[2][22*40:])

    def test_both_cards_leave_the_zuraw_and_city_uncovered(self):
        from title_plasma import ZURAW_TOP, ZURAW_LEFT, ZURAW, ZURAW_WIDTH, ZURAW_HEIGHT, zuraw_hue
        masks=artwork()[4]
        for index in (1,5):
            mask=masks[index*FRAME_BYTES:(index+1)*FRAME_BYTES]
            self.assertFalse(any(mask[ZURAW_TOP*40:]))
        self.assertEqual((ZURAW_WIDTH,ZURAW_HEIGHT),(36,29))
        self.assertGreater(sum(v is not None for row in ZURAW for v in row),600)
        # The rear gatehouse joins the left tower to the timber shaft at
        # every facade row: no transparent plasma slit may split the building.
        for y in range(16,26):
            self.assertNotIn(None,ZURAW[y][13:20],y)
        inks={v for row in ZURAW for v in row}
        self.assertTrue({0,1,3,9,10}.issubset(inks))

    def test_all_phases_ignore_text_masks_and_keep_falling_sparks(self):
        data=graphics(bytes(FRAME_BYTES))
        self.assertEqual(data,graphics(bytes([255])*FRAME_BYTES))
        self.assertEqual(len(data),3072)
        for phase in range(16):
            for p in range(4):
                stream=data[p*512+phase*32:p*512+(phase+1)*32]
                self.assertGreaterEqual(sum(v.bit_count() for v in stream),2,(p,phase))
            missiles=data[2048+phase*64:2048+(phase+1)*64]
            self.assertTrue(any(missiles),(phase,missiles))
        # Late fragments descend after the burst and shrink in pixel count.
        first=data[9*32:10*32];last=data[15*32:16*32]
        self.assertGreater(sum(last[i]*i for i in range(32))/sum(last),
                           sum(first[i]*i for i in range(32))/sum(first))
        self.assertLess(sum(v.bit_count() for v in last),sum(v.bit_count() for v in first))

    def test_rockets_rise_from_bottom_and_burst_in_the_upper_sky(self):
        from pmg_preview import player_masks
        for plane in range(4):
            # Same cycle, staggered by one quarter for the four rockets.
            start=2048+((-plane*64)&255)
            head_rows=[]
            for age in range(16):
                tick=start+age*4;m=sequence.execute(tick).memory
                base=(m[0xd407]&0xfc)<<8
                rows=[r for r in range(128) if m[base+0x200+plane*128+r]]
                head_rows.append(2*min(rows)-8)
            self.assertGreaterEqual(head_rows[0],188)
            self.assertEqual(head_rows,sorted(head_rows,reverse=True))
            self.assertLess(head_rows[-1],CENTRES[plane][1]+12)
            m=sequence.execute(start+64).memory
            base=(m[0xd407]&0xfc)<<8
            flash=m[base+0x200+plane*128:base+0x280+plane*128]
            self.assertGreater(sum(v.bit_count() for v in flash),25)
            centre=(CENTRES[plane][1]+8)//2
            self.assertEqual(flash[centre],255)
            self.assertLess(2*centre-8,80)

    def test_burst_cycles_rainbow_and_detached_missiles_spread(self):
        for plane in range(4):
            start=2048+((-plane*64)&255)+64
            colours=set();positions=[]
            for age in range(0,128,4):
                tick=start+age;m=sequence.execute(tick).memory
                colours.add(m[0xd012+plane]>>4)
                self.assertEqual(m[0xd012+plane]&15,14)
                self.assertEqual(m[0xd004+plane],missile_fragments((tick>>2)&63,plane)[0])
                positions.append(m[0xd004+plane])
            self.assertGreaterEqual(len(colours),12)
            self.assertGreaterEqual(max(positions)-min(positions),20)

    def test_fireworks_keep_gtia11_and_use_only_inactive_pmg(self):
        from engine_effects import PMBASE_SHADOW

        class WriteOnlyPMBaseMemory(TrackedMemory):
            def __getitem__(self, address):
                if address == 0xd407:
                    return 0xff
                return super().__getitem__(address)

        memory = WriteOnlyPMBaseMemory(sequence.XEX.read_bytes())
        cpu = sequence.MPU(memory=memory)
        sequence.execute(96, cpu)
        for tick in (112,256,768,1496,1752,2008,2304,32,96,1592):
            m = cpu.memory
            active = (m[PMBASE_SHADOW] & 0xfc) << 8
            m.writes.clear()
            sequence.execute(tick, cpu)
            self.assertEqual((m[PMBASE_SHADOW] & 0xfc) << 8, active ^ 0x8000)
            self.assertFalse(any(active+0x180<=a<active+0x400 for a in m.writes),tick)
            self.assertEqual(m[0xd01b],0xc1)
            self.assertEqual(m[0xd400],0x2e)
            self.assertEqual(m[0xd301],0xff)
        sequence.execute(2992,cpu)
        self.assertEqual(cpu.memory[0xd01b]&0xc0,0)

    def test_late_raster_does_not_blank_the_last_burst(self):
        for line in (248,255,290,305,306,311):
            m=BeamMemory(sequence.XEX.read_bytes());cpu=sequence.MPU(memory=m)
            sequence.execute(768,cpu)
            cpu.processorCycles=0;m.start=line*114;m.cpu=cpu;m.events=[]
            cpu.pc=json.loads(sequence.METADATA.read_text())['callback'];cpu.sp=0xfd
            m[0x1fe:0x200]=[0xfe,0x7f]
            for _ in range(100000):
                if cpu.pc==0x7fff:break
                cpu.step()
            else:self.fail('callback did not return')
            self.assertFalse(any(a==0xd01d and v!=3 for _,a,v in m.events))
            commits=[t/114%312 for t,a,v in m.events if 0xd000<=a<=0xd015 or a==0xd01d]
            self.assertGreaterEqual(min(commits),248)
            self.assertLess(max(commits),260)
