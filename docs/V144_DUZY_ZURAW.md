# V144 — duży historyczny Żuraw w intro

[ODCZYT] Żuraw ma 40×32 piksele GTIA na siatce 80×64; zaczyna się w (20,32).
Jego obszar ma połowę szerokości i połowę wysokości aktywnego obrazu
(ćwierć powierzchni), zamiast dawnych 13×15. Obie plansze mają tę samą
sylwetkę: dwie obłe, murowane baszty, strome dachy, wysoka drewniana część
z górnym i dolnym wysuniętym okapem, brama wodna, lina oraz nabrzeże.

[ODCZYT] Rysunek jest ręcznie wyznaczany w `tools/title_plasma.py`,
bez kopiowania fotografii do bitmapy. Referencje bryły:

- [Narodowe Muzeum Morskie — historyczne fotografie i opis konstrukcji](https://nmm.pl/2022/04/04/gdanski-zuraw-na-czarno-bialych-zdjeciach-nielatwy-los-zabytkowego-dzwigu-portowego/).
- [Visit Gdańsk — fotografia od Motławy](https://kartaturysty.visitgdansk.com/res/10002/10019/fotka.jpg).

[ODCZYT] Kolorystyka jest sceniczna: turkusowe/cyjanowe baszty z rytmem
cegieł, ciepłe czerwono-pomarańczowe dachówki, ciemne drewno ze złotymi
krawędziami i czarny obrys. Chłodne baszty odcinają się od plazmy z zakresu
hue 2–7. GTIA 11 zachowuje wspólną, istniejącą luminancję i jej fade;
nie dodano rasterowych zmian jasności ani muzycznych DLI.

[ODCZYT] Napisy zajmują górną połowę. TAME/IMPALA startują w liniach
rastra 0/48 i zachowują podwojenie wierszy glifu. Tytuł ma pojedynczą
wysokość wiersza glifu: THE LESS / I KNOW / THE BETTER startują w 0/33/66.
Litery i cienie kończą się przed źródłowym wierszem 32. Kolejność wejść
I KNOW → THE BETTER → THE LESS oraz momenty reveal, przenikania i końca
plansz pozostają bez zmian. Nie zmieniono żadnych granic aktów.

[ODCZYT] Maski fajerwerków uwzględniają cały obrys Żurawia, także czarne
drewno i czarne krawędzie. Duszki ani pociski nie przecinają budynku.
To zmiana danych generowanych na hoście; kod 6502 i bufory pozostają
bez zmian. Wszystko mieści się w istniejących 16 klatkach plazmy,
dotychczasowych maskach tytułu i strumieniach PMG. Nadal 64 banki,
29 901 B odzysku netto względem v141 i 2560 B głównego kodu.

Wydanie: `build/visual-prototype-v144.xex` i JSON.
Podglądy: `build/v144-duzy-zuraw.gif`, `build/v144-zuraw-cards.png`.
GIF wykonuje kolejne callbacki py65 co 24 ticki. Paleta i tempo są
przybliżone; nie jest to nagranie emulatora ani pomiar FPS z DMA ANTIC.

## Walidacja

[ODCZYT] Końcowy `make check`: 101 testów, 98 zaliczonych, 3 pominięte
(brak archiwalnego v126), 81,864 s. Testy sprawdzają nowy obszar budynku,
brak kolizji z napisami, chronienie sylwetki przed wszystkimi fazami PMG,
kolejność wejść słów, bezpieczne bufory oraz przejście do dalszych scen.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 12 213 216
identycznych bajtów względem v035, cały utwór. Bez odsłuchu i bez testu
na fizycznym Atari. Porównanie v143/v144 potwierdza zmianę wyłącznie siedmiu
banków danych plazmy/masek (indeksy loadera 40–44, 47–48); pozostałe banki,
niebankowana RAM i kod są identyczne.

[ODCZYT] XEX ma 1 109 100 B, tyle samo co v143. SHA-256:
`8db4ca4de50c7db85d02732e416a9734b1ceab91a9e9e999c59e0e32fc828f21`.
Numerowane wydanie i sprawdzony build roboczy są identyczne bajt w bajt.
