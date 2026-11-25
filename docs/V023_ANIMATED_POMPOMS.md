> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# v023 — animated pompoms and shot palettes

[READ] Four pompom-band wave phases were added to four performance shots
(14960–20943). The update touches only selected fragments of the pompom
bitmap. The base images and every phase are rebuilt without accumulating
errors, also across clock jumps. Skin pixels remain protected.
Blinks and the hair band on PMG still work.

[READ] Each frame has separate COLPF0/COLPF1 colours: pink/cyan,
purple/turquoise, red pink/blue and magenta/green.
COLPF2 stays `$2C` to keep warm skin and blonde hair.
The palette is set after waiting for vblank.

## V2 / V3 — memory and code

[READ] The routine under `$6900` in bank 15 applies local change packages.
4164 B of packages fit in `$6F90–$7FD3`; PMG restoration ends before
`$6F90`. The test checks the boundaries against the ball code and both
helpers. The data stays packed at 80 pixels per row; during the update it is
expanded horizontally into the current 160-pixel buffer.

[READ] A call without a phase change: about 5700 py65 instruction cycles,
with a new phase: about 12900–28400 depending on the shot. These are costs
without DMA, NMI and vblank waiting; they are not a claim about a single
frame budget. The full bitmap and list are not rebuilt when a shot is held.

## V1 / V6 — verification

[READ] The tests check all phases in any order, full output pixels, the four
palettes, skin protection, bank boundaries, blinking, recovery after restart
and the earlier school cut-in. Atari800 PAL `-1088xe`: screenshots of the
four phases of each of the four shots match the source; the school cut-in and
return, the ball and the exit from the portrait shots were also checked.

[READ] Full stereo POKEY music matches the original:
8 568 144 identical bytes, about 2386.7 s of emulation.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v023.xex --seconds 12
```

[ASSUMPTION] The PAL colour preview is an approximation. Physical hardware
still needs checking. Preview: `build/v023-pompoms.gif`.
