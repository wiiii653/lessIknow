# Report for Codex — starting the demo on Atari with 1 MB Rambo via AVG

Date: 2026-11-11. Author: OpenCode session. Scope: diagnosis of the failure to
start the full demo on the user's physical Atari. **The production timeline,
music and bank allocation were not changed.**

Legend: `[READ]` — a verified fact; `[CONCLUSION]` — a conclusion from the
evidence; `[ASSUMPTION]` — a hypothesis to be checked. `[LIMITATION]` — what
must not be treated as confirmation.

---

## 1. User environment

- Physical Atari XL/XE with a clone of the **Rambo 1 MB** expansion (information
  from the user).
- XEX files are launched from **AVG** (cartridge loader; exact model and
  firmware unknown).
- The same hardware setup correctly runs:
  - `less-i-know-release-v035.xex` (original player with music),
  - Starfish remixes (player + music),
  - another 1 MB demo that detects banks by itself and loads 53 banks.
- The full demo (`releases/less-i-know-demo-release-008.xex` = v261 and
  candidates 009/010/011) **does not start**; symptom: no image / no loading
  message.

`[READ]` SHA-256 of `less-i-know-release-v035.xex`:
`6d5d9cf3004f9003ede8d91aa4891a100f672c5a0e9429a6ecf20d1f5fef0ff0`
(234 348 B).

---

## 2. Facts confirmed in the code and XEX files

### 2.1. Fixed early-screen bug (CHBASE)

`[READ]` `tools/loading_screen.py` set `$D018=$00`. ANTIC then pointed
CHBASE at page `$0000` instead of the font ROM at `$E000`, so all
characters were blank → a black screen with no text.

`[READ]` After the fix to `$D018=$E0`, the rebuilt
`build/visual-prototype-dev.xex` differs from the previous one by **a single
byte** (offset `$0D71`: `$00` → `$E0`). Full test suite: **200/200**.

`[READ]` The same bug was present in `releases/avg-first-bank-diagnostic-001.xex`
and in the first versions of the diagnostics. **The black screen in those files
was not the result of the bank test.**

### 2.2. The early screen works on hardware

`[READ user]` `releases/avg-early-screen-diagnostic-004.xex`
(1106 B) displayed `EARLY SCREEN OK` / `AVG / XEX INIT + ROM FONT` on the Atari.
Conclusion: the early INIT in the XEX, DMA, the font ROM and ANTIC mode 2 work
in the AVG environment.

### 2.3. INIT works, RUN (`$02E0`) does not

`[READ user]` `releases/avg-first-bank-diagnostic-004.xex` showed
only the header `ORIGINAL V035 BANK PROBE`, without a result line. The same
symptom occurred with `avg-bank-map-diagnostic-001.xex`: INIT displayed
`PROBING...`, but the result never appeared.

`[CONCLUSION]` Code executed through INIT works; code under the RUN vector
`$02E0` **did not execute or crashed** in those two builds.

`[READ]` In the original `v035`, the RUN vector `$13E0` is used and the player
works. `[CONCLUSION]` The AVG loader handles RUNAD at least for that file,
so the mechanism itself cannot be ruled out — but there is no direct
evidence that our RUN `$13E0` was fully executed.

### 2.4. The first diagnostic 004 was not reliable

`[READ]` `avg-first-bank-diagnostic-004.xex` (2664 B) contains only two
player segments: `$2000–$24B2` and `$24BD–$28BC`. It **does not contain** the
`$3300`/`$3400` segments or the music banks (`$8000–$BFFF`). The original
detection of 14 selectors reads data from `$26FC`, `$270A`, `$2734`, `$2737`
and writes to `$4000` in the bank window — without the full context, the
result is not meaningful.

### 2.5. The selector list of our loader is consistent with this hardware's map

`[READ]` `tools/school_portrait_bank.py` generates 64 candidates:

```
81 83 85 87 89 8B 8D 8F A1 A3 A5 A7 A9 AB AD AF
C1 C3 C5 C7 C9 CB CD CF E1 E3 E5 E7 E9 EB ED EF
01 03 05 07 09 0B 0D 0F 21 23 25 27 29 2B 2D 2F
41 43 45 47 49 4B 4D 4F 61 63 65 67 69 6B 6D 6F
```

Bits: **0 = always 1, 4 = always 0**, variable **1, 2, 3, 5, 6, 7**
(6 bits = 64 banks).

`[READ]` An independent analysis of another 1 MB demo that works on the same
Atari and loads 53 banks shows the following method of deriving
selectors: the base is computed as a rotation of the index number (`LSR` + three `ROR` +
`ADC #1`), then four variants per base via `EOR #$04` / `EOR #$0C`
with `AND #$FE`, and when switching banks `ORA #$01`.

`[CONCLUSION]` After accounting for `|1`, the set derived by this method is
**identical** to the 64 values of our loader. The same combination of bits
(1, 2, 3, 5, 6, 7) is therefore sufficient on this hardware to address at
least 53 banks. Our candidate list is thus not a unique bug in the
demo.

`[LIMITATION]` This does not prove that all 64 values are unique on
this machine — only that at least 53 of them work. The missing number
is resolved by `avg-bank-map-diagnostic-003.xex`.

### 2.6. Video loader mechanism

`[READ]` `tools/school_portrait_bank.py`, function `loader(frame, index)`:

- `index < 2`: selector computed arithmetically (`$2709 + 2` or `+ 4`),
  **without uniqueness verification**; write to `$24B3+index`.
- `2 <= index < 50`: loop over 64 candidates, uniqueness test by
  writing `$55`/`$AA` to `$4000` and comparing with known banks; the result
  is written to `$08C0+index` after `AND #$FE`.
- No bank: `no_bank` — `LDA #$32 / STA $D01A` and a **loop with no text**.

`[READ]` The demo XEX (release 009/011) loads 64 segments `$8000–$BFFF`
and executes 67–68 INITs; RUN = `$13E0`.

`[READ]` Startup stub `tools/os_ram.py`, function `run_stub()`:

```
78 A9 00 8D 0E D4 AD 01 D3 29 FE 8D 01 D3 4C 46 21
SEI / LDA #0 / STA $D40E / LDA $D301 / AND #$FE / STA $D301 / JMP $2146
```

`[ASSUMPTION]` This is a read-modify-write on `$D301`. On XL/XE, PORTB is a
PIA port and usually can be read, but that is not guaranteed on all
clones; if the read returns garbage, the `$4000–$7FFF` window will be switched
to the wrong bank and the player will crash despite a correct image.

`[READ]` A similar pattern `LDA $D301 / PHA … PLA / STA $D301` is
in `school_portrait_bank.loader`, `banana_cache`, `build_bitmap_sequence`
(`banked_effects`, `ribbon_copy`, `final_boy`).

### 2.7. PORTB bit conflict between expansions

`[READ]` Standard 130XE: bit 0 = OS ROM, bit 1 = BASIC, bits 2–3 = CPU
bank, bits 4–5 = ANTIC bank. 1 MB clones (Rambo, Newell, Compy-Shop, Ultimate
1 MB) assign the bits **differently**; U1MB additionally has registers `$D380–$D3FF`.

`[CONCLUSION]` Our 64 selectors use bit 1 as a bank bit and do not use bit 4
at all. If on a given clone bit 1 controls BASIC rather than a bank,
then `$81` and `$83` point to the same bank and only 32 banks are available.
The loader then enters `no_bank` after exhausting the candidates and hangs —
which matches the reported symptom.

`[LIMITATION]` At least 53 banks from this bit set work on this
hardware, but it is unknown whether all 64 are unique — this variant requires
confirmation by test.

---

## 3. Bugs found in the diagnostic tools (fixed)

1. `loading_screen.py`: `$D018=$00` → `$E0` (blank screen). **Fixed.**
2. `avg-bank-map-diagnostic-001`: the INIT page ended with a `halt` loop
   instead of `RTS`, so the probe never started. **Fixed in 002/003.**
3. `avg-bank-map-diagnostic-001`: the loop switched `PORTB=$00`, which disables
   the OS ROM without a copy under ROM and crashes the NMI vector. **Fixed in 002/003.**
4. `avg-bank-map-diagnostic-003`: does not read `$D301`; at the end it writes a constant
   `$FF`. **This is the version to run.**

---

## 4. Diagnostic artifacts

| File | Size | SHA-256 | Purpose | Result on hardware |
| --- | ---: | --- | --- | --- |
| `releases/avg-early-screen-diagnostic-004.xex` | 1 106 B | `49992187…e4a6ce4` | screen + INIT + font ROM only | **OK**: `EARLY SCREEN OK` |
| `releases/avg-first-bank-diagnostic-001.xex` | 3 589 B | `2f1a7d66…4b3fa92e2f` | first attempt at 14 banks (old, faulty CHBASE) | black screen |
| `releases/avg-first-bank-diagnostic-004.xex` | 2 664 B | `92185952…ac8a2169d160` | header + PASS/FAIL after the test | **header only** |
| `releases/avg-bank-map-diagnostic-001.xex` | 466 B | `c1bc824b…40208e24` | 64 selectors, result via RUN | `PROBING…`, no result |
| `releases/avg-bank-map-diagnostic-002.xex` | 487 B | `dfb7c2a1…765a0ce8` | everything in INIT | not run |
| `releases/avg-bank-map-diagnostic-003.xex` | 485 B | `46b812e0…c885f2763320` | everything in INIT, no `$D301` read | **`BANK MAP PASSED`** |
| `releases/avg-run-vector-diagnostic-001.xex` | 285 B | `2f31a6fc…d101e6359` | INIT writes `INIT OK`, RUN writes `RUN OK` | **to be run** |

`[READ]` The `*.debug.xex` files are earlier, faulty variants kept
for history; they are not intended for hardware tests.

### 4.1. What exactly `avg-bank-map-diagnostic-003.xex` does

`[READ]` 11 segments, all below `$4000`:

```
$2C00 DLIST (21 B)          $2C16 TITLE      $2C3E PROBING
$2C66 PASSED                $2C8E FAILED     $2CC0..$2D7F code (192 B)
$2E00 CANDIDATES (64 B)     $2E40 INDEX      $02E2 INIT = $2CC0
$02E0 RUN = $2CC0 (safe halt loop)
```

Algorithm: for each of the 64 candidates, select the bank and write a
unique marker (`index+1`) to `$4000`; in a second pass, read the marker through
the same candidate and compare. A mismatch = two selectors point to the same
bank → `BANK MAP FAILED`. Bit 0 of PORTB remains set (OS ROM visible,
VBI alive), and at the end `$FF` is written.

`[READ]` py65 simulation: a distinct map → `BANK MAP PASSED`; deliberate
aliasing of `$A5`→the same as `$A7` → `BANK MAP FAILED`.

---

## 5. Open hypotheses, in order of probability

**H1. The Rambo 1 MB clone has a different PORTB bit semantics.**
`[READ]` **A HARDWARE TEST DISPROVED THIS HYPOTHESIS.** `avg-bank-map-diagnostic-003.xex`
showed `BANK MAP PASSED`, i.e. all 64 selectors point to different banks.
The bit map 1, 2, 3, 5, 6, 7 is correct on this clone, and bit 4 can remain
zero. There is no conflict here with BASIC or with the Self-Test.

**H2. Reading `$D301` (write-only) in `run_stub()` and in the loaders.** If the
read returns garbage, `AND #$FE` and the write switch the bank window to the wrong bank,
despite correct earlier loading.
Resolution: replace the read-modify-write with a constant write; check on
hardware.

**H3. Copying 16 KiB with BASIC/ROM enabled.** The source `$8000–$BFFF`
may read the BASIC ROM if a given selector sets bit 1. Effect:
corrupted frames, not necessarily a hang.
Resolution: compare 16 KiB after copying (checksum on screen).

**H4. RUN vector unsupported or interrupted by the AVG loader.**
The RUNAD mechanism works for the original player, but there is no proof that our
`$13E0` executes in full; two diagnostic tests stopped at
the state left by INIT.
Resolution: a build that does everything in INIT (already exists: 003).

**H5. Banks 0/1 computed without verification** (`$2709 + 2` / `+4`). If the
first selector is not `$81` (a different clone), the arithmetic lands in the wrong bank.
Resolution: add verification as for the other indices.

---

## 6. Plan for Codex (order of execution)

1. `[READ]` `avg-bank-map-diagnostic-003.xex` → **`BANK MAP PASSED`**.
   64 selectors are distinguishable; the bit map is correct. Hypothesis H1
   is disproved; do not change the candidate list "blindly".
2. Run `avg-run-vector-diagnostic-001.xex` (285 B): INIT writes
   `INIT OK` on line 0, RUN writes `RUN OK - RUNAD WORKS` on line 2.
   - only `INIT OK` → this loader does not execute RUNAD for our XEX;
     the demo must start from the last INIT, not from `$02E0`.
   - both lines → RUNAD works and the problem is in the loader/copying.
3. If RUNAD works, check the 16 KiB copy (checksum after
   copying) and `run_stub()` reading `$D301`.
4. After every change: `make check` (200 tests) and a comparison of stereo POKEY
   in Atari800 1088XE as a regression — **remembering that 1088XE is not the
   same as Rambo 1 MB**.
5. Do not announce compo readiness without a test on a physical Atari.

---

## 7. Reproduction and commands

```sh
# Test dependencies (py65 is not in the system Python)
python3 -m venv /tmp/opencode/tliktb-venv
/tmp/opencode/tliktb-venv/bin/pip install -r requirements-dev.txt

# Full test suite
PYTHONPATH=tests:tools /tmp/opencode/tliktb-venv/bin/python \
  -m unittest discover -s tests

# Rebuild the working build
PYTHONPATH=tools /tmp/opencode/tliktb-venv/bin/python \
  tools/build_bitmap_sequence.py --replace

# Recreate the diagnostics
PYTHONPATH=tools python3 tools/build_early_screen_diagnostic.py
PYTHONPATH=tools python3 tools/build_first_bank_diagnostic_002.py
PYTHONPATH=tools python3 tools/build_bank_map_diagnostic.py
PYTHONPATH=tools python3 tools/build_avg_candidate.py \
  releases/less-i-know-demo-release-009-stereo.xex \
  releases/less-i-know-demo-release-011-avg-stereo.xex

# Preview the XEX segment map
python3 -c "from pathlib import Path; from tools.extract_music import segments; \
[print(i, hex(a), hex(b), len(x)) for i,(a,b,x) in \
 enumerate(segments(Path('releases/avg-bank-map-diagnostic-003.xex').read_bytes()))]"
```

`[READ]` The builders save new files in `xb` mode (refusing to overwrite).
To rebuild, you must first delete the file or change the output name.

---

## 8. Repository state (relevant files)

Changed or added in this session:

- `tools/loading_screen.py` — **`$D018=$E0`** (CHBASE fix).
- `tools/build_early_screen_diagnostic.py` → `avg-early-screen-diagnostic-004.xex`.
- `tools/build_first_bank_diagnostic_002.py` → `avg-first-bank-diagnostic-004.xex`.
- `tools/build_bank_map_diagnostic.py` → `avg-bank-map-diagnostic-00{1,2,3}.xex`.
- `tools/build_avg_candidate.py` (earlier) → `less-i-know-demo-release-011-avg-stereo.xex`.
- `docs/V271_SCREEN_AND_DIAGNOSTICS.md` — change note.
- `docs/REPORT_FOR_CODEX_AVG_RAMBO_START.md` — this report.

Untracked and left unchanged: `releases/less-i-know-demo-release-009*`,
`010*`, `011*`, the `releases/less-i-know-sv2026we-v260-candidate/` directory and
older ZIPs. Release 008 (`fff207ea…`) is still the official v261.

`[READ]` `build/visual-prototype-dev.xex` after the fix:
SHA-256 `c9a73fdf68b86558b0c8d5204c79d612ab741ba5146958d16e4b948a3734022c`,
2 560 B of code, 298 shared rows.

---

## 9. What this report does not claim

- It does not confirm that the demo has been fixed.
- It does not confirm that the cause is banks, PORTB, RUNAD or the `$D301` read.
- It contains no test on a physical Atari performed in this session — all
  hardware results come from the user.
- Atari800 in the `-1088xe` configuration does not emulate the Rambo 1 MB clone.
- py65 tests do not model ANTIC DMA, VBI, line timing or the behaviour of
  write-only registers.
