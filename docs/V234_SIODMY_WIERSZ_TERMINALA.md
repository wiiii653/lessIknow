# V234 — siódmy wiersz terminala

Terminal ma teraz **7 wierszy: status i 6 wierszy wpisywanego tekstu**.
Greetz zachowują jedną wcześniejszą linię dłużej na ekranie przed jej
przewinięciem. Dotychczasowe credits, greetz, pisanie, Entery, kursor
i delikatny glitch pozostają. Nie zmieniono treści ani ticków ich wpisywania.

## Kadr i raster

Dotychczas sześć wierszy tekstu zastępowało górny margines i pierwszych
8 czarnych linii bitmapy. Siódmy zastępuje kolejnych 8: wyświetlane są
linie bitmapy 16–191. Pierwszy nieczarny piksel postaci jest dopiero
w źródłowym wierszu 9, czyli w linii bitmapy 27; nic z postaci nie znika.
Każdy widoczny piksel chłopca oraz PMG zachowuje fizyczną wysokość.

Prywatna display lista $BC00 ma 554 B: bitmapa zaczyna się od $BC16,
ma 176 linii, stopka leży pod $BE26. Cały obraz nadal ma 235 linii.
DLI wypadają w 1/57/79/157/235; dodatkowy 57 jest wyłącznie zmianą
palety, rozpoznawaną przy VCOUNT 32. Muzyka pozostaje co 78 linii.
Litery nadal są zielone, tło czarne, paleta ciała przywracana po tekście.

## Pamięć

- Ekran historii: 240 B, $BF00–$BFEF, nadal w tej samej stronie RAM.
- Typewriter: 195 B, $EB44–$EC06, +1 B; bez zmiany jego rezerwy.
- Tabela czasu: 48 wpisów, 96 B, $23CE–$242D.
- Długości 47 logicznych wierszy: $C828–$C856, w nieużywanych glyphach
  kontrolnych fontu. Ładowane dopiero z zasobami finału, nie statycznie
  do bufora bitmapy. Pozostałe znaki i status nie korzystają z tych glyphów.
- Zasoby outro po kompresji: 1743 B, +52 B; audytowane luki mają 1783 B.
- Loader: 373 B, $3E58–$3FCC, przed ogonem zasobów zaczynającym się $3FCE.
  Został tylko jeden bajt luzu, więc nie należy go powiększać bez relokacji.
- Główny kod: nadal 2551 B. Żadna luka banków rozszerzenia nie jest zajęta.

## Weryfikacja

[ODCZYT] 46 testów ukierunkowanych zaliczonych: tekst i kursor we wszystkich
sześciu wierszach historii, scroll, końcowe wyczyszczenie, stała mapa bitmapy,
PMG i powrót poza finał. Nowa regresja sprawdza jednoczesną widoczność
`ATARIONLINE.PL / PTODT` w pierwszym i `PERSONALLY` w szóstym wierszu greetz.

[ODCZYT] Atari800 PAL/1088XE, stereo POKEY: **6 749 784 bajty identyczne
z v035**, cały utwór. Bez próby na fizycznym Atari.

[ODCZYT] Pełna regresja: **173/173 testy**, bez pominięć, 119,4 s.
XEX v234 i roboczy `visual-prototype-dev` są identyczne.
SHA-256: `9fedec90111c52c56d2a184cd12390ff382b613d858db3cfd13f589807d910b2`.

Podgląd CPU/ANTIC/PMG: `build/terminal-v234.png` (przybliżona paleta PAL).
