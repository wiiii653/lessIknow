# 1. Potok budowania

Każdy etap jest osobnym narzędziem w `tools/`. Wszystkie zapisują nowy plik
w trybie `xb` (odmowa nadpisania) — przy przebudowie usuń plik wyjściowy
albo podaj inną nazwę.

## 1.1. Etapy

| # | Narzędzie | Wejście | Wyjście | Co robi |
| ---: | --- | --- | --- | --- |
| 1 | `tools/build_bitmap_sequence.py` | `less-i-know-release-v035.xex`, asety w `build/` i `assets/` | `build/visual-prototype-dev.xex` | pełny obraz: 64 banki, kod scen, PMG, outro |
| 2 | `tools/build_init_trace_high.py` | release 009 (lub inny 64-bankowy) | `releases/avg-full-demo-init-trace-002.xex` | przenosi ekran ładowania do `$3800` i opakowuje każdy INIT wrapperem `$3900` |
| 3 | `tools/build_compact_xex.py` | wynik etapu 2 | plik pośredni | 64× INIT `$3A00` czyszczący bank + pomijanie długich ciągów zer |
| 4 | `tools/build_avg_late_lowram.py` | wynik etapu 3 | release | odkłada niską pamięć do `$4000–$47FF`, dodaje bootstrap `$4800` |
| 5 | `tools/make_mono.py` | wynik etapu 4 (stereo) | wariant mono | wyłącza zapisy do drugiego POKEY |

`[ODCZYT]` Etapy 2–4 mają w kodzie **zaszyte na stałe** nazwy plików
wejściowych i wyjściowych (`SOURCE`/`OUTPUT`). Aby zbudować inną wersję,
trzeba je zmienić lub wywołać funkcje `build()` z własnego skryptu.

## 1.2. Komendy

```sh
# 1. pełny build roboczy
PYTHONPATH=tools python3 tools/build_bitmap_sequence.py --replace

# 2. ekran w wysokiej pamięci + wrapper INIT-ów
PYTHONPATH=tools python3 tools/build_init_trace_high.py

# 3. kompaktowanie (zero-run + czyszczenie banku)
PYTHONPATH=tools python3 - <<'PY'
from pathlib import Path
from build_compact_xex import build
src = Path('releases/avg-full-demo-init-trace-002.xex')
out = Path('releases/avg-compact-001.xex')
out.write_bytes(build(src.read_bytes()))
print(out.stat().st_size)
PY

# 4. późny start z niskiej pamięci
PYTHONPATH=tools python3 - <<'PY'
from pathlib import Path
from build_avg_late_lowram import build
src = Path('releases/avg-compact-001.xex')
out = Path('releases/avg-compact-late-start-001.xex')
out.write_bytes(build(src.read_bytes()))
print(out.stat().st_size)
PY

# 5. mono (opcjonalnie)
PYTHONPATH=tools python3 tools/make_mono.py <stereo.xex> <mono.xex>
```

## 1.3. Co dokładnie zmienia etap 2

`[ODCZYT]` `tools/build_init_trace_high.py`:

- ustawia `ls.SCREEN, ls.DLIST, ls.ENTRY = $3800, $3880, $38A0`;
- usuwa oryginalne segmenty ekranu `$0600`, `$0700`, `$0780` i ich `$02E2`;
- wstawia `ls.segments()` na początku pliku;
- każdy INIT z `$02E2` zamienia na wrapper `$3900`, który wypisuje
  `INIT nn ENTER $xxxx`, wywołuje prawdziwy cel i wypisuje
  `INIT nn RETURN $xxxx`;
- NOP-uje `$20F1` (`STA $D400`) w pierwszym INIT playera, żeby DMA nie
  gasło podczas kopiowania banków muzyki.

`[WNIOSEK]` To etap **diagnostyczny**: pokazuje postęp ładowania na ekranie.
Nie jest wymagany do działania dema — można go pominąć, jeśli nie chcesz
numerów INIT na ekranie.

## 1.4. Co zmienia etap 3 (kompaktowanie)

`[ODCZYT]` `tools/build_compact_xex.py`:

- dla każdego z 64 segmentów `$8000–$BFFF` wstawia INIT `$3A00` i `$02E2=$3A00`;
- INIT `$3A00` zeruje całe `$8000–$BFFF` (64 strony po 256 B), zachowując
  A/X/Y i flagi;
- z bloku banku emitowane są tylko fragmenty niezerowe; ciąg zer długości
  ≥16 B jest pomijany (nagłówek segmentu kosztuje 4 B);
- asercja wymaga dokładnie 64 bloków banków.

`[WNIOSEK]` Dane banków po dekompozycji są identyczne bajt w bajt z
pierwowzorem — potwierdzono to porównaniem (patrz `docs/V273_START_AVG_RAMBO.md`).

## 1.5. Co zmienia etap 4 (późny start)

`[ODCZYT]` `tools/build_avg_late_lowram.py`:

- wyciąga z pliku segmenty niskiej pamięci występujące **po ostatnim**
  `$02E2` i składa je w bufor `$4000–$47FF`;
- przed `$02E0` wstawia segment `$4000` (bufor), segment `$4800`
  (bootstrap) i `$02E2=$4800`;
- bootstrap kopiuje bufor do `$0400–$0BFF`, wyłącza NMI i wykonuje
  `JMP $13E0`.

Zakresy kopiowania (`LOW` w narzędziu):

| Zakres docelowy | Bajty | Źródło w buforze |
| --- | ---: | --- |
| `$0400–$07E4` | 997 | `$4000–$43E4` |
| `$0800–$08BF` | 192 | `$4400–$44BF` |
| `$0900–$0974` | 117 | `$4500–$4574` |
| `$0980–$09FF` | 128 | `$4580–$45FF` |
| `$0A00–$0BFF` | 512 | `$4600–$47FF` |

## 1.6. Weryfikacja po budowie

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

Oczekiwany wynik dla obecnego builda:

```
rozmiar 935472 segmentów 1775
{'0x38a0': 1, '0x3900': 66, '0x3a00': 64, '0x4800': 1}
```

`[ODCZYT]` Brak `$02E2=$1000` w histogramie nie oznacza braku loadera OS-RAM —
jest on jednym z 66 celów wywoływanych przez wrapper `$3900`.
