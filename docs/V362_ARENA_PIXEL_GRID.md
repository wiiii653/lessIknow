> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V362 — shared pixel grid in front of the arena

The boy and the girl in the close-up by the arena use the same
160 × 64 grid. The girl's close-up comes directly from the original party
drawing sampled to 96 × 128. The outline, hair, seams and Fuji sign
now have details one scene pixel wide. The position, scale and
waist-up framing match v361.

[Comparison with Atari800](../build/v362-arena-pixel-grid.png) ·
[Party reference](../assets/art/reference/v330/README.md)

## AVG releases

Both files are 945 890 B each. The prototype uses 64 banks and 297 shared
rows (11 478 B). The main code is 2 542 B.

- [081 mono, one POKEY](../releases/less-i-know-demo-release-081-mono.xex)
  · SHA-256 `5e2161ef0467001f3988445cf3c8d8fa89b39a38fba1302b62133bdcf9dacf58`
- [080 stereo](../releases/less-i-know-demo-release-080-stereo.xex)
  · SHA-256 `862cf2d1a06a8b3b89e3e1549c4e5c59864eff90ddb9668c7c280370e1c485fd`

## Verification

21 tests of graphics, scene transitions, the loader and the director after Trevor passed.
Comparisons in Atari800 PAL, emulated 1088 XE and Altirra OS showed
differences only in the girl's close-up. In both releases 59 833
POKEY register updates match the previous releases 078 and 079.
A test on physical Atari and a full `make check` remain unperformed.
