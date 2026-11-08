# V157 — ciągłe szarfy we wszystkich ujęciach

## Przyczyna

Generator `ribbon_streams()` zaznaczał tylko zaokrąglone punkty próbkowanej
krzywej. Przy największej prędkości pionowej kolejne punkty różniły się
o dwa wiersze, pozostawiając pośrodku pusty wiersz. Przerwy były więc
zapisane w samych maskach, używanych przez wszystkie ujęcia szarf.
Przykład: player 0, faza 0 miał puste wiersze lokalne 26 i 38.

## Naprawa

Kolejne próbki są łączone rasteryzowanymi odcinkami, które uzupełniają
każdy pomijany wiersz i zachowują ciągłą ścieżkę. Zmiana obejmuje wszystkie
cztery players i 16 faz, czyli 64 maski. Zachowano kształty pętli, kotwice
przy dłoniach, ruch postaci, tęczowe pasy, rozmiary oraz tempo.

Iskry missiles, fajerwerki wyrzutu i smugi wiatru są oddzielnymi kształtami;
nie wypełniano ich celowych odstępów.

[ODCZYT] Nadal 5120 B danych w banku 49, `$6A00–$7DFF`.
Brak wzrostu RAM-u, kodu lub liczby banków. Nie zmieniono mechanizmu
podwójnych buforów PMG, publikacji obrazu ani ticków muzyki i scen.
Mapa pamięci i bilans v156 pozostają aktualne.

## Walidacja

Regresja obejmuje wszystkie 64 maski: każdy wiersz pomiędzy skrajnymi
punktami jest zajęty, a wszystkie piksele należą do jednej ścieżki
przy sąsiedztwie ośmiokierunkowym. Zachowane testy nieaktywnego bufora,
ruchomego VCOUNT i NMI muzyki.

[ODCZYT] `make check`: 119 testów, 116 zaliczonych, 3 pominięte
(brak archiwalnego v126), 89,045 s.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
14 720 904 identyczne bajty względem v035 przez cały utwór.
Nie wykonano odsłuchu ani testu na fizycznym Atari; py65 nie modeluje
DMA ANTIC i nie ustala rzeczywistego FPS.

## Wydanie i podglądy

`build/visual-prototype-v157.xex` i JSON.
`build/v157-connected-ribbons.gif` pokazuje boczne ujęcie, grupę i solówkę;
`build/v157-connected-ribbons.png` zestawia te trzy ujęcia.
Podglądy po wykonaniu callbacku 6502 mają przybliżoną paletę i tempo,
nie są nagraniem emulatora.

SHA-256 XEX: `4b2efb01129cabacb5be767dcfaec1132d409c803b21df6bc3654fd105213235`.
Numerowane XEX/JSON są identyczne z plikami roboczymi dev.
