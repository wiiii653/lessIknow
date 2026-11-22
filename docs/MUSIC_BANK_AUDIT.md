# v035 Music Bank Audit

Source: `less-i-know-release-v035.xex`. Banks are numbered from 1 and contain
16,384 bytes each.

| Banks | Bytes read by decoder | Unused bytes |
|---|---:|---:|
| 1–7 | 114,688 total | 0 |
| 8 | 2,820 | 13,564 |
| 9–14 | 0 | 98,304 |
| Total | **117,508** | **111,868** |

The loader reserves 229,376 B (224 KiB). The decoder reads 114.754 KiB and
does not read 109.246 KiB (48.77%). Six whole banks account for 96 KiB; another
13.246 KiB is at the end of bank 8.

## End-of-song marker

The final byte other than `$FF` is at offset 2818 in bank 8. The decoder reads
`$FF` at offset 2819 as its end marker. Only offsets 2820–16383 are unused.
Trimming every trailing `$FF` would remove the required marker.

## Method and limits

`tools/audit_music_banks.py --trace` executes the v035 restart, decoder and DLI
procedures in py65 with a modeled `$4000–$7FFF` bank window. It records bank
reads until the end flag at `$24C8`. The trace covered 59,833 updates; the last
read was in bank 8, and banks 9–14 were not read. This is a decoder audit, not
an ANTIC profiler or physical Atari measurement.

A probe XEX replaced bank 8 from offset 2820 and banks 9–14 with `$55`.
Atari800 PAL / emulated 1088 XE comparison found 2,941,200 identical stereo
POKEY register bytes (about 819 seconds, covering the whole song). Initial
silence was aligned once; samples were not shifted during playback.

The audit did not trim or modify the original XEX or the current production
build. Reproduce it with py65 from `requirements-dev.txt`:

```sh
python tools/audit_music_banks.py --trace --json build/music-bank-audit.json
```

Conclusion: v035 requires **eight** banks of music data, not seven. The older
seven-bank assumption from the v024 analysis does not apply to v035.
