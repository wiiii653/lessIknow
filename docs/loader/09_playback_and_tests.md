# 9. Playback, tests and checklist

## 9.1. Environment

`[READ]` The tests require `py65`; it is not in the system Python.
Verified environment:

```sh
python3 -m venv /tmp/opencode/tliktb-venv
/tmp/opencode/tliktb-venv/bin/pip install -r requirements-dev.txt
```

`[READ]` Full suite after the latest changes: **200/200** (~146 s).

## 9.2. Working build

```sh
make all PYTHON=/tmp/opencode/tliktb-venv/bin/python
# or directly:
PYTHONPATH=tools /tmp/opencode/tliktb-venv/bin/python tools/build_bitmap_sequence.py --replace
```

`[READ]` Result: `build/visual-prototype-dev.xex` + `.json`,
~1,111,730 B, 298 shared rows, 2560 B of code.

## 9.3. Tests

```sh
make check PYTHON=/tmp/opencode/tliktb-venv/bin/python
```

`[READ]` Tests relevant to the loader:

| Test | What it checks |
| --- | --- |
| `tests/test_loading_screen.py` | order of the screen segments, text, registers, `$20F1` = NOP |
| `tests/test_sequence.py` | OS-RAM loader, start vector, banks |
| `tests/test_engine_cache.py` | contents of banks 24–39 and 08C3+ |
| `tests/test_mosaic.py` | `bank_value(18)` and bank mapping |
| `tests/test_banana_cache.py` | no collisions with bitmaps and PMG |

## 9.4. XEX structure verification

```sh
PYTHONPATH=tools python3 - <<'PY'
from pathlib import Path
from collections import Counter
from extract_music import segments

p = Path('releases/less-i-know-demo-release-018-stereo.xex')
ss = list(segments(p.read_bytes()))
inits = Counter(int.from_bytes(x, 'little')
                for a, b, x in ss if (a, b) == (0x02e2, 0x02e3))
run = [int.from_bytes(x, 'little')
       for a, b, x in ss if (a, b) == (0x02e0, 0x02e1)]
print('rozmiar', p.stat().st_size)
print('segmentów', len(ss))
print('INIT', {hex(k): v for k, v in sorted(inits.items())})
print('RUN', [hex(v) for v in run])
PY
```

Expected for release 018:

```
rozmiar 935472
segmentów 1775
INIT {'0x38a0': 1, '0x3900': 66, '0x3a00': 64, '0x4800': 1}
RUN ['0x13e0']
```

## 9.5. Reconstructing the full chain

```sh
PYTHONPATH=tools python3 tools/build_bitmap_sequence.py --replace
PYTHONPATH=tools python3 tools/build_init_trace_high.py
PYTHONPATH=tools python3 - <<'PY'
from pathlib import Path
from build_compact_xex import build as compact
src = Path('releases/avg-full-demo-init-trace-002.xex')
dst = Path('releases/avg-compact-001.xex')
dst.write_bytes(compact(src.read_bytes())); print(dst.stat().st_size)
PY
PYTHONPATH=tools python3 - <<'PY'
from pathlib import Path
from build_avg_late_lowram import build as late
src = Path('releases/avg-compact-001.xex')
dst = Path('releases/avg-compact-late-start-002.xex')
dst.write_bytes(late(src.read_bytes())); print(dst.stat().st_size)
PY
```

`[LIMITATION]` A byte-for-byte reconstruction requires the **same** version of the base
(build/visual-prototype-dev.xex) and the same assets. After changes
in `tools/` the output hash will change.

## 9.6. Checklist before a new release

1. `make check` — all tests pass.
2. XEX structure: 64 bank blocks, INITs `$38A0`/`$3900`/`$3A00`/`$4800`.
3. Size < 1 MiB (currently 935,472 B).
4. Stereo POKEY comparison in Atari800 1088XE with v035.
5. Physical Atari test: boot, loading screen, first seconds.
6. Saving the SHA-256 and release number in `docs/PLAN_STATUS.md`.

`[LIMITATION]` Items 1–4 do not confirm physical AVG or smoothness.

## 9.7. Known unfinished issues

- `[READ]` `no_bank` in the video loader does not show text — only
  a COLBK change.
- `[READ]` Banks 0/1 are counted without uniqueness verification.
- `[READ]` Several places read `$D301` (PORTB) — it works on the tested
  hardware, but is not portable to every clone.
- `[LIMITATION]` No confirmation of a full run on physical Atari
  after the latest graphics changes (release 018).
- `[LIMITATION]` The mono variant has not been checked on hardware.

## 9.8. Reference hashes

| File | SHA-256 |
| --- | --- |
| `less-i-know-release-v035.xex` | `6d5d9cf3…fef0ff0` |
| `releases/less-i-know-demo-release-008.xex` | `fff207ea…5b8a6d836` |
| `releases/less-i-know-demo-release-011-avg-stereo.xex` | `4f8f14d6…e0df6d2289` |
| `releases/less-i-know-demo-release-018-stereo.xex` | `f9b5635d…ba1d8877ba5ad85` |
| `build/visual-prototype-dev.xex` | `c9a73fdf…948a3734022c` |

`[READ]` The release 018 hash refers to the build from 2026-11-12 02:03; later
changes in `tools/` (including the loading-screen palette) are not included in it.
