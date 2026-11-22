# V361 — girl from the party version

The starting point is the original from v330 / 058. All 18 panorama frames
and four shots at the arena were reproduced pixel for pixel before retouching.
In the close-up from behind, 36 pixels of hair bands were added. In the panorama,
four profile pixels per frame were corrected at the ear and chin. The silhouette,
the jacket with the Fuji logo, the poses, the background and all three further
shots come from the party.

[Original frames and sources](../assets/art/reference/v330/README.md) ·
[Comparison with Atari800](../build/v361-party-opening-comparison.png)

## AVG releases

Both files are 945 929 B each and pass through the hardware loader of releases
based on 058. The v361 prototype occupies 64 banks and uses 298 shared
rows (11 527 B). The main code is 2 542 B.

- [079 mono, one POKEY](../releases/less-i-know-demo-release-079-mono.xex)
  · SHA-256 `69c4a9a7a4ef114bec788527d8a406003834052d46548af417ea909b99e4911d`
- [078 stereo](../releases/less-i-know-demo-release-078-stereo.xex)
  · SHA-256 `d947ca8088af51ab5f6589eb712233a92386ba300757d8fe0057b798ea17d270`

## Verification

21 tests of graphics, scene transitions, the loader and the director after Trevor passed.
Replay of all 64 banks and the final bootstrap were checked. Atari800 PAL,
emulated 1088 XE and Altirra OS showed the same opening in both
releases. Frames taken later match 076 and 077 respectively.

In each release, 59 833 POKEY register updates were compared with the previous
mix. The data were identical, and four updates still fall on
each PAL frame on the final screen. The new files were checked in the emulator.
A trial on physical Atari and a full `make check` remain unperformed.
