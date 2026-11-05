# Sala gimnastyczna za cheerleaderkami — v006

Data: 2026-11-04. Plik: `build/visual-prototype-v006.xex`.

- [ODCZYT] Tło w czterech kolorach: wysokie okna, konstrukcja dachu,
  tablica do koszykówki z obręczą i siatką, granatowe ściany oraz parkiet
  z liniami boiska. Źródło geometrii: `tools/gym_background.py`.
- [ODCZYT] Zachowane wszystkie niezerowe piksele czterech póz i pojawianie
  się kolejnych tancerek przy oryginalnych tickach. Maski PMG mają kolor
  ściany i obejmują wyłącznie obszar tancerek; nie zasłaniają okien i parkietu.
- [ODCZYT] Podglądy z wykonania callbacku 6502 i odczytu list ANTIC:
  `build/v006-gym-solo.png`, `build/v006-gym-duo.png`, `build/v006-gym-trio.png`.
  Kolory RGB są przybliżeniem sprzętowej palety.
- [ODCZYT] 19 testów zaliczonych, w tym przejścia scen, pełne scanline'y,
  granice DMA, brak nakładania segmentów, NORTH i pamięć pod ROM.

## Pamięć i V2/V3 — kontrola dostępu playera

- [ODCZYT] 835 unikalnych wierszy, 31 173 B danych z wyrównaniem.
  Łączenie wierszy według wspólnych końcówek/początków jest bezstratne.
  Callback ma 1135 B; tablice wierszy mają 3264 B.
- [ODCZYT] Dodatkowo wykorzystano `$0600–$07FF`, `$08C0–$09FF`
  oraz `$1880–$18FF`. Tablicę dzielenia przez 2 zastępuje instrukcja LSR.
  Banki muzyki i okno `$4000–$7FFF` pozostają poza danymi obrazu.
- [ODCZYT] Oryginalny restart, dekoder i DLI wykonane w py65 przez
  59 833 aktualizacje do końca utworu z zakazem odczytów i zapisów
  w nowych regionach: brak dostępu do tych regionów.
  Mechanizm: `audit_music_banks.trace(..., protected_ranges=...)`.
  Nie jest to pełna weryfikacja wszystkich zachowań PORTB z V2.

## V6 — regresja odtwarzania

- [ODCZYT] Atari800, PAL, rozszerzenie `-1088xe`, Altirra OS,
  stereo POKEY, headless. DLI nadal w liniach 0, 78, 156, 234.
- [ODCZYT] Porównanie v006 z v035: **7 183 296 identycznych bajtów**
  rejestrów stereo POKEY, około 2001,0 s emulacji, cały utwór objęty testem.
  Początkową ciszę wyrównano raz. Nie wykonano odsłuchu ani testu
  na fizycznym Atari; nie zmieniano odstępów DLI w eksperymencie V6.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v006.xex --seconds 10
```

## Zachowane wersje

- [ODCZYT] v035, pierwotny prototyp i v003 zachowały poprzednie SHA-256.
- [ODCZYT] SHA-256 v006: `f261c0128dec5760c016c0fdd4553ebf3eb6701d11395fde3e03a224c9effbd5`.
- [ODCZYT] v004 i v005 są zachowanymi pośrednimi buildami tej zmiany.
