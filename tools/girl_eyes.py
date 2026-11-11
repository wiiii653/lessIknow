"""Animated close-up for the post-Trevor montage, in four tunnel slots."""
import math
from functools import lru_cache
from build_sequence import Code

START = 43379 - 4000
END = START + 748
BANK_ENTRY = 0x7500

@lru_cache(maxsize=4)
def pixels(phase):
    """Four hand-drawn 160x96 ANTIC E images: glance, glance, blink, glance."""
    out = bytearray(160 * 96)
    for y in range(96):
        for x in range(160):
            # A dark face framing the eyes, with two arched eyebrows.
            color = 1 if 15 < x < 145 and 17 < y < 78 else 0
            for cx in (47, 113):
                dx=x-cx
                brow=25 + .008 * dx * dx
                if abs(dx)<27 and abs(y-brow)<2.3: color=0
                # Almond-shaped eyelids, tapered at both corners.
                if abs(dx) <= 28:
                    u=abs(dx)/28
                    middle=50 + .035*dx*(1 if cx==47 else -1)
                    height=(1-u*u)*10
                    if phase == 2: height=0.7
                    if abs(y-middle)<=height+2: color=0
                    if height>2 and abs(y-middle)<height-1: color=3
                    pupil_x=cx+(-5,0,0,5)[phase]
                    if height>2 and ((x-pupil_x)/6)**2+((y-middle)/8)**2<1:
                        color=2
                        if ((x-pupil_x)/3)**2+((y-middle)/5)**2<1: color=0
                        if (x-pupil_x+2)**2+(y-middle+3)**2<3: color=3
                # Thick eyelashes at outer corners.
                for lash in range(3):
                    lx=cx + (-1 if cx==47 else 1)*(19+lash*3)
                    ly=44+lash
                    if abs(x-lx)<=1 and ly-4<=y<=ly+2: color=0
            out[y*160+x]=color
    return bytes(out)

def frame_at(tick, frame, scene=6):
    if scene == 6 and START <= tick < END:
        return 60 + ((tick >> 5) & 3)
    return frame-4 if 60 <= frame < 64 else frame

def helper():
    c=Code(BANK_ENTRY)
    def a(op,addr): c.emit(op,addr&255,addr>>8)
    a(0xad,0x83e0);c.emit(0xc9,6);c.branch(0xd0,'normal')
    a(0xad,0x83e3);c.emit(0xc9,START>>8);c.branch(0x90,'normal');c.branch(0xd0,'check_end')
    a(0xad,0x83e2);c.emit(0xc9,START&255);c.branch(0x90,'normal')
    c.label('check_end');a(0xad,0x83e3);c.emit(0xc9,END>>8);c.branch(0x90,'eyes');c.branch(0xd0,'normal')
    a(0xad,0x83e2);c.emit(0xc9,END&255);c.branch(0xb0,'normal')
    c.label('eyes');a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x4a,0x29,3,0x09,60);c.jump(0x4c,'save')
    c.label('normal');a(0xad,0x83ed);c.emit(0xc9,60);c.branch(0x90,'done');c.emit(0xc9,64);c.branch(0xb0,'done');c.emit(0x38,0xe9,4)
    c.label('save');a(0x8d,0x83ed)
    c.label('done');c.emit(0x60)
    data=bytes(c.finish());assert BANK_ENTRY+len(data)<=0x7600
    return data
