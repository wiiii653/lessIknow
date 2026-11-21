"""Hand-traced profile and flowing hair on the preserved arena walk.

Only the head/hair footprint is replaced. The background plate is sampled at
the original parallax offsets; jacket, hands, steps and camera remain original.
"""
from arena_art import background, inside

BACKGROUND_OFFSETS = tuple(range(17)) + (18,)
HAIR = ((48,1),(54,1),(57,3),(58,7),(56,11),(56,17),
        (53,20),(48,20),(44,23),(35,23),(39,19),(31,21),
        (26,20),(33,16),(29,16),(35,12),(38,8),(44,7),(45,4))
FACE = ((51,8),(55,9),(57,11),(57,13),(59,14),(57,15),
        (57,18),(53,19),(50,16),(50,12))
STRANDS = (((46,5),(48,4),(46,10),(40,14),(35,16),
            (41,12),(44,9)),
           ((49,10),(50,11),(47,16),(42,20),(40,20),
            (45,16)),
           ((50,7),(52,8),(51,11),(51,15),(53,18),
            (52,19),(49,16),(49,12)))


def polish(frame, index, offset):
    result = bytearray(frame)
    plate = background()
    # This rectangle encloses the old flowing hair but stops above the jacket.
    for y in range(24):
        for x in range(24,61):
            result[y*160+x+offset] = plate[y*200+x+offset+BACKGROUND_OFFSETS[index]]
    hair = {(x,y) for y in range(24) for x in range(24,61)
            if inside(x+.5,y+.5,HAIR)}
    face = {(x,y) for y in range(24) for x in range(24,61)
            if inside(x+.5,y+.5,FACE)}
    shape = hair | face
    for x,y in shape:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)):
            xx,yy=x+dx,y+dy
            if 0<=yy<24 and (xx,yy) not in shape:
                result[yy*160+xx+offset] = 0
        result[y*160+x+offset] = 3
    for y in range(24):
        for x in range(24,61):
            if (x,y) in shape and any(
                    inside(x+.5,y+.5,line) for line in STRANDS):
                result[y*160+x+offset] = 0
    # Three deliberately sparse features, attached to the original head path.
    for x,y,ink in ((53,12,0),(55,14,1),(54,16,1)):
        result[y*160+x+offset] = ink
    return bytes(result)
