# V069 — multicolour letters at the beginning

The two opening screens use ANTIC F and GTIA 11: an 80×192 pixel image
with up to 16 shades at a common brightness. The letters received a rainbow
fill, an offset colour shadow and brightness pulsing. A pixel with value
zero remains black. The content and boundaries of the screens are as in v064.

The helper `$FEF0–$FF92` switches only the inactive display list between
modes F and E, preserving the music DLI bits. It works during the regular
screens; before banked scenes both lists return to mode E. The music player
was not changed.

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 63 tests OK,
including GTIA 11 colours, mode switching and DLI on lines 0, 78, 156 and 234.
Atari800 7.2.1, PAL, 1088XE, Altirra OS, stereo: 14 958 frames up to tick
59832 had music counters and four sampled POKEY registers consistent with v064.
From tick 3200 the screen shortcuts were consistent on all compared frames;
at the transition from title to school two frames differed. A full stereo POKEY
comparison with the original v035 gave 7 489 080 identical bytes after
a single alignment of the start. This does not replace listening on the target Atari.

The preview is a screenshot from Atari800 with the emulator's approximate palette. Release:
`releases/visual-prototype-v069.xex`; SHA-256
`a7e7599a2ab63df7d88b492bc284582abdbbaa66fb59fdd01b814eae1704916c`.
