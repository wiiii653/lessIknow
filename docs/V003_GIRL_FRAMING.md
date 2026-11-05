# Korekta pierwszego kadru dziewczyny — v003

Data: 2026-11-04. Wynik: `build/visual-prototype-v003.xex`.

- [ODCZYT] Pierwsze ustawienie sprite: `(0, 0, 96, 128)` w płótnie 160×64.
  Dolna krawędź pokazuje źródło do wiersza 31, czyli do pasa.
- [ODCZYT] NORTH: font 3×4, początek `(14, 15)` w źródle 48×64.
  Cały prostokąt napisu mieści się w oryginalnym turkusowym panelu kurtki.
- [ODCZYT] 18 testów zakończonych powodzeniem, w tym wykonanie callbacku 6502,
  kadrowanie, napis, oddalanie, pamięć pod ROM i oryginalne banki muzyki.
- [ODCZYT] Podgląd wykonany z listy obrazu nowego XEX-a:
  `build/v003-school-girl-waist.png`.

## V6 — regresja rytmu (bez zmiany odstępów DLI)

- [ODCZYT] Atari800, PAL, `-1088xe` (rozszerzenie 1088XE), stereo POKEY,
  Altirra OS, headless. Porównanie z oryginalnym v035: 10 478 232 identyczne
  bajty rejestrów stereo POKEY (~2918,8 s emulacji), obejmujące cały utwór.
  DLI pozostają w liniach 0, 78, 156, 234. Nie wykonano odsłuchu ani testu
  na fizycznym Atari. To test regresji, nie eksperyment ze zmianą odstępów V6.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v003.xex --seconds 15
```

## Zachowanie poprzednich plików

[ODCZYT] SHA-256 po zmianie zgodne z odczytem przed pracą:

- `build/visual-prototype.xex`: `41f1ef9bb4156d8466b32cce17f1d2ca132b3b443742654d16c841c0988802b9`
- `less-i-know-release-v035.xex`: `6d5d9cf3004f9003ede8d91aa4891a100f672c5a0e9429a6ecf20d1f5fef0ff0`

Nowy XEX: `04a398c7b38497055827f229a5fb0550d0bedde5be61c56319a3b1ba2351650e`.
Generator odmawia zapisu pod istniejącą nazwą XEX; kolejna wersja wymaga
nowej ścieżki przez `--output`. v002 to zachowany pośredni build korekty.
