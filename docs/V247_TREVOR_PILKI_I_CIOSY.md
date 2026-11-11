# V247 — piłki i ciosy Trevora

Każdy z 40 istniejących ciosów zachowuje swój tick, rysunek, pozę i
naprzemienny napis BUM/BAM. Mała piłka z masek koszykarskiego wsadu
nadlatuje od strony właściwej pięści w ostatnich 32 tickach przed ciosem.
Następnie pełny efekt uderzenia trwa 80 ticków, po czym piłka odlatuje
w stronę tej samej krawędzi w tickach 80–105. Ciosy są miejscami oddalone
o 140 ticków: loty i napis muszą zmieścić się w tym istniejącym rytmie.
Poprzednie chmury i duża piłka z satelitami nie są wywoływane w tej scenie.

## Pamięć i weryfikacja

Nowy helper oraz osiem zestawów czterech masek zajmują 1078 B w banku
loadera 2, `$6E10–$7245`. Instalator sprawdza, że obszar jest pusty;
koniec wolnej luki po tym helperze to `$7246–$77FF`. Kod Trevora ma teraz
1823 B, bez zmian danych jego bitmap i bez zmiany liczby banków. Przygotowanie
PMG odbywa się w nieaktywnym buforze, publikacja we wczesnym blankingu;
wywołanie bankowe zachowuje bank foreground i nie odczytuje HPOS.

[ODCZYT] Testy py65 sprawdzają wszystkie 40 przylotów i odlotów, maski
piłki, pozy, BUM/BAM, nieaktywny bufor, ruchomy VCOUNT i muzyczne NMI.
Porównanie reprezentatywnych bitmap Trevora z v246 nie wykazało zmian.
Atari800 PAL/1088XE, stereo POKEY: 16 392 024 bajtów identycznych z v035,
pełny utwór. AppImage uruchomiono po wypakowaniu do `/tmp`, bez FUSE.
To nie jest odsłuch ani pomiar FPS z ANTIC DMA; brak testu na fizycznym Atari.

[ODCZYT] Pełne `make check` dla v247: 188/188 testów, 148,501 s.
