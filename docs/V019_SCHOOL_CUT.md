> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# v019 — cutaway to the girl before school

[READ] A blonde girl portrait was inserted before the school, from reserved
material `assets/art/source/act1_blonde_portraits_reserved_v014.png` (top-left
frame). No new illustration was generated. 160×64 conversion, each row repeated
three times, like the other images before the school.

| Ticks | Shot |
| --- | --- |
| 2992–3552 | Boy from the front |
| 3553–3926 | Girl from the front, before the school |
| 3927–4487 | Back to the boy from the front |
| 4488–4861 | Girl appears in the foreground, boy still looking straight ahead |
| 4862–5983 | Girl walks away towards the doors, boy looks back at her |
| 5984 | Start of the hall and training, without a shift |

## V2 / V3 — additional bank

[READ] The previous 14 banks had no room for another full image.
A new INIT loads an additional 8 KiB in the next bank, preserving PORTB.
The bank value is stored at `$24B3`, in the gap between the existing
player segments. The selection continues the detected PORTB table: `$AA→$AC`,
`$C6→$CA` or `$E6→$EA` (runtime values with the OS disabled).
It does not shift or overwrite banks 1–14. The data goes into the inactive
buffer through the existing copy, and the NMI restores the foreground bank.

## V1 / V6 — validation

[READ] 30 tests OK, including the full shot sequence and its pixels,
the transition to training and the existing performance-scene tests.
In Atari800 PAL `-1088xe` full memory dumps were compared: the boy,
the cutaway to the girl, the hold, the return to the boy, the girl's entrance
and walk-away, and four later performance frames. All images
match the sources.

[ASSUMPTION] The two remaining memory-expansion tables and physical Atari
require separate checking; the emulator test covers the specified `-1088xe`.
Preview: `build/v019-school-cuts.png`.

[READ] Full stereo POKEY track comparison in Atari800:
8 648 064 identical bytes, about 2409.0 s of emulation.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v019.xex --seconds 12
```
