# V128 — maski postaci i paleta tańca

[ODCZYT] `build/visual-prototype-v128.xex`, identyczny z roboczym buildem.

- Cheerleaderki: jednopikselowy kontur zamiast rozszerzenia o dwa piksele
  górnej części sylwetki. Drobne zamknięte otwory maski w rejonie twarzy
  i stroju są nieprzezroczyste; większe prześwity między ramionami pozostają
  otwarte. Kolorowe piksele źródła są zachowane.
- Paleta wyłącznie tańca: PF0=$5A, PF1=$AC, PF2=$2E — jaśniejszy róż,
  turkus i ciepły kolor skóry/podłogi. Cztery kolory ANTIC E pozostają
  wspólne dla sali i postaci.
- Trevor: ponownie dopasowane kontury głowy, włosów, barków, rękawów,
  pięści i dolnej krawędzi obu póz. Usunięte fragmenty starej sali,
  dopracowany prześwit między opuszczoną pięścią a tułowiem.
  Odbicia lustrzane korzystają z tych samych masek co obrazy źródłowe.

[ODCZYT] Wizualnie sprawdzono wygenerowane pozy oraz raster po wykonaniu
callbacku: solo, duet, trio i obie strony uderzenia Trevora z PMG.
Podgląd: `build/v128-live-preview.png`. Paleta PNG jest przybliżeniem PAL.

[ODCZYT] Porównanie stereo POKEY w Atari800 PAL/1088XE: PASS,
3 626 640 identycznych bajtów, około 1010,2 s emulacji, cały utwór.

Test porównawczy v126 uwzględnia zamierzone różnice masek i palety;
pozostałe sceny nadal są porównywane piksel w piksel. Bieżące testy
postaci porównują raster z aktualnymi wygenerowanymi pozami.

[ODCZYT] `make check`: 83/83 testy OK, 95,529 s.
