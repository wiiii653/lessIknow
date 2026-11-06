"""Banked geometric rotozoom and polar mosaic. 64 frames, 160x96, ANTIC E.

Four frames and identical $7C00 copy code per bank. Only the inactive RAM
framebuffer is written; ANTIC never fetches from a banked window.
"""
import math
from pmg_preview import atari_rgb
from functools import lru_cache
from engine_effects import COPY_PAGES, cached_display_list
from build_sequence import Code
from music_timing import tick_at_bar
ENTRY=0x7c00
KALEIDO_START=tick_at_bar(32)
TREVOR_START=tick_at_bar(88)

@lru_cache(maxsize=64)
def pixels(frame):
    phase=(frame&31)/32*math.tau
    angle=phase/4
    scale=0.78+0.3*math.cos(phase)
    co,si=math.cos(angle)*scale,math.sin(angle)*scale
    out=bytearray()
    for y in range(96):
        for x in range(160):
            xx,yy=x-79.5,(y-47.5)*1.66
            if frame<32:
                u=(co*xx-si*yy)/22
                v=(si*xx+co*yy)/22
                a,b=(u+0.5)%1-0.5,(v+0.5)%1-0.5
                radius=math.hypot(a,b)
                angle_cell=math.atan2(b,a)
                petal=0.29+0.07*math.cos(4*angle_cell)
                if abs(radius-petal)<0.035: color=0
                elif radius<0.095: color=3
                elif radius<petal: color=1
                else: color=2
            else:
                radius=math.hypot(xx,yy)
                theta=math.atan2(yy,xx)
                # Curving spiral ribbons and soft starbursts, periodic at wrap.
                wave=math.sin(theta*6+math.log(max(3,radius))*4-phase)
                ripple=math.sin(math.log(max(3,radius))*9-2*phase+math.sin(theta*3))
                if radius<5:color=0
                elif abs(wave)<0.09:color=0
                elif ripple>0.92:color=3
                else:color=1 if wave>0 else 2
            out.append(color)
    return bytes(out)


def palette_pairs():
    """Separate hues by at least 60 degrees and keep both pulse states distinct."""
    angles=(0,42,25,8,330,300,270,240,220,195,165,140,110,80,60,45)
    def separated(a,b,luma_a,luma_b):
        return math.dist(atari_rgb(a*16+luma_a),atari_rgb(b*16+luma_b))>=105
    candidates=[]
    for a in range(1,16):
        for b in range(1,16):
            gap=abs(angles[a]-angles[b]);gap=min(gap,360-gap)
            if gap>=60 and all(separated(a,b,l,l+4) for l in (6,10)):
                candidates.append((a,b))
    assert len(candidates)==144
    pairs=[candidates[(i*73)%len(candidates)] for i in range(len(candidates))]
    alternate=[pair for pair in pairs if all(separated(*pair,l+2,l-2) for l in (6,10))]
    return pairs+alternate[-17:]

def contrast_indices():
    return [i for i,(a,b) in enumerate(palette_pairs())
            if math.dist(atari_rgb(a*16+8),atari_rgb(b*16+8))<105]

def helper():
    c=Code(ENTRY)
    def a(op,address):c.emit(op,address&255,address>>8)
    # Frame number is computed from the coherent music clock by the main callback.
    a(0xad,0x83ed);c.emit(0x09,0x80);a(0xcd,0x83fa)
    c.branch(0xd0,'changed');c.jump(0x4c,'colors')
    c.label('changed');a(0x8d,0x83fa)
    a(0xad,0x83ed);c.emit(0x29,3,0xaa)
    c.jump(0xbd,'source_hi');c.emit(0x48)
    a(0xad,0x83e6);c.emit(0x29,4,0x0a,0x0a,0x0a,0x49,0xb0);a(0x8d,0x83fe)
    c.emit(0x68,0xa2,3);a(0x20,COPY_PAGES)
    cached_display_list(c, 1)
    a(0xad,0x83e6);c.jump(0x8d,'dl1_hi');c.jump(0x8d,'dl2_hi')
    c.emit(0xa9,3);c.jump(0x8d,'dl1_lo');c.emit(0xa9,4);c.jump(0x8d,'dl2_lo');c.emit(0xa0,0)
    c.label('rows');c.jump(0xb9,'row_lo');c.label('dl1');c.emit(0x8d,0,0)
    c.jump(0xb9,'row_hi');c.emit(0x18);a(0x6d,0x83fe);c.label('dl2');c.emit(0x8d,0,0)
    for label in ('dl1','dl2'):
        c.emit(0x18);c.jump(0xad,label+'_lo');c.emit(0x69,3);c.jump(0x8d,label+'_lo');c.branch(0x90,label+'ok');c.jump(0xee,label+'_hi');c.label(label+'ok')
    c.emit(0xc8,0xc0,192);c.branch(0xd0,'rows')
    c.label('swap');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'swap')
    c.emit(0xa9,0);a(0x8d,0xd402);a(0xad,0x83e6);a(0x8d,0xd403);c.emit(0x49,4);a(0x8d,0x83e6)
    c.emit(0xa9,255);a(0x8d,0x83f8);a(0x8d,0x83f9)
    c.label('colors')
    # Preserve v051's visual pulse phase; scene dispatch uses the corrected clock.
    a(0xad,0x83e3);c.emit(0xc9,32912>>8);c.branch(0x90,'intro_base')
    c.emit(0xa2,16);a(0xad,0x83e2);c.emit(0x38,0xe9,32912&255);a(0x8d,0x83ea)
    a(0xad,0x83e3);c.emit(0xe9,32912>>8);a(0x8d,0x83eb);c.branch(0xb0,'mod')
    c.emit(0xa9,0);a(0x8d,0x83ea);a(0x8d,0x83eb);c.jump(0x4c,'mod')
    c.label('intro_base');c.emit(0xa2,0);a(0xad,0x83e2);c.emit(0x38,0xe9,11968&255);a(0x8d,0x83ea)
    a(0xad,0x83e3);c.emit(0xe9,11968>>8);a(0x8d,0x83eb);c.branch(0xb0,'mod')
    c.emit(0xa9,0);a(0x8d,0x83ea);a(0x8d,0x83eb)
    c.label('mod');c.emit(0xa0,7)
    c.label('divide')
    a(0xad,0x83eb);c.jump(0xd9,'divisor_hi');c.branch(0x90,'divide_next');c.branch(0xd0,'divide_sub')
    a(0xad,0x83ea);c.jump(0xd9,'divisor_lo');c.branch(0x90,'divide_next')
    c.label('divide_sub');c.emit(0x38);a(0xad,0x83ea);c.jump(0xf9,'divisor_lo');a(0x8d,0x83ea)
    a(0xad,0x83eb);c.jump(0xf9,'divisor_hi');a(0x8d,0x83eb)
    c.emit(0x8a,0x18);c.jump(0x79,'quotient_bits');c.emit(0xaa)
    c.label('divide_next');c.emit(0x88);c.branch(0x10,'divide')
    a(0xad,0x83ea)
    c.label('beat');c.emit(0xc9,24,0xa9,8);c.branch(0xb0,'luma');c.emit(0xa9,12)
    c.label('luma');a(0x8d,0x83ea)
    c.label('color_wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'color_wait')
    c.label('palette');c.emit(0xe0,161);c.branch(0x90,'palette_index_ok');c.emit(0xa2,160)
    c.label('palette_index_ok');c.emit(0xe0,144);c.branch(0x90,'brightness_ready')
    a(0xad,0x83ea);c.emit(0x18,0x69,2);a(0x8d,0x83ea)
    c.label('brightness_ready');c.jump(0xbd,'hue_pairs');a(0x8d,0x83eb)
    c.emit(0x29,0xf0);a(0x0d,0x83ea);a(0x8d,0xd016)
    # Boost only the second ink of hue pairs that need more contrast at
    # low luminance. Keep the pale pulse below the four-bit maximum.
    a(0xad,0x83ea);c.emit(0xc9,12);c.branch(0xb0,'second_luma_ready')
    c.emit(0xa0,0)
    c.label('contrast_lookup');c.emit(0x8a);c.jump(0xd9,'contrast_indices');c.branch(0xf0,'contrast_boost')
    c.emit(0xc8,0xc0,len(contrast_indices()));c.branch(0xd0,'contrast_lookup');c.jump(0x4c,'second_luma_ready')
    c.label('contrast_boost');a(0xad,0x83ea);c.emit(0x18,0x69,4);a(0x8d,0x83ea)
    c.label('second_luma_ready')
    a(0xad,0x83eb);c.emit(0x29,0x0f,0x0a,0x0a,0x0a,0x0a);a(0x0d,0x83ea);a(0x8d,0xd017)
    c.emit(0xa9,0x0e);a(0x8d,0xd018)
    for addr,val in ((0xd01a,0),(0xd01d,0),(0xd400,0x22)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    for label in ('dl1','dl2'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    c.label('source_hi');c.emit(0x40,0x4f,0x5e,0x6d)
    c.label('divisor_lo');c.emit(*((187<<i)&255 for i in range(8)))
    c.label('divisor_hi');c.emit(*((187<<i)>>8 for i in range(8)))
    c.label('quotient_bits');c.emit(*(1<<i for i in range(8)))
    c.label('contrast_indices');c.emit(*contrast_indices())
    c.label('hue_pairs');c.emit(*((a<<4)|b for a,b in palette_pairs()))
    c.label('row_lo');c.emit(*((y//2*40)&255 for y in range(192)))
    c.label('row_hi');c.emit(*((y//2*40)>>8 for y in range(192)))
    result=c.finish();assert len(result)<=1024,len(result)
    return result

def banks():
    code=helper()
    for bank in range(16):
        out=bytearray(16384)
        out[0x3c00:0x3c00+len(code)]=code
        for half,offset in enumerate((0,0x0f00,0x1e00,0x2d00)):
            p=pixels(bank*4+half)
            out[offset:offset+3840]=bytes(sum(p[i+k]<<(6-k*2) for k in range(4)) for i in range(0,len(p),4))
        yield bytes(out)
