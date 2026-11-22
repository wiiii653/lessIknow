# POKEY timbre audit — stereo 066 and mono 067

November 18, 2026. The user reported badly sounding instruments or patterns
on a real Atari. There is no recording, information about the selected file or
the exact configuration from that attempt. Below are the results of program
analysis, without attributing unmeasured symptoms to a specific Atari.

## Mono 067 mixing bug

The mixer at `$2C00` selects the louder side separately for channels 3 and 4 on
every update (about 5.014 ms). A comparison of 59,833 full updates confirmed
that the mono trace matches this algorithm. Cases were identified in which both
sources were active and their divisors and modes remained the same between two
updates. In those places only the side selection changed.

| Time from music start | Channel | Example |
| --- | --- | --- |
| 0:07.737–0:07.747 | 3, drums | Switching the right `$82` with divisor `$05` to the left `$C1` with divisor `$57`, even though both sources are still playing. Recurs around 0:08.213 and 0:08.684. |
| 0:45.873 | 4, organ | The divisor changes from `$55` to `$AA` while the level changes from 5 to 6. That is a jump of almost an octave. |
| 0:47.121–0:47.136 | 4, organ and ornament | Back to the left, over to the right and back to the left within about 15 ms. |

Throughout the piece there are 807 such changes on channel 4 (579 organ/organ,
228 organ/ornament), all with a jump of at least five semitones. On channel 3
there are 126 changes during constant divisors of both sources, each changing
the generator mode. Most melody jumps occur in 7.5 s windows starting at
3:00, 3:07.5 and 4:07.5. This is a defect of voice reduction in 067, already
present in 065. When fixing it, base melody selection on attack and phrase
continuity, and drum selection on attack and hit priority. A change of the
envelope level alone should not switch the voice.

## Stereo 066

The entire active recording of 066 is byte-identical to the v035 arrangement
stream from the music repository. All updates are present, including on the
end card. The 067 mixing discrepancies do not occur in the trace of the two
POKEYs of 066.

- **Stereo XEX run with one POKEY.** Atari800 with the `STEREO_POKEY` option
  disabled confirmed 59,833 updates in which the second series of writes
  overwrites the first. The left drums are active from the start, and the right
  ones begin only at 0:07.737. Under stock address decoding this explains the
  missing drums at the opening when the stereo version is run on a single chip.
- **On two POKEYs.** From the very start the bass is detuned between the sides
  by about five cents. When the outputs are summed it may pulse. The sum of the
  requested levels on the left chip reaches 30 in 34 updates. The first case at
  0:45.477 combines level 10 of bass, 13 of drums and 7 of organ. Previously the
  maximum was 26. The sum of levels is an upper bound on the instantaneous
  signal, not a measurement of clipping. Analog non-linearity is possible,
  especially with voice accumulation, but does not by itself explain the whole
  opening.

## Basis

Atari800 PAL, 1088 XE, Altirra OS, emulator with single-write POKEY logging.
`066-full` for two chips, `067-full` and `066-one-pokey` for one.
Times from the package index and a rate of 199,443 updates/s.
Role sources `voice-roles.bin` and state sources `registers.bin` from the v035 archive.
For analog interpretation: [Altirra Hardware Reference, Appendix E](https://www.virtualdub.org/downloads/Altirra%20Hardware%20Reference%20Manual.pdf).
No listening session or measurement on a physical Atari was performed.
