# v016 — cheerleaderka podczas występu

## Realizacja

[ODCZYT] Nowa scena 2C: ticki 14960–20943, cięcia co 1496 ticków.
Blondynka w stroju cheerleaderki, z pomponami, w czterech pozach podczas
występu w sali. Styl europejskiego komiksu, naturalne proporcje twarzy.
Źródło: `assets/art/source/act2_cheer_performance_v015.png`.

[ODCZYT] Warianty w kurtce odłożono do ewentualnego wykorzystania:
`assets/art/source/act1_blonde_portraits_reserved_v014.png` (plener)
oraz `assets/art/source/act2_crush_gym_portraits_v014.png` (sala).
Nie zostały wstawione do początku dema.

## V2 / V3 — pamięć

[ODCZYT] Bank 8, offsety `$0000–$0B0F`, pozostają identyczne z oryginałem.
Przed wstawieniem builder sprawdza wypełnienie `$FF` w `$0B10–$1FFF`.
Pod `$4B10` działa renderer portretów, `$4F00` przywraca PMG tańca,
`$4FC0–$5FFF` zawiera cztery obrazy 80×52 (4160 B).
Pierwszy obraz jest rozwijany do nieaktywnego bufora, potem budowana jest
lista 192 LMS. Nieruchomy kadr nie jest kopiowany ponownie.
NMI przywraca bank przerwanego kodu, również podczas wykonywania helpera
w pamięci rozszerzonej. Zegar scen pozostaje licznikiem playera.

## V1 / V6 — sprawdzenie

[ODCZYT] 29 testów OK: obrazy wszystkich czterech ujęć, cache, mruganie,
powrót po restarcie oraz dotychczasowe testy muzyki, banków i rastera.
W Atari800 PAL `-1088xe` sprawdzono zrzuty pamięci ujęć i ich podtrzymania,
przejście końcowe oraz restart. Raster portretów zgadza się ze źródłem.

[ODCZYT] Pełny test stereo POKEY:

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v016.xex --seconds 12
```

9 238 464 identyczne bajty, około 2573,4 s emulacji, cały utwór objęty
porównaniem z oryginałem. Po ticku 20944 powrót do kalejdoskopu jest
placeholderem do realizacji aktu koszykarza.

[ZAŁOŻENIE] Pozostaje odsłuch i profilowanie na fizycznym Atari. Podgląd
kolorów i proporcji pikseli jest przybliżeniem: `build/v016-performance-preview.png`.

## Grafika i prompt

Użyto wbudowanego image_gen, zgodnie ze skillem imagegen. Finalny prompt:

```text
Use case illustration-story. NEW production 2x2 contact sheet for an Atari audiovisual demo. Input1 is character face identity and European ligne claire drawing reference ONLY; input2 is cheerleading uniform and performance poses reference ONLY, do NOT adopt its cartoon/anime face. Show the SAME dark blonde/blonde European teenage CHEERLEADER DURING HER PERFORMANCE INSIDE SCHOOL GYM in four expressive medium closeups. Natural European comic proportions, small realistically sized eyes, natural nose, clear bold black contours. Pink sleeveless cheerleading uniform with cyan V-neck trim and pink/cyan pompoms, pink hair bow, blonde hair with movement. Absolutely no jacket, no varsity collar, no casual clothes. Four panels: 1 front, one pompom lifted beside shoulder, energetic smile; 2 looking left midturn, raised arm and pompom toward upper corner; 3 looking right midroutine, other arm raised, relaxed smile; 4 front, both pompom hands beside shoulders, confident smile. Frame from chest or waist up so costume and movement visible, face large and center; keep eyes open. Upper arms and pompoms visible, do not obscure face. Tall INDOOR windows, wooden wall bars, roof beams, basketball backboard in sparse gym backgrounds. No outdoor scenery. Match clean European bande dessinee drawing, NOT manga/anime, NOT giant eyes, NOT doll face. Four flat palette colors black #000000 hotpink #ff32a0 cyan #00dcff peach/gold #ffbe96; hair uses peach/gold large masses with thin black shadows. Broad shapes readable at80x52 each panel. EXACTLY four equal landscape panels 2 columns 2rows, no gutters, no borders, no text.
```
