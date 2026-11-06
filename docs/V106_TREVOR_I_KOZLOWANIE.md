# V106 — spójne światło Trevora i wspólne tło kozłowania

W pozach Trevora wyrównano jasność głównych kolorów i skóry; zamachy mają
jedynie delikatnie ciemniejszy kolor drugoplanowy. Usunięto migające jasne
fragmenty obrysu zależne od fazy tunelu. Poprawiono też renderer podglądu,
który jednemu z odcieni przypisywał specjalny, znacznie jaśniejszy kolor RGB.

Kozłowanie wykorzystuje jedno wspólne tło sali. Druga poza jest zapisana
jako fragment 76×56, a po inicjalizacji obu buforów animacja kopiuje tylko ten
obszar zawierający postać. Ilość kopiowanych danych maleje z 2240 do 1064
bajtów; dane grafik zajmują o 1176 bajtów mniej w istniejącym banku. Liczba
fizycznych banków i rozmiar segmentu XEX pozostają takie same. Scena wsadu
zachowuje oddzielne kadry. Obie animacje nadal używają zegara muzyki.

[ODCZYT] Pełny zestaw 72 testów zakończył się poprawnie. Następnie dodano
regresję jasności wszystkich póz Trevora i sprawdzono 9 testów tego modułu.
Test kozłowania śledzi zapisy pamięci i wymaga, aby po rozgrzaniu buforów
nie zapisywać pikseli poza fragmentem postaci. [ODCZYT] Atari800 PAL,
1088XE, Altirra OS, stereo: 5 746 896 bajtów rejestrów POKEY było identycznych
z v035 po jednokrotnym wyrównaniu początku; obejmuje cały utwór.
[WNIOSEK] Programowe podglądy nie zastępują oceny płynności i kolorów na Atari.

Podglądy: `build/visual-prototype-v106-trevor.gif` oraz
`build/visual-prototype-v106-dribble.gif` (przybliżone kolory i tempo).
XEX: `build/visual-prototype-v106.xex`; SHA-256
`98773f3886d5aaf00e825d23f263e49ef2a8380f3fa3c7c7a72f46d551fd6140`.
