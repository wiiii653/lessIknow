# 9. Odtwarzanie, testy i checklista

## 9.1. Środowisko

`[ODCZYT]` Testy wymagają `py65`; nie ma go w systemowym Pythonie.
Sprawdzone środowisko:

```sh
python3 -m venv /tmp/opencode/tliktb-venv
/tmp/opencode/tliktb-venv/bin/pip install -r requirements-dev.txt
```

`[ODCZYT]` Pełny zestaw po ostatnich zmianach: **200/200** (~146 s).

## 9.2. Build roboczy

```sh
make all PYTHON=/tmp/opencode/tliktb-venv/bin/python
# lub bezpośrednio:
PYTHONPATH=tools /tmp/opencode/tliktb-venv/bin/python tools/build_bitmap_sequence.py --replace
```

`[ODCZYT]` Wynik: `build/visual-prototype-dev.xex` + `.json`,
~1 111 730 B, 298 współdzielonych wierszy, 2560 B kodu.

## 9.3. Testy

```sh
make check PYTHON=/tmp/opencode/tliktb-venv/bin/python
```

`[ODCZYT]` Testy istotne dla loadera:

| Test | Co sprawdza |
| --- | --- |
| `tests/test_loading_screen.py` | kolejność segmentów ekranu, tekst, rejestry, `$20F1` = NOP |
| `tests/test_sequence.py` | loader OS-RAM, wektor startowy, banki |
| `tests/test_engine_cache.py` | zawartość banków 24–39 i 08C3+ |
| `tests/test_mosaic.py` | `bank_value(18)` i mapowanie banków |
| `tests/test_banana_cache.py` | brak kolizji z bitmapami i PMG |

## 9.4. Weryfikacja struktury XEX

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

Oczekiwane dla release 018:

```
rozmiar 935472
segmentów 1775
INIT {'0x38a0': 1, '0x3900': 66, '0x3a00': 64, '0x4800': 1}
RUN ['0x13e0']
```

## 9.5. Odtworzenie pełnego łańcucha

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

`[OGRANICZENIE]` Odtworzenie bajt w bajt wymaga **tej samej** wersji bazy
(build/visual-prototype-dev.xex) i tych samych assetów. Po zmianach
w `tools/` hash wyjścia się zmieni.

## 9.6. Checklista przed nowym wydaniem

1. `make check` — wszystkie testy przechodzą.
2. Struktura XEX: 64 bloki banków, INIT-y `$38A0`/`$3900`/`$3A00`/`$4800`.
3. Rozmiar < 1 MiB (obecnie 935 472 B).
4. Porównanie stereo POKEY w Atari800 1088XE z v035.
5. Test na fizycznym Atari: start, ekran ładowania, pierwsze sekundy.
6. Zapisanie SHA-256 i numeru release w `docs/PLAN_STATUS.md`.

`[OGRANICZENIE]` Punty 1–4 nie potwierdzają fizycznego AVG ani płynności.

## 9.7. Znane niedokończone sprawy

- `[ODCZYT]` `no_bank` w loaderze wideo nie pokazuje tekstu — tylko
  zmianę COLBK.
- `[ODCZYT]` Banki 0/1 są liczone bez weryfikacji unikalności.
- `[ODCZYT]` Kilka miejsc czyta `$D301` (PORTB) — działa na testowanym
  sprzęcie, ale nie jest przenośne na każdy klon.
- `[OGRANICZENIE]` Brak potwierdzenia pełnego przebiegu na fizycznym Atari
  po ostatnich zmianach graficznych (release 018).
- `[OGRANICZENIE]` Wariant mono nie został sprawdzony na sprzęcie.

## 9.8. Hashe referencyjne

| Plik | SHA-256 |
| --- | --- |
| `less-i-know-release-v035.xex` | `6d5d9cf3…fef0ff0` |
| `releases/less-i-know-demo-release-008.xex` | `fff207ea…5b8a6d836` |
| `releases/less-i-know-demo-release-011-avg-stereo.xex` | `4f8f14d6…e0df6d2289` |
| `releases/less-i-know-demo-release-018-stereo.xex` | `f9b5635d…ba1d8877ba5ad85` |
| `build/visual-prototype-dev.xex` | `c9a73fdf…948a3734022c` |

`[ODCZYT]` Hash release 018 dotyczy builda z 2026-11-12 02:03; późniejsze
zmiany w `tools/` (m.in. paleta ekranu ładowania) nie są w nim zawarte.
