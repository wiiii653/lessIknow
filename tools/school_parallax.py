"""Precomposed independent layers for school pan, 18 clocked frames."""
from pathlib import Path
from build_sequence import Code, PALETTE
from school_story import color
ENTRY=0x7000
START=3553

# The three roots are fixed on original blonde pixels; only the tips move.
HAIR_ROOTS=((26,9,20,0),(26,13,19,2),(27,19,21,4))
HAIR_WAVE=(0,1,1,0,-1,-1)

def hair_strands(phase):
    strands=[]
    for root_x,root_y,tip_x,offset in HAIR_ROOTS:
        lift=HAIR_WAVE[(phase+offset)%len(HAIR_WAVE)]
        points=[]
        for x in range(tip_x,root_x+1):
            # Fade to zero at the root, which never leaves its original pixel.
            y=root_y+round(lift*(root_x-x)/(root_x-tip_x))
            points.append((x,y))
        strands.append(points)
    return strands

def frames():
    bg=Path('build/school-wide-v034.rgb').read_bytes()
    fg=Path('build/school-girl-cutout-v034.rgba').read_bytes()
    assert len(bg)==200*64*3 and len(fg)==160*64*4
    bg=[color(bg[i:i+3]) for i in range(0,len(bg),3)]
    fg=[(color(fg[i:i+3]),fg[i+3]) for i in range(0,len(fg),4)]
    result=[]
    for phase in range(18):
        back=phase*18//17
        left=phase*38//17
        img=bytearray(bg[y*200+x+back] for y in range(64) for x in range(160))
        for y in range(64):
            for x in range(160):
                target=left+x
                ink,alpha=fg[y*160+x]
                if 0<=target<160 and alpha>=128:img[y*160+target]=ink
        # Draw only three slender, attached trailing tips over the unchanged
        # silhouette. Fixed roots and the original hair stay in place.
        for strand in hair_strands(phase):
            for x,y in strand[:-1]:
                target=left+x
                if 0<=target<160:
                    img[y*160+target]=3
        result.append(bytes(img))
    return result

def helper():
    c=Code(ENTRY)
    def a(op,address):c.emit(op,address&255,address>>8)
    # Frame number is computed from the coherent music clock by the main callback.
    a(0xad,0x83ed);c.emit(0x09,0xc0);a(0xcd,0x83fa)
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
    for addr,val in ((0xd01a,0),(0xd016,0x48),(0xd017,0x9a),(0xd018,0x2c),(0xd01d,0),(0xd400,0x22)):
        c.emit(0xa9,val);a(0x8d,addr)
    c.emit(0x60)
    for label in ('read','write','dl1','dl2'):
        c.labels[label+'_lo']=c.labels[label]+1;c.labels[label+'_hi']=c.labels[label]+2
    c.label('source_hi');c.emit(0x40,0x4a,0x54,0x5e)
    c.label('row_lo');c.emit(*((y//3*40)&255 for y in range(192)))
    c.label('row_hi');c.emit(*((y//3*40)>>8 for y in range(192)))
    result=c.finish();assert len(result)<=4096,len(result)
    return result


def banks():
    pictures=frames(); code=helper()
    for group in range(5):
        out=bytearray(16384);out[0x3000:0x3000+len(code)]=code
        for i in range(4):
            p=pictures[min(group*4+i,17)]
            data=bytes(sum(p[j+k]<<(6-2*k) for k in range(4)) for j in range(0,len(p),4))
            out[i*2560:(i+1)*2560]=data
        yield bytes(out)
