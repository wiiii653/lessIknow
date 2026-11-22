# 2. XEX format and program startup

## 2.1. What an XEX is

An XEX file (Atari DOS binary) is an `FF FF` header followed by a sequence of segments:

```
start_lo start_hi end_lo end_hi <data>
```

Meaning of the special addresses:

| Address | Meaning |
| --- | --- |
| `$02E0–$02E1` | RUNAD — program start address |
| `$02E2–$02E3` | INITAD — address of the procedure called **immediately** after this segment is loaded |

`[READ]` After loading all segments, the OS loader jumps to RUNAD.
The program may also never return from INIT, and then RUNAD does not matter.

## 2.2. Order in our file

`[READ]` Release 018 (1775 segments) has the following logical structure:

1. loading screen: `$3800` (text), `$3880` (DL), `$38A0` (INIT), `$02E2`;
2. original v035 segments: `$2000–$24B2` (player code), `$24BD–$28BC`
   (tables), `$3300`/`$3400` (DL and player screen);
3. 50× video bank loader: segment `$8000–$BFFF`, INIT `$1000`
   (packed at `$3900`), `$02E2`;
4. 64× bank clearing: INIT `$3A00` before the data of each bank;
5. runtime segments: `$1400–$1DFF`, `$0C00–$0F3F`, PMG, display lists,
   `$9000`/`$B000` (bitmaps) etc.;
6. low memory buffer `$4000–$47FF`;
7. bootstrap `$4800` + `$02E2=$4800`;
8. `$02E0=$13E0` (RUNAD, not used for startup in this variant).

`[READ]` Count of INITs in release 018:

| INIT | Count | Role |
| --- | ---: | --- |
| `$38A0` | 1 | loading screen |
| `$3900` | 66 | diagnostic wrapper for every INIT |
| `$3A00` | 64 | clearing `$8000–$BFFF` before a bank |
| `$4800` | 1 | bootstrap + direct start |

## 2.3. Why the start is "late"

`[READ]` The `$4800` bootstrap ends with a `JMP $13E0` instruction, not `RTS`.
This means the program **does not return** to the OS loader and does not wait for RUNAD.

`[READ]` `$13E0` is the startup stub (`tools/os_ram.py`, `run_stub()`):

```
78              SEI
A9 00 8D 0E D4  LDA #0 / STA $D40E   ; NMI off
AD 01 D3        LDA $D301             ; read PORTB
29 FE           AND #$FE              ; OS ROM off
8D 01 D3        STA $D301
4C 46 21        JMP $2146             ; player entry
```

`[CONCLUSION]` As a result, startup does not depend on whether the file loader
(AVG/DOS) executes RUNAD. This was one of the things changed relative to the
earlier, non-working builds.

`[LIMITATION]` The stub reads `$D301`. PORTB is a writable register;
on XL/XE a read usually returns the last written value, but this is not
guaranteed on every clone. It works on the tested hardware. If
random behavior appears, the first candidate for change is replacing
`LDA $D301 / AND #$FE` with a constant value.

## 2.4. OS copy under ROM

`[READ]` Before startup, INIT `$1000` (`tools/os_ram.py`, `loader()`) copies
a 14 KiB OS image into RAM under ROM:

- source regions: `$8000–$BFFF` (ROM image from the XEX),
- destinations: `$C000–$CFFF` and `$D800–$FFFF`,
- in the same step the music selector table `$26FC–$2709` is masked
  by `AND #$FE` (bit 0 cleared),
- the NMI vector `$FFFA` is set to `$2210` (original DLI handler),
- at the end PORTB and `$D400=$40` are restored.

`[CONCLUSION]` The runtime works with the **OS ROM disabled** and uses the copy
in RAM. That is why bank selectors written to the tables have bit 0 = 0.

## 2.5. What happens when the loader does not execute an INIT

`[READ]` If any INIT does not return (e.g. an error loop), the OS will never
reach the subsequent segments or RUNAD. Symptom: the screen frozen in its
last state, no further loading. That is why every error path in the
bank loader should be visible on screen — the current `no_bank`
does not do that (see [04_bank_switching.md](04_bank_switching.md)).

## 2.6. Difference from the 1.06 MiB version

| Feature | Old builds (008–011) | Current (012+) |
| --- | --- | --- |
| size | 1 111 730 B (1.06 MiB) | 935 472 B |
| start | RUNAD `$13E0` | `JMP $13E0` from the `$4800` bootstrap |
| low memory | loaded in segments along the way | buffered and copied at the end |
| bank data | full 16 KiB | only non-zero fragments, bank zeroed |

`[LIMITATION]` It was not established which of these changes was necessary on
the tested hardware — they were changed at the same time.
