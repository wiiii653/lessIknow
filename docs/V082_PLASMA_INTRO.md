# V082 — plazma i napisy otwarcia

Obie dotychczasowe plansze GTIA 11 zachowują swoje granice: wykonawca od
 ticku 0, tytuł od 1496, szkoła od 2992. Plazma rozjaśnia się z ciemności,
przelewa przez zmianę adresów linii i odsłania kolejne wiersze napisu. Pod
koniec każdej planszy linie gasną w różnej kolejności. Zmiana fazy korzysta
z licznika muzyki co 16 ticków; DLI nie zostały dodane ani przesunięte.
Napisy mają czarne tło w swoich pasach, aby zachować czytelność i zmieścić
obraz w dostępnej pamięci.

Kod i dane efektu zajmują `$E4C0–$E9D2` pod ROM-em systemowym; cała rezerwa
`$E4C0–$EABF` jest wyłączona z puli wierszy. Procedura modyfikuje tylko
nieaktywną display listę. Bufory późniejszych scen pozostają dostępne, a kod
plazmy zachowuje się także przy powrocie do początku utworu.

[ODCZYT] `make check PYTHON=/tmp/tliktb-plasma-venv/bin/python`: 64 testy OK,
w tym fazy napisów, zanik, powrót do intra, granice scen i cztery pozycje DLI.
[ODCZYT] Atari800, PAL, 1088XE, Altirra OS, stereo POKEY: porównanie z v035
przeszło dla 4 670 136 bajtów po jednokrotnym wyrównaniu początku; obejmuje
cały utwór. [ODCZYT] W izolowanym teście py65 przebudowa obrazu intra zajmuje
około 40–46 tys. cykli 6502, więc pojedyncza faza może trwać kilka klatek.
[WNIOSEK] Przerwania muzyki pozostają aktywne podczas przebudowy; porównanie
POKEY nie zastępuje odsłuchu ani testu na prawdziwym Atari.

Podgląd `build/visual-prototype-v082-preview.png` wykorzystuje przybliżone
kolory, obliczone z display listy, nie jest zrzutem z emulatora. XEX:
`build/visual-prototype-v082.xex`, SHA-256
`3aac79b1a6c03b6a4d95f267937d979133f956b892cb15639cb206056c08a6dc`.
