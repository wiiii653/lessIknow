> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V281 — basketball from release 001 and corrected masks

[READ] `less-i-know-demo-release-001.xex` is v254. The basketball player's
bytes in its bank 15 match the preserved `assets/art/reference/v175/basketball.bin`.
The set of five full frames, three dribbling patches, four hand poses, insert
phases, ball trajectories and three backboard-break patches were returned to
this source. The earlier replacement with six v177 poses was reverted.

`tools/hero_mask_cleanup.py` removes fragments of the purple background from
around the thighs, the space between the legs and the area around the legs.
Small, explicitly defined areas of the negative mask replace only pixels of
the old pink with the corresponding pixels of the clean hall; outlines, skin
and the turquoise outfit are not repainted.
The correction also covers the moving-hand patches so that they do not
restore the background.

The stereo build `releases/less-i-know-demo-release-018-stereo.xex` uses the
compact AVG loader and a late start. The bank layout and the size of the
basketball player graphics remain as in release 001; the additional full
v177 frames and their helper are no longer installed.

[READ] The comparison with release 001 checks the original data, the unchanged
backboard-break patches, key phases, poses, ball parameters and the restriction
of pixel changes to explicit masks. The frame preview after the correction was
reviewed. The dribbling comparison every 8 ticks preserves the pose numbers,
phases and ball position from release 001.
[READ] Full suite: 200/200 tests, 146.239 s; the additional dribbling
comparison with release 001 also passed. Atari800 PAL/1088XE: 16 097 040
identical stereo POKEY bytes against v035, the whole track.

[LIMITATION] This build has not yet been checked on physical Atari.
Emulation and CPU tests do not confirm actual smoothness or audio output.
