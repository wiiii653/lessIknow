> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# 5. Compaction and late start from low memory

## 5.1. Problem

`[READ]` The 64-bank base has ~1 111 730 B (1.06 MiB). A large part of the data is
zeros: PNG/bitmaps and unused areas of the banks. Besides size, the problem
is low memory: runtime segments `$0400–$0BFF` are loaded during
loading and overwrite each other with the loader buffers.

## 5.2. Clearing the bank before loading (`$3A00`)

`[READ]` `tools/build_compact_xex.py`, `clear_code()`:

```
PHP / SEI / PHA / TXA / PHA / TYA / PHA
LDA #$80 / STA $3A14      ; self-modification: high byte of the STA address
LDA #0 / LDX #$40 / LDY #0
loop:  STA $8000,Y
       INY / BNE loop
       INC $3A14
       DEX / BNE loop
PLA / TAY / PLA / TAX / PLA / PLP / RTS
```

`[READ]` `INC $3A14` modifies the high byte of the `STA $8000,Y` operand;
after 64 pages the whole `$8000–$BFFF` is zeroed. The code preserves A/X/Y
and the flags, so it can be called as an INIT between segments.

`[CONCLUSION]` Thanks to the zeroing, only non-zero fragments of the
bank can be emitted — the rest is guaranteed zero.

## 5.3. Skipping runs of zeros

`[READ]` For each bank block the tool:

- skips the leading zeros,
- emits data up to the place where a run of ≥16 zeros begins,
- skips that run and resumes emission from the next non-zero byte,
- shorter runs (1–15 zeros) remain in the segment, because the header costs 4 B.

`[READ]` The assertion `count == 64` ensures that all banks have been processed.

`[READ]` Comparison after decomposition: the data of the 64 banks is identical byte
for byte with the original (confirmed in `docs/backup/V273_AVG_RAMBO_STARTUP.md`).

## 5.4. Low-memory buffer (`$4000–$47FF`)

`[READ]` `tools/build_avg_late_lowram.py`, constant `LOW`:

```
(0x0400,0x07e4) (0x0800,0x08bf) (0x0900,0x0974)
(0x0980,0x09ff) (0x0a00,0x0bff)
```

Segments that belong to these ranges and occur **after the last**
`$02E2` are:

1. cut from their current place in the file,
2. assembled into a 2 KiB buffer,
3. emitted as one segment `$4000–$47FF` before `$02E0`,
4. restored in the `$4800` bootstrap.

`[READ]` The buffer lies in the bank window `$4000–$7FFF`. This means that the data
will be written to the **currently selected** bank. The bootstrap reads from the
same mapping, so the pair "segment $4000 + INIT $4800" must occur without
a PORTB change between them.

`[ASSUMPTION]` The buffer occupies 2 KiB in one of the 1 MB banks. If it lands
in a bank used by the demo, it will overwrite its first 2 KiB. On the tested
hardware this does not cause a visible error; if the order of
segments changes, it requires checking.

## 5.5. `$4800` bootstrap

`[READ]` 116 bytes:

```
78              SEI
A9 00 8D 0E D4  NMI off
```

Then it copies pages from the buffer in sequence:

| Destination | Source | Bytes |
| --- | --- | ---: |
| `$0400` | `$4000` | 256 |
| `$0500` | `$4100` | 256 |
| `$0600` | `$4200` | 256 |
| `$0700` | `$4300` | 229 (`$07E4`) |
| `$0800` | `$4400` | 192 (`$08BF`) |
| `$0900` | `$4500` | 117 (`$0974`) |
| `$0980` | `$4580` | 128 (`$09FF`) |
| `$0A00` | `$4600` | 256 |
| `$0B00` | `$4700` | 256 |

At the end:

```
4C E0 13        JMP $13E0
```

`[CONCLUSION]` The bootstrap is the **last** INIT and never returns. From that
moment only runtime code runs.

## 5.6. Why this works

`[CONCLUSION]` Three things changed relative to older builds:

1. the file is smaller than 1 MiB (935 472 B instead of 1 111 730 B);
2. low memory is not overwritten during loading — it is restored
   at the end;
3. startup does not depend on RUNAD, only on `JMP $13E0` in the bootstrap.

`[LIMITATION]` It was not established which of these changes was a necessary
condition — all three were introduced together.

## 5.7. Pitfalls when modifying

- Do not add segments to `$0400–$0BFF` after the last `$02E2` without
  extending `LOW` and the bootstrap — they will be lost.
- Do not change PORTB between the `$4000–$47FF` segment and the `$4800` INIT.
- Do not increase the buffer above `$47FF` without checking what lies further.
- `clear_code` modifies its own operand at `$3A14` — do not move the code
  without updating that address.
