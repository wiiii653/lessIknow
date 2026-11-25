> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V257 — story cutaways in the existing montage

[READ] In response to the request to close the story within the existing
montage, four compositions were added from existing character sources:

- 37884–39378: mosaic of Trevor's face;
- 40875–42370: three panels — Trevor, the girl and the boy;
- 42371–43866: confrontation between Trevor and the basketball player;
- 46858–49849: close-up of Trevor before the shot of the defeated boy.

In each of these windows the static comic frame is interleaved every 256
ticks with the previous moving rotator/tunnel. These are comic cutaways,
not a new fight animation. The approved 13 punches with balls remain,
the girl's eyes 39379–40126 and the boy and terminal from 49850. None of the
existing cut ticks or the music clock was shifted.

[READ] The graphics occupy slots 56–59 of the organic tunnel in the loader of bank 17;
outside the scenes, slots 56–63 were redirected to 52–55. This replaces four
further tunnel phases, in addition to the four used earlier for the eyes.
Bank 2: scene selector `$7600–$7647`, PMG publication and gating `$7700–$772D`;
extended eye selector `$7500–$7550`. In the new panels the PMG ball is
disabled during blanking so that it does not cover the faces; after returning
to the effect the previous ball renderer resumes. Main code with no growth,
one JSR address change; 64 banks. CPU callback preview with approximate
palette: `build/v257-story-preview.png` — it is not an emulator recording.

[READ] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 16 377 408
bytes identical to v035 throughout the whole track. No A/V evaluation on hardware;
py65 tests do not model ANTIC DMA or FPS.

[READ] `make check PYTHON=/tmp/tliktb-fix-venv/bin/python`: 203/203
cases, no skips; 152.000 s.
