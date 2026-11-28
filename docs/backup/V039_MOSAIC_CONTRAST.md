> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# v039 — checkerboard contrast

The rotator and tunnel palettes select hues at least 60° apart according to the
approximate PAL colour wheel used in the preview. One field is additionally
brighter. The filter checks both pulsing phases so that it does not pick
similar colours in the dimmed phase either. The PAL preview is an
approximation; the actual appearance depends on the display and emulation.

Throughout the track there are 161 different pairs of colour values. The first
144 have different hue pairs; after they are used, the last 17 return to
earlier hues with an inverted brightness difference, maintaining contrast. The
remaining rhythm of changes, animations, PMG, transitions and scene timings are
unchanged.

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 50 tests PASS;
161 combinations were checked in both brightness phases and no identical sets
were found.

[READ] Atari800 PAL 1088XE stereo POKEY: `APPIMAGE_EXTRACT_AND_RUN=1 python3
tools/check_playback.py --demo build/visual-prototype-v039.xex --seconds 12`:
8 954 784 identical bytes (~2494.4 s of emulation), the full track. Without a
separate listening test on physical Atari. Preview: `build/v039-palettes.png`.

SHA256: `6e37272884e90d8125ae8204e04980c74ee8932a641cb9559c6663a007580b77`.
