# v044 — Trevor refinement

The old Trevor was an enlarged PMG silhouette on a 16×24 grid. It was replaced
by four more detailed comic frames of 160×64: entering through the doors, a
closer shot in the hall, and two poses in the neon hall. In the first part the
character approaches in two cuts, and the image gradually brightens.
After the musical hit, two illustrations change every 256 ticks; four PMG
missiles form moving coloured sparks. Instead of the previous hardware zoom,
two illustrated close-ups and a change of poses are used.

The boundaries are unchanged: 23936 start, 26928 hit, 32912 the next scene.
The bitmap frames are held in a new bank 39, detected by the same alias
checking; its selector is located at `$08D8`. The music and surrounding scenes
keep their banks. The earlier Trevor bank remains in use by the ball effect in
the tunnel and rotator. Each close-up is copied to the inactive buffer; with a
still frame only the sparks and colours are refreshed.

Source: `assets/art/source/act4_trevor_polished_v043.png`. Generated with
imagegen using the original Trevor sheet as reference.

Prompt: "Production contact sheet for an Atari 8-bit demo, exact 2 columns x
2 rows of equal wide landscape panels without gutters. Based on reference, same
character Trevor: muscular gorilla with violet fur, pink chest, pale expressive
face, natural proportions, confident expression. European bande dessinée /
1980s European comic, not anime, no manga or giant eyes. Flat graphic, bold
black shapes and contours, restricted palette EXACTLY black, dark violet
#740090, hot pink #ff32a0, pale pink #ffbece. Designed to remain readable when
each panel is reduced to 160 x 64 pixels: large features, no tiny lines, broad
separations. Top left: Trevor waist-up emerging through the dark doors at far
end of a school gym, centered and ominous, gym wall bars and floor visible,
no other people. Top right: same Trevor closer, from waist up, strong chest and
arms, face readable, dark gym setting. Bottom left: Trevor in dramatic upper-body
front three-quarter pose, one fist forward, energised neon gym, converging
geometric architectural beams behind him. Bottom right: same character in
alternate strong pose with raised fist, dramatic head-and-torso closeup and
stylized neon gym beams. Same recognizable face and body across panels. Crisp
large silhouette, no text, no numbers, no watermark, no decorative frames."

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 53 tests PASS,
including all frames, act boundaries, spark movement and the return of the
remaining effects. Atari800 PAL 1088XE: 18 screenshots covering the scene, its
boundaries and the restart; the active bitmap matches the source frames, the
missile data is present.

[READ] `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v044.xex --seconds 12`: 7 539 984 identical bytes of
stereo POKEY (~2100.3 s of emulation, the whole track). Without a separate
listening test on physical Atari. `build/v044-trevor.gif` shows the preview
with an approximation of PAL colours.

SHA256 XEX: `ab0f017d68e57e69186865c4e51c96a4c794b0e29dc0c66bb1e6f149bf18dea6`.
Previous XEXes preserved.
