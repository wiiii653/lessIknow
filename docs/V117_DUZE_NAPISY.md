# V117 — większe i kontrastowe napisy na plazmie

TAME i IMPALA zajmują dwa wycentrowane wiersze. Litery wykonawcy są dwa razy
szersze i wyższe od wariantu jednowierszowego. Tytuł utworu ma również większą
wysokość. Wypełnienia liter są teraz jednolite i różnokolorowe, niezależnie
od szczegółów plazmy; wąskie przesunięte krawędzie mają osobny kolor.
Przezroczyste piksele nie zmieniają tła, a fazy rastrowego wyłaniania,
podmiany napisów i zaniku pozostają zachowane.

Kompozycja używa dwóch tablic po 256 bajtów: maski zachowania tła i kolorów
liter. Rezerwa kodu pod ROM-em systemowym wzrosła do `$E4C0–$ECBF`; kod i
jego dane kończą się pod `$EB9F`. Nie dodano banków rozszerzenia.
[ODCZYT] W izolowanym py65 świeża klatka tytułu kosztuje około 98–157 tys.
cykli zależnie od maski zaniku. [WNIOSEK] Cięższe fazy mogą pomijać kroki
animacji na sprzęcie; wymagają oceny płynności na Atari.

[ODCZYT] 78 testów zakończyło się poprawnie, w tym test stałych kolorów
liter nad wszystkimi odcieniami plazmy, dwóch dużych wierszy i przejść.
[ODCZYT] Atari800 PAL, 1088XE, Altirra OS, stereo: po jednokrotnym wyrównaniu
początku 6 131 448 bajtów POKEY było identycznych z v035; obejmuje cały utwór.

`build/visual-prototype-v117-tytul.gif` to podgląd sekwencyjnego wykonania
py65 o przybliżonych kolorach i tempie. XEX: `build/visual-prototype-v117.xex`;
SHA-256 `f03f4b1b340032e860298aa7e8c9d2607eb585482fc278daa3469782d2526622`.
