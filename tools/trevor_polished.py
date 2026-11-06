"""Four illustrated Trevor compositions, with hardware missile glints."""
import math
from pathlib import Path
from build_sequence import Code
from trevor_awakens import COLORS, HIT as TREVOR_HIT, MIDPOINT as TREVOR_MIDPOINT
ENTRY=0x6000

def frames():
    out=[]
    for i in range(4):
        rgb=Path(f'build/trevor-polished-{i}.rgb').read_bytes()
        assert len(rgb)==160*64*3
        out.append(bytes(min(range(4),key=lambda j:sum((rgb[n+k]-COLORS[j][k])**2 for k in range(3))) for n in range(0,len(rgb),3)))
    return out


# Outlines trace Trevor himself in the two existing 160x64 source frames.
# Everything outside is replaced by a perspective tunnel.
POLYGONS=(
 ((77,0),(85,1),(94,4),(99,9),(100,19),(112,20),(122,24),(130,30),(134,40),(132,48),(126,56),(114,63),(22,63),(11,58),(11,51),(18,46),(27,38),(38,32),(45,26),(58,23),(61,18),(60,13),(62,8),(67,5),(73,3)),
 ((68,2),(78,2),(87,5),(92,10),(92,12),(105,12),(109,6),(118,4),(130,5),(138,8),(143,13),(144,20),(147,26),(146,36),(141,43),(128,47),(116,49),(110,63),(19,63),(8,58),(7,49),(14,43),(24,38),(35,33),(47,30),(54,25),(50,21),(48,15),(49,12),(54,8),(60,5))
)

def inside(x,y,polygon):
    hit=False
    for (x1,y1),(x2,y2) in zip(polygon,polygon[1:]+polygon[:1]):
        if (y1>y)!=(y2>y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1:hit=not hit
    return hit

def tunnel_frames(phase):
    art=frames();result=[]
    for index,poly in enumerate(POLYGONS,2):
        p=bytearray(160*64)
        for y in range(64):
            for x in range(160):
                # The gap between Trevor's head and raised fist is background.
                gap = index == 3 and 92 <= x < 107 and 9 <= y < 20
                if not gap and inside(x+0.5,y+0.5,poly):
                    p[y*160+x]=art[index][y*160+x]
                else:
                    xx=(x-79.5)/80;yy=(y-31.5)/32
                    r=max(abs(xx),abs(yy),0.025)
                    rings=(math.log(r)*2.5-phase/16)%1
                    # Bands expand from the center; radial facets add depth.
                    if rings<0.10:ink=3
                    elif rings<0.22:ink=1
                    elif rings<0.59:ink=0
                    else:ink=2 if abs(xx)>abs(yy) else 1
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
      (0x78,0x44,0x44,0x78,0x44,0x44,0x78),
      (0x38,0x44,0x44,0x7c,0x44,0x44,0x44),
      (0x44,0x64,0x54,0x54,0x4c,0x44,0x44),
      (0x38,0x44,0x40,0x5c,0x44,0x44,0x38),
    )
    return bytes(small+medium+full),tuple(bytes(v for row in glyph for v in (row,row)) for glyph in fonts)

def helper():
    c=Code(ENTRY)
    def a(op,address):c.emit(op,address&255,address>>8)
    # Keep the exact act boundaries. First two pictures make the reveal;
    # the two energetic poses alternate on 256-tick intervals.
    c.emit(0xa9,16);a(0x8d,0x83e0)
    a(0xad,0x83e3);c.emit(0xc9,TREVOR_HIT>>8);c.branch(0x90,'quiet')
    c.branch(0xd0,'energetic');a(0xad,0x83e2);c.emit(0xc9,TREVOR_HIT&255);c.branch(0xb0,'energetic')
    c.label('quiet');a(0xad,0x83e3);c.emit(0xc9,TREVOR_MIDPOINT>>8);c.branch(0x90,'stage0')
    c.branch(0xd0,'stage1');a(0xad,0x83e2);c.emit(0xc9,TREVOR_MIDPOINT&255);c.branch(0xb0,'stage1')
    c.label('stage0');c.emit(0xa9,0);c.jump(0x4c,'stage_ready')
    c.label('stage1');c.emit(0xa9,1);c.jump(0x4c,'stage_ready')
    c.label('energetic');a(0xad,0x83e3);c.emit(0x29,1,0x09,2)
    c.label('stage_ready');a(0x8d,0x83ed);c.emit(0xc9,2);c.branch(0x90,'quiet_key')
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a);a(0x8d,0x83e8)
    a(0xad,0x83e3);c.emit(0x29,1,0x0a,0x0a,0x0a,0x0a);a(0x0d,0x83e8);c.emit(0x09,0x80);c.jump(0x4c,'check_key')
    c.label('quiet_key');c.emit(0x09,0x70)
    c.label('check_key');a(0xcd,0x83fa)
    c.branch(0xd0,'changed');c.jump(0x4c,'colors')
    c.label('changed');a(0x8d,0x83fa)
    a(0xad,0x83ed);c.emit(0x29,3,0xaa);c.jump(0xbd,'source_hi');c.jump(0x8d,'read_hi')
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
    c.label('bright');c.emit(0xa9,0x4a);a(0x8d,0xd016);c.emit(0xa9,0x6a);a(0x8d,0xd017);c.emit(0xa9,0x2e);a(0x8d,0xd018)
    c.label('accents')
    # A short comic impact appears on every forward-punch pose.
    a(0xad,0x83ed);c.emit(0xc9,2);c.branch(0xd0,'sparks')
    a(0xad,0x83e2);c.emit(0xc9,192);c.branch(0xb0,'sparks');c.jump(0x4c,'bang')
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
    # Select a stable per-punch offset shared by the word, burst and sparks.
    a(0xad,0x83e3);c.emit(0x4a,0x29,3,0xaa)
    c.jump(0xbd,'bang_dx');a(0x8d,0x83e8)
    c.jump(0xbd,'bang_dy');a(0x8d,0x83e9)
    a(0xad,0x83e2);c.emit(0xc9,96);c.branch(0x90,'bang_burst_start')
    c.jump(0x4c,'bang_scatter')
    c.label('bang_burst_start')
    # 24 double-lines of shared missile data: expand, impact, disperse.
    c.emit(0xa9,68,0x18);a(0x6d,0x83e9);a(0x8d,0x83eb)
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0xaa);c.jump(0xbd,'bang_phase');c.emit(0xaa)
    c.emit(0xa9,36,0x18);a(0x6d,0x83e9);c.emit(0xa8)
    c.label('burst_rows');c.jump(0xbd,'bang_burst');a(0x99,0x0980);c.emit(0xe8,0xc8);a(0xcc,0x83eb);c.branch(0xd0,'burst_rows')
    # The word is visible during the central six phases of the impact.
    a(0xad,0x83e2);c.emit(0xc9,16);c.branch(0x90,'bang_positions');c.emit(0xc9,96);c.branch(0xb0,'bang_positions')
    c.emit(0xa2,0,0xa9,45,0x18);a(0x6d,0x83e9);c.emit(0xa8)
    c.label('glyph_rows')
    for i in range(4):c.jump(0xbd,f'bang_glyph{i}');a(0x99,0x0a00+i*128)
    c.emit(0xe8,0xc8,0xe0,14);c.branch(0xd0,'glyph_rows')
    c.label('bang_positions')
    for i in range(4):
        c.emit(0xa9,152+i*8,0x18);a(0x6d,0x83e8);a(0x8d,0xd000+i);a(0x8d,0xd004+i)
        c.emit(0xa9,0);a(0x8d,0xd008+i);a(0x8d,0xd012+i)
    # Fifth player carries the colorful splash, black players form lettering.
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x29,3,0xaa);c.jump(0xbd,'bang_color');a(0x8d,0xd019)
    for addr,val in ((0xd407,8),(0xd01b,0x11),(0xd01d,3),(0xd400,0x2e),(0xd00c,0xff)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    c.label('bang_scatter')
    # Impact fragments expand from the fist, moving outwards and diagonally.
    a(0xad,0x83e2);c.emit(0x38,0xe9,96,0x4a);a(0x8d,0x83ea)
    c.emit(0x4a);a(0x8d,0x83eb)
    for i,(base,row) in enumerate(((150,48),(157,54),(174,48),(181,54))):
        c.emit(0xa9,base,0x38 if i<2 else 0x18)
        a(0xed if i<2 else 0x6d,0x83ea)
        c.emit(0x18);a(0x6d,0x83e8);a(0x8d,0xd004+i)
        c.emit(0xa9,row,0x38 if i%2==0 else 0x18)
        a(0xed if i%2==0 else 0x6d,0x83eb)
        c.emit(0x18);a(0x6d,0x83e9);c.emit(0xa8)
        for dy,bits in enumerate((1,1,3,1,1)):
            a(0xb9,0x0980+dy);c.emit(0x09,bits<<(2*i));a(0x99,0x0980+dy)
    for addr,val in ((0xd01a,0),(0xd012,0x2e),(0xd013,0x9e),(0xd014,0x4e),(0xd015,0xce),
                     (0xd407,8),(0xd01b,1),(0xd01d,1),(0xd400,0x26),(0xd00c,0x55)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    for label in ('read','write','dl1','dl2'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    c.label('source_hi');c.emit(0x40,0x4a,0x54,0x6a)
    c.label('row_lo');c.emit(*((y//3*40)&255 for y in range(192)))
    c.label('row_hi');c.emit(*((y//3*40)>>8 for y in range(192)))
    burst,glyphs=bang_art()
    c.label('bang_phase');c.emit(0,32,64,64,64,32,64,64)
    c.label('bang_color');c.emit(0x1e,0x0e,0x9e,0x1e)
    c.label('bang_dx');c.emit(0,4,0xfa,2)
    c.label('bang_dy');c.emit(0,2,0xff,1)
    c.label('bang_burst');c.emit(*burst)
    for i,glyph in enumerate(glyphs):c.label(f'bang_glyph{i}');c.emit(*glyph)
    result=c.finish();assert len(result)<=2560,len(result)
    return result


def bank(phase=0):
    out=bytearray(16384);code=helper();out[0x2000:0x2000+len(code)]=code
    art=frames()[:2]+tunnel_frames(phase)
    for offset,p in zip((0,0xa00,0x1400,0x2a00),art):
        out[offset:offset+2560]=bytes(sum(p[i+k]<<(6-2*k) for k in range(4)) for i in range(0,len(p),4))
    return bytes(out)
