# V141 — wyższe napisy i gdański Żuraw

[ODCZYT] Podniesiono oba zestawy napisów. TAME/IMPALA zaczynają się w liniach
18 i 84 widocznego obrazu. Trzy wiersze tytułu zaczynają się w 0, 48 i 96;
ich twarze oraz ekstrudowany cień kończą się w wierszu źródłowym 47.
Kolejność wejść pozostaje I KNOW → THE BETTER → THE LESS, a układ końcowy
to THE LESS / I KNOW / THE BETTER. Nie zmieniono zegara ani chwil odsłaniania.

[ODCZYT] Żuraw jest ręcznie wyznaczoną grafiką 13×15 pikseli GTIA, od
kolumny 34 i wiersza 49 źródła 80×64. Dwie baszty, dachy, środkowa wysoka
część drewniana i wysunięte obudowy dźwigu odcinają się od otoczenia.
Nocna paleta rozdziela chłodne baszty, ciepłą konstrukcję drewna i okna.
Otaczającą panoramę lekko podniesiono; napis nie zasłania szczytu zabytku.

Referencje: [Narodowe Muzeum Morskie — historia Żurawia](https://nmm.pl/zuraw/historia-zurawia/),
[zdjęcie od strony Motławy](https://www.earthtrekkers.com/wp-content/uploads/2018/07/Zuraw.jpg.optimal.jpg).
Nie kopiowano zdjęcia do bitmapy — rysunek powstaje w `tools/title_plasma.py`.

[ODCZYT] Miasto jest częścią już istniejących 16 klatek plazmy. Maski liter,
przenikania i ochrony przed PMG są regenerowane dla wyższego układu. Liczba
klatek, wielkość tablic i przydział 64 banków pozostają niezmienione;
zmiana nie zwiększa zapotrzebowania na pamięć Atari.

Testy sprawdzają kolejność wejść w podniesionym układzie, oddzielenie napisów
i cieni od panoramy, ochronę liter podczas dissolve, nieaktywny bufor PMG,
restart i przejście do szkoły. Podgląd `build/v141-gdansk-intro.gif` pochodzi
z sekwencyjnych callbacków py65; kolor i tempo są przybliżone, bez DMA ANTIC.

Wydanie: `build/visual-prototype-v141.xex`.

[ODCZYT] Pełny `make check`: 100 testów, 97 zaliczonych, 3 pominięte
z powodu braku archiwalnego v126; 85,797 s. Atari800 PAL/1088XE,
Altirra OS, stereo POKEY: 14 639 760 identycznych bajtów względem v035,
cały utwór. Nie jest to odsłuch na fizycznym Atari.

[ODCZYT] XEX ma tyle samo bajtów co v140: 1 109 022 B. Build roboczy
identyczny z v141. SHA-256:
`cbde55ed1cb77faf55cd54043119bdc7cfcba06cd14dedc806196927e124dba6`.
