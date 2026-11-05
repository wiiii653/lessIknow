"""Prepare exact v033 pixels as separate foreground and extended background."""
from pathlib import Path
from PIL import Image, ImageDraw
src=Image.open('assets/art/source/act1_girl_side_walking_v033.png').convert('RGB').resize((160,64),Image.Resampling.NEAREST)
clean=Image.open('assets/art/source/act1_school_background_v034.png').convert('RGB').resize((160,64),Image.Resampling.NEAREST)
mask=Image.new('L',(160,64));d=ImageDraw.Draw(mask)
d.polygon([(45,1),(53,1),(55,4),(55,8),(57,12),(56,16),(53,19),(51,20),(52,26),(53,35),(57,44),(61,47),(66,48),(68,51),(67,55),(64,57),(60,57),(55,54),(53,54),(51,58),(50,63),(22,63),(24,59),(28,54),(30,50),(27,49),(19,51),(17,55),(14,59),(11,62),(8,61),(7,58),(9,55),(14,50),(16,44),(18,40),(22,36),(27,32),(31,27),(34,24),(31,24),(26,23),(23,21),(21,18),(21,12),(23,9),(26,8),(25,7),(27,5),(32,6),(36,5),(41,3)],fill=255)
# The foreground is sampled directly from the previous release, unchanged.
fg=src.convert('RGBA');fg.putalpha(mask);Path('build/school-girl-cutout-v034.rgba').write_bytes(fg.tobytes())
# Preserve every original pixel outside the foreground; fill its footprint.
back=clean.copy()
wide=Image.new('RGB',(200,64));wide.paste(back,(0,0));wide.paste(back.crop((120,0,160,64)),(160,0))
Path('build/school-wide-v034.rgb').write_bytes(wide.tobytes())
