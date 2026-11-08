"""ATARI ARENA palette conversion and production plate assets."""
from pathlib import Path
from functools import lru_cache
from collections import deque
from school_story import color

FUJI=("0000101010000","0000101010000","0000101010000",
      "0000101010000","0001101011000","0001001001000",
      "0011001001100","0110001000110","1100001000011")
FUJI_ORIGIN=(17,15)


def logo(pixels,width,left,top,ink=3,small=False,alpha=None):
    rows=("0010100","0010100","0010100","0110110","1101011") if small else (
        "0000101010000","0000101010000","0000101010000","0000101010000",
        "0001101011000","0001001001000","0011001001100","0110001000110",
        "1100001000011")
    for y,row in enumerate(rows):
        for x,bit in enumerate(row):
            n=(top+y)*width+left+x
            if bit=='1' and (alpha is None or alpha[n]):pixels[n]=ink


@lru_cache(maxsize=2)
def background(interior=False):
    name='arena-interior-v151.rgb' if interior else 'arena-exterior-v151.rgb'
    rgb=Path('build',name).read_bytes()
    assert len(rgb)==(160*56 if interior else 200*64)*3
    p=bytearray(color(rgb[i:i+3]) for i in range(0,len(rgb),3))
    if interior:
        # Reduce distant stands to sparse lights so player silhouettes read.
        for y in range(27,48):
            for x in range(160):
                n=y*160+x;ink=p[n]
                if ink==2:p[n]=2 if y%4==1 and x%8<3 else 0
                elif ink==3:p[n]=3 if x%24<2 else 0
                elif ink==1:p[n]=1 if 32<=y<=33 else 0
        for y in range(50,56):
            for x in range(160):p[y*160+x]=3
    return bytes(p)


def inside(x,y,polygon):
    odd=False
    for (ax,ay),(bx,by) in zip(polygon,polygon[1:]+polygon[:1]):
        if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax:odd=not odd
    return odd


def actor_mask(image,polygons,height):
    """Use colored connected artwork and its keyline inside a loose guide."""
    guides={y*160+x for y in range(height) for x in range(160)
            if any(inside(x+.5,y+.5,p) for p in polygons)}
    expanded=set(guides)
    for n in guides:
        x,y=n%160,n//160
        for yy in range(max(0,y-1),min(height,y+2)):
            for xx in range(max(0,x-1),min(160,x+2)):expanded.add(yy*160+xx)
    visited=set();selected=set()
    for start in guides:
        if start in visited or not image[start]:continue
        todo=[start];visited.add(start);component=set()
        while todo:
            n=todo.pop();component.add(n);x,y=n%160,n//160
            for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                j=yy*160+xx
                if 0<=xx<160 and 0<=yy<height and j not in visited and image[j]==image[start]:
                    visited.add(j);todo.append(j)
        if len(component&expanded)*10>=len(component)*9:selected|=component
    mask=set(selected)
    # The boy artwork uses literal black for hair, eye line, and the jacket's
    # inner contour.  Those pixels are indistinguishable from the black key
    # at this resolution, so preserve black pixels inside the hand-drawn
    # silhouette guide as opaque actor pixels.  This also closes tiny gaps
    # introduced when the source is reduced to 160x64.
    mask.update(n for n in guides if image[n]==0 or n//160>=48)
    for n in selected:
        x,y=n%160,n//160
        for yy in range(max(0,y-1),min(height,y+2)):
            for xx in range(max(0,x-1),min(160,x+2)):
                j=yy*160+xx
                if image[j]==0:mask.add(j)
    outside=set();queue=deque()
    for n in (list(range(160))+list(range((height-1)*160,height*160))+
              [y*160 for y in range(height)]+[y*160+159 for y in range(height)]):
        if n not in mask and n not in outside:outside.add(n);queue.append(n)
    while queue:
        n=queue.popleft();x,y=n%160,n//160
        for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            j=yy*160+xx
            if 0<=xx<160 and 0<=yy<height and j not in outside and j not in mask:
                outside.add(j);queue.append(j)
    return set(range(160*height))-outside


def portrait(image):
    guide=((104,8),(118,0),(145,0),(160,4),(160,64),(81,64),
           (87,57),(100,52),(115,47),(116,43),(108,37),(106,27),(102,20))
    mask=actor_mask(image,(guide,),64)
    bg=background()
    return bytearray(image[n] if n in mask else bg[n//160*200+n%160]
                     for n in range(160*64))
