"""Remove inherited magenta matte fragments around the v001 hero's legs."""
from arena_art import background

# Half-open rectangles in the five original 160x56 keyframes. These enclose
# negative space, not limbs: only pink pixels in these areas are replaced.
# The cyan clothing, peach skin, black contour and every pose stay intact.
NEGATIVE_SPACE={
    0: ((25,22,28,25),(29,24,32,25),(32,23,35,25),
        (30,29,38,47),(37,26,39,29),(43,29,48,31),
        (40,42,46,47),(47,36,62,47),(64,41,71,47)),
    1: ((45,34,50,39),(53,40,58,45),(48,46,53,48)),
    2: ((51,34,57,39),(61,34,67,37)),
    3: ((65,43,73,47),(71,34,79,37)),
    4: ((105,25,108,35),(95,37,99,45),
        (96,45,101,48),(109,42,113,48)),
}

# Outside the back shoulder of the original dribble pose.  The stepped right
# edge follows the silhouette; clear the solid-colour matte to black.
# The arm patches reuse this mask.
SHOULDER_SPACE={11:(35,43),12:(35,44),13:(35,44),14:(35,43),
                15:(35,42),16:(35,40),17:(35,39),18:(35,38),
                19:(35,39),20:(35,37),21:(35,37),22:(35,37)}

# Repair the notch in the original bent knee. Coordinates are source pixels.
KNEE_SKIN = ((63,35),(62,36),(63,36),(64,36),(67,36))

def clean(pixels,pose):
    result=bytearray(pixels);plate=background(interior=True)
    for x0,y0,x1,y1 in NEGATIVE_SPACE.get(pose,()):
        for y in range(y0,y1):
            for x in range(x0,x1):
                offset=y*160+x
                if result[offset]==1:result[offset]=plate[offset]
    if pose==0:
        for y,(x0,x1) in SHOULDER_SPACE.items():
            for x in range(x0,x1):
                offset=y*160+x
                if result[offset]==3:result[offset]=0
        for y in range(17,21):
            for x in range(70,76):
                offset=y*160+x
                if result[offset]==1:result[offset]=0
        for x,y in KNEE_SKIN:
            result[y*160+x]=3
    return bytes(result)
