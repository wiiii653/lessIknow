# V216 — credits i greetz nad leżącym chłopcem

## Obraz i timeline

- 53850–56841: trzy plansze credits, po około pięć sekund.
- 56842–59084: greetz, pięć widocznych wierszy; tekst przesuwa się w górę,
  a każdy wiersz faluje poziomo według sinusoidy z przesuniętą fazą.
- Od 59085: powrót pełnego dotychczasowego kadru i istniejący fade.
- Zachowano całą bitmapę chłopca. W PAL pięć wierszy ANTIC 2 zastępuje
  wcześniejsze górne i dolne marginesy. Bitmapa oraz PMG przesuwają się o
  32 linie w dół na czas napisów, bez skalowania ani obcinania postaci.
- ANTIC 2 dostaje białe litery na czarnym tle; przed bitmapą wraca
  dotychczasowa paleta postaci. Zmiana palety odbywa się przez VCOUNT/WSYNC
  w foreground, bez dodatkowych muzycznych DLI.
- DLI wypadają po liniach 1, 79, 157, 235; odstęp pozostaje równy 78 liniom.
- Treść pochodzi z `GREETZ_I_CREDITS.md`, z krótszym łamaniem i zapisem ASCII.
  Nie pokazano niewypełnionych `[NAME]` ani proponowanego disclaimera przed intro.

## Własność pamięci

- Nie zajęto żadnej luki w bankach rozszerzenia.
- 1738 B spakowanych zasobów w sprawdzonych lukach podstawowej pamięci
  wskazanych przez `outro_loader.GAPS`; końcówka danych zaczyna się pod `$3FC4`.
- Loader: 364 B, `$3E58–$3FC3`. Loader i dane nie nakładają się.
- Kontroler finału w banku 49: 816 B, `$5CD0–$5FFF` — brak dalszego zapasu.
- Zmienne napisów: `$0DD0–$0DD7`, poza scanline pool, selektorem i jego
  przestrzenią `$0DC0–$0DCF` oraz kluczami DL `$0DFE–$0DFF`.
- Dopiero po skopiowaniu leżącego chłopca do `$9000` drugi bufor zostaje
  oddany napisom: `$B000` — sklejony strumień LZ, `$B800–$BAFF` — kopia
  normalnego DL, `$BC00–$BE53` — osobny DL napisów, `$C000–$CEFF` — rozpakowany kod, tekst i charset `$C800`.
  Wcześniejsze sceny nadal posiadają oba pełne bufory.
- Rozpakowanie jest jednorazowym zadaniem wieloramkowym. Muzyka nadal działa
  przez NMI. Próg 210000 cykli w teście dotyczy zimnego wejścia, a nie FPS.
- Przy końcu greetz normalny DL jest przygotowywany w nieaktywnym `$8400`
  i publikowany w oknie VCOUNT 124–127.

## Weryfikacja

Podgląd CPU/ANTIC: `build/outro-v216-preview.png` — credits, greetz i finał.
To rekonstrukcja obrazu, nie zrzut z fizycznego Atari. Testy obejmują
rozpakowanie, wskaźniki tekstu, pełną bitmapę, powrót do finału, PMG, restart
oraz porównania wcześniejszych scen z v198. [ODCZYT] Pełny przebieg dla v216: **154 testy, wszystkie zaliczone,
bez pominięć**, 114,3 s. Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
**9 791 424 identycznych bajtów** względem oryginalnej v035; cały utwór.
Ponowny build z aktualnych źródeł jest bajt w bajt zgodny z v216 (`cmp`).
Wszystkie 64 bloki bankowe zachowano; zmienił się wyłącznie blok 63,
czyli loader index 49 z kontrolerem finału. Pozostałe 63 bloki bankowe
są identyczne z v198.

Generator rekonstrukcji podglądu: `tools/preview_outro.py`. Testy CPU
nie stanowią pomiaru ANTIC DMA ani potwierdzenia działania na fizycznym Atari.

Robocze v199–v215 nie są wersjami do prezentacji.
