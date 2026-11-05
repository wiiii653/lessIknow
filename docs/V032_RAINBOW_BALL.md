# v032 — tęczowa piłka i satelity

Piłka w tunelu ma dwie jaskrawe, kontrastujące połówki. Osiem zestawów
przechodzi przez róż, fiolet, błękit, turkus, zieleń, żółć, pomarańcz i czerwień.
Satelity mają trzeci, odmienny od obu połówek odcień. Luminancja piłki 14/12,
satelitów 14; szwy i obrys czarne. Kolory zmieniają się co 32 ticki playera.

Pociski są dwukrotnie szersze (SIZEM `$FF`) i mają wyraźniejsze ogonki.
Nadal cztery duszki piłki, cztery pociski i wspólny kolor satelitów w trybie
piątego gracza. Kod w banku 17 pod `$7800` zajmuje 1690 B, mieści się w
zarezerwowanych 2048 B. Nie dodano banków ani nie zmieniono granic scen.

## Walidacja V5–V7

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 48 testów PASS.
Test palet obejmuje wszystkie osiem zestawów, trzy odmienne odcienie,
minimalną luminancję 12, czarne szwy oraz szerokość pocisków. Pozostałe testy
sprawdzają maski, przejścia, cache i zachowanie banków podczas przerwań muzyki.

[ODCZYT] Atari800 PAL, `-1088xe`, stereo POKEY, Altirra OS:

```sh
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py \
  --demo build/visual-prototype-v032.xex --seconds 12
```

8 417 160 identycznych bajtów stereo POKEY, około 2344,7 s emulacji.
Cały utwór objęty porównaniem z oryginałem. Bez osobnego testu na sprzęcie.
Podgląd wykonuje kod 6502; kolory PAL są przybliżone.

- `build/visual-prototype-v032.xex`
- `build/v032-rainbow-ball.gif`
- `build/v032-rainbow-ball-sheet.png`

SHA256 v032: `43ce5f8cf4439c5f00d8c1907281d13b5d648cda6df56470dc154f973ac4791e`.
Zachowany v031: `db98f9398570e10238a6a411734d7cb1ac9b52fac9cfef3c4885954c7913ade8`.
