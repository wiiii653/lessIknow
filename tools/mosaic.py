"""Banked rotozoom and polar mosaic. 64 runtime frame IDs, 160x96, ANTIC E.

Banana banks hold four raw frames from either of the two 32-phase motifs.
Tunnel banks keep four raw frames and $7C00
copy code. Only the inactive RAM framebuffer is written;
ANTIC never fetches from a banked window.
"""
import math
from pmg_preview import atari_rgb
from functools import lru_cache
from engine_effects import COPY_PAGES, cached_display_list
from build_sequence import Code
from music_timing import tick_at_bar
from post_trevor_director import LATE_BANANA_START
ENTRY=0x7c00
HIGHLIGHT_SHIFT=6  # Hold each hue for 16 PAL frames.
KALEIDO_START=tick_at_bar(32)
TREVOR_START=tick_at_bar(88)-4000

@lru_cache(maxsize=1)
def banana_tile():
    """Hand-traced hanging bunch; distinct tips, black seams and golden ribs."""
    shapes = (
        ((43,12),(48,21),(50,32),(47,43),(40,52),(29,57),(18,57),(11,52),
         (22,51),(32,45),(38,36),(40,25),(39,15)),
        ((38,13),(42,23),(41,34),(36,45),(27,51),(17,52),(9,48),(6,43),
         (17,45),(26,40),(31,32),(33,22),(33,15)),
        ((32,13),(35,22),(32,31),(26,39),(17,43),(9,42),(4,36),(4,32),
         (12,36),(19,33),(24,27),(27,19),(27,14)),
    )
    def contains(x,y,poly):
        hit=False
        for (ax,ay),(bx,by) in zip(poly,poly[1:]+poly[:1]):
            if (ay>y)!=(by>y) and x < (bx-ax)*(y-ay)/(by-ay)+ax:
                hit=not hit
        return hit
    tile=bytearray([2]*4096)
    for shape in shapes:
        mask={(x,y) for y in range(64) for x in range(64)
              if contains(x+.5,y+.5,shape)}
        for x,y in mask:
            edge=any((x+dx,y+dy) not in mask for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
            shade=any((x+dx,y+dy) not in mask for dx,dy in ((2,0),(0,2)))
            tile[y*64+x]=0 if edge else 1 if shade else 3
    # Thick cut stalk and crown visibly join the three separate fruit.
    stalk=((27,15),(32,8),(35,3),(41,4),(40,9),(44,14),(40,19),(33,18))
    for y in range(3,20):
        for x in range(26,45):
            if contains(x+.5,y+.5,stalk):
                tile[y*64+x]=0 if y<6 or x<30 or x>40 else 1
    return bytes(tile)

@lru_cache(maxsize=128)
def pixels(frame,variant=0):
    phase=((frame+(16 if variant and frame<32 else 0))&31)/32*math.tau
    # A full turn over all 32 stored frames. A quarter-turn cannot wrap
    # seamlessly for the asymmetric banana tile.
    angle=phase
    scale=0.78+0.3*math.cos(phase)
    co,si=math.cos(angle)*scale,math.sin(angle)*scale
    if frame<32:
        from banana_variants import peeled_tile
        tile=peeled_tile() if variant else banana_tile()
    out=bytearray()
    for y in range(96):
        for x in range(160):
            xx,yy=x-79.5,(y-47.5)*1.66
            if frame<32:
                u=int(co*xx-si*yy+32)%64
                v=int(si*xx+co*yy+32)%64
                color=tile[v*64+u]
            else:
                radius=math.hypot(xx,yy)
                theta=math.atan2(yy,xx)
                # The eye portrait owns IDs 60–63, so the organic tunnel
                # uses twelve evenly spaced frames in IDs 48–59. Its phase
                # still completes a full revolution at the same cadence.
                tunnel_phase=((frame-48)%12)/12*math.tau if frame>=48 else (frame&15)/16*math.tau
                if frame<48:
                    # First tunnel texture: the existing curling spiral.
                    wave=math.sin(theta*6+math.log(max(3,radius))*4-tunnel_phase)
                    ripple=math.sin(math.log(max(3,radius))*9-2*tunnel_phase+math.sin(theta*3))
                    if radius<5:color=0
                    elif abs(wave)<0.09:color=0
                    elif ripple>0.92:color=3
                    else:color=1 if wave>0 else 2
                else:
                    # Warped liquid folds: continuous contours instead of
                    # intersecting radial/ring signs that formed a checkerboard.
                    depth=math.log(max(3,radius))
                    bend=theta+0.28*math.sin(depth*2.7-tunnel_phase)
                    fold=math.sin(5*bend+depth*5.2-tunnel_phase
                                  +1.2*math.sin(3*theta+depth*1.7+tunnel_phase))
                    glow=math.sin(depth*7-2*tunnel_phase
                                  +2*math.sin(bend*3+tunnel_phase))
                    if radius<5:color=0
                    elif abs(fold)<0.075:color=0
                    elif fold>0.76 and glow>0.25:color=3
                    else:color=1 if fold>0 else 2
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

def helper(origin=ENTRY,copy_entry=COPY_PAGES,cache_key=None,banana_only=False,cache_address=0x83fa,raw=False,peeled=False):
    c=Code(origin)
    def a(op,address):c.emit(op,address&255,address>>8)
    def highlight_index():
        a(0xad,0x83e3);c.emit(0x0a,0x0a);a(0x8d,0x83ea)
        a(0xad,0x83e2);c.emit(*([0x4a]*HIGHLIGHT_SHIFT))
        a(0x0d,0x83ea);c.emit(0x29,15,0xaa)
    def before_late(early, late):
        a(0xad,0x83e3);c.emit(0xc9,LATE_BANANA_START>>8)
        c.branch(0x90,early);c.branch(0xd0,late)
        a(0xad,0x83e2);c.emit(0xc9,LATE_BANANA_START&255)
        c.branch(0x90,early)
    # Frame number is computed from the coherent music clock by the main callback.
    a(0xad,0x83ed)
    if cache_key is None:c.emit(0x09,0x80)
    else:a(0x0d,cache_key)
    a(0xcd,cache_address)
    c.branch(0xd0,'changed');c.jump(0x4c,'colors')
    c.label('changed');a(0x8d,cache_address)
    if not banana_only or raw:
        a(0xad,0x83ed);c.emit(0x29,3,0xaa)
        c.jump(0xbd,'source_hi');c.emit(0x48)
    a(0xad,0x83e6);c.emit(0x29,4,0x0a,0x0a,0x0a,0x49,0xb0);a(0x8d,0x83fe)
    if not banana_only or raw:c.emit(0x68,0xa2,3)
    a(0x20,copy_entry)
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
    a(0xad,0x0dd4);c.emit(0xc9,32912>>8);c.branch(0x90,'intro_base')
    c.emit(0xa2,16);a(0xad,0x0dd3);c.emit(0x38,0xe9,32912&255);a(0x8d,0x83ea)
    a(0xad,0x0dd4);c.emit(0xe9,32912>>8);a(0x8d,0x83eb);c.branch(0xb0,'mod')
    c.emit(0xa9,0);a(0x8d,0x83ea);a(0x8d,0x83eb);c.jump(0x4c,'mod')
    c.label('intro_base');c.emit(0xa2,0);a(0xad,0x0dd3);c.emit(0x38,0xe9,11968&255);a(0x8d,0x83ea)
    a(0xad,0x0dd4);c.emit(0xe9,11968>>8);a(0x8d,0x83eb);c.branch(0xb0,'mod')
    c.emit(0xa9,0);a(0x8d,0x83ea);a(0x8d,0x83eb)
    c.label('mod');c.emit(0xa0,7)
    c.label('divide')
    a(0xad,0x83eb);c.jump(0xd9,'divisor_hi');c.branch(0x90,'divide_next');c.branch(0xd0,'divide_sub')
    a(0xad,0x83ea);c.jump(0xd9,'divisor_lo');c.branch(0x90,'divide_next')
    c.label('divide_sub');c.emit(0x38);a(0xad,0x83ea);c.jump(0xf9,'divisor_lo');a(0x8d,0x83ea)
    a(0xad,0x83eb);c.jump(0xf9,'divisor_hi');a(0x8d,0x83eb)
    c.emit(0x8a,0x18);c.jump(0x79,'quotient_bits');c.emit(0xaa)
    c.label('divide_next');c.emit(0x88);c.branch(0x10,'divide')
    # Change the hue pair on the music cue with steady brightness.
    c.emit(0xa9,6);a(0x8d,0x83ea)
    c.label('color_wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'color_wait')
    c.label('palette');c.emit(0xe0,161);c.branch(0x90,'palette_index_ok');c.emit(0xa2,160)
    c.label('palette_index_ok');c.emit(0xe0,144);c.branch(0x90,'brightness_ready')
    a(0xad,0x83ea);c.emit(0x18,0x69,2);a(0x8d,0x83ea)
    c.label('brightness_ready');c.jump(0xbd,'hue_pairs');a(0x8d,0x83eb)
    c.emit(0x29,0xf0);a(0x0d,0x83ea);a(0x8d,0xd016)
    # Keep the second ink brighter while the darker first ink keeps the PAL
    # hues strong.
    a(0xad,0x83ea);c.emit(0x18,0x69,4);a(0x8d,0x83ea)
    a(0xad,0x83eb);c.emit(0x29,0x0f,0x0a,0x0a,0x0a,0x0a);a(0x0d,0x83ea);a(0x8d,0xd017)
    # On the late banana passes, cycle only the backdrop (PF1).
    if banana_only and raw:
        before_late('early_banana','late_banana_hue')
        c.label('late_banana_hue')
        highlight_index()
        c.jump(0xbd,'hue_pairs');c.emit(0x29,0xf0,0x09,0x0a);a(0x8d,0xd017)
        c.jump(0x4c,'banana_highlight')
        c.label('early_banana')
        c.emit(0xa9,0xee);a(0x8d,0xd018)
        c.emit(0xa9,0xca if peeled else 0xea);a(0x8d,0xd016)
        c.jump(0x4c,'highlight_done')
    if not banana_only:
        a(0xad,0x83ed);c.emit(0xc9,32);c.branch(0x90,'banana_highlight')
        before_late('early_tunnel','tunnel_hue')
        c.label('tunnel_hue')
        c.emit(0xa9,0x0a);c.branch(0xd0,'tunnel_luma')
        c.label('early_tunnel')
        c.emit(0xa9,0x08)
        c.label('tunnel_luma')
        c.jump(0x8d,'highlight_luma')
        highlight_index()
        c.jump(0xbd,'hue_pairs');c.emit(0x29,0xf0,0x09)
        c.label('highlight_luma');c.emit(0)
        a(0x8d,0xd018)
        c.jump(0x4c,'highlight_done')
    c.label('banana_highlight');c.emit(0xa9,0xee);a(0x8d,0xd018)
    # Bright yellow flesh with a lighter yellow highlight.
    c.emit(0xa9,0xec if not peeled else 0xea);a(0x8d,0xd016)
    c.label('highlight_done')
    # Keep the previous ball and its DMA alive until the PMG helper can
    # safely update it. A second wait may cross an entire frame boundary.
    for addr,val in ((0xd01a,0),):
        c.emit(0xa9,val);a(0x8d,addr)
    if raw:c.emit(0xa9,0xff);a(0x8d,0x83fa)
    c.emit(0x60)
    for label in ('dl1','dl2'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    if not banana_only or raw:
        c.label('source_hi');c.emit(0x40,0x4f,0x5e,0x6d)
    c.label('divisor_lo');c.emit(*((187<<i)&255 for i in range(8)))
    c.label('divisor_hi');c.emit(*((187<<i)>>8 for i in range(8)))
    c.label('quotient_bits');c.emit(*(1<<i for i in range(8)))
    c.label('hue_pairs');c.emit(*((a<<4)|b for a,b in palette_pairs()))
    c.label('row_lo');c.emit(*((y//2*40)&255 for y in range(192)))
    c.label('row_hi');c.emit(*((y//2*40)>>8 for y in range(192)))
    result=c.finish();assert len(result)<=1024,len(result)
    return result

def banks():
    code=helper()
    for bank in range(16):
        if bank<8:
            from banana_variants import raw_bank as banana_bank
            yield banana_bank(bank)
            continue
        out=bytearray(16384)
        out[0x3c00:0x3c00+len(code)]=code
        for half,offset in enumerate((0,0x0f00,0x1e00,0x2d00)):
            frame=bank*4+half
            if frame>=60:
                from girl_eyes import pixels as eye_pixels
                p=eye_pixels(frame-60)
            else:
                p=pixels(frame)
            out[offset:offset+3840]=bytes(sum(p[i+k]<<(6-k*2) for k in range(4)) for i in range(0,len(p),4))
        yield bytes(out)
