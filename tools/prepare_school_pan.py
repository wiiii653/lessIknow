"""Prepare the v176 left-facing arena walker and extended background."""
from pathlib import Path
from PIL import Image
import sys
sys.path.insert(0,'tools')
from build_sequence import PALETTE
from school_story import color
source=Image.open('assets/art/source/act1_girl_arena_walk_v176.png').convert('RGBA')
alpha=source.getchannel('A')
source=source.crop(alpha.getbbox())
width=round(source.width*64/source.height)
source=source.resize((width,64),Image.Resampling.LANCZOS)
rgb=source.convert('RGB')
rgb_data=rgb.tobytes()
mapped=bytes(channel for i in range(0,len(rgb_data),3)
             for channel in PALETTE[color(rgb_data[i:i+3])])
rgb=Image.frombytes('RGB',source.size,mapped)
source=Image.merge('RGBA',(*rgb.split(),source.getchannel('A')))
fg=Image.new('RGBA',(160,64),(0,0,0,0))
fg.alpha_composite(source,(4,0))
clean=Image.open('assets/art/source/act1_school_background_v034.png').convert('RGB').resize((160,64),Image.Resampling.NEAREST)
Path('build/school-girl-cutout-v176.rgba').write_bytes(fg.tobytes())
# Preserve every original pixel outside the foreground; fill its footprint.
back=clean.copy()
wide=Image.new('RGB',(200,64));wide.paste(back,(0,0));wide.paste(back.crop((120,0,160,64)),(160,0))
Path('build/school-wide-v034.rgb').write_bytes(wide.tobytes())
