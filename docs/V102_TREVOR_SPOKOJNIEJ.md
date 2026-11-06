# V102 — czytelniejsze uderzenia Trevora

Tempo sceny zmniejszono: kombinacja zachowuje kolejność prawa, lewa, lewa,
prawa, lewa, lecz odstępy wynoszą 140–141 lub 187 ticków. BANG i rozbłysk
trwają 48 ticków, a cząstki kolejne 48; razem trzy razy dłużej niż w v100.
Pomiędzy uderzeniami widać zamach właściwej ręki. Punkt startu cząstek nadal
jest powiązany z pozycją BANG. Granice aktów nie zostały zmienione.

Usunięto wykryty skok fazy tunelu przed pierwszym ciosem: zamach korzysta z
banku tej samej animowanej fazy co dalsza scena, zamiast krótkiego powrotu do
fazy zerowej. Dopracowano jasność drugiej planszy wejścia i neony sali,
obrys Trevora, błyski tunelu oraz grubość liter BANG. Dodatki mieszczą się w
istniejących bankach i nie zmieniają liczby banków rozszerzenia.

[ODCZYT] 71 testów py65 zakończyło się poprawnie, w tym testy fazy pierwszego
zamachu, tempa, pozy, długości efektów, kierunku cząstek oraz odtworzenia PMG
po zmianie sceny. [ODCZYT] Atari800 PAL, 1088XE, Altirra OS, stereo: po
jednokrotnym wyrównaniu początku zapis rejestrów POKEY był identyczny z v035
dla 5 834 736 bajtów; porównanie obejmuje cały utwór. [WNIOSEK] Nadal potrzebna
jest ocena płynności obrazu i odsłuch na docelowym Atari; test POKEY nie
potwierdza wizualnie przyczyny każdej zaobserwowanej usterki klatki.

`build/visual-prototype-v102-trevor.gif` to programowy podgląd sceny z
przybliżonymi kolorami i tempem, nie nagranie emulatora. XEX:
`build/visual-prototype-v102.xex`; SHA-256
`a749d448bb54b516c1e3efa84cddac72ad7aa9d7e0ca2b47fda90f8ffd005efa`.
