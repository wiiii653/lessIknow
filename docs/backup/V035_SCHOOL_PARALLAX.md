> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# v035 — two planes in a cutaway before school

The exact figure from the v033 frame is used: cut out with a mask from the
original illustration, preserving its scale and framing. The background under
her silhouette was reconstructed, and the canvas was extended to 200 pixels.
During the cutaway the background moves 18 pixels to the left and the girl 38
pixels to the right. Independent small shifts of the hair bands create a gust
of wind. The shot lasts from tick 3553 to 4113; the following cuts remained at
their existing positions.

18 frames are created during the build by compositing the cut-out figure and
the background; Atari replays the finished frames every 32 ticks and copies
them into the inactive buffer. Five new banks hold a total of 20 frame slots
(the last two are repeats), the rendering code and the tables. Altogether the
demo uses 38 banks. The effect is not computed as two overlaid layers per frame
on the 6502.

Figure source: `assets/art/source/act1_girl_side_walking_v033.png`.
The completed background `assets/art/source/act1_school_background_v034.png`
was created by removing the girl from that image and recreating the occluded
fragments in imagegen. Mask and pixel preparation: `tools/prepare_school_pan.py`
(system Python with Pillow). Frame generator: `tools/school_parallax.py`.

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 49 tests PASS,
including all 18 frames and the scene boundaries. Atari800 PAL 1088XE: captures
of the active display list for all 18 frames match the source artwork.

[READ] `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v035.xex --seconds 12`: 7 637 040 identical bytes of
stereo POKEY (~2127.4 s of emulation, the whole track). No separate listening
test was performed on physical Atari. The GIF preview is generated from the
execution of the 6502 code, PAL colours approximated.

SHA256 v035: `3bbea99f540375d923b531b6c8f0ac3a9b072c66e14647018826be17ad8a9726`.
v033 and the intermediate v034 were preserved.
