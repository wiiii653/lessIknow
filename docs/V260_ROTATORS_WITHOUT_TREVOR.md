> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V260 — rotators without Trevor's last cutaways

[READ] At the user's request, four comic cutaways from v257 were withdrawn:
the repeated/replaced Trevor close-up, the panel of three characters, the
confrontation and the large Trevor portrait. In their place the moving montage
of bananas/tunnels works again as in v256. The girl's eye sequence, the earlier
fight of Trevor with the balls, the terminal, the final boy, the music and the
ticks remain. The former generator/test files were kept in `docs/archive/`
outside the build.

[READ] XEX v260 differs from v256 only by 17 bytes of the load signature
`AI-SLOP/OGNJEN`; the remaining segments are identical. In it, the four tunnel
phases displaced by v257 are restored. The next four still contain the v252
eyes. There are no additional banks. 16 targeted tests passed;
CPU tests do not prove real FPS or ANTIC DMA behavior on hardware.

[READ] `make check PYTHON=/tmp/tliktb-fix-venv/bin/python`: 199/199
cases, no skips; 152.233 s. Atari800 PAL/1088XE, Altirra OS,
stereo POKEY: 16 272 720 identical bytes to v035 across the whole track.
