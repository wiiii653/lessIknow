"""Read-only v134 PMG audit; run from repository root.

Uses the built XEX selected by tests/artifact.py. BeamMemory advances VCOUNT
at 114 instruction cycles per PAL scanline and 312 lines per frame. It does
NOT emulate ANTIC DMA, WSYNC, PMG fetches or music NMIs. This demonstrates
the reachable enable/disable race; it is not a live Atari capture or FPS test.
The coverage check uses the same raster mapping as test_tunnel_ball.py.
"""
import sys,json
from pathlib import Path
sys.path[:0]=['tools','tests']
import test_sequence as seq
from scene_memory import RuntimeMemory

cpu=None;holes=[]
for tick in range(38892,39916,4):
    cpu=seq.execute(tick,cpu);m=cpu.memory;miss=[]
    for y in range(88,105):
        for x in range(75,86):
            if (x-79.5)**2+((y//2-47.5)*1.66)**2>=25: continue
            covered=False
            for p in range(4):
                col=(x-(m[0xd000+p]-48))//2
                if 0<=col<8 and m[0xa00+p*128+(y+17)//2]&(0x80>>col): covered=True
            if not covered:miss.append((x,y))
    if miss:holes.append({'tick':tick,'pixels':len(miss),'frame':m[0x83ed],'rotation':(tick&255)//32,'dx':m[0x83e8],'dy':m[0x83e9]})
print('UNCOVERED_HOLE',json.dumps(holes[:10]),'total',len(holes))

class BeamMemory(RuntimeMemory):
    def __init__(self,data):
        super().__init__(data);self.cpu=None;self.events=[];self.start=0
    def __getitem__(self,a):
        if a==0xd40b and self.cpu:
            return ((self.start+self.cpu.processorCycles)//114%312)//2
        return super().__getitem__(a)
    def __setitem__(self,a,v):
        if isinstance(a,int) and self.cpu and (0x980<=a<0xc00 or a in (0xd000,0xd01d,0xd403)):
            self.events.append((self.cpu.processorCycles,a,v))
        super().__setitem__(a,v)

m=BeamMemory(seq.XEX.read_bytes());cpu=seq.MPU(memory=m);m.cpu=cpu
for start,tick in [(s,38904) for s in range(300,310)]:
    m.cpu=None;cpu=seq.execute(tick,cpu);m.cpu=cpu
    cpu.processorCycles=0;m.start=start*114;m.events=[]
    m[0x24a7]=tick&255;m[0x24a8]=tick>>8;m[0x24a9]=0
    cpu.sp=0xfd;m[0x1fe:0x200]=[0xfe,0x7f];cpu.pc=json.loads(seq.METADATA.read_text())['callback']
    enter=None
    for i in range(300000):
        if cpu.pc==0x7fff: break
        if cpu.pc==0x7800:enter=cpu.processorCycles
        cpu.step()
    writes=[e for e in m.events if 0x980<=e[1]<0xc00]
    def loc(c):return (round((m.start+c)/114,2), round(((m.start+c)/114)%312,2))
    print('BEAM',start,tick,'enter',loc(enter),'firstwrite',loc(writes[0][0]),'lastwrite',loc(writes[-1][0]),'cycles',writes[-1][0]-writes[0][0])
    print('GRACTL',[(loc(c),v) for c,a,v in m.events if a==0xd01d])
