"""Trevor reveal, alternating punches and synchronized comic impacts."""
import math
from pathlib import Path
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
    return out


# Outlines trace Trevor himself in the two existing 160x64 source frames.
# Everything outside is replaced by a perspective tunnel.
POLYGONS=(
 ((77,0),(85,1),(94,4),(99,9),(100,19),(112,20),(122,24),(130,30),(134,40),(132,48),(126,56),(114,63),(22,63),(11,58),(11,51),(18,46),(27,38),(38,32),(45,26),(58,23),(61,18),(60,13),(62,8),(67,5),(73,3)),
 ((68,2),(78,2),(87,5),(92,10),(92,12),(105,12),(109,6),(118,4),(130,5),(138,8),(143,13),(144,20),(147,26),(146,36),(141,43),(128,47),(116,49),(110,63),(19,63),(8,58),(7,49),(14,43),(24,38),(35,33),(47,30),(54,25),(50,21),(48,15),(49,12),(54,8),(60,5))
)

# Small openings follow the original outlines more closely than the outer
# silhouette, excluding the old gym floor and the space under the raised fist.
CUTOUTS = (
    (((33, 64), (36, 58), (43, 53), (51, 51), (55, 54), (51, 58), (48, 64)),
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
                    r=max(abs(xx),abs(yy),0.025)
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
    return bytes(small+medium+full),tuple(bytes(v for row in glyph for v in (row,row)) for glyph in fonts)

def helper():
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
    a(0xae,0x83ed);c.jump(0xbd,'source_hi');c.jump(0x8d,'read_hi')
    c.emit(0xa9,0);c.jump(0x8d,'read_lo');c.jump(0x8d,'write_lo')
    a(0xad,0x83e6);c.emit(0x29,4,0x0a,0x0a,0x0a,0x49,0xb0);a(0x8d,0x83fe);c.jump(0x8d,'write_hi')
    c.emit(0xa2,10,0xa0,0)
    c.label('copy');c.label('read');c.emit(0xb9,0,0);c.label('write');c.emit(0x99,0,0,0xc8);c.branch(0xd0,'copy')
    c.jump(0xee,'read_hi');c.jump(0xee,'write_hi');c.emit(0xca);c.branch(0xd0,'copy')
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
    c.label('bang')
    # Clear all players: their old RAM may contain art from preceding scenes.
    c.emit(0xa9,0,0xa2,0)
    c.label('bang_clear')
    for base in (0x0980,0x0a00,0x0b00):a(0x9d,base)
    c.emit(0xe8);c.branch(0xd0,'bang_clear')
    # The hand chooses the side; two small variants use the same origin
    # for lettering, burst and departing fragments.
    c.jump(0xad,'hit_index');c.emit(0x29,1);a(0x8d,0x83e8)
    c.jump(0xae,'hit_index');c.jump(0xbd,'hit_hand');c.emit(0xc9,4);c.branch(0xd0,'bang_side_ready')
    a(0xad,0x83e8);c.emit(0x18,0x69,2);a(0x8d,0x83e8)
    c.label('bang_side_ready');a(0xae,0x83e8)
    c.jump(0xbd,'bang_bx');a(0x8d,0x83ec)
    c.jump(0xbd,'bang_by');a(0x8d,0x83ef)
    c.jump(0xad,'hit_age');c.emit(0xc9,BUBBLE_END);c.branch(0x90,'bang_burst_start')
    c.jump(0x4c,'bang_scatter')
    c.label('bang_burst_start')
    # 24 double-lines of shared missile data: expand, impact, disperse.
    c.emit(0xa9,68,0x18);a(0x6d,0x83ef);a(0x8d,0x83eb)
    c.jump(0xad,'hit_age');c.emit(0x4a,0x4a,0x4a,0xaa);c.jump(0xbd,'bang_phase');c.emit(0xaa)
    c.emit(0xa9,36,0x18);a(0x6d,0x83ef);c.emit(0xa8)
    c.label('burst_rows');c.jump(0xbd,'bang_burst');a(0x99,0x0980);c.emit(0xe8,0xc8);a(0xcc,0x83eb);c.branch(0xd0,'burst_rows')
    # The word appears after the initial flash and before the fragments.
    c.jump(0xad,'hit_age');c.emit(0xc9,8);c.branch(0x90,'bang_positions');c.emit(0xc9,LETTER_END);c.branch(0xb0,'bang_positions')
    c.emit(0xa2,0,0xa9,45,0x18);a(0x6d,0x83ef);c.emit(0xa8)
    c.label('glyph_rows')
    for i in range(4):c.jump(0xbd,f'bang_glyph{i}');a(0x99,0x0a00+i*128)
    c.emit(0xe8,0xc8,0xe0,14);c.branch(0xd0,'glyph_rows')
    c.label('bang_positions')
    for i in range(4):
        c.emit(0xa9,152+i*8,0x18);a(0x6d,0x83ec);a(0x8d,0xd000+i);a(0x8d,0xd004+i)
        c.emit(0xa9,0);a(0x8d,0xd008+i);a(0x8d,0xd012+i)
    # Fifth player carries the colorful splash, black players form lettering.
    c.jump(0xad,'hit_age');c.emit(0x4a,0x4a,0x4a,0x29,3,0xaa);c.jump(0xbd,'bang_color');a(0x8d,0xd019)
    for addr,val in ((0xd407,8),(0xd01b,0x11),(0xd01d,3),(0xd400,0x2e),(0xd00c,0xff)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    c.label('bang_scatter')
    # The burst centre and its departing fragments share the same origin.
    c.jump(0xad,'hit_age');c.emit(0x38,0xe9,BUBBLE_END,0x4a);a(0x8d,0x83ea)
    c.emit(0x4a);a(0x8d,0x83eb)
    for i,(base,row) in enumerate(((162,51),(165,53),(171,51),(174,53))):
        c.emit(0xa9,base,0x38 if i<2 else 0x18)
        a(0xed if i<2 else 0x6d,0x83ea)
        c.emit(0x18);a(0x6d,0x83ec);a(0x8d,0xd004+i)
        c.emit(0xa9,row,0x38 if i%2==0 else 0x18)
        a(0xed if i%2==0 else 0x6d,0x83eb)
        c.emit(0x18);a(0x6d,0x83ef);c.emit(0xa8)
        for dy,bits in enumerate((1,1,3,1,1)):
            a(0xb9,0x0980+dy);c.emit(0x09,bits<<(2*i));a(0x99,0x0980+dy)
    for addr,val in ((0xd01a,0),(0xd012,0x2e),(0xd013,0x9e),(0xd014,0x4e),(0xd015,0xce),
                     (0xd407,8),(0xd01b,1),(0xd01d,1),(0xd400,0x26),(0xd00c,0x55)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    for label in ('read','write','dl1','dl2'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    c.label('pose_pf0');c.emit(0x46,0x48,0x48,0x48,0x48,0x48)
    c.label('pose_pf1');c.emit(0x66,0x68,0x68,0x66,0x68,0x66)
    c.label('pose_skin');c.emit(0x28,0x2a,0x2a,0x2a,0x2a,0x2a)
    c.label('source_hi');c.emit(0x40,0x4a,0x54,0x6a,0x74,0x40)
    c.label('row_lo');c.emit(*((y//3*40)&255 for y in range(192)))
    c.label('row_hi');c.emit(*((y//3*40)>>8 for y in range(192)))
    burst,glyphs=bang_art()
    c.label('bang_phase');c.emit(0,32,*([64]*11))
    c.label('bang_color');c.emit(0x1e,0x0e,0x9e,0x1e)
    c.label('bang_bx');c.emit(0,0xfc,0xd8,0xdc)
    c.label('bang_by');c.emit(0,0xfe,2,1)
    c.label('hit_index');c.emit(0)
    c.label('hit_age');c.emit(0)
    c.label('hit_lo');c.emit(*(tick & 255 for tick in HITS))
    c.label('hit_hi');c.emit(*(tick >> 8 for tick in HITS))
    c.label('hit_hand');c.emit(*HANDS)
    c.label('bang_burst');c.emit(*burst)
    for i,glyph in enumerate(glyphs):c.label(f'bang_glyph{i}');c.emit(*glyph)
    result=c.finish();assert len(result)<=2560,len(result)
    return result


def bank(phase=0, quiet=False):
    out=bytearray(16384);code=helper();out[0x2000:0x2000+len(code)]=code
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
