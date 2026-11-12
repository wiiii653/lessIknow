# 8. Diagnostyka loadera

Pliki diagnostyczne powstały podczas ustalania, dlaczego pełne demo nie
startuje na fizycznym Atari z AVG. Wszystkie leżą w `releases/`.

## 8.1. Tabela plików

| Plik | Rozmiar | Co sprawdza | Wynik na sprzęcie |
| --- | ---: | --- | --- |
| `avg-early-screen-diagnostic-004.xex` | 1 106 B | ekran, INIT, font ROM | **`EARLY SCREEN OK`** |
| `avg-bank-map-diagnostic-003.xex` | 485 B | 64 selektory PORTB, bez RUNAD | **`BANK MAP PASSED`** |
| `avg-run-vector-diagnostic-001.xex` | 285 B | czy działa RUNAD | `INIT OK` + `RUN OK` |
| `avg-first-bank-diagnostic-004.xex` | 2 664 B | pierwsze 14 selektorów v035 | niepełny (tylko nagłówek) |
| `avg-full-demo-init-trace-001.xex` | 1.1 MB | ślad wszystkich INIT-ów | patrz `.stages.txt` |
| `avg-compact-late-start-001.xex` | 935 921 B | kompakt + późny start | **wystartował** |
| `avg-final-segment-trace-001.xex` | 938 896 B | znaczniki końcowych segmentów | **wystartował** |
| `avg-bank-map-diagnostic-001/002` | 466/487 B | wcześniejsze wersje testu banków | zawieszały się |
| `*.debug.xex` | różne | zachowane wadliwe warianty | nie używać |

## 8.2. Co dokładnie dowiódł każdy test

### Ekran (004)

`[ODCZYT]` Wyświetlił trzy wiersze tekstu. To potwierdziło, że:

- INIT w XEX jest wykonywany przez loader AVG,
- DMA i ANTIC tryb 2 działają,
- font ROM `$E000` jest dostępny.

`[ODCZYT]` Nie sprawdzał banków — nie zawiera playera.

### Mapa banków (003)

`[ODCZYT]` Wszystko w jednym INIT: wyświetlenie, 64× zapis znacznika,
64× odczyt i porównanie, wynik.

`[ODCZYT]` Wynik `BANK MAP PASSED` oznacza, że wszystkie 64 selektory
wskazują różne banki. To obaliło hipotezę o konflikcie bitów 1/4 PORTB.

`[ODCZYT]` Wcześniejsze wersje (001/002) nie działały, bo:

- 001 kończył INIT pętlą zamiast `RTS` — probe nigdy nie ruszał;
- 001/002 przełączały PORTB na `$00`, co wyłącza ROM OS bez kopii pod ROM
  i wywala NMI;
- 001 polegał na RUNAD.

### Wektor RUN (285 B)

`[ODCZYT]` INIT pisze `INIT OK`, RUN pisze `RUN OK - RUNAD WORKS`.
Na sprzęcie pojawiły się oba wiersze → RUNAD **jest** obsługiwany.

`[WNIOSEK]` Brak wyników wcześniejszych diagnostyk nie był winą RUNAD.

### Ślad INIT-ów

`[ODCZYT]` `avg-full-demo-init-trace-001.xex` instrumentuje 66 INIT-ów:
wrapper wypisuje numer, adres i `ENTER`, wywołuje cel, potem `RETURN`.
Lista etapów: `avg-full-demo-init-trace-001.stages.txt`.

`[ODCZYT]` Wrapper zachowuje A/X/Y i flagi, a jego kod leży w `$3900`,
poza segmentami runtime.

### Warianty startujące

`[ODCZYT]` `avg-compact-late-start-001.xex` i
`avg-final-segment-trace-001.xex` wystartowały na fizycznym Atari z AVG.
Oba mają < 1 MiB, kompaktowe banki, bufor niskiej pamięci i bootstrap
`$4800` z `JMP $13E0`.

## 8.3. Jak zbudować testy

```sh
# ekran wczesny
PYTHONPATH=tools python3 tools/build_early_screen_diagnostic.py

# mapa 64 banków (bez RUNAD, bez odczytu $D301)
PYTHONPATH=tools python3 tools/build_bank_map_diagnostic.py

# wektor RUN
PYTHONPATH=tools python3 tools/build_run_vector_diagnostic.py

# ślad INIT-ów
PYTHONPATH=tools python3 tools/build_init_trace_high.py

# kompakt + późny start
PYTHONPATH=tools python3 tools/build_compact_xex.py <wejście> <wyjście>
PYTHONPATH=tools python3 tools/build_avg_late_lowram.py <wejście> <wyjście>
```

`[ODCZYT]` Część narzędzi ma zaszyte nazwy `SOURCE`/`OUTPUT`; przy
ponownym użyciu trzeba je zmienić albo wywołać funkcję `build()`.

## 8.4. Zasady budowania nowych testów

1. **Nie czytaj `$D301`** w kodzie startowym — PORTB bywa write-only.
2. **Nie pisz `$00` do PORTB** podczas testu — wyłączysz ROM OS i NMI.
3. **Nie polegaj wyłącznie na RUNAD** — testuj też ścieżkę z INIT.
4. **Umieszczaj kod i ekran poza segmentami runtime** (`$3800–$3AFF`
   jest wolne w obecnym buildzie).
5. **Nie zakładaj, że pętla błędu jest widoczna** — dodaj tekst.
6. **Każdy test powinien mieć jednoznaczny wynik na ekranie**, np.
   `PASSED`/`FAILED`, nie tylko zmianę koloru.

## 8.5. Ograniczenia diagnostyki

- `[OGRANICZENIE]` Testy używają własnego ekranu i własnego INIT-a;
  sukces nie dowodzi, że loader radzi sobie z 64 bankami w pełnym demie.
- `[OGRANICZENIE]` py65 nie modeluje DMA, VBI ani fizycznego PORTB.
- `[OGRANICZENIE]` Atari800 `-1088xe` nie jest tym samym co klon
  Rambo 1 MB użytkownika.
