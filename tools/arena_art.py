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


PORTRAIT_OUTLINES={
    'neutral': ((125,2),(136,1),(143,3),(151,6),(157,11),(160,16),
                (160,20),(158,23),(154,24),(157,27),(156,31),(153,33),
                (150,36),(149,40),(152,44),(155,47),(156,49),(160,50),
                (160,64),(81,64),(85,59),(94,54),(106,49),(115,44),
                (117,40),(112,35),(110,31),(111,25),(108,23),(107,17),
                (110,12),(115,8),(120,5)),
    'turned': ((124,2),(140,2),(147,4),(154,7),(158,11),(160,14),
               (160,17),(159,21),(157,25),(157,32),(160,34),
               (158,37),(154,39),(152,41),(149,43),(152,46),(155,49),(160,50),(160,64),
               (81,64),(85,59),(94,54),(106,49),(115,44),(116,40),
               (112,37),(110,32),(110,26),(107,24),(105,20),(106,16),
               (110,11),(116,8),(119,5)),
    'whistle': ((125,2),(135,1),(143,3),(151,6),(157,12),(159,16),
                (160,19),(159,23),(157,26),(154,29),(153,32),(150,34),
                (150,38),(147,41),(150,44),(153,47),(155,49),(160,51),
                (160,64),(81,64),(85,59),(94,54),(106,49),(115,44),
                (117,40),(113,37),(111,33),(111,28),(108,26),(106,21),
                (107,16),(110,12),(115,8),(120,5)),
}


def portrait(image,pose='turned'):
    # The black hair and jacket are opaque inside the traced silhouette.
    # Everything outside comes from the clean arena plate.
    guide=PORTRAIT_OUTLINES[pose]
    bg=background()
    out=bytearray(image[y*160+x] if inside(x+.5,y+.5,guide) else bg[y*200+x]
                  for y in range(64) for x in range(160))
    # Blue inside the head guide belongs to the old school background.
    for y in range(17,40):
        for x in range(105,159):
            if inside(x+.5,y+.5,guide) and image[y*160+x]==2:
                out[y*160+x]=bg[y*200+x]
    # Separate the skin from the blue arena with the portrait's black keyline.
    before=bytes(out)
    for y in range(18,40):
        for x in range(105,159):
            if (inside(x+.5,y+.5,guide) and before[y*160+x]==2 and
                any(before[(y+dy)*160+x+dx]==3 for dx,dy in ((0,1),(0,-1),(1,0),(-1,0)))):
                out[y*160+x]=0
    # The source is cropped at the right border. Continue the jacket fabric
    # behind its dark seam so the cutout reaches the edge of the picture.
    for y in range(51,64):
        for x in (158,159):out[y*160+x]=1
    return out
