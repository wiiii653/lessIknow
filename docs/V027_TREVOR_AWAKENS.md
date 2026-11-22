# v027 — TREVOR AWAKENS

[READ] Act 4 covers ticks 23936–32911. The quiet part: 23936–26927,
the energetic part: 26928–32911. The start of the next act remains
at 32912 and transitions to the existing kaleidoscope.

## Implementation

[READ] Two backdrops: a night-time hall with doors and a neon geometric passage.
The Trevor character is drawn by four players. Twelve PMG sets
cover three sizes plus four pose/mirrored variants. In the first
part the size and brightness grow. After the music hit, full colours return,
pulsating zoom, sinusoidal motion and four orbiting missile accents.
Rotation applies to the orbital accents, and the character changes and bounces its poses.

[READ] The backdrops and character studies were generated with the built-in image_gen:
`assets/art/source/act4_trevor_awakens_v025.png`.
The final PMG silhouette is drawn in code on a 16×24 grid, with a larger
face and shoulders to stay readable when limited to 16 columns.
The sets are scaled vertically and use the hardware player widths.
Previews: `build/v027-trevor-reveal.gif`, `build/v027-trevor-energy.gif`.

## V2 / V3 — bank 17

[READ] The new INIT probes 64 PORTB candidates, comparing each with
the sixteen loaded banks. It uses the markers `$55` and `$AA` to
distinguish an alias from an accidental data value. On each attempt it restores
the original byte. Only an independent bank receives the new act's data.
In Atari800 PAL `-1088xe`, `$C0` was selected, stored at `$24B5`.
We do not assume that `$B0` is the next bank.

[READ] Bank 17: backdrops `$4000–$53FF`; the first six PMG blocks
`$5400–$5FFF`; code and tables from `$6000`; the remaining six PMG blocks
`$6C00–$77FF`. The code in bank 16 delegates act 4 through the existing
unbanked bank-switching procedure and then restores its standard operand.
The main code remains 1788 B long, without overwriting bitmaps.

[READ] Maintaining the backdrop costs about 7050–10530 py65 instruction cycles
depending on the PMG size. Without DMA, NMI and vblank waiting; this is not
a guarantee of a free budget on every line. The full backdrop is copied
only when the act part changes. Exit and restart restore the dance PMG.

## V1 / V6 — verification

[READ] 42 tests OK: act boundaries, two rasters, three sizes, foreground
motion, behaviour of earlier scenes, restart and the safe trial of a
new bank. A separate test places `$55` in one of the earlier
banks and verifies that detection still selects an independent bank and
restores all sixteen earlier blocks byte for byte.

[READ] Full stereo POKEY recording matching the original:
9 295 992 identical bytes, about 2589.5 s of emulation.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v027.xex --seconds 12
```

[ASSUMPTION] Physical hardware and other memory expansion configurations remain to
be checked. The preview uses a PAL colour approximation; the reference signal model
is described by the [Atari800 code](https://github.com/atari800/atari800/blob/master/src/colours_pal.c).

## Graphics prompt — imagegen skill

```text
Production illustration-story contact sheet for Atari demo, EXACTLY 2 columns and 2 rows, four equal landscape panels without gutters. European comic illustration with bold black contours and broad flat colors, NOT anime/manga, no giant human eyes. Palette only black #000000, deep violet #740090, hot pink #ff32a0, pale warm pink #ffbece, cyan #00dcff limited highlights. Top left: EMPTY school gym at night, centered dark double doorway, tall windows, wall bars, parquet in perspective, dim sparse pink/cyan outlines, NO characters. Top right: SAME empty gym transformed into psychedelic neon geometric arches and radial rays toward center, clear dark central area for a large animated character, NO characters. Bottom left: TREVOR, anthropomorphic powerful male gorilla, front view full body, slightly bent knees, very broad shoulders and long arms hanging down, violet fur, pink chest and hands, pale face, strong readable gorilla muzzle, small natural eyes and confident calm expression, on pure black background. Keep entire body and feet inside panel. Bottom right: SAME gorilla identity, full body front view, shoulders raised, one broad forearm lifted to chest, confident powerful stance. Character silhouettes must remain readable when reduced to16x24 pixels for hardware sprites. No clothing, no text, no basketball, no decorative particles. Reference gorilla supplies identity and palette only; make it more grounded European comic, no goofy tongue or doll eyes. Top backgrounds wide cinematic compositions, bottom characters centered.
```

[READ] Atari800 PAL `-1088xe`: 23 consecutive memory dumps cover
earlier scenes, the image/Trevor boundary, the quiet part, the exact tick
26928, the motion after the hit, the last tick of the act, exit and restart.
The compared bitmaps match the sources; the value of bank 17 is `$C0`.
