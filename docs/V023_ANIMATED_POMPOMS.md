# v023 — animowane pompony i palety ujęć

[ODCZYT] W czterech ujęciach występu (14960–20943) dodano cztery fazy
falowania pasm pomponów. Aktualizacja dotyczy wyłącznie wybranych fragmentów
bitmapy pomponów. Bazowe obrazy i każda faza są odtwarzane bez kumulowania
błędów, również przy przeskokach zegara. Piksele skóry pozostają chronione.
Mruganie i pasmo włosów na PMG działają nadal.

[ODCZYT] Każdy kadr ma osobne kolory COLPF0/COLPF1: róż/cyjan,
fiolet/turkus, czerwony róż/niebieski oraz magenta/zieleń.
COLPF2 pozostaje `$2C`, żeby zachować ciepłą skórę i blond włosy.
Paleta jest ustawiana po oczekiwaniu na vblank.

## V2 / V3 — pamięć i kod

[ODCZYT] Procedura pod `$6900` w banku 15 nakłada lokalne pakiety zmian.
4164 B pakietów mieści się w `$6F90–$7FD3`; przywracanie PMG kończy się
przed `$6F90`. Test kontroluje granice z kodem piłki i obydwoma pomocnikami.
Dane pozostają spakowane 80 pikseli na wiersz; podczas aktualizacji są
rozwijane poziomo do aktualnego bufora 160 pikseli.

[ODCZYT] Wywołanie bez zmiany fazy: około 5700 cykli instrukcji py65,
z nową fazą: około 12900–28400 w zależności od ujęcia. To koszty bez DMA,
NMI i oczekiwania na vblank; nie stanowią deklaracji budżetu jednej ramki.
Pełna bitmapa i lista nie są ponownie budowane przy podtrzymaniu ujęcia.

## V1 / V6 — sprawdzenie

[ODCZYT] Testy sprawdzają wszystkie fazy w dowolnej kolejności, pełne
piksele wyjściowe, cztery palety, ochronę skóry, granice banku, mruganie,
powrót po restarcie i wcześniejszą przebitkę przed szkołą.
Atari800 PAL `-1088xe`: zrzuty czterech faz każdego z czterech ujęć zgodne
ze źródłem, sprawdzone też szkolna przebitka i powrót, piłka oraz wyjście
z ujęć portretowych.

[ODCZYT] Pełna muzyka stereo POKEY zgodna z oryginałem:
8 568 144 identyczne bajty, około 2386,7 s emulacji.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v023.xex --seconds 12
```

[ZAŁOŻENIE] Podgląd kolorów PAL jest przybliżeniem. Fizyczny sprzęt
pozostaje do kontroli. Podgląd: `build/v023-pompoms.gif`.
