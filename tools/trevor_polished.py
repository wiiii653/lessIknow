"""Trevor reveal, alternating punches and synchronized comic impacts."""
import math
from pathlib import Path
from engine_effects import COPY_PAGES, cached_display_list, clear_pmg
from build_sequence import Code
from trevor_awakens import COLORS, HIT as TREVOR_HIT, END as TREVOR_END, MIDPOINT as TREVOR_MIDPOINT
from music_timing import tick_at_beat
ENTRY=0x6000
LETTER_END=80
BUBBLE_END=104
EFFECT_END=136
# A two-bar combination mixing one-and-a-half- and two-beat gaps.
# 2 and 4 are the right- and left-handed punch poses respectively.
COMBO_HALF_BEATS = (0, 3, 6, 9, 12)
COMBO_HANDS = (2, 4, 4, 2, 4)
HITS = tuple(32 + tick_at_beat(72*8 + block*16 + half, 2)
             for block in range(8) for half in COMBO_HALF_BEATS)
HANDS = COMBO_HANDS * 8
assert HITS[0] == TREVOR_HIT + 32 and HITS[-1] < TREVOR_END


def impact_anchor(index):
    """Repeatable xorshift scatter, held for the whole hit; close to its fist."""
    seed=0x6d2b
    for _ in range(index+1):
        seed^=(seed<<7)&0xffff;seed^=seed>>9;seed^=(seed<<8)&0xffff
    base_x,base_y=(-2,-1) if HANDS[index]==2 else (-38,2)
    return base_x+seed%13-6,base_y+(seed>>8)%7-3


# Near entrance pose is composited over the same gym as the distant pose.
# Black pixels inside the actor stay opaque; the old rectangular black gym
# backing must not cover the doorway and wall behind his shoulders.
ENTRANCE_OUTLINE = (
 (65,13),(70,13),(75,12),(78,10),(81,12),(87,12),(89,14),
 (91,14),(92,17),(93,19),(97,19),(99,21),(99,24),(96,26),
 (94,26),(95,29),(102,30),(108,32),(113,35),(117,39),
 (125,42),(129,47),(131,52),(132,57),(130,61),(130,64),
 (29,64),(29,60),(27,57),(27,53),(30,48),(33,44),(38,40),
 (41,36),(45,32),(52,29),(61,28),(65,27),(62,25),(60,25),
 (60,21),(62,19),(65,19),(66,17),(65,16),
)
_ENTRANCE_LEFT_GAP = ((44,64),(46,58),(50,55),(50,51),(56,47),
                      (60,48),(61,54),(57,57),(54,64))
ENTRANCE_GAPS = (_ENTRANCE_LEFT_GAP,
                 tuple((159-x,y) for x,y in reversed(_ENTRANCE_LEFT_GAP)))


def entrance_mask():
    return bytes(inside(x+.5,y+.5,ENTRANCE_OUTLINE) and
                 not any(inside(x+.5,y+.5,gap) for gap in ENTRANCE_GAPS)
                 for y in range(64) for x in range(160))


def frames():
    out=[]
    for i in range(4):
        rgb=Path(f'build/trevor-polished-{i}.rgb').read_bytes()
        assert len(rgb)==160*64*3
        pixels=bytearray(min(range(4),key=lambda j:sum((rgb[n+k]-COLORS[j][k])**2 for k in range(3))) for n in range(0,len(rgb),3))
        if i >= 2:
            # Remove single-pixel holes on the large fists without changing
            # eyes, facial expression or deliberate finger/crease lines.
            box = (81, 35, 126, 60) if i == 2 else (112, 3, 145, 22)
            original = bytes(pixels)
            for y in range(max(1,box[1]), min(63,box[3])):
                for x in range(max(1,box[0]), min(159,box[2])):
                    pos=y*160+x
                    neighbors=[original[(y+dy)*160+x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dx or dy]
                    for color in (1,3):
                        if original[pos] == 0 and neighbors.count(color) >= 7:
                            pixels[pos]=color
        if i < 2:
            # Polish the quiet gym with restrained paired neon glints at its
            # edges, keeping Trevor and the centre of the original art intact.
            for y in range(8, 59):
                if (y + i*3) % 11 in (0, 1):
                    for x in (7, 8, 151, 152):
                        pixels[y*160+x] = 3
        out.append(bytes(pixels))
    mask = entrance_mask()
    near = out[1]
    composite = bytearray(out[0])
    for pos, keep in enumerate(mask):
        if not keep:
            continue
        y, x = divmod(pos, 160)
        # Discard isolated black backing at the traced boundary. Preserve a
        # one-pixel black contour beside colored art and all interior details.
        supported = any(near[yy*160+xx] for yy in range(max(0,y-1),min(64,y+2))
                        for xx in range(max(0,x-1),min(160,x+2)))
        boundary = any(not mask[yy*160+xx]
                       for yy in range(max(0,y-3),min(64,y+4))
                       for xx in range(max(0,x-3),min(160,x+4)))
        if near[pos] or supported or not boundary:
            composite[pos] = near[pos]
    # A dark one-pixel keyline on the gym side separates the purple fur
    # from the purple wall without changing Trevor's face or body colours.
    for y in range(64):
        for x in range(160):
            pos = y * 160 + x
            if not mask[pos] and any(
                0 <= xx < 160 and 0 <= yy < 64 and mask[yy * 160 + xx]
                for xx, yy in ((x-1, y), (x+1, y), (x, y-1), (x, y+1))
            ):
                composite[pos] = 0
    out[1] = bytes(composite)
    return out


# Outlines trace Trevor himself in the two existing 160x64 source frames.
# Everything outside is replaced by a perspective tunnel.
POLYGONS=(
 ((59,9),(62,5),(70,3),(79,2),(80,0),(87,2),(95,7),(99,11),
  (100,17),(99,21),(109,21),(117,24),(124,28),(130,33),(134,39),
  (134,44),(131,48),(123,52),(117,56),(109,58),(114,64),(47,64),
  (44,60),(48,57),(54,54),(52,52),(46,54),(39,57),(34,60),
  (28,63),(20,62),(12,57),(10,53),(10,49),(17,46),(23,45),
  (28,42),(38,39),(40,32),(45,28),(52,25),(61,24),(64,21),
  (60,18),(59,14),(61,11)),
 ((48,10),(53,6),(61,5),(64,3),(68,5),(75,4),(80,5),(85,8),
  (89,11),(91,16),(94,20),(92,24),(98,26),(104,26),(110,29),
  (115,27),(116,23),(113,20),(110,18),(106,16),(106,12),(109,8),
  (115,5),(124,5),(131,6),(138,10),(141,14),(140,19),(144,22),
  (147,28),(149,33),(147,39),(141,43),(133,45),(126,48),
  (120,50),(115,52),(115,57),(112,64),(9,64),(9,59),(12,54),
  (18,48),(24,44),(26,40),(31,36),(38,33),(48,30),(54,29),
  (56,26),(53,23),(50,21),(49,18),(48,14))
)

# Small openings follow the original outlines more closely than the outer
# silhouette, excluding the old gym floor and the space under the raised fist.
CUTOUTS = (
    (((28, 64), (32, 58), (39, 54), (48, 52), (53, 52), (54, 54), (49, 57), (44, 60), (44, 64)),
     ((112, 64), (116, 59), (120, 56), (124, 54), (134, 49), (131, 64))),
    (((92, 10), (107, 10), (107, 20), (110, 21), (110, 25), (103, 24), (98, 22), (93, 20)),),
)

def inside(x,y,polygon):
    hit=False
    for (x1,y1),(x2,y2) in zip(polygon,polygon[1:]+polygon[:1]):
        if (y1>y)!=(y2>y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1:hit=not hit
    return hit

def tunnel_frames(phase):
    art=frames();result=[]
    # Morph the tunnel's rectangular frame into an oval and back over the
    # sixteen banked background phases; Trevor's bitmap and silhouette stay fixed.
    morph=0.5-0.5*math.cos((phase&15)*math.tau/16)
    # Stages 4 and 5 mirror the punch and wind-up for the opposite hand.
    for index,poly in ((2, POLYGONS[0]), (3, POLYGONS[1]),
                       (4, POLYGONS[0]), (5, POLYGONS[1])):
        p=bytearray(160*64)
        actor=bytearray(160*64)
        thrust = 0  # character pose is independent of the moving tunnel phase
        for y in range(64):
            for x in range(160):
                sample_x = x - thrust if index == 2 else x + thrust if index == 4 else x
                character_x = 159-sample_x if index in (4, 5) else sample_x
                cutouts = CUTOUTS[0 if index in (2, 4) else 1]
                gap = any(inside(character_x+.5, y+.5, cutout) for cutout in cutouts)
                actor[y*160+x] = not gap and inside(character_x+.5, y+.5, poly)
        for y in range(64):
            for x in range(160):
                # Stage 4 reuses the forward-punch silhouette and its art
                # mirrored together, so the opposite fist leads the punch.
                # Keep the body registered across all tunnel phases; movement
                # comes from the wind-up/punch sequence, not background time.
                sample_x = x - thrust if index == 2 else x + thrust if index == 4 else x
                character_x = 159-sample_x if index in (4, 5) else sample_x
                if actor[y*160+x]:
                    source = 2 if index in (2, 4) else 3
                    p[y*160+x]=art[source][y*160+character_x]
                else:
                    xx=(x-79.5)/80;yy=(y-31.5)/32
                    square_r=max(abs(xx),abs(yy))
                    oval_r=math.hypot(xx,yy)/math.sqrt(2)
                    r=max(square_r+(oval_r-square_r)*morph,0.025)
                    rings=(math.log(r)*2.5-phase/16)%1
                    # Bands expand from the center; radial facets add depth.
                    if rings<0.035:ink=3
                    elif rings<0.12:ink=1
                    elif rings<0.72:ink=0
                    else:ink=2 if abs(xx)>abs(yy) else 1
                    # A thin neon rim separates the character from the
                    # moving tunnel without painting over the illustration.
                    if y < 62 and ((x and actor[y*160+x-1]) or (y and actor[(y-1)*160+x])):
                        ink=1  # stable rim: no phase-dependent pale outline
                    # Narrow, moving edge glints frame the action without
                    # crossing Trevor's silhouette or the BANG lettering.
                    if (x < 15 or x >= 145) and ((y*3 + x + phase*2) % 53 < 2):
                        ink=3
                    p[y*160+x]=ink
        result.append(bytes(p))
    return result


def bang_art():
    # Eight 4-color-clock columns are provided by the four quadruple-width
    # missiles; four normal-width players supply crisp black B A N G glyphs.
    small=(0,0,0,0,0x18,0x18,0x3c,0x3c,0x7e,0x7e,0xff,0xff,
           0xff,0xff,0x7e,0x7e,0x3c,0x3c,0x18,0x18,0,0,0,0)
    # Successive apertures: a flash, a compact bubble and a wider raster burst.
    # The six central missile columns stay opaque behind the four glyphs.
    small=(0,)*4+small+(0,)*4
    medium=(0,0,0x18,0x18,0x3c,0x7e,0x7e,0xff,
            0xff,0x7e,0xff,0x7e,0xff,0x7e,0xff,0x7e,
            0xff,0x7e,0xff,0x7e,0xff,0x7e,0xff,0xff,
            0x7e,0x7e,0x3c,0x18,0x18,0,0,0)
    full=(0x18,0x18,0x5a,0x3c,0x7e,0x7e,0xff,0x7e,
          0xff,0xfe,0xff,0x7f,0xff,0xfe,0xff,0x7f,
          0xff,0xfe,0xff,0x7f,0xff,0xfe,0xff,0xff,
          0x7e,0xff,0x7e,0x3c,0x5a,0x18,0x18,0x08)
    fonts=(
      (0xf8,0xcc,0xcc,0xf8,0xcc,0xcc,0xf8),
      (0x78,0xcc,0xcc,0xfc,0xcc,0xcc,0xcc),
      (0xcc,0xec,0xfc,0xdc,0xcc,0xcc,0xcc),
      (0x78,0xcc,0xc0,0xdc,0xcc,0xcc,0x7c),
    )
    exclamation=(0x18,0x18,0x18,0x18,0x18,0,0x18)
    glyphs=tuple(bytes(v for row in glyph for v in (row,row)) for glyph in fonts)
    return bytes(small+medium+full),glyphs+(bytes(v for row in exclamation for v in (row,row)),)


def impact_word(index):
    return 'BAM' if index & 1 else 'BUM'


def impact_glyphs(index):
    glyphs=bang_art()[1]
    m=bytes(v for row in (0xc6,0xee,0xfe,0xd6,0xc6,0xc6,0xc6) for v in (row,row))
    if index & 1:
        return glyphs[0],glyphs[1],m,bytes(14)
    # Mirror the actual BAM A vertically, removing only its crossbar.
    a_rows=glyphs[1][::2]
    u=bytes(v for row in reversed(a_rows)
            for v in ((0xcc if row==0xfc else row),)*2)
    return glyphs[0],u,m,bytes(14)


IMPACT_HUES=(0x2e,0x3c,0x4e,0x5c,0x6e,0x7c,0x8e,0x9c,
             0xae,0xbc,0xce,0xdc,0xee,0xfc,0x1e,0x2c)

def helper(bank_wrapper=0):
    c=Code(ENTRY)
    def a(op,address):c.emit(op,address&255,address>>8)
    # Impacts follow the music clock; the next hand is raised in recovery.
    c.emit(0xa9,16);a(0x8d,0x83e0)
    a(0xad,0x83e3);c.emit(0xc9,TREVOR_HIT>>8);c.branch(0x90,'quiet')
    c.branch(0xd0,'energetic');a(0xad,0x83e2);c.emit(0xc9,TREVOR_HIT&255);c.branch(0xb0,'energetic')
    c.label('quiet')
    c.label('quiet_reveal');a(0xad,0x83e3);c.emit(0xc9,TREVOR_MIDPOINT>>8);c.branch(0x90,'stage0')
    c.branch(0xd0,'stage1');a(0xad,0x83e2);c.emit(0xc9,TREVOR_MIDPOINT&255);c.branch(0xb0,'stage1')
    c.label('stage0');c.emit(0xa9,0);c.jump(0x4c,'stage_ready')
    c.label('stage1');c.emit(0xa9,1);c.jump(0x4c,'stage_ready')
    c.label('energetic')
    # Anticipation belongs to the action, after the entrance has finished.
    a(0xad,0x83e3);c.emit(0xc9,HITS[0]>>8);c.branch(0x90,'opening_windup')
    c.branch(0xd0,'scan_hits');a(0xad,0x83e2);c.emit(0xc9,HITS[0]&255);c.branch(0xb0,'scan_hits')
    c.label('opening_windup');c.emit(0xa9,255);c.jump(0x8d,'hit_age');c.emit(0xa9,HANDS[0]+1);c.jump(0x4c,'stage_ready')
    c.label('scan_hits');c.emit(0xa2,len(HITS)-1)
    c.label('find_hit')
    a(0xad,0x83e3);c.jump(0xdd,'hit_hi');c.branch(0x90,'previous_hit')
    c.branch(0xd0,'hit_found')
    a(0xad,0x83e2);c.jump(0xdd,'hit_lo');c.branch(0xb0,'hit_found')
    c.label('previous_hit');c.emit(0xca);c.branch(0x10,'find_hit')
    # Defensive fallback; normal dispatch starts at the first hit.
    c.emit(0xa2,0)
    c.label('hit_found');c.jump(0x8e,'hit_index')
    c.emit(0x38);a(0xad,0x83e2);c.jump(0xfd,'hit_lo');c.jump(0x8d,'hit_age')
    c.emit(0xc9,120);c.branch(0xb0,'windup')
    c.jump(0xbd,'hit_hand');c.jump(0x4c,'stage_ready')
    c.label('windup')
    c.emit(0xe0,len(HITS)-1);c.branch(0x90,'next_windup')
    c.jump(0xbd,'hit_hand');c.jump(0x4c,'stage_ready')
    c.label('next_windup');c.emit(0xe8);c.jump(0xbd,'hit_hand');c.emit(0x18,0x69,1)
    c.label('stage_ready');a(0x8d,0x83ed);c.emit(0xc9,2);c.branch(0x90,'quiet_key')
    # Rebuild the tunnel at most every 32 ticks unless the punch pose changes.
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x4a);a(0x8d,0x83e8)
    a(0xad,0x83e3);c.emit(0x29,3,0x0a,0x0a,0x0a);a(0x0d,0x83e8);c.emit(0x09,0x80);c.jump(0x4c,'check_key')
    c.label('quiet_key');c.emit(0x09,0x70)
    c.label('check_key');a(0x8d,0x83e7);a(0xcd,0x83fa);c.branch(0xd0,'changed')
    a(0xad,0x83ed);a(0xcd,0x83fb);c.branch(0xd0,'changed');c.jump(0x4c,'colors')
    c.label('changed');a(0xad,0x83e7);a(0x8d,0x83fa);a(0xad,0x83ed);a(0x8d,0x83fb)
    a(0xae,0x83ed)
    c.jump(0xbd,'source_hi');c.emit(0x48)
    a(0xad,0x83e6);c.emit(0x29,4,0x0a,0x0a,0x0a,0x49,0xb0);a(0x8d,0x83fe)
    c.emit(0x68,0xa2,2);a(0x20,COPY_PAGES)
    cached_display_list(c, 2)
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
    c.label('color_wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'color_wait')
    # Keep the scene legible: colors match the source artwork. Dim first half.
    a(0xad,0x83ed);c.emit(0xc9,2);c.branch(0xb0,'bright')
    a(0xad,0x83ed);c.emit(0x0a,0x18,0x69,0x46);a(0x8d,0xd016)
    c.emit(0x18,0x69,0x20);a(0x8d,0xd017);c.emit(0x18,0x69,0xc4);a(0x8d,0xd018);c.jump(0x4c,'accents')
    c.label('bright');a(0xae,0x83ed)
    c.jump(0xbd,'pose_pf0');a(0x8d,0xd016)
    c.jump(0xbd,'pose_pf1');a(0x8d,0xd017)
    c.jump(0xbd,'pose_skin');a(0x8d,0xd018)
    c.label('accents')
    # A departing splash may continue into the next hand's wind-up.
    # Before the first hit the opening wind-up sets hit_age to 255.
    a(0xad,0x83ed);c.emit(0xc9,2);c.branch(0x90,'sparks')
    c.jump(0xad,'hit_age');c.emit(0xc9,EFFECT_END);c.branch(0xb0,'sparks')
    c.jump(0x4c,'bang')
    c.label('sparks')
    # No unrelated ambient insects: the tunnel and Trevor carry the idle shot.
    for addr,val in ((0xd01b,1),(0xd01d,0),(0xd400,0x22)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    # Every PMG write below targets the INACTIVE $08/$88 buffer. Positions
    # and colours are committed together in the early bottom-blank window.
    pmg_fixups=[]
    def pmg(op,address):
        label=f'impact_pmg{len(pmg_fixups)}'
        c.label(label);a(op,address)
        pmg_fixups.append((label,address>>8))
    c.label('bang')
    c.jump(0x20,'bang_prepare')
    c.emit(0xa9,0,0xa2,127)
    c.label('bang_clear')
    for base in (0x980,0xa00,0xa80,0xb00,0xb80):pmg(0x9d,base)
    c.emit(0xca);c.branch(0x10,'bang_clear')
    c.jump(0xae,'hit_index')
    c.jump(0xbd,'bang_bx');a(0x8d,0x83ec)
    c.jump(0xbd,'bang_by');a(0x8d,0x83ef)
    c.jump(0xad,'hit_age');c.emit(0xc9,BUBBLE_END);c.branch(0x90,'bang_burst_start')
    c.jump(0x4c,'bang_scatter')
    c.label('bang_burst_start')
    c.emit(0xa9,68,0x18);a(0x6d,0x83ef);a(0x8d,0x83eb)
    c.jump(0xad,'hit_age');c.emit(0x4a,0x4a,0x4a,0xc9,2);c.branch(0x90,'burst_phase_ready');c.emit(0xa9,2)
    c.label('burst_phase_ready');c.emit(0x0a,0x0a,0x0a,0x0a,0x0a,0xaa)
    c.emit(0xa9,36,0x18);a(0x6d,0x83ef);c.emit(0xa8)
    c.label('burst_rows');c.jump(0xbd,'bang_burst');pmg(0x99,0x0980)
    c.emit(0xe8,0xc8);a(0xcc,0x83eb);c.branch(0xd0,'burst_rows')
    c.jump(0xad,'hit_age');c.emit(0xc9,8);c.branch(0x90,'bang_positions');c.emit(0xc9,LETTER_END);c.branch(0xb0,'bang_positions')
    c.emit(0xa2,0,0xa9,45,0x18);a(0x6d,0x83ef);c.emit(0xa8)
    c.label('glyph_rows')
    for i in range(4):
        if i == 0:
            c.jump(0xbd,'bang_glyph0')
        else:
            c.jump(0xad,'hit_index');c.emit(0x29,1);c.branch(0xf0,f'word_bng{i}')
            if i==1:c.jump(0xbd,'bang_glyph1')
            elif i==2:c.jump(0xbd,'bam_m')
            else:c.emit(0xa9,0)
            c.jump(0x4c,f'word_write{i}')
            c.label(f'word_bng{i}')
            c.jump(0xbd,('bang_glyph2' if i==1 else 'bang_glyph3' if i==2 else 'bang_exclamation'))
            c.label(f'word_write{i}')
        pmg(0x99,0x0a00+i*128)
    c.emit(0xe8,0xc8,0xe0,14);c.branch(0xd0,'glyph_rows')
    c.label('bang_positions')
    c.emit(0xa9,0);c.jump(0x8d,'puff_size')
    c.emit(0xa9,0xff);c.jump(0x8d,'missile_size')
    c.emit(0xa9,0x11);c.jump(0x8d,'impact_prior')
    for i in range(4):
        c.emit(0xa9,152+i*8,0x18);a(0x6d,0x83ec);c.jump(0x8d,f'impact_mx{i}')
        # Both BUM and BAM occupy three 8-clock cells in a 32-clock bubble.
        c.emit(0x18,0x69,4);c.jump(0x8d,f'impact_px{i}')
    c.jump(0xad,'hit_age');c.emit(0xc9,LETTER_END);c.branch(0x90,'bang_word_publish')
    c.jump(0x4c,'bang_puffs')
    c.label('bang_word_publish')
    c.jump(0x4c,'bang_publish')
    c.label('bang_scatter')
    c.emit(0xa9,1);c.jump(0x8d,'impact_prior')
    c.jump(0xad,'hit_age');c.emit(0xc9,120,0xa9,0x55);c.branch(0x90,'missile_size_ready');c.emit(0xa9,0)
    c.label('missile_size_ready');c.jump(0x8d,'missile_size')
    c.jump(0xad,'hit_age');c.emit(0x38,0xe9,BUBBLE_END,0x4a);a(0x8d,0x83ea)
    c.emit(0x4a);a(0x8d,0x83eb)
    for i,(base,row) in enumerate(((162,51),(165,53),(171,51),(174,53))):
        c.emit(0xa9,base,0x38 if i<2 else 0x18)
        a(0xed if i<2 else 0x6d,0x83ea)
        c.emit(0x18);a(0x6d,0x83ec);c.jump(0x8d,f'impact_mx{i}')
        c.emit(0xa9,row,0x38 if i%2==0 else 0x18)
        a(0xed if i%2==0 else 0x6d,0x83eb)
        c.emit(0x18);a(0x6d,0x83ef);c.emit(0xa8)
        # Several isolated bits per missile make a breaking particle train.
        for dy,bits in enumerate((3,1,0,2,0,1)):
            if not bits:continue
            pmg(0xb9,0x0980+dy);c.emit(0x09,bits<<(2*i));pmg(0x99,0x0980+dy)
    c.label('bang_puffs')
    c.jump(0xad,'hit_index')
    c.label('ball_mod');c.emit(0xc9,3);c.branch(0x90,'ball_mod_done');c.emit(0x38,0xe9,3);c.jump(0x4c,'ball_mod')
    c.label('ball_mod_done');c.emit(0xc9,2);c.branch(0xd0,'normal_puffs');c.jump(0x4c,'impact_ball')
    c.label('normal_puffs')
    c.jump(0xad,'hit_age');c.emit(0x38,0xe9,LETTER_END,0x4a);a(0x8d,0x83ea)
    c.emit(0x4a);a(0x8d,0x83eb)
    c.jump(0xad,'hit_age');c.emit(0xc9,120,0xa9,1);c.branch(0x90,'puff_size_ready');c.emit(0xa9,0)
    c.label('puff_size_ready');c.jump(0x8d,'puff_size')
    for i,(base,row) in enumerate(((157,47),(165,55),(167,47),(175,55))):
        c.emit(0xa9,base,0x38 if i<2 else 0x18);a(0xed if i<2 else 0x6d,0x83ea)
        c.emit(0x18);a(0x6d,0x83ec);c.jump(0x8d,f'impact_px{i}')
        c.emit(0xa9,row,0x38 if i%2==0 else 0x18);a(0xed if i%2==0 else 0x6d,0x83eb)
        c.emit(0x18);a(0x6d,0x83ef);c.emit(0xa8)
        c.jump(0xad,'hit_age');c.emit(0xc9,120,0xa2,0);c.branch(0x90,f'puff_start{i}');c.emit(0xa2,8)
        c.label(f'puff_start{i}');c.emit(0x8a,0x18,0x69,8);a(0x8d,0x83e7)
        c.label(f'puff_rows{i}');c.jump(0xbd,'puff_shape');pmg(0x99,0x0a00+i*128)
        c.emit(0xe8,0xc8);a(0xec,0x83e7);c.branch(0xd0,f'puff_rows{i}')
    c.jump(0x4c,'bang_publish')
    c.label('impact_ball')
    # Borrow the actual rotator ball + orbit renderer via the unbanked
    # trampoline. Only hand/age cross banks; there are no copied ball assets.
    c.jump(0xad,'hit_age');c.emit(0x38,0xe9,LETTER_END);a(0x8d,0x83eb)
    c.jump(0xae,'hit_index');c.jump(0xbd,'hit_hand');a(0x8d,0x83e7)
    for addr,value in ((bank_wrapper+5,0xb5),(bank_wrapper+6,0x24),(bank_wrapper+11,0),(bank_wrapper+12,0x40)):
        c.emit(0xa9,value);a(0x8d,addr)
    a(0x20,bank_wrapper)
    for addr,value in ((bank_wrapper+5,0xb3),(bank_wrapper+6,0x24),(bank_wrapper+11,0),(bank_wrapper+12,0x60)):
        c.emit(0xa9,value);a(0x8d,addr)
    c.emit(0x60)
    c.label('bang_publish')
    c.label('impact_wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'impact_wait');c.emit(0xc9,128);c.branch(0xb0,'impact_wait')
    a(0xad,0x83e9);c.emit(0x09,8);a(0x8d,0xd407)
    for i in range(4):
        c.jump(0xad,f'impact_px{i}');a(0x8d,0xd000+i)
        c.jump(0xad,f'impact_mx{i}');a(0x8d,0xd004+i)
        c.jump(0xad,'puff_size');a(0x8d,0xd008+i)
    c.jump(0xad,'missile_size');a(0x8d,0xd00c)
    c.jump(0xad,'impact_prior');a(0x8d,0xd01b)
    c.jump(0xad,'hit_age');c.emit(0x4a,0x4a,0x4a,0x29,15,0xaa)
    c.jump(0xad,'hit_age');c.emit(0xc9,LETTER_END);c.branch(0x90,'black_letters')
    for i in range(4):c.jump(0xbd,f'impact_hues{i}');a(0x8d,0xd012+i)
    c.jump(0x4c,'missile_colour')
    c.label('black_letters');c.emit(0xa9,0)
    for i in range(4):a(0x8d,0xd012+i)
    c.label('missile_colour');c.jump(0xbd,'impact_spark_hues');c.emit(0x09,14);a(0x8d,0xd019)
    for addr,val in ((0xd01d,3),(0xd400,0x2e)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    c.label('bang_prepare')
    a(0xad,0xd407);c.emit(0x29,0x80,0x49,0x80);a(0x8d,0x83e9)
    for high in (9,10,11):
        c.emit(0xa9,high);a(0x0d,0x83e9)
        for label,hi in pmg_fixups:
            if hi==high:c.jump(0x8d,label+'_hi')
    c.emit(0x60)
    for label,high in pmg_fixups:c.labels[label+'_hi']=c.labels[label]+2
    for label in ('dl1','dl2'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    c.label('pose_pf0');c.emit(0x46,0x48,0x48,0x48,0x48,0x48)
    c.label('pose_pf1');c.emit(0x66,0x68,0x68,0x66,0x68,0x66)
    c.label('pose_skin');c.emit(0x28,0x2a,0x2a,0x2a,0x2a,0x2a)
    c.label('source_hi');c.emit(0x40,0x4a,0x54,0x6a,0x74,0x40)
    c.label('row_lo');c.emit(*((y//3*40)&255 for y in range(192)))
    c.label('row_hi');c.emit(*((y//3*40)>>8 for y in range(192)))
    burst,glyphs=bang_art()
    c.label('bang_bx');c.emit(*(impact_anchor(i)[0]&255 for i in range(len(HITS))))
    c.label('bang_by');c.emit(*(impact_anchor(i)[1]&255 for i in range(len(HITS))))
    c.label('hit_index');c.emit(0)
    c.label('hit_age');c.emit(0)
    c.label('hit_lo');c.emit(*(tick & 255 for tick in HITS))
    c.label('hit_hi');c.emit(*(tick >> 8 for tick in HITS))
    c.label('hit_hand');c.emit(*HANDS)
    c.label('impact_hues');c.emit(*((IMPACT_HUES*2)[:28]))
    for i in range(4):c.labels[f'impact_hues{i}']=c.labels['impact_hues']+i*4
    c.labels['impact_spark_hues']=c.labels['impact_hues']+2
    c.label('puff_shape');c.emit(0x18,0x3c,0x6e,0xff,0xfb,0x76,0x3c,0x18,
                                0x20,0x70,0x20,0,0x04,0x0e,0x04,0)
    c.label('bam_m');c.emit(*impact_glyphs(1)[2])
    for name in ('puff_size','missile_size','impact_prior'):
        c.label(name);c.emit(0)
    for kind in ('p','m'):
        for i in range(4):c.label(f'impact_{kind}x{i}');c.emit(0)
    c.label('bang_burst');c.emit(*burst)
    bum=impact_glyphs(0)
    for i,glyph in enumerate((glyphs[0],glyphs[1],bum[1],bum[2],bytes(14))):
        c.label(f'bang_glyph{i}');c.emit(*glyph)
    c.label('bang_exclamation');c.emit(*bytes(14))
    result=c.finish();assert len(result)<=2560,len(result)
    return result


def bank(phase=0, quiet=False, bank_wrapper=0):
    out=bytearray(16384);code=helper(bank_wrapper);out[0x2000:0x2000+len(code)]=code
    # Quiet poses are selected only in bank 49; action banks never read
    # $4A00. Keep these disjoint slots available for future banked assets.
    if quiet:
        art = zip((0, 0xa00), frames()[:2])
    else:
        punches = tunnel_frames(phase)
        art = zip((0, 0x1400, 0x2a00, 0x3400),
                  (punches[3], punches[0], punches[1], punches[2]))
    for offset,p in art:
        out[offset:offset+2560]=bytes(sum(p[i+k]<<(6-2*k) for k in range(4)) for i in range(0,len(p),4))
    return bytes(out)
