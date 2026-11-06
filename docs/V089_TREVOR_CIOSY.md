# V089 — naprzemienne ciosy Trevora

W scenie uderzenia dodano przeciwną pozę pięści, tworzoną przez lustrzane
odbicie sylwetki i grafiki istniejącego ciosu. Kolejne uderzenia przełączają
pięść; pomiędzy nimi używana jest istniejąca poza przygotowania. Rozbłyski
zachowują dotychczasowy cykl co 512 ticków oraz granice sceny. Na krawędziach
tunelu dodano ruchome błyski i dopracowano szerokość jego kolorowych pasm.

BANG i cztery cząstki używają wspólnego przesunięcia pozycji. Cząstki zaczynają
blisko środka rozbłysku i rozchodzą się w lewo i prawo, także po zmianie ręki.
Dodatkowa klatka zajmuje `$7400–$7DFF` w istniejącym banku fazy Trevora;
nie wymaga kolejnego banku rozszerzenia.

[ODCZYT] 66 testów py65 zakończyło się poprawnie. Testy obejmują naprzemienność
póz, zachowane czasy uderzeń, wszystkie pozycje BANG, początek i kierunek
cząstek oraz przywrócenie PMG przy powrocie do tańca. [ODCZYT] Atari800 PAL,
1088XE, Altirra OS, stereo: 6 127 344 bajtów rejestrów POKEY identycznych z
v035 po jednokrotnym wyrównaniu początku; porównanie obejmuje cały utwór.
[WNIOSEK] Porównanie nie zastępuje odsłuchu ani oceny płynności na sprzęcie.

`build/visual-prototype-v089-trevor.gif` jest programowym podglądem display
listy i PMG, z przybliżonymi kolorami, a nie nagraniem emulatora. XEX:
`build/visual-prototype-v089.xex`, SHA-256
`e1e693aacfe8fc4d5d7f4f490d987cbdb0c5cb375bf2c6fac397a59facd8bf7c`.
