# 8. Loader diagnostics

The diagnostic files were created while determining why the full demo does not
start on a physical Atari with AVG. They all live in `releases/`.

## 8.1. File table

| File | Size | What it checks | Result on hardware |
| --- | ---: | --- | --- |
| `avg-early-screen-diagnostic-004.xex` | 1 106 B | screen, INIT, font ROM | **`EARLY SCREEN OK`** |
| `avg-bank-map-diagnostic-003.xex` | 485 B | 64 PORTB selectors, no RUNAD | **`BANK MAP PASSED`** |
| `avg-run-vector-diagnostic-001.xex` | 285 B | whether RUNAD works | `INIT OK` + `RUN OK` |
| `avg-first-bank-diagnostic-004.xex` | 2 664 B | first 14 selectors of v035 | incomplete (header only) |
| `avg-full-demo-init-trace-001.xex` | 1.1 MB | trace of all INITs | see `.stages.txt` |
| `avg-compact-late-start-001.xex` | 935 921 B | compact + late start | **it started** |
| `avg-final-segment-trace-001.xex` | 938 896 B | markers of the final segments | **it started** |
| `avg-bank-map-diagnostic-001/002` | 466/487 B | earlier versions of the bank test | they hung |
| `*.debug.xex` | various | preserved faulty variants | do not use |

## 8.2. What exactly each test proved

### Screen (004)

`[READ]` It displayed three lines of text. This confirmed that:

- INIT in the XEX is executed by the AVG loader,
- DMA and ANTIC mode 2 work,
- font ROM `$E000` is available.

`[READ]` It did not check banks — it contains no player.

### Bank map (003)

`[READ]` Everything in one INIT: display, 64× marker write,
64× read and comparison, result.

`[READ]` The result `BANK MAP PASSED` means that all 64 selectors
point to different banks. This refuted the hypothesis of a conflict of PORTB bits 1/4.

`[READ]` The earlier versions (001/002) did not work because:

- 001 ended INIT with a loop instead of `RTS` — the probe never started;
- 001/002 switched PORTB to `$00`, which disables the OS ROM without a copy under ROM
  and crashes the NMI;
- 001 relied on RUNAD.

### RUN vector (285 B)

`[READ]` INIT writes `INIT OK`, RUN writes `RUN OK - RUNAD WORKS`.
On hardware both lines appeared → RUNAD **is** supported.

`[CONCLUSION]` The lack of results in the earlier diagnostics was not RUNAD's fault.

### INIT trace

`[READ]` `avg-full-demo-init-trace-001.xex` instruments 66 INITs:
the wrapper prints the number, address and `ENTER`, calls the target, then `RETURN`.
Stage list: `avg-full-demo-init-trace-001.stages.txt`.

`[READ]` The wrapper preserves A/X/Y and the flags, and its code lies at `$3900`,
outside the runtime segments.

### Starting variants

`[READ]` `avg-compact-late-start-001.xex` and
`avg-final-segment-trace-001.xex` started on a physical Atari with AVG.
Both are < 1 MiB, with compact banks, a low memory buffer and `$4800`
bootstrap with `JMP $13E0`.

## 8.3. How to build the tests

```sh
# early screen
PYTHONPATH=tools python3 tools/build_early_screen_diagnostic.py

# map of 64 banks (no RUNAD, no $D301 read)
PYTHONPATH=tools python3 tools/build_bank_map_diagnostic.py

# RUN vector
PYTHONPATH=tools python3 tools/build_run_vector_diagnostic.py

# INIT trace
PYTHONPATH=tools python3 tools/build_init_trace_high.py

# compact + late start
PYTHONPATH=tools python3 tools/build_compact_xex.py <input> <output>
PYTHONPATH=tools python3 tools/build_avg_late_lowram.py <input> <output>
```

`[READ]` Some tools have hardcoded `SOURCE`/`OUTPUT` names; when
reusing them you must change them or call the `build()` function.

## 8.4. Rules for building new tests

1. **Do not read `$D301`** in startup code — PORTB is sometimes write-only.
2. **Do not write `$00` to PORTB** during the test — you will disable the OS ROM and NMI.
3. **Do not rely solely on RUNAD** — also test the path with INIT.
4. **Place code and screen outside the runtime segments** (`$3800–$3AFF`
   is free in the current build).
5. **Do not assume the error loop is visible** — add text.
6. **Every test should have an unambiguous result on screen**, e.g.
   `PASSED`/`FAILED`, not just a colour change.

## 8.5. Diagnostics limitations

- `[LIMITATION]` The tests use their own screen and their own INIT;
  success does not prove that the loader handles 64 banks in the full demo.
- `[LIMITATION]` py65 does not model DMA, VBI or physical PORTB.
- `[LIMITATION]` Atari800 `-1088xe` is not the same as the user's
  Rambo 1 MB clone.
