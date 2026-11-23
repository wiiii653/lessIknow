# Pompom Dance — standalone Atari project

The cheerleader scene extracted from TLIKTB v141. It contains its own sources,
both input images, the original v035 player, reference frames, the generator,
tests and a ready `build/pompom-dance-v001.xex`. It does not require files from
the parent project.

## Running

PAL, stereo POKEY, expansion compatible with Atari800 `1088XE` (the same test
configuration as the main demo), Altirra OS. In Altirra choose 65XE/PAL with
1 MB expansion and stereo POKEY. The project uses 14 banks of 16 KiB each:
8 music and 6 graphics.

```sh
atari800 -1088xe -pal -nobasic -run build/pompom-dance-v001.xex
```

From the start of the music, the entrances of one, two and three girls are
looped, in a cycle of 2992 ticks (~15 s). The four poses of each group, shadows,
the four-colour hall and PMG accents are preserved. This is a separate scene
show; it does not contain the remaining acts of the main demo. The music remains
the full v035 track.

## Building and verification

Python 3, GNU Make and ImageMagick (`convert`):

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
make all PYTHON=.venv/bin/python
make check PYTHON=.venv/bin/python
```

`make all` creates a replaceable `build/pompom-dance-dev.xex` and JSON. Do not
overwrite numbered releases. New release:

```sh
.venv/bin/python tools/build_pompom_demo.py --output build/pompom-dance-v002.xex
```

`reference/dance_frames_v141.bin` contains exactly 98 304 B: 12 frames of
8192 B. The generator refuses to build if the reproduced graphics differ by
even a single byte. `reference/provenance.json` records the sums of the sources
and of the output v141.

The tests check all groups and poses by executing 6502 code, the identity of the
reference, the music banks and the spacing of the four DLIs. A copy of the full
bitmap is prepared in the inactive buffer; this project does not use the main
demo's dirty-pages optimisation. The callback rate requires evaluation in an
emulator/hardware.

The music comparison requires Atari800 and the Altirra OS ROM. The paths and
settings are in `tools/check_playback.py`; in the host environment the command
`make playback PYTHON=/path/to/python` used the available Atari800 wrapper.

## v001 results

[READ] 3/3 tests passed. The original graphics of all 12 frames match v141 byte
for byte. Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
16 312 896 identical bytes against v035; the entire track.
No test on physical Atari and no FPS measurement with ANTIC DMA was
performed.

XEX: 253 197 B, SHA-256:
`47c558dd06ba0bf2163b69e7d6bf8441e9fe1589d4f819d2df2e763a731ee8e5`.

RAM map: callback `$1000`, state `$13E0`, display lists `$1400`/`$1800`,
effects `$1C00`, bitmap buffers `$8000`/`$A000`, PMG `$0980–$0BFF`.
Archival notes on the scene's development are in `docs/`; they describe the
earlier engine of the main project, while the map above applies to standalone
v001.
