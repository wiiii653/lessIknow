"""Crop production character sheets and quantize their alpha masks for Atari."""
from pathlib import Path
from PIL import Image

PALETTE=((0,0,0),(255,50,160),(0,220,255),(255,190,150))


def palette_ink(rgb):
    return min(range(4),key=lambda ink:sum((rgb[c]-PALETTE[ink][c])**2 for c in range(3)))


def clean_alpha(image):
    alpha=image.getchannel('A').point(lambda value:255 if value>=112 else 0)
    return Image.merge('RGBA',(*image.convert('RGB').split(),alpha))


def fit_rgba(image,size):
    image=clean_alpha(image)
    box=image.getchannel('A').getbbox()
    if not box:
        raise ValueError('production sprite cell has an empty alpha mask')
    image=image.crop(box)
    image.thumbnail(size,Image.Resampling.NEAREST)
    canvas=Image.new('RGBA',size,(0,0,0,0))
    canvas.alpha_composite(image,((size[0]-image.width)//2,(size[1]-image.height)//2))
    return canvas


def store_rgba(image,path):
    image=clean_alpha(image)
    raw=image.tobytes();out=bytearray(raw)
    for i in range(0,len(out),4):
        ink=PALETTE[palette_ink(out[i:i+3])]
        out[i:i+3]=bytes(ink)
    Path(path).write_bytes(out)


def prepare():
    girl=Image.open('assets/art/source/act1_girl_walk_cycle_v177.png').convert('RGBA')
    cell_w,cell_h=girl.width//2,girl.height//2
    girl_out=bytearray()
    for row in range(2):
        for col in range(2):
            cell=girl.crop((col*cell_w,row*cell_h,(col+1)*cell_w,(row+1)*cell_h))
            girl_out.extend(fit_rgba(cell,(48,64)).tobytes())
    Path('build/girl-walk-cycle-v177.rgba').write_bytes(girl_out)

    boy=Image.open('assets/art/source/act1_boy_whistle_v177.png').convert('RGBA')
    portrait=fit_rgba(boy,(76,64))
    boy_canvas=Image.new('RGBA',(160,64),(0,0,0,0))
    boy_canvas.alpha_composite(portrait,(84,0))
    store_rgba(boy_canvas,'build/boy-whistle-v177.rgba')

    basketball=Image.open('assets/art/source/act3_basketball_hero_v177.png').convert('RGBA')
    cell_w,cell_h=basketball.width//2,basketball.height//3
    placements=((22,0,58,56),(22,0,58,56),(24,0,58,56),
                (42,0,58,56),(44,0,58,56),(62,0,64,56))
    hero_out=bytearray()
    for index,(left,top,width,height) in enumerate(placements):
        row,col=divmod(index,2)
        cell=basketball.crop((col*cell_w,row*cell_h,(col+1)*cell_w,(row+1)*cell_h))
        actor=fit_rgba(cell,(width,height))
        canvas=Image.new('RGBA',(160,56),(0,0,0,0))
        canvas.alpha_composite(actor,(left,top))
        hero_out.extend(canvas.tobytes())
    Path('build/basketball-hero-v177.rgba').write_bytes(hero_out)


if __name__=='__main__':
    prepare()
