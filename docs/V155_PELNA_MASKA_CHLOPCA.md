# V155 — pełna maska chłopca przed areną

## Przyczyna i poprawka

Podmiana otoczenia w v151 wyznaczała maskę chłopca przez selekcję spójnych
obszarów koloru. Czarne wnętrze włosów nie było poprawnie zamknięte maską,
a magenta kurtki mogła należeć do tego samego komponentu co stare boisko.
Odrzucone obszary zostały zastąpione grafiką areny, dając przezroczystość.

`arena_art.portrait()` używa teraz pełnej maski sylwetki, niezależnej od
koloru pikseli. Czerń włosów i magenta kurtki pozostają kryjące. Maska
obejmuje także uciętą prawą krawędź postaci na ekranie. Poprawka dotyczy
obu poz chłopca oraz scen z odchodzącą dziewczyną. Nie zmieniono maskowania
kosza, zawodnika we wnętrzu, dziewczyny ani żadnych ticków.

## Pamięć

[ODCZYT] Zmiana dotyczy kompozycji assetów podczas budowania. Bez nowego
kodu Atari i bez dodatkowych banków. Nadal main 2546 B, hero 2652 B,
64 banki. Spakowane wiersze zajmują 10 764 B zamiast 10 927 B w v153,
czyli 163 B mniej. Odzysk względem v141: 23 834 B (23,28 KiB).

## Walidacja

Nowa regresja wykonuje callback obu poz i porównuje obszary włosów oraz
kurtki, włącznie z czernią i prawą krawędzią, z oryginalnymi pikselami.
Podgląd po callbacku: `build/v155-opaque-boy.png`.
Paleta podglądu jest przybliżona; nie jest to nagranie emulatora.
Testy CPU nie modelują DMA ANTIC ani realnego FPS. Nie wykonano odsłuchu
ani testu na fizycznym Atari.

[ODCZYT] `make check`: 117 testów, 114 zaliczonych, 3 pominięte
(brak archiwalnego v126), 87,656 s.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
14 573 016 identycznych bajtów względem v035 przez cały utwór.

## Wydanie

`build/visual-prototype-v155.xex` i JSON; identyczne z plikami roboczymi dev.
Roboczy numerowany v154 pozostaje zachowany; v155 obejmuje też pełną prawą
krawędź sylwetki.

SHA-256: `faa9c90b7bf141f96a9ba342d246c025562a8d5855a91b384c2c53b5a5578b91`.
