> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# v049 — Trevor in front of a moving tunnel

Both existing Trevor poses from the energy part were cut from the bitmap
with masks in `tools/trevor_polished.py`; their pixels inside the masks remained the
same. The former static background was replaced by a tunnel with rings expanding
from the centre. This gives the impression of the viewer moving towards Trevor.
Four moving PMG sparks remain. The two earlier frames of entering the hall,
the hit at tick 26928 and the exit at tick 32912 are preserved.

The tunnel has 16 phases changing every 16 ticks, for each of the two poses.
The image is assembled at build time and copied to the inactive buffer;
Atari does not assemble separate bitmaps in real time. The banks with code copies
are 16 KiB each, are detected by alias checking, and in total the demo uses
54 banks (864 KiB). Selectors of the new variants `$08D8–$08E7`. The original
bank 17 still handles the ball in the tunnel/rotator. The colour sequence remained.

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 55 tests PASS.
The tests cover all phases, the behaviour of Trevor's pixels in the masks, the change
of the background itself, both poses, scene boundaries and PMG. Atari800 PAL 1088XE: 39 dumps
covering all phases and both poses, the entrance and the restart; the content of the
active bitmap agrees with the generated graphics.

[READ] `APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo
build/visual-prototype-v049.xex --seconds 12`: 8 601 480 identical bytes
of stereo POKEY (~2396.0 s of emulation, the whole piece). No separate listening
on physical Atari was performed. Preview: `build/v049-trevor-tunnel.gif`; the colours approximate
PAL, and the speed corresponds to the selected music clock phases.

SHA256 of the XEX: `55405a1328e9fce22f1b574f39ad68f20767be0d701c443bb125585a32c101a7`.
Previous XEX files preserved.
