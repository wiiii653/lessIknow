> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# v038 — rotator and tunnel palettes

The rotator and the tunnel change the colour pair once per half beat (187 ticks). The sequence
covers 161 different ordered pairs of shades, without repeating the set:
16 pairs in the first occurrence (tick 11968–14959), the next from tick 32912
through the end of the piece. The two shades in a pair are always different. Individual
shades inevitably return in other combinations: GTIA has a finite palette.
Brightness still pulses with the rhythm. If the effect ran past the final position 59840,
the last pair is held instead of reading beyond the table.

The ball and satellites keep the existing PMG colour animation. No changes to scene
boundaries, effect geometry, memory banks or the music interrupt.

[READ] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 50 tests PASS;
an additional test executed the 6502 callback for all 161 pairs, checking the absence of
repetitions, two different shades and the brightness pulse.

[READ] Atari800 PAL, 1088XE, stereo POKEY: `APPIMAGE_EXTRACT_AND_RUN=1
python3 tools/check_playback.py --demo build/visual-prototype-v038.xex --seconds 12`
compared the whole piece: 8 702 928 identical bytes, about 2424.3 s of emulation.
No separate listening on physical Atari was performed.

Preview of 12 successive sets: `build/v038-palettes.png` (PAL palette
approximated). SHA256 of the v038 XEX:
`7c8e7be755c581d7246f17baa516890ed7445ad8622cb9f8b65dd0bcb7863031`.
Previous XEX files remain preserved.
