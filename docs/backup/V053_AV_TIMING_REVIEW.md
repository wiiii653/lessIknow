> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# Comparison of video synchronisation in v051 and v053

## Method

[READ] Both XEX releases were run in a separately compiled Atari800 7.2.1:
PAL, `-1088xe`, Altirra OS, stereo POKEY, without BASIC, with every frame
drawn. The instrumented emulator and traces were saved in `/tmp`; the XEX files
were not modified. The frame trace contains the music counter `$24A7–$24A9`,
the scene state `$83E0`, the display list pointer, the GTIA colours, four
POKEY registers and an FNV-1a hash of the previously rendered screen buffer. A
separate trace records the actual writes to GTIA, ANTIC and POKEY with a
counter, raster line and cycle position.

[READ] 14 958 frames were compared from the first non-zero counter to tick
59832. On corresponding frames the music counter, scene state and the four
sampled POKEY registers matched. The screen hash and the scene state describe
different moments: the hash refers to the previously rendered frame. A matching
`$83E0` state does not by itself prove that the new shot is already visible.

## Observed differences

[READ] In the first school and training scenes as well as in the girl's
portraits and the Trevor scene, the hashes of corresponding frames matched in
the examined run. Differences occurred in the dance (46 of 748 frames), the
first mosaic (333 of 748), the basketball (190 of 748) and the second mosaic
(3168 of 6731). The FNV hash is an indicator of differences, not an analysis of
their content nor proof of the absence of collisions.

[READ] First mosaic, GTIA write `$D016` of value `$8A`: v053 at tick 12552,
line 255; v051 at tick 12560, line 255. The difference is two PAL frames, about
40 ms. In both versions the POKEY AUDF1 write of value `$03` occurred at tick
12528, line 9. This is a reference point in the register stream; the AUDF write
alone does not prove that it is the audible start of the beat.

[READ] Second mosaic, GTIA write `$D016` of value `$AA`: v053 at tick 33112,
line 254; v051 at tick 33128, line 310. That is about four frames and 56 raster
lines of difference, about 84 ms. In both versions the AUDF1 write of value
`$FE` occurred at tick 33095, line 243. In v053 the GTIA change occurs before
the later AUDF1 write of `$43` at tick 33118, line 166; in v051 after it. It was
not determined which POKEY write corresponds to the perceived beat.

[CONCLUSION] The change in v053 shifts some actual visual accents more than
would follow from the 1–3 threshold ticks alone: the callback can work over
several frames and finish the update in a different blanking interval. This
explains the possibility of a perceptible difference relative to v051, but by
itself it does not indicate which version is better matched to the audible
musical attack.

## Limitations

- The register trace has the resolution of an emulator instruction and the
  raster, while the video trace is sampled once per frame. No analysis of the
  actual audio waveform and no A/B listening test were performed; the AUDF entry
  is a register change, not automatically a beat.
- The previous stereo POKEY comparison of v053 with v035 aligned the recordings
  at the first non-zero sample; it did not measure absolute A/V synchronisation.
- Atari800 and one memory expansion configuration were examined, not Altirra or
  hardware.
- Temporary traces: `/tmp/tliktb-v051-trace.csv`, `/tmp/tliktb-v053-trace.csv`,
  `/tmp/tliktb-v051-writes.csv`, `/tmp/tliktb-v053-writes.csv`. The instrumented
  code is located in `/tmp/atari800-7.2.1/src/` and is not part of the release.
