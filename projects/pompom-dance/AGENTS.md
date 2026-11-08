# Pompom Dance — extracted project

This is a self-contained Atari scene project extracted from TLIKTB v141.
It must build without reading files from the parent repository. Preserve
the source images and `reference/dance_frames_v141.bin`; the builder requires
the 12 generated frames to match that reference exactly.

Use Python 3, ImageMagick and `requirements-dev.txt`. `make all`, `make check`
and `make playback` accept `PYTHON=/path/to/venv/bin/python`. Numbered outputs
must not be overwritten. The target is PAL Atari800/1088XE, Altirra OS, stereo
POKEY. Music comes from the supplied v035 player in `player/`; preserve its
four evenly spaced updates and bank-restoring NMI wrapper.

The standalone player loops one/two/three cheerleaders over the original
music. Eight music banks and six art banks use the original fourteen-bank
loader. Bitmap buffers are `$8000`/`$A000`, display lists `$1400`/`$1800`,
callback `$1000`, state `$13E0`, beat-effect helper `$1C00`, PMG `$0980–$0BFF`.
Do not reuse the parent's later PMG buffer at `$8980`, which is inside this
project's framebuffer. CPU-only tests do not establish actual FPS.
