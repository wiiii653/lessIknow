"""Local animated pompom strands; bank-15 code and lossless patch packets."""
import math
from crush_portraits import portraits
ENTRY, DATA = 0x6900, 0x6f90
PALETTES=((0x48,0x9a,0x2c),(0x68,0xac,0x2c),(0x38,0x8c,0x2c),(0x58,0xba,0x2c))
POMS=(((14,32,15,11),),((75,6,13,11),),((13,45,14,9),(69,6,13,11)),((14,37,15,12),(67,38,14,12)))

def variants():
    result=[]
    for shot,source in enumerate(portraits()):
        views=[]
        for phase in range(4):
            out=bytearray(source)
            if phase:
                for cx,cy,rx,ry in POMS[shot]:
                    for y in range(max(0,cy-ry),min(52,cy+ry+1)):
                        for x in range(max(0,cx-rx),min(80,cx+rx+1)):
                            if ((x-cx)/rx)**2+((y-cy)/ry)**2>1:continue
                            if source[y*80+x] not in (1,2):continue
                            dx=round(2*math.sin(phase*math.pi/2+(y-cy)*0.6))
                            dy=round(math.sin(phase*math.pi/2+(x-cx)*0.4))
                            sx,sy=max(0,min(79,x+dx)),max(0,min(51,y+dy))
                            value=source[sy*80+sx]
                            if value!=3:out[y*80+x]=value
            views.append(bytes(out))
        result.append(views)
    return result

def rows(pixels):
    return [bytes(sum(pixels[y*80+x+k]<<(6-2*k) for k in range(4)) for x in range(0,80,4)) for y in range(52)]

def packets():
    blob=bytearray();pointers=[]
    for views in variants():
        packed=[rows(view) for view in views]
        spans=[]
        for y in range(52):
            varying=[x for x in range(20) if len({v[y][x] for v in packed})>1]
            for x in varying:
                if spans and spans[-1][0]==y and spans[-1][1]+spans[-1][2]==x:
                    yy,start,n=spans[-1];spans[-1]=(yy,start,n+1)
                else:spans.append((y,x,1))
        for frame in packed:
            pointers.append(DATA+len(blob))
            for y,x,n in spans:
                offset=y*40+x*2
                blob.extend((offset&255,offset>>8,n));blob.extend(frame[y][x:x+n])
            blob.extend((255,255))
    return bytes(blob),pointers

def helper():
    from build_sequence import Code
    blob,pointers=packets()
    c=Code(ENTRY)
    def a(op,addr):c.emit(op,addr&255,addr>>8)
    a(0xad,0x83ff);c.emit(0x0a,0x0a);a(0x8d,0x83ed)
    a(0xad,0x83e2);c.emit(0x4a,0x4a,0x4a,0x4a,0x29,3);a(0x0d,0x83ed)
    a(0xcd,0x83eb);c.branch(0xd0,'changed');c.emit(0x60)
    c.label('changed');a(0x8d,0x83eb);c.emit(0xaa)
    c.jump(0xbd,'pointers_lo');c.jump(0x8d,'get_lo')
    c.jump(0xbd,'pointers_hi');c.jump(0x8d,'get_hi')
    c.label('packet')
    c.jump(0x20,'get');c.jump(0x8d,'dst1_lo');c.jump(0x8d,'dst2_lo')
    c.jump(0x20,'get');c.emit(0xc9,255);c.branch(0xd0,'address');c.emit(0x60)
    c.label('address');c.emit(0x18);a(0x6d,0x83fe);c.jump(0x8d,'dst1_hi');c.jump(0x8d,'dst2_hi')
    c.jump(0x20,'get');a(0x8d,0x83ed);c.emit(0xa0,0)
    c.label('bytes');c.jump(0x20,'get');c.emit(0x48,0x4a,0x4a,0x4a,0x4a,0xaa);c.jump(0xbd,'expand')
    c.label('dst1');c.emit(0x99,0,0,0xc8,0x68,0x29,15,0xaa);c.jump(0xbd,'expand')
    c.label('dst2');c.emit(0x99,0,0,0xc8);a(0xce,0x83ed);c.branch(0xd0,'bytes');c.jump(0x4c,'packet')
    c.label('get');c.emit(0xad,0,0);c.jump(0xee,'get_lo');c.branch(0xd0,'get_done');c.jump(0xee,'get_hi');c.label('get_done');c.emit(0x60)
    for label in ('get','dst1','dst2'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    c.label('expand');c.emit(*(sum(((n>>(2-2*k))&3)<<(6-2*(2*k+d)) for k in range(2) for d in range(2)) for n in range(16)))
    c.label('pointers_lo');c.emit(*(ptr&255 for ptr in pointers))
    c.label('pointers_hi');c.emit(*(ptr>>8 for ptr in pointers))
    code=c.finish()
    assert ENTRY+len(code)<0x6f00
    assert DATA+len(blob)<=0x8000,(len(blob),0x8000-DATA)
    return code,blob
