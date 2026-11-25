> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# Assignment for Codex — independent verification of the v035 music banks

## Question

Does the player `less-i-know-release-v035.xex` need **7 or 8 music data banks**? Please verify independently the claim from the current audit that bank 8 is needed because it contains a read end marker. Do not base the answer solely on the assumption recorded for v024.

## Materials to check

- Player: `less-i-know-release-v035.xex`
- Extracted segments: `assets/music/v035/bank_01.bin` … `bank_14.bin`
- Manifest and hashes: `assets/music/v035/manifest.json`
- Extraction implementation: `tools/extract_music.py`
- Decoder trace: `tools/audit_music_banks.py`
- Previous result: `docs/MUSIC_BANK_AUDIT.md`
- Older assumptions and tasks V1–V7: `TLIKTB_Technical_Constraints.md`

SHA-256 of the XEX under study: `6d5d9cf3004f9003ede8d91aa4891a100f672c5a0e9429a6ecf20d1f5fef0ff0`.

## Claim to independently confirm or refute

The current audit claims that:

- the segments `$8000–$BFFF` contain 14 blocks of 16,384 B in load order;
- the decoder reads all of banks 1–7 and 2,820 B of bank 8;
- the last data byte different from `$FF` is at offset 2818 of bank 8, and the `$FF` at offset 2819 is the read end marker;
- banks 9–14 are not read, and their contents are `$FF`;
- therefore **7 banks are not enough; the minimum for the current v035 stream is 8**.

Please check in the XEX code and in the decoder path whether these numbers follow from actual reads, and not merely from block sizes or the number of segments. Also explain the difference between the number of banks loaded by the original XEX (14), the number of banks read by the decoder (allegedly 8) and the number of banks that can safely be removed or reused after player initialisation.

## Additional checkpoints

1. Confirm the bank indexing and the exact address/offset of each final read, in particular the `$FF` read at offset 2819 in bank 8. Does removing bank 8 or shortening its contents cause a missing end marker or a change in player behaviour?
2. Check whether the PORTB model in `tools/audit_music_banks.py` matches the memory detection path in v035. Point out any limitations of the simulation compared with a real Atari/Altirra.
3. Verify the number of updates until the end: the report gives 59,833, while the timeline calculates 59,840 (`160 × 374`). Determine whether the difference comes from initialisation/the end marker/the counting method, or is an unresolved discrepancy. Keep this question separate from the 7-vs-8 answer.
4. In the v035 used here there is no v024 file in the directory for comparison. If it cannot be confirmed where the older seven-bank assumption came from, state that explicitly — do not guess.

## Expected result

Add a short conclusion to this report: **7 or 8 banks for v035**, together with the justification, the exact range of reads, the verification limitations and a safe recommendation concerning shortening/reusing blocks. If the result of the current tool's audit is wrong, identify the specific error and how to reproduce the corrected result.

## Work constraints

- Read-only analysis. Do not modify the original XEX, banks, tools or demo builds.
- If a machine report or logs need to be written, direct them to `/tmp`, not to `build/` in the active project.
- Do not perform trimming or rebuild the player as part of this verification.

---

## Independent verification — result

**For the current v035 stream and its current decoder, 8 banks
of 16 KiB are needed.** Seven hold only 114,688 B, whereas the stream being read
has 117,508 B, including the required read in the eighth bank. This is not proof
that the music cannot fit in seven banks after a change of format or decoder.

[READ] The XEX SHA-256 matches the one given in the assignment. All 14 segments
`$8000–$BFFF` are byte for byte identical with the files `bank_01.bin`–`bank_14.bin`
and with the sums in the manifest. Banks 9–14 contain only `$FF`.

[READ] An independent py65 trace executed the initialisation routines `$232D`,
the preliminary decoding `$237D` and the original NMI path from `$2210` to setting
the `$24C8` flag. The reads were continuous, each of the following bytes was read
once:

| Load bank, numbered from 1 | Read in the CPU window `$4000–$7FFF` | Offsets | Bytes |
| --- | --- | --- | ---: |
| 1–7, each | `$4000–$7FFF` | 0–16383 | 16384 each |
| 8 | `$4000–$4B03` | 0–2819 | 2820 |
| 9–14 | none | none | 0 |

The last reads from bank 8: offsets 2813–2817 (`$4AFD–$4B01`) have the value
`$00` at update 59825; offset 2818 (`$4B02`) is `$86` at 59826;
offset 2819 (`$4B03`) is `$FF` at 59833. The fetch is performed by the
`LDA ($A0),Y` instruction at `$2353`. The command decoder at `$2A0C` compares the
result with `$FF` and jumps to `$2A5F`, where it sets the end flag. The cursor
address after this read is `$4B04`. The marker is therefore needed as a **byte
with the value** `$FF`; it does not have to be physically the same file byte, if
at the same logical place another valid loader provides `$FF`.

[READ] The original XEX was independently run in Atari800, PAL, `-1088xe`,
Altirra OS. After INIT the table `$26FC–$2709` was
`81 83 85 87 89 8B 8D 8F A1 A3 A5 A7 A9 AB`. When stopped at `$2A5F`
the accumulator contained `$FF`, the bank index `$24A5` was equal to 7 (counting
from zero), the cursor `$A0/$A1` pointed to `$4B04`, and the counter
`$24A7–$24A9` was 59833. The stop occurred before execution of the instruction
that sets the flag. This confirms the final path on a specific emulator
configuration; it is not a complete independent trace of all reads on real
hardware.

### Attempts to change data in the model — without modifying the XEX

[READ] After replacing only bank 8 in memory with all `$FF`, the end flag was set
after 58221 instead of 59833 updates — 1612 ticks earlier
(about 8.1 s at 199.44 Hz). In this variant the first `$FF` bytes in bank 8
were first used as packet data, and the end marker was recognised at
offset 3. This is not equivalent to any physical removal of the bank:
the actual contents of unallocated memory depend on the hardware and the loader.

[READ] After changing only byte 2819 from `$FF` to `$00`, while leaving the rest
of the `$FF` tail, the decoder also read offsets 2820–2822 and finished
after 59834 updates. So removing this specific marker changes the
path; in this attempt it does not cause a permanent absence of the end, because
later `$FF` bytes remain available. One must not assume that shortening the data
and leaving uninitialised memory will provide the correct byte at `$4B03`.

### Limitations and recommendation

[READ] The `audit_music_banks.py` model substitutes the first of the selector
tables and maps each of its values to a separate byte table. It does not execute
the bank detection routine or the copying INIT, and does not model PORTB aliases,
CPU/ANTIC, ROM, DMA, line timing or the actual POKEY registers. A write to
`$4000–$7FFF` in the model is not a write to a modelled bank. Therefore the model
alone proves the reads on the decoder path under an assumed correct map, not the
correctness of all expansion configurations. Atari800 confirmed that for the
configuration under study the player did in fact detect this first table and
reached the same end. The earlier experiment with `$55` on unread areas is
additional evidence for the emulator under study, not a guarantee for every
expansion.

[CONCLUSION] 14 is the number of originally loaded blocks; 8 is the number of
banks from which the decoder actually reads. After INIT finishes, all of banks
9–14 and the tail of bank 8 from offset 2820 can be devoted to other data,
provided the real banks are correctly identified and PORTB ownership is
protected. Banks 1–7 and the first 2820 bytes of bank 8 must not be overwritten
during playback. Removing six segments from the **original file** is a separate
loader/format modification and requires re-verification of INIT,
synchronisation, restart and complete playback — the mere absence of later reads
is not proof that any physical truncation of the XEX will work. This distinction
is also important for the current demo, which already uses the indicated unread
areas.

### 59833 vs 59840

[READ] The preliminary `$237D` call occurs before NMI counting. The adopted
model counted 59833 NMI calls up to the end flag and the player counter was also
59833; Atari800 on the original XEX confirmed 59833 on entry to the
end routine. The last `$86` command was read at 59826, and the final
`$FF` at 59833, seven updates later. This gap describes the end of the
stream, but by itself does not explain the difference from 59840; the rate and
PAL frequency calculation below explains it.

[READ] The timeline assumes 128 BPM, 160 bars of 4 beats and a duration of 300 s.
The player documentation gives 4 updates per PAL frame, i.e. 199.443 Hz.
The Altirra reference manual gives an ideal PAL clock of 49.86074 Hz; four
updates give 199.44296 Hz, which rounds to the player's figure.

[CONCLUSION] One bar lasts 1.875 s, so it corresponds to `199,44296 × 1,875 =
373,95555` updates, not exactly 374. For 160 bars this gives
`373,95555 × 160 = 59832,888`, i.e. 59833 whole ticks. The measured counter
59833 corresponds to 300.00056 s — practically exactly five minutes. The earlier
engine map multiplied the bar number by 374, e.g. 24 × 374 = 8976 and 160 × 374 =
59840. This accumulated an excess of 0.04445 tick per bar up to 7.112 ticks (35.7 ms).

[READ] The v051 engine used these approximate values in the scene and shot
thresholds. It is a bar-to-tick mapping error in the image engine, not a counter
error or a lack of player updates.

[READ] In v052 the shared function `tools/music_timing.py` determines the bar
threshold as `ceil(n × 373,95555)` from the start of the song. For example bar 24
begins at 8975, bar 88 at 32909, and bar 160 at 59833. The mosaic colour rhythm
uses alternating intervals of 186/187 ticks, not a constant 187. In v053 the same
map was extended to the internal Trevor shot threshold at bar 68.

[READ] This checkout does not contain the v024 XEX. The origin of the seven-bank
assumption therefore cannot be confirmed here; it should not be carried over to
v035.
