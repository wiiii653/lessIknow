"""Post-Trevor PMG carousel; each active object covers the tunnel itself."""
import math
from functools import lru_cache
from build_sequence import Code
from music_timing import tick_at_bar
START=tick_at_bar(88)
ENTRY=0x4000
DATA=0x4400
META=0x6400
POINTERS=0x6a00
PRIMARY=0x6b00
PRIMARY_META=0x7300
PRIMARY_POINTERS=0x7400
NAMES=('tunnel_ball','shot_ball','beating_heart','bang_bam','cloud_scatter','orbit_stars','wind_rush','glass_shards')
HUES=(0x2e,0x4e,0x6e,0x8e,0xae,0xce,0xee,0x1e)


def frame_index(tick):
    elapsed=max(0,tick-START)
    return ((elapsed>>9)&7)*8+((elapsed>>4)&7)


def _sprite(points,rows=32):
    out=bytearray(rows)
    for x,y in points:
        if 0<=x<8 and 0<=y<rows:out[y]|=0x80>>x
    return bytes(out)


@lru_cache(maxsize=64)
def full_frame(index):
    from tunnel_ball import masks
    from rainbow_ball import spin_masks
    from ribbon_dance import wind_shapes
    from trevor_polished import bang_art
    mode,phase=divmod(index,8);t=phase*math.tau/8
    p=[bytes(32) for _ in range(4)];missiles=bytearray(32)
    x=[112,64,180,155];y=[40,35,50,65];size=[3,1,1,1]
    mx=[70,105,163,190];my=40;msize=0
    colours=[HUES[phase],HUES[(phase+2)&7],HUES[(phase+4)&7],HUES[(phase+6)&7]]
    if mode==0:
        p=[bytes(v) for v in masks()[phase*2]]
        left=112+round(3*math.sin(t));top=40+round(2*math.cos(t))
        x=[left,left+16,left,left+16];y=[top]*4;size=[1]*4
    elif mode==1:
        p=[bytes(v)+bytes(16) for v in spin_masks()[phase]]
        x=[120]*4;y=[48]*4;size=[1]*4
    elif mode==2:
        # Two quick systolic peaks, then rest. The minimum heart is still
        # broad enough at its centre to cover the whole tunnel aperture.
        beat=(.88,1.0,.93,.87,.91,.98,.91,.87)[phase]
        planes=[bytearray(32) for _ in range(4)]
        for row in range(32):
            for col in range(16):
                u=(col-7.5)/(6.5*beat);v=-(row-14)/(11.5*beat)
                if (u*u+v*v-1)**3-u*u*v*v*v>0 or v>.92+abs(u)*1.3:continue
                glow=((u+.34)/.23)**2+((v-.35)/.2)**2<1
                bright=glow or u<-.35 or (v>.2 and u>.2)
                plane=col//8+(2 if bright else 0)
                planes[plane][row]|=0x80>>(col%8)
        p=[bytes(v) for v in planes]
        x=[112,128,112,128];y=[40]*4;size=[1]*4
        colours=[0x46,0x48,0x3e,0x5c if phase in (1,5) else 0x5a]
    elif mode==3:
        p[0]=bang_art()[0][64:96]
        font={'B':('110','101','110','101','110'),'A':('010','101','111','101','101'),
              'N':('101','111','111','111','101'),'G':('011','100','101','101','011'),
              'M':('101','111','111','101','101')}
        word='BANG' if phase<4 else 'BAM'
        rows=['0'.join(font[ch][r] for ch in word).ljust(16,'0') for r in range(5)]
        for i in range(2):p[i+1]=bytes(int(row[i*8:i*8+8],2) for row in rows for _ in range(2))+bytes(22)
        p[3]=_sprite(((3,0),(3,1),(2,2),(3,2),(4,2),(3,3),(3,4)))
        shift=5 if phase>=4 else 0
        x=[112,112+shift,128+shift,158];y=[40,49,49,30+phase];size=[3,1,1,1];colours[1:3]=[0,0]
        # Hardware P0 has priority over P1/P2: keep the opaque bubble on
        # P3, below its black lettering. The preview alone cannot prove this.
        for values in (p,x,y,size,colours):values[0],values[3]=values[3],values[0]
    elif mode==4:
        shape=(0x18,0x3c,0x7e,0xff,0xff,0x7e,0x3c,0x18)
        p[0]=bytes(v for v in shape for _ in range(4))
        for i in range(1,4):
            p[i]=bytes(v for v in shape for _ in range(2))+bytes(16)
            x[i]=128+(i-2)*(24+phase*6);y[i]=32+i*7+phase
        size=[3]+[1 if phase<5 else 0]*3
    elif mode==5:
        main=(0x18,0x18,0x18,0x3c,0xff,0x7e,0x3c,0x18,0x18,0x18)
        p[0]=bytes(1)+bytes(v for v in main for _ in range(3))+bytes(1)
        small=(0x10,0x10,0x38,0xfe,0x38,0x10,0x10)
        for i in range(1,4):
            angle=t+(i-1)*math.tau/3
            p[i]=bytes(v for v in small for _ in range(2))+bytes(18)
            x[i]=124+round(55*math.cos(angle));y[i]=48+round(30*math.sin(angle))
    elif mode==6:
        # A broad lightning-like rush of air is the active central effect;
        # it has a solid middle, not a separate circle beneath the trails.
        wind=wind_shapes()
        main=[]
        for row in range(32):
            bits=0xff if 10<=row<=23 else (0x1f if row<10 else 0x78 if row<28 else 0x30)
            main.append(bits)
        p[0]=bytes(main)
        for i in range(1,4):
            p[i]=wind[phase*16:(phase+1)*16]+bytes(16)
            x[i]=57+i*37;y[i]=12+((phase*5+i*13)%62);size[i]=0
        colours=[0x9e,0x0e,0x8e,0xae]
    else:
        # A rotating/cracking solid shard at the aperture, smaller fragments
        # around it. Facets colour the same object rather than a guard ball.
        body=[];left=[];right=[]
        for row in range(32):
            r=max(.4,4-abs(row-15.5)*.22)
            bits=sum(0x80>>col for col in range(8) if abs(col-3.5)<=r)
            body.append(bits);left.append(bits&0xf0);right.append(bits&0x0f if (row+phase)%4<2 else 0)
        p[:3]=[bytes(body),bytes(left),bytes(right)]
        p[3]=_sprite(((2,0),(3,1),(4,2),(3,3),(2,4)))
        x=[112,112,112,175-phase*5];y=[40,40,40,25+phase*4];size=[3,3,3,1]
        colours=[0x9a,0x8e,0x0e,0x2e]
        # Opaque glass sits on P3 behind its P1/P2 highlights.
        for values in (p,x,y,size,colours):values[0],values[3]=values[3],values[0]
    for i in range(4):
        angle=t+i*math.pi/2
        if mode in (0,5):mx[i]=128+round(48*math.cos(angle));row=16+round(12*math.sin(angle))
        elif mode in (3,4,7):mx[i]=136+round((i-1.5)*(6+phase*5));row=8+((phase*phase+i*5)%20)
        elif mode==6:mx[i]=65+i*37;row=(phase*5+i*7)%24
        else:mx[i]=110+i*12;row=(phase*4+i*7)%24
        for dy,bits in ((0,3),(1,1),(3,2),(5,1)):
            if row+dy<32:missiles[row+dy]|=bits<<(2*i)
    meta=bytes(v&255 for v in x[1:]+mx+y[1:]+[my]+size[1:]+[msize]+colours+[0x0e,1])
    assert len(meta)==21
    return b''.join(p[1:])+bytes(missiles),meta,p[0],(x[0],y[0],size[0])


def frame(index):return full_frame(index)[:2]
def primary(index):return full_frame(index)[2:]


def helper():
    c=Code(ENTRY)
    def a(op,address):c.emit(op,address&255,address>>8)
    def m(field):c.emit(0xa0,field);c.jump(0x20,'meta')
    a(0xad,0x83e2);c.emit(0x38,0xe9,START&255);a(0x8d,0x83ea)
    a(0xad,0x83e3);c.emit(0xe9,START>>8,0x4a,0x29,7,0x0a,0x0a,0x0a);a(0x8d,0x83e9)
    a(0xad,0x83ea);c.emit(0x4a,0x4a,0x4a,0x4a,0x29,7);a(0x0d,0x83e9);c.emit(0xaa);a(0x8d,0x83e9)
    for table,label in ((POINTERS,'get_lo'),(POINTERS+64,'get_hi'),(POINTERS+128,'meta_lo'),(POINTERS+192,'meta_hi')):
        a(0xbd,table);c.jump(0x8d,label)
    a(0xad,0xd407);c.emit(0x29,0x80,0x49,0x80);a(0x8d,0x83e8)
    for label,high in [(f'clear{i}',v) for i,v in enumerate((9,10,10,11,11))]+ [('primary_put',10)]+[(f'put{i}',v) for i,v in enumerate((10,11,11,9))]:
        c.emit(0xa9,high);a(0x0d,0x83e8);c.jump(0x8d,label+'_hi')
    c.emit(0xa9,0,0xa2,127);c.label('clear')
    for i,addr in enumerate((0x980,0xa00,0xa80,0xb00,0xb80)):
        c.label(f'clear{i}');a(0x9d,addr)
    c.emit(0xca);c.branch(0x10,'clear')
    a(0xae,0x83e9)
    a(0xbd,PRIMARY_POINTERS);c.jump(0x8d,'primary_get_lo')
    a(0xbd,PRIMARY_POINTERS+64);c.jump(0x8d,'primary_get_hi')
    a(0xbd,PRIMARY_META+64);c.emit(0xa8,0xa2,0)
    c.label('primary_rows');c.label('primary_get');c.emit(0xbd,0,0)
    c.label('primary_put');a(0x99,0xa00)
    c.emit(0xe8,0xc8,0xe0,32);c.branch(0xd0,'primary_rows')
    for p in range(4):
        m(7+p);c.emit(0xa8,0xa2,p*32)
        c.label(f'copy{p}');c.jump(0x20,'get');c.emit(0xc0,128);c.branch(0xb0,f'skip{p}')
        c.label(f'put{p}');a(0x99,(0xa80,0xb00,0xb80,0x980)[p])
        c.label(f'skip{p}');c.emit(0xc8,0xe8,0x8a,0x29,31);c.branch(0xd0,f'copy{p}')
    c.label('wait');a(0xad,0xd40b);c.emit(0xc9,124);c.branch(0x90,'wait');c.emit(0xc9,128);c.branch(0xb0,'wait')
    a(0xad,0x83e8);c.emit(0x09,8);a(0x8d,0xd407)
    for field,reg in [(i,0xd001+i) for i in range(3)]+[(3+i,0xd004+i) for i in range(4)]+[(11+i,0xd009+i) for i in range(3)]+[(14,0xd00c)]+[(15+i,0xd012+i) for i in range(4)]+[(19,0xd019),(20,0xd01b)]:
        m(field);a(0x8d,reg)
    a(0xae,0x83e9);a(0xbd,PRIMARY_META);a(0x8d,0xd000)
    a(0xbd,PRIMARY_META+128);a(0x8d,0xd008)
    for reg,value in ((0xd01d,3),(0xd400,0x2e)):
        c.emit(0xa9,value);a(0x8d,reg)
    c.emit(0x60)
    c.label('get');c.emit(0xbd,0,0,0x60)
    c.label('meta');c.emit(0xb9,0,0,0x60)
    for name in ('get','meta','primary_get'):
        c.labels[name+'_lo']=c.labels[name]+1;c.labels[name+'_hi']=c.labels[name]+2
    for name in [f'clear{i}' for i in range(5)]+['primary_put']+[f'put{i}' for i in range(4)]:c.labels[name+'_hi']=c.labels[name]+2
    code=c.finish();assert len(code)<=DATA-ENTRY,len(code)
    return code


def bank():
    from tunnel_ball import helper as original
    out=bytearray(16384)
    pieces=[(ENTRY,helper()),(DATA,b''.join(frame(i)[0] for i in range(64))),
            (META,b''.join(frame(i)[1] for i in range(64))),
            (POINTERS,bytes((DATA+i*128)&255 for i in range(64))+bytes((DATA+i*128)>>8 for i in range(64))+
             bytes((META+i*21)&255 for i in range(64))+bytes((META+i*21)>>8 for i in range(64))),
            (PRIMARY,b''.join(primary(i)[0] for i in range(64))),
            (PRIMARY_META,bytes(primary(i)[1][0] for i in range(64))+bytes(primary(i)[1][1] for i in range(64))+bytes(primary(i)[1][2] for i in range(64))),
            (PRIMARY_POINTERS,bytes((PRIMARY+i*32)&255 for i in range(64))+bytes((PRIMARY+i*32)>>8 for i in range(64))),
            (0x7800,original())]
    occupied=set()
    for address,payload in pieces:
        assert address>=0x4000 and address+len(payload)<=0x8000
        span=set(range(address,address+len(payload)));assert not occupied&span
        occupied|=span;out[address-0x4000:address-0x4000+len(payload)]=payload
    return bytes(out)
