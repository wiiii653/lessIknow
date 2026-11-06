# V087 — ciemna plazma i rastrowa podmiana tytułu

Plazma ma maksymalną jasność GTIA 11 równą 8. Na początku wyłania się z
ciemności przestrzenną maską z rastrem uporządkowanym. Płynne tło działa bez
przerwy od początku do końca planszy tytułowej, a jego faza liczona jest z
bezwzględnego ticku muzyki. Dopiero przed wejściem kolejnej sceny plazma gaśnie.

W przedziale 256 ticków wokół granicy wykonawcy i tytułu osiem masek rastrowo
podmienia piksele liter TAME IMPALA na piksele THE LESS. Litery nadal różnią
się od tła tylko kolorem, bez prostokątnego podkładu. Potem pojawiają się
pozostałe wiersze tytułu. Granica sceny 1496 i wejście szkoły 2992 pozostają
bez zmian.

[ODCZYT] Testy py65 porównują wynikowe klatki z maskami, badają zachowanie
PORTB, powrót po innych scenach i ciągłość pikseli tła oraz jasności bezpośrednio
przez granicę 1495/1496. [ODCZYT] Atari800 PAL, 1088XE, Altirra OS, stereo:
zapis rejestrów POKEY był identyczny z v035 dla 6 151 248 bajtów po jednokrotnym
wyrównaniu początku; porównanie obejmuje cały utwór. [ODCZYT] W izolowanym
py65 przebudowa klatki trwa około 53–130 tys. cykli, zależnie od maski.
[WNIOSEK] Dłuższe przebudowy mogą pominąć fazy obrazu; wymagają oceny płynności
i odsłuchu na Atari. Efekt wykorzystuje 63 z 64 banków konfiguracji 1 MB.

Podgląd `build/visual-prototype-v087-preview.gif` odtwarza display listy z
przybliżonymi kolorami i założonym tempem, nie jest nagraniem emulatora. XEX:
`build/visual-prototype-v087.xex`; SHA-256
`1a6d43a84548950af90933327f2eb3935f6b9abf5bc69f9e158f60c48ccb9424`.
