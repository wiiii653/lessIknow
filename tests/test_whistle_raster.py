"""Trace a moving PAL beam, including late callbacks and synthetic stalls.

Tests register/buffer lifetimes between callbacks, rather than only their
final values. This is CPU timing simulation, not full ANTIC emulation.
"""
import unittest
import test_sequence as s
from test_tunnel_raster import BeamMemory
from whistle_pmg import START,END

@unittest.skipIf(s.MPU is None,'py65 required')
class WhistleRasterTests(unittest.TestCase):
    def test_continuous_dma_and_atomic_publish_even_if_preparation_runs_late(self):
        for tick in (5106,5236,5514):
            for line in (0,124,248,254,255,256,290,311):
                for stall in (0,5000):
                    m=BeamMemory(s.XEX.read_bytes());c=s.MPU(memory=m)
                    s.execute(tick-4,c)
                    front=(m[0xd407]&0xfc)<<8
                    old=m[front+0x180:front+0x400]
                    bank=m[0xd301]
                    c.processorCycles=0;m.start=line*114;m.cpu=c;m.events.clear()
                    # execute() supplies the coherent music tick; reads of
                    # VCOUNT follow the beam and continue over PAL frames.
                    import json
                    for i in range(3):m[0x24a7+i]=(tick>>(8*i))&255
                    c.pc=json.loads(s.METADATA.read_text())['callback'];c.sp=0xfd
                    m[0x1fe:0x200]=[0xfe,0x7f];paused=False
                    for _ in range(100000):
                        if c.pc==0x7fff:break
                        c.step()
                        if not paused and any(0x980<=a<0xc00 or 0x8980<=a<0x8c00 for _,a,_ in m.events):
                            c.processorCycles+=stall;paused=True
                    else:self.fail('callback failed to finish')
                    case=(tick,line,stall)
                    self.assertFalse(any(a==0xd01d and v!=3 for _,a,v in m.events),case)
                    self.assertFalse(any(a==0xd400 and v!=0x2e for _,a,v in m.events),case)
                    swaps=[t for t,a,v in m.events if a==0xd407]
                    self.assertEqual(len(swaps),1,case)
                    writes=[t for t,a,v in m.events if 0x980<=a<0xc00 or 0x8980<=a<0x8c00]
                    self.assertLess(max(writes),swaps[0],case)
                    self.assertTrue(248<=swaps[0]/114%312<256,case)
                    self.assertEqual(old,m[front+0x180:front+0x400],case)
                    self.assertEqual(bank,m[0xd301],case)

    def test_scene_exit_still_disables_melody(self):
        m=BeamMemory(s.XEX.read_bytes());c=s.MPU(memory=m)
        s.execute(END-16,c)
        c.processorCycles=0;m.start=248*114;m.cpu=c;m.events.clear()
        s.execute(END,c)
        self.assertEqual(m[0xd01d],0)
        self.assertEqual(m[0xd400]&12,0)
