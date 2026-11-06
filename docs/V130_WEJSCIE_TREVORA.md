# V130 — maska wejścia Trevora

[ODCZYT] Wcześniejsza bliska poza wejścia zawierała osobny kadr sali z dużym
czarnym obszarem za głową i barkami. Przy przełączeniu z dalekiej pozy znikały
fragmenty ściany i drzwi. Ujęcie nie korzystało z maski wycinającej postać.

[ODCZYT] Dodano kontur bliskiej pozy oraz osobne prześwity pod ramionami.
Bliski Trevor jest składany na tle dalekiego ujęcia. Oczyszczono czarne resztki
podkładu przy krawędzi, zachowując obrys i szczegóły wewnątrz sylwetki.
Kompozycja odbywa się podczas budowania assetów; kod odtwarzający i momenty
zmiany pozy pozostają takie jak wcześniej.

Gotowy plik: `build/visual-prototype-v130.xex`.
Porównanie rastra v128/v130: `build/v130-entrance-preview.png`.
V129 był pośrednim wariantem konturu; v130 dodatkowo oczyszcza podkład
przy krawędziach maski.

Dodano sprawdzenie zachowania wspólnej sali poza maską i zachowania twarzy.

[ODCZYT] Końcowy build: 20 testów Trevora, BANG i regresji optymalizacji OK.
Atari800 PAL/1088XE: 3 527 496 identycznych bajtów stereo POKEY,
około 982,6 s emulacji, cały utwór.

[ODCZYT] Pełny `make check` na końcowym buildzie: 84/84 testy OK, 99,982 s.
