"""Native four-ink artwork for the cheerleader in her casual clothes outside Atari Arena."""
from functools import lru_cache
from math import hypot, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

BLACK, ROSE, BLUE, LIGHT, AIR = range(5)
CLOSE_FUJI = (29, 41)
# Frame 0: front contact. The following three frames plant that foot while
# the other lifts. A three-pixel move per frame cancels the contact's drift
# against the moving arena plate.
STEPS = ((6, 0), (3, 0), (0, 0), (-3, 0),
         (-6, 0), (-4, 3), (0, 5), (4, 2))


class Drawing:
    def __init__(self, width, height, scale=(1, 1)):
        self.image = Image.new('L', (width, height), AIR)
        self.pen = ImageDraw.Draw(self.image)
        self.sx, self.sy = scale

    def points(self, points):
        return [(round(x*self.sx), round(y*self.sy)) for x, y in points]

    def shape(self, ink, *points):
        self.pen.polygon(self.points(points), fill=ink)

    def line(self, ink, *points):
        self.pen.line(self.points(points), fill=ink)

    def result(self):
        data = self.image.tobytes()
        return (bytes(i if i != AIR else BLACK for i in data),
                bytes(i != AIR for i in data))


def limb(drawing, points, widths, light):
    """A tapered sleeve or leg, with both sides of the bend outlined."""
    sides = ([], [])
    for i, ((x, y), width) in enumerate(zip(points, widths)):
        x0, y0 = points[max(i-1, 0)]
        x1, y1 = points[min(i+1, len(points)-1)]
        nx, ny = y1-y0, x0-x1
        length = hypot(nx, ny) or 1
        for sign, side in zip((1, -1), sides):
            side.append((x + sign*nx*width/length, y + sign*ny*width/length))
    drawing.shape(light, *sides[0], *reversed(sides[1]))
    # The clothing and torso can cover one end of the outline.
    for side in sides:
        drawing.line(BLACK, *side)


DANCER_ART = Path('assets/art/source/act2_ribbon_dancer_v136.png')
DANCER_HEAD_BOX = (559, 73, 678, 162)
PORTRAIT_SIZE = (54, 34)


@lru_cache(maxsize=8)
def dancer_head(width, height, rear=False):
    """Retain the ribbon dancer's actual face, curls and black ink."""
    with Image.open(DANCER_ART) as source:
        crop = source.crop(DANCER_HEAD_BOX).convert('RGB')
    # The head and hair are warm; the pink/cyan performance collar falls
    # outside this mask. Near-white teeth and eye highlights remain.
    foreground = Image.new('L', crop.size)
    rgb = iter(crop.tobytes())
    foreground.putdata([
        255 if (r > 132 and g > 86 and r > 1.19*b and g > 1.07*b
                or min(r,g,b) > 158 and max(r,g,b)-min(r,g,b) < 46)
        else 0 for r,g,b in zip(rgb,rgb,rgb)
    ])
    if rear:
        # When she walks away, use the same waves around the silhouette but
        # turn the exposed face into the back of her hair.
        pen = ImageDraw.Draw(crop)
        pen.polygon(((48,26),(58,17),(74,14),(83,18),(89,34),(92,49),
                     (86,62),(78,70),(64,69),(53,60),(46,42)), fill=(247,205,119))
        pen.line(((60,21),(68,27),(65,43),(60,52),(64,64)), fill=(111,69,39), width=4)
        pen.line(((77,20),(82,32),(79,46),(84,56),(82,65)), fill=(111,69,39), width=4)
    foreground = foreground.resize((width,height), Image.Resampling.LANCZOS)
    keyline = foreground.filter(ImageFilter.MaxFilter(3))
    pixels = bytearray()
    rgb = iter(crop.resize((width,height), Image.Resampling.LANCZOS).tobytes())
    for (r,_,_), opaque, edge in zip(zip(rgb,rgb,rgb), foreground.tobytes(), keyline.tobytes()):
        if edge < 120:
            pixels.append(AIR)
        elif opaque < 130:
            pixels.append(BLACK)
        elif r < 116:
            pixels.append(BLACK)
        elif r < 175 and width >= 28:
            pixels.append(ROSE)
        else:
            pixels.append(LIGHT)
    if not rear and (width, height) == PORTRAIT_SIZE:
        # The original teeth are thinner than a scanline at this scale.
        # Keep the bright edge of the smile when sampling the four inks.
        inks = {'.':LIGHT,'r':ROSE,'k':BLACK}
        for y, row in enumerate(('..rr...', 'rkkkkkr', '.k...k.', '..rkr..', '...r...'),18):
            start = y*width + 27
            pixels[start:start+len(row)] = bytes(inks[c] for c in row)
    image = Image.frombytes('L',(width,height),bytes(pixels))
    mask = Image.frombytes('L',(width,height),bytes(255 if color!=AIR else 0 for color in pixels))
    return image, mask


def encounter(drawing, stride):
    """The turn toward the boy, with the same character at each distance."""
    p, line = drawing.shape, drawing.line

    for x, step, far in ((37, -stride, True), (58, stride, False)):
        ankle = x + step
        foot_y = 120 if step >= 0 else 114
        limb(drawing, ((x, 78), (x+step*.4, 96), (ankle, foot_y-3)),
             (6.2, 4.6, 3.2), ROSE if far else LIGHT)
        limb(drawing, ((ankle-step*.15, foot_y-8), (ankle, foot_y)),
             (3.6, 3.4), BLUE)
        p(BLACK, (ankle-4, foot_y-3), (ankle+3, foot_y-3),
          (ankle+7, foot_y), (ankle+7, foot_y+4), (ankle-5, foot_y+4))
        p(LIGHT if not far else ROSE, (ankle-3, foot_y), (ankle+2, foot_y-1),
          (ankle+6, foot_y+1), (ankle+6, foot_y+2), (ankle-3, foot_y+2))

    # High-waisted denim shorts: cuffs, yoke and two little back pockets.
    p(BLACK, (34, 61), (57, 60), (63, 70), (67, 79), (65, 85),
      (54, 86), (48, 80), (44, 86), (32, 85), (28, 81), (29, 71))
    p(BLUE, (35, 63), (56, 62), (61, 71), (64, 79), (63, 82),
      (55, 83), (49, 77), (43, 83), (32, 82), (30, 80), (32, 71))
    line(ROSE, (33, 69), (46, 71), (59, 68))
    line(BLACK, (36, 73), (42, 73), (42, 78), (36, 77), (36, 73))
    line(BLACK, (51, 73), (57, 72), (59, 77), (53, 78), (51, 73))
    line(LIGHT, (32, 82), (43, 83))
    line(LIGHT, (55, 83), (63, 82))

    # Bare shoulders, tapered limbs and a soft middle shadow. Hands swing
    # near the hips; the silhouette leaves space between each arm and waist.
    for points, far in ((((30, 35),(24, 50),(24-stride*.55, 63)), True),
                        (((60, 35),(66, 48),(66+stride*.55, 60)), False)):
        x, y = points[-1]
        p(BLACK, (x-4,y-1), (x+3,y-2), (x+5,y+1), (x+3,y+5),
          (x-1,y+7), (x-3,y+5))
        p(ROSE if far else LIGHT, (x-2,y), (x+2,y-1), (x+4,y+1),
          (x+2,y+4), (x-1,y+5))
        limb(drawing, points, (7.2,4.5,3.1), ROSE if far else LIGHT)
        if not far:
            line(ROSE, (65, 41), (67, 47), (x+2, y-2))

    # Casual ribbed tank with a compact Fuji stitch and a single hem seam.
    p(BLACK, (32,32), (41,27), (50,27), (58,30), (64,34), (62,41),
      (58,47), (58,55), (61,62), (54,66), (39,66), (31,62),
      (33,53), (33,47), (28,41), (27,36))
    p(LIGHT, (33,33), (41,29), (51,29), (59,33), (61,36),
      (55,39), (38,39), (30,36))
    p(ROSE, (32,34), (35,32), (38,38), (42,41), (51,41), (55,38),
      (57,32), (60,34), (61,39), (58,47), (57,55),
      (60,61), (54,64), (39,64), (33,61), (35,52),
      (34,46), (30,40))
    p(BLUE, (33,38), (36,42), (38,47), (37,56), (40,62), (35,61),
      (36,53), (35,45))
    line(BLUE, (58,45), (56,51), (57,56), (59,60))
    line(BLACK, (37,56), (43,58), (51,58), (56,56))
    line(BLUE, (34,61), (40,63), (52,63), (58,61))

    # The neck sits over the stance and stays the same light ink as the
    # face. Keep the dark lines at the hair and neckline, off the jaw.
    p(BLACK, (44,23), (56,23), (57,28), (60,32),
      (56,36), (48,38), (42,36), (38,33), (43,29))
    p(LIGHT, (45,23), (55,23), (55,28), (58,32),
      (55,35), (48,37), (43,35), (40,33), (44,29))

    # Fit the portrait on the target raster. Its face and hair come from
    # the ribbon dancer rather than a new approximation of her profile.
    width, height = (PORTRAIT_SIZE if drawing.sx == 1 else drawing.points(((54, 30),))[0])
    x, y = drawing.points(((18, 1),))[0]
    image, mask = dancer_head(width, height, rear=drawing.sx < 1)
    drawing.image.paste(image, (x,y), mask)

    x, y = CLOSE_FUJI
    if drawing.sx >= .25:
        for side in (-1, 1):
            line(LIGHT, (x+16+side*5, y), (x+16+side*5, y+4),
                 (x+16+side*8, y+7))
        line(LIGHT, (x+16, y), (x+16, y+7))


@lru_cache(maxsize=8)
def sprite(width=96, height=128):
    # Rasterize paths at each destination size. The large shot is already on
    # the 160×64 scene's pixel grid and is cropped naturally at the waist.
    drawing = Drawing(width, height, (width/96, height/128))
    stride = {96: 1, 36: 7, 24: -5, 12: 3}[width]
    if width == 12:
        rows = ("............", ".....lb.....", "....kllpl...", "....lklpl...",
                "...llplk....", "...lkppl....", "...lpppl....", "....ppp.....",
                "....bbb.....", "....blbl....", "....l.lk....", "....l.k.....",
                "....l.l.....", "...bl.bl....", "...kk..k....", "............")
        lut = dict(zip('.kpbl', (AIR, BLACK, ROSE, BLUE, LIGHT)))
        drawing.image.putdata([lut[pixel] for row in rows for pixel in row])
    else:
        encounter(drawing, stride)
    return drawing.result()


def profile_head(drawing, x, y, swing):
    def p(ink, *points):
        drawing.shape(ink, *((x+dx, y+dy) for dx, dy in points))

    def line(ink, *points):
        drawing.line(ink, *((x+dx, y+dy) for dx, dy in points))

    # Recompose the dancer's hair from the side, with an upright neck,
    # small nose and narrow chin. Leave the cheek a single light ink.
    p(BLACK, (-4,1), (1,0), (6,1), (8,3), (8,6), (9,7),
      (9,8), (8,9), (8,11), (5,13), (3,12), (3,16),
      (-2,17), (-3,15), (-6,14), (-8+swing,16), (-12+swing,15),
      (-10+swing,12), (-12+swing,10), (-8,9), (-7,6), (-7,3))
    p(LIGHT, (1,2), (5,2), (7,3), (7,6), (8,7), (7,8),
      (7,10), (5,12), (3,11), (2,13), (2,15), (-2,16),
      (-3,14), (-2,11), (-3,8), (-1,4))
    p(LIGHT, (-5,2), (-1,1), (4,1), (5,2), (1,3), (-1,5),
      (-2,8), (-4,11), (-4,13), (-7+swing,15), (-10+swing,15),
      (-9+swing,13), (-10+swing,11), (-7,10), (-6,7), (-6,4))
    line(BLACK, (-2,6), (-4,9), (-4,12), (-7+swing,14))
    line(ROSE, (-4,3), (0,2), (2,2))
    line(ROSE, (-7,11), (-7+swing,13), (-9+swing,14))
    line(BLACK, (4,5), (6,5))
    line(BLACK, (5,6), (5,7))
    line(ROSE, (6,9), (7,9))


def walk_pose(frame, center):
    """A side-on stride staged against the 200-column arena background."""
    d = Drawing(160, 64)
    p, line = d.shape, d.line
    k = frame % len(STEPS)
    bob = (0, 0, -1, -1, 0, 0, -1, -1)[k]
    h = 39+bob

    # Draw the far leg, then the far arm, then the near limbs. Rather than
    # pixel shifting an old silhouette, the knees and elbows have their own
    # positions in each frame.
    def leg(phase, near):
        step, lift = STEPS[phase]
        ankle_x, ankle_y = center+step, 59-lift
        hip = (center-1 if near else center+1, h)
        knee = (center+step*.45+2+lift*.65, 49-lift*.55+bob)
        limb(d, (hip, knee, (ankle_x, ankle_y-1)), (3.5, 2.8, 2),
             LIGHT if near else ROSE)
        calf_x = (knee[0]+ankle_x)/2
        limb(d, ((calf_x, ankle_y-6),(ankle_x,ankle_y-2),(ankle_x,ankle_y)),
             (2.4, 2, 2), BLUE)
        line(LIGHT if near else ROSE, (calf_x-1, ankle_y-5), (calf_x+1, ankle_y-5))
        toe_y = ankle_y + (1 if phase in (4, 5) else 0)
        p(BLACK, (ankle_x-2, ankle_y-2),(ankle_x+2,ankle_y-2),
          (ankle_x+5,toe_y),(ankle_x+6,toe_y+1),(ankle_x+5,toe_y+2),
          (ankle_x-3,ankle_y+2))
        line(LIGHT if near else ROSE, (ankle_x-2,ankle_y+1),(ankle_x+4,toe_y+1))

    def arm(phase, near):
        s = sin((phase+2)*pi/4)
        dx = center + (0 if near else 3)
        endx, endy = dx+7*s+2, 38+bob
        p(BLACK, (endx-2,endy-2),(endx+4,endy-2),(endx+5,endy+1),
          (endx+3,endy+4),(endx-1,endy+3))
        p(LIGHT if near else ROSE, (endx-1,endy-1),(endx+3,endy-1),
          (endx+4,endy+1),(endx+2,endy+3),(endx,endy+2))
        limb(d, ((dx,22+bob),(dx+4*s-1,31+bob),(endx,endy)), (3.8, 2.8, 1.9),
             LIGHT if near else ROSE)
        if near:
            line(ROSE, (dx+4*s-2,32+bob),(endx-1,endy-1))

    leg((k+4)%8, False)
    arm(k, False)
    leg(k, True)
    # The shorts have straight cuffs and a stitched yoke, not a pleated hem.
    p(BLACK, (center-6,h-5), (center+4,h-6), (center+7,h-2),
      (center+8,h+4), (center+2,h+5), (center-1,h+3),
      (center-3,h+5), (center-8,h+4), (center-8,h+1))
    p(BLUE, (center-5,h-4), (center+3,h-5), (center+5,h-2),
      (center+6,h+2), (center+1,h+3), (center-1,h+1),
      (center-4,h+3), (center-6,h+2))
    line(ROSE, (center-4,h-2), (center+2,h-2), (center+4,h-1))
    line(LIGHT, (center+2,h+4), (center+7,h+3))
    line(LIGHT, (center-7,h+3), (center-3,h+4))

    p(BLACK, (center-5,18+bob),(center+1,17+bob),(center+6,19+bob),
      (center+8,24+bob),(center+6,28+bob),(center+4,32+bob),
      (center+4,36+bob),(center-6,37+bob),(center-8,34+bob),
      (center-6,28+bob),(center-7,23+bob))
    p(ROSE, (center-4,19+bob),(center+1,18+bob),(center+5,20+bob),
      (center+7,24+bob),(center+5,27+bob),(center+3,32+bob),
      (center+3,35+bob),(center-6,36+bob),(center-5,28+bob),
      (center-6,23+bob))
    line(BLUE, (center+4,21+bob),(center+6,24+bob),(center+5,27+bob),
         (center+3,31+bob),(center+3,34+bob))
    line(BLUE, (center-5,35+bob),(center+2,35+bob))
    arm((k+4)%8, True)
    profile_head(d, center-1, 2+bob, (0,1,1,0,-1,-1,0,1)[k])
    return d.result()
