"""Reconstruct outro ANTIC/PMG frames (approximate PAL colours, not a capture).

ATARI_TEST_XEX=build/visual-prototype-v224.xex PYTHONPATH=tools:tests python tools/preview_outro.py
Requires py65 and Pillow. The default output is build/outro-preview.png.
"""
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',default='build/outro-preview.png')
parser.add_argument('--animate',action='store_true')
args=parser.parse_args()
import test_sequence as s
import outro_text as text
from PIL import Image
from pmg_preview import atari_rgb
out=Image.new('RGB',(960,235));cpu=None;frames=[]
ticks=range(text.START,text.START+1000,8) if args.animate else (text.START+300,text.page_starts()[5]+300,text.END)
for idx,tick in enumerate(ticks):
 cpu=s.execute(tick,cpu);m=cpu.memory;dl=m[0xd402]|m[0xd403]<<8;pc=dl;lines=[]
 pal=[atari_rgb(m[a]) for a in (0xd01a,0xd016,0xd017,0xd018)]
 for _ in range(220):
  op=m[pc];pc+=1;mode=op&15
  if mode==1:break
  if mode==0:lines.extend([[pal[0]]*320 for _ in range(((op>>4)&7)+1)]);continue
  if op&64:addr=m[pc]|m[pc+1]<<8;pc+=2
  if mode in (2,4):
   for y in range(8):
    line=[]
    for char in m[addr:addr+40]:
     bits=m[0xc800+(char&127)*8+y] ^ (255 if char&128 else 0)
     if mode==2:line.extend(atari_rgb(0xce) if bits&(128>>x) else atari_rgb(0) for x in range(8))
     else:
      for x in range(4):line.extend([atari_rgb(0x0e if (m[0x83e2]&0xfc)==0 else 0xce) if (bits>>(6-x*2))&3 else (0,0,0)]*2)
    lines.append(line)
  elif mode==14:
   line=[]
   for byte in m[addr:addr+40]:
    for shift in (6,4,2,0):line.extend([pal[(byte>>shift)&3]]*2)
   lines.append(line)
 im=Image.new('RGB',(320,235));pix=im.load()
 for y,line in enumerate(lines[:235]):
  for x,color in enumerate(line):pix[x,y]=color
 base=(m[0xd407]&0xfc)<<8
 for plane in range(3,-1,-1):
  left=(m[0xd000+plane]-48)*2;color=atari_rgb(m[0xd012+plane])
  for y in range(235):
   bits=m[base+0x200+plane*128+(y+8)//2]
   for x in range(8):
    if bits&(128>>x):
     for dx in range(2):
      xx=left+x*2+dx
      if 0<=xx<320:pix[xx,y]=color
 if args.animate:frames.append(im.resize((640,470)))
 else:out.paste(im,(idx*320,0))
if args.animate:frames[0].save(args.output,save_all=True,append_images=frames[1:],duration=40,loop=0)
else:out.resize((1920,470)).save(args.output)
