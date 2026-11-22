# 1. Build pipeline

Each stage is a separate tool in `tools/`. All of them write a new file in `xb`
mode (refusing to overwrite) — when rebuilding, delete the output file or
provide a different name.

## 1.1. Stages

| # | Tool | Input | Output | What it does |
| ---: | --- | --- | --- | --- |
| 1 | `tools/build_bitmap_sequence.py` | `less-i-know-release-v035.xex`, assets in `build/` and `assets/` | `build/visual-prototype-dev.xex` | full image: 64 banks, scene code, PMG, outro |
| 2 | `tools/build_init_trace_high.py` | release 009 (or another 64-bank one) | `releases/avg-full-demo-init-trace-002.xex` | moves the loading screen to `$3800` and wraps each INIT with a `$3900` wrapper |
| 3 | `tools/build_compact_xex.py` | result of stage 2 | intermediate file | 64× INIT `$3A00` clearing the bank + skipping long runs of zeros |
| 4 | `tools/build_avg_late_lowram.py` | result of stage 3 | release | defers low memory to `$4000–$47FF`, adds the `$4800` bootstrap |
| 5 | `tools/make_mono.py` | result of stage 4 (stereo) | mono variant | disables writes to the second POKEY |

`[READ]` Stages 2–4 have the input and output file names (`SOURCE`/`OUTPUT`)
**hard-coded** in the code. To build a different version, they must be changed
or the `build()` functions must be called from your own script.

## 1.2. Commands

```sh
# 1. full working build
PYTHONPATH=tools python3 tools/build_bitmap_sequence.py --replace

# 2. screen in high memory + INIT wrappers
PYTHONPATH=tools python3 tools/build_init_trace_high.py

# 3. compaction (zero-run + bank clearing)
PYTHONPATH=tools python3 - <<'PY'
from pathlib import Path
from build_compact_xex import build
src = Path('releases/avg-full-demo-init-trace-002.xex')
out = Path('releases/avg-compact-001.xex')
out.write_bytes(build(src.read_bytes()))
print(out.stat().st_size)
PY

# 4. late start from low memory
PYTHONPATH=tools python3 - <<'PY'
from pathlib import Path
from build_avg_late_lowram import build
src = Path('releases/avg-compact-001.xex')
out = Path('releases/avg-compact-late-start-001.xex')
out.write_bytes(build(src.read_bytes()))
print(out.stat().st_size)
PY

# 5. mono (optional)
PYTHONPATH=tools python3 tools/make_mono.py <stereo.xex> <mono.xex>
```

## 1.3. What exactly stage 2 changes

`[READ]` `tools/build_init_trace_high.py`:

- sets `ls.SCREEN, ls.DLIST, ls.ENTRY = $3800, $3880, $38A0`;
- removes the original screen segments `$0600`, `$0700`, `$0780` and their `$02E2`;
- inserts `ls.segments()` at the beginning of the file;
- replaces each INIT from `$02E2` with a `$3900` wrapper that prints
  `INIT nn ENTER $xxxx`, calls the real target and prints
  `INIT nn RETURN $xxxx`;
- NOPs `$20F1` (`STA $D400`) in the first player INIT so that DMA does not
  go dark while copying the music banks.

`[CONCLUSION]` This is a **diagnostic** stage: it shows the loading progress on
screen. It is not required for the demo to work — it can be skipped if you do
not want the INIT numbers on screen.

## 1.4. What stage 3 changes (compaction)

`[READ]` `tools/build_compact_xex.py`:

- for each of the 64 segments `$8000–$BFFF` inserts INIT `$3A00` and `$02E2=$3A00`;
- INIT `$3A00` zeroes all of `$8000–$BFFF` (64 pages of 256 B), preserving
  A/X/Y and the flags;
- only non-zero fragments are emitted from the bank block; a run of zeros of
  length ≥16 B is skipped (a segment header costs 4 B);
- the assertion requires exactly 64 bank blocks.

`[CONCLUSION]` After decomposition the bank data is identical byte for byte to
the original — this was confirmed by comparison (see
`docs/V273_AVG_RAMBO_STARTUP.md`).

## 1.5. What stage 4 changes (late start)

`[READ]` `tools/build_avg_late_lowram.py`:

- extracts from the file the low-memory segments occurring **after the last**
  `$02E2` and assembles them into a `$4000–$47FF` buffer;
- before `$02E0` it inserts the `$4000` segment (buffer), the `$4800` segment
  (bootstrap) and `$02E2=$4800`;
- the bootstrap copies the buffer to `$0400–$0BFF`, disables NMI and executes
  `JMP $13E0`.

Copy ranges (`LOW` in the tool):

| Target range | Bytes | Source in the buffer |
| --- | ---: | --- |
| `$0400–$07E4` | 997 | `$4000–$43E4` |
| `$0800–$08BF` | 192 | `$4400–$44BF` |
| `$0900–$0974` | 117 | `$4500–$4574` |
| `$0980–$09FF` | 128 | `$4580–$45FF` |
| `$0A00–$0BFF` | 512 | `$4600–$47FF` |

## 1.6. Verification after the build

```sh
PYTHONPATH=tools python3 - <<'PY'
from pathlib import Path
from collections import Counter
from extract_music import segments
p = Path('releases/less-i-know-demo-release-018-stereo.xex')
ss = list(segments(p.read_bytes()))
inits = Counter(int.from_bytes(x, 'little') for a, b, x in ss if (a, b) == (0x02e2, 0x02e3))
print('rozmiar', p.stat().st_size, 'segmentów', len(ss))
print({hex(k): v for k, v in sorted(inits.items())})
PY
```

Expected result for the current build:

```
rozmiar 935472 segmentów 1775
{'0x38a0': 1, '0x3900': 66, '0x3a00': 64, '0x4800': 1}
```

`[READ]` The absence of `$02E2=$1000` in the histogram does not mean the absence
of the OS-RAM loader — it is one of the 66 targets called by the `$3900`
wrapper.
