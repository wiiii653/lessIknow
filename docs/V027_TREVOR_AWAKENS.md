# v027 — TREVOR AWAKENS

[ODCZYT] Akt 4 obejmuje ticki 23936–32911. Część cicha: 23936–26927,
część energetyczna: 26928–32911. Początek następnego aktu pozostaje
przy 32912 i przechodzi do istniejącego kalejdoskopu.

## Realizacja

[ODCZYT] Dwa tła: nocna sala z drzwiami i neonowe geometryczne przejście.
Postać Trevora jest rysowana przez cztery playery. Dwanaście zestawów
PMG obejmuje trzy wielkości oraz cztery pozy/lustrzane warianty. W pierwszej
części rosną wielkość i jasność. Po uderzeniu muzyki wracają pełne kolory,
pulsujący zoom, ruch sinusoidalny i cztery krążące akcenty missiles.
Rotacja dotyczy akcentów orbitalnych, a postać zmienia i odbija pozy.

[ODCZYT] Tła i studia postaci wygenerowano wbudowanym image_gen:
`assets/art/source/act4_trevor_awakens_v025.png`.
Końcowa sylwetka PMG jest narysowana w kodzie na siatce 16×24, z większą
twarzą i barkami, żeby zachować czytelność przy ograniczeniu do 16 kolumn.
Zestawy są skalowane pionowo i używają sprzętowych szerokości playerów.
Podglądy: `build/v027-trevor-reveal.gif`, `build/v027-trevor-energy.gif`.

## V2 / V3 — bank 17

[ODCZYT] Nowy INIT sonduje 64 kandydatów PORTB, porównując każdy z
szesnastoma załadowanymi bankami. Używa znaczników `$55` i `$AA`, aby
odróżnić alias od przypadkowej wartości danych. Przy każdej próbie odtwarza
oryginalny bajt. Dopiero niezależny bank dostaje dane nowego aktu.
W Atari800 PAL `-1088xe` wybrano `$C0`, zapisane pod `$24B5`.
Nie zakładamy, że `$B0` jest kolejnym bankiem.

[ODCZYT] Bank 17: tła `$4000–$53FF`; pierwsze sześć bloków PMG
`$5400–$5FFF`; kod i tablice od `$6000`; pozostałe sześć bloków PMG
`$6C00–$77FF`. Kod w banku 16 deleguje akt 4 przez istniejącą niebankowaną
procedurę przełączania banku i potem przywraca jej standardowy operand.
Główny kod pozostaje długości 1788 B, bez nadpisania bitmap.

[ODCZYT] Podtrzymanie tła kosztuje około 7050–10530 cykli instrukcji py65
zależnie od rozmiaru PMG. Bez DMA, NMI i oczekiwania na vblank; nie jest
to gwarancja wolnego budżetu w każdej linii. Pełne tło jest kopiowane
tylko przy zmianie części aktu. Wyjście i restart przywracają PMG tańca.

## V1 / V6 — sprawdzenie

[ODCZYT] 42 testy OK: granice aktu, dwa rastry, trzy rozmiary, ruch
foreground, zachowanie wcześniejszych scen, restart i bezpieczna próba
nowego banku. Osobny test umieszcza `$55` w jednym z wcześniejszych
banków i sprawdza, że wykrywanie nadal wybiera niezależny bank oraz
odtwarza wszystkie szesnaście wcześniejszych bloków bajt w bajt.

[ODCZYT] Pełny zapis stereo POKEY zgodny z oryginałem:
9 295 992 identyczne bajty, około 2589,5 s emulacji.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v027.xex --seconds 12
```

[ZAŁOŻENIE] Fizyczny sprzęt i inne konfiguracje rozszerzenia pozostają do
kontroli. Podgląd stosuje przybliżenie barw PAL; model sygnału odniesienia
opisuje [kod Atari800](https://github.com/atari800/atari800/blob/master/src/colours_pal.c).

## Prompt grafiki — skill imagegen

```text
Production illustration-story contact sheet for Atari demo, EXACTLY 2 columns and 2 rows, four equal landscape panels without gutters. European comic illustration with bold black contours and broad flat colors, NOT anime/manga, no giant human eyes. Palette only black #000000, deep violet #740090, hot pink #ff32a0, pale warm pink #ffbece, cyan #00dcff limited highlights. Top left: EMPTY school gym at night, centered dark double doorway, tall windows, wall bars, parquet in perspective, dim sparse pink/cyan outlines, NO characters. Top right: SAME empty gym transformed into psychedelic neon geometric arches and radial rays toward center, clear dark central area for a large animated character, NO characters. Bottom left: TREVOR, anthropomorphic powerful male gorilla, front view full body, slightly bent knees, very broad shoulders and long arms hanging down, violet fur, pink chest and hands, pale face, strong readable gorilla muzzle, small natural eyes and confident calm expression, on pure black background. Keep entire body and feet inside panel. Bottom right: SAME gorilla identity, full body front view, shoulders raised, one broad forearm lifted to chest, confident powerful stance. Character silhouettes must remain readable when reduced to16x24 pixels for hardware sprites. No clothing, no text, no basketball, no decorative particles. Reference gorilla supplies identity and palette only; make it more grounded European comic, no goofy tongue or doll eyes. Top backgrounds wide cinematic compositions, bottom characters centered.
```

[ODCZYT] Atari800 PAL `-1088xe`: 23 kolejne zrzuty pamięci obejmują
wcześniejsze sceny, granicę wsad/Trevor, część cichą, dokładny tick
26928, ruch po uderzeniu, ostatni tick aktu, wyjście i restart.
Porównywane bitmapy są zgodne ze źródłami; wartość banku 17 to `$C0`.
