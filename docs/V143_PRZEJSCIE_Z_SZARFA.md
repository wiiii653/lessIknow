# V143 — przejście dziewczyny i szarfy przez kadr

[ODCZYT] W bocznym ujęciu 8975–11967 dziewczyna przesuwa się z x=40
do x=128. Osiem pozycji ciała i fazy sali zachowują dotychczasową animację.
Tło nadal przewija się w lewo; postać i jej cztery players oraz cztery
missiles przechodzą w prawo. Przesunięcie to 4 piksele co 128 ticków,
ograniczone do 22 kroków, bez zawijania do lewego brzegu pod koniec.
Nie zmieniono granic scen ani ticków muzyki.

[ODCZYT] Boczne klatki bankowane zawierają teraz samo tło. Niezależne
maskowane postacie są składane do nieaktywnej bitmapy przez niebankowany
helper `$0E00`. Osiem aktorów ma po 2048 B: piksele i maska zachowująca
tło, kadrowanie 68×56 od x=4/y=8, po 17 bajtów wiersza. Dane zajmują
`$4A00–$51FF` w bankach loadera 24–31. W tych bankach pozostaje po 512 B
wolnego slotu; banki 32–39 zachowują całe wolne `$4A00–$53FF`.

[ODCZYT] Cache uwzględnia również pozycję. Przesunięcie przy niezmienionej
pozie wymusza odtworzenie tła i postaci; zmiana HPOS jest publikowana z
kompletną bitmapą/PMG w ograniczonym oknie wygaszania. PORTB odtwarzany
przez wrapper NMI i trampoline kopii. Nowy helper nie czyści aktywnego PMG.

[ODCZYT] Względem v142: +16 384 B danych postaci, +256 B rezerwacji
runtime (`$0C00–$0EFF` zamiast końca `$0DFF`) oraz +92 B kontrolera
(1854 zamiast 1762 B). Kod główny nadal 2560 B. Pozostały odzysk netto
względem v141: **29 901 B = 29,20 KiB**. Nadal 64 banki. Osobny projekt
pomponiar i wcześniejsze wydania pozostają zachowane.

[ODCZYT] `make check`: 101 testów w 84,063 s, 98 zaliczonych, 3 pominięte
z powodu braku v126. Nowy test sprawdza piksele na początku, w środku i na
końcu przejścia, zgodność wszystkich czterech zaczepów oraz wspólny ruch
ośmiu HPOS przy tej samej fazie animacji. Testy obejmują też zapisy wyłącznie
do nieaktywnych buforów i NMI muzyki podczas maskowanego składania.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15 040 296
identycznych bajtów względem v035, cały utwór. Py65: zimne wejście bocznego
ujęcia 80 681 cykli, zmiana pozycji 80 643; to koszty instrukcji bez DMA
ANTIC, nie pomiar FPS. Bez odsłuchu i próby na fizycznym Atari.

Wydanie: `build/visual-prototype-v143.xex` z JSON.
SHA-256: `cd24ccf06843bc1ba833d8b4cf7380b1d0c89e286186a8c095fd422bc5759f22`.
Wydanie i sprawdzony build roboczy są identyczne bajt w bajt.
Podgląd: `build/v143-side-crossing.gif` oraz `build/v143-side-crossing.png`.
Podgląd pochodzi z kolejnych callbacków 6502 co 16 ticków; tempo i paleta
są przybliżone, bez modelowania czasu kopiowania i DMA.
