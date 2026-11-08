# V147 — jedno przygotowanie i jeden wyrzut

[ODCZYT] V146 używało w przygotowaniu do lotu ośmiokrokowej sekwencji
powtarzanej przez większość trzeciego ujęcia. Mimo pojedynczego końcowego
lotu powodowało to wrażenie wielokrotnego rozpoczynania wyrzutu.

[ODCZYT] Zastąpiono ją jednym przebiegiem. Po kompresji trzymanych klatek
kolejność kompozycji to 8, 9, 35, 10, 11, 12, 13, 14, 15. Żaden etap
nie pojawia się ponownie po przejściu do następnego. Pozycja 35 to teraz
małe obniżenie przed wyrzutem, zamiast dużej pozy lotu, po której postać
wracała do mniejszej skali. Końcowe zbliżenie pozostaje do cięcia.

[ODCZYT] Ujęcie nadal trwa od 17950 do 20942. Start lotu i fajerwerków
pozostaje w 20662; wcześniejsze dwa ujęcia i ich taniec nie są zmieniane.
Zmiana dotyczy wyłącznie tablicy kolejności oraz istniejącej bitmapy pozy 35.
Kod 6502, rozmiary danych, 64 banki i bilans 24 954 B odzysku względem
v141 pozostają bez zmian.

Nowy test wykonuje rzeczywisty kontroler 6502 przez całe trzecie ujęcie,
sprawdza pojedynczy przebieg wszystkich etapów i utrzymanie ostatniego kadru.

Wydanie: `build/visual-prototype-v147.xex` i JSON.
Podgląd: `build/v147-single-launch.gif`, odtwarzany jednokrotnie.
Paleta i tempo podglądu są przybliżone; py65 nie modeluje DMA ANTIC ani
rzeczywistych terminów prezentacji.

[ODCZYT] `make check`: 114 testów, **111 zaliczonych, 3 pominięte**
(brak archiwalnego v126), 89,766 s. Atari800 PAL/1088XE, Altirra OS,
stereo POKEY: **14 837 040 identycznych bajtów** względem v035, cały utwór.
Bez próby i odsłuchu na fizycznym Atari.

[ODCZYT] GIF nie zawiera rozszerzenia zapętlania. XEX ma 1 109 034 B,
tyle samo co v146. SHA-256:
`d4e3a7c3ab99de36c2c80703602d84e75f56f4354295a773514772ed097e85fc`.
Numerowane wydanie jest identyczne bajt w bajt z buildem roboczym.
