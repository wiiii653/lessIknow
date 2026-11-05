# v024 — BASKETBALL HERO

[ODCZYT] Akt 3 zastępuje placeholder w tickach 20944–23935.
Kozłowanie trwa 20944–22439, wsad 22440–23935. Zmiany wcześniejszych
aktów i początek Trevora (23936) zachowują swoje ticki. Po 23936 nadal
działa kalejdoskop jako placeholder następnego aktu.

## Obraz

[ODCZYT] Sześć ilustracji: dwie pozy kozłowania i cztery fazy wsadu.
Europejski komiks, zawodnik w cyjanowym stroju z różowymi akcentami,
sala i niska kamera przy parkiecie. Ilustracje nie zawierają piłki.
Piłka 16×32 piksele logiczne składa się z czterech playerów z obracanymi
szwami i panelami. Cztery missiles rysują kolorowe krople.
Kozłowanie ma okres 187 ticków, wsad jedną sekwencję przez cały podakt.
Przy przejściu przez obręcz następuje krótki błysk koloru oświetlenia.

[ODCZYT] Materiał źródłowy:
`assets/art/source/act3_basketball_hero_v024.png`.
Konwersja do sześciu kadrów 160×56; wiersze są powtarzane do 192 linii.
Podglądy: `build/v024-dribble.gif`, `build/v024-dunk.gif`.

## V2 / V3 — pamięć

[ODCZYT] Bank 16 kontynuuje wykrytą tablicę PORTB: w testowanej konfiguracji
bank 15 to `$AC`, bank 16 `$AE`. Wartości runtime przechowywane pod
`$24B3` i `$24B4`. Nowy INIT zachowuje PORTB i wczytuje 16 KiB.
Kod w banku 16: `$4000–$4779` (1914 B); sześć obrazów po 2240 B:
`$4B80–$7FFF`. NMI zachowuje foreground bank także podczas wykonania
kodu w banku 16. Bufory i listy pozostają w niebankowanym RAM.

[ODCZYT] Przebudowa obrazu zachodzi przy zmianie pozy. Podtrzymanie
aktualizuje PMG, bez kopiowania całego kadru i przebudowy listy.
Wyjście z aktu i restart przywracają PMG sceny tanecznej.
Główny kod ma 1788 B, do `$1AFB`; przed `$1B00` zostają tylko 4 B.
Kolejne akty wymagają dalszego przenoszenia dispatchu do banków lub
przebudowy układu kodu. Nie zakładać, że kolejny bank można uzyskać
przez proste zwiększenie PORTB do `$B0`; dotychczas sprawdzono `$AC/$AE`.

## V1 / V6 — sprawdzenie

[ODCZYT] 39 testów OK: granice aktu, wszystkie sześć póz i ich piksele,
czas kozłowania, pojedynczy wsad, błysk, cache i odtworzenie PMG.
Pełna muzyka stereo POKEY zgodna z oryginałem: 8 767 152 identyczne
bajty, około 2442,2 s emulacji.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v024.xex --seconds 12
```

[ZAŁOŻENIE] Konfiguracja referencyjna to Atari800 PAL `-1088xe` ze stereo
POKEY. Fizyczny sprzęt i pozostałe tablice rozszerzeń wymagają kontroli.
GIF-y przybliżają kolory PAL i proporcje pikseli.

## Grafika — wbudowany image_gen

Użyto skilla imagegen i wbudowanego narzędzia. Finalny prompt:

```text
Production illustration-story asset for Atari audiovisual demo. SIX equal landscape panels, EXACT 2 columns by 3 rows, edge-to-edge panels without gutters, labels or writing. Same teenage male basketball player in all panels, dark short hair, CYAN basketball uniform with pink trim, peach skin. EUROPEAN bande dessinee comic, realistic natural facial proportions, small eyes, bold thick black outlines, broad clean flat shapes, NOT manga/anime. School gym interior with roof beams, tall windows, wallbars, wooden parquet. Four colors only black #000000 hotpink #ff32a0 cyan #00dcff peach #ffbe96. NO gradients. Reference supplies world/palette only, make face more European. IMPORTANT: NO BALL DRAWN ANYWHERE, ball will be hardware animated later. Leave space just below or above open hands for the ball. Each panel readable at160x64 logical pixels, composed like a cinematic 2.5:1 view. Row1 left and right: SAME FIXED very low court-side camera, full player at left/center with body bent toward dribble, hand extended on his RIGHT toward empty space at x60percent and y60percent. Left is downstroke with bent knees, right is recovery with slightly straighter knees and raised right hand. Player entire body, parquet foreground, hoop far upper right. Keep architecture identical between this pair. Row2 left: dunk approach, NEW fixed low camera, basket and backboard upper right, player center-left crouches for jump, empty hands at chest height. Row2 right: SAME camera and basket, player airborne mid jump, right arm extended diagonally high toward rim, knees bent behind him, no ball. Row3 left: SAME camera/basket, player at apex beside basket, right open hand immediately above rim upperright, ready to slam ball, left hand stretched back for balance. Row3 right: alternate follow-through dunk pose with one hand gripping rim and legs below. Realistic basketball anatomy and strong silhouettes. Gym lights visible as simple peach ceiling fixtures. Keep hoop in same location for last four panels. No text, no basketball in image, no decorative particles, no extra foreground players.
```

[ODCZYT] Dodatkowo w Atari800 sprawdzono 24 kolejne zrzuty pamięci:
wcześniejsze sceny, wejście w akt 3, kozłowanie i jego podtrzymanie,
cztery fazy wsadu, błysk, ostatni tick aktu, wyjście i restart.
Wszystkie porównywane rastry zgadzają się ze źródłem.
