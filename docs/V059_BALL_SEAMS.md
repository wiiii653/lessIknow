# V059 — kolorowe szwy piłki

Cztery playery tworzą dwa kolory: oba fizyczne obszary piłki mogą zawierać
każdy z nich. Zakrzywiony szew jest równocześnie granicą kolorów, a szew
poprzeczny powstaje przez miejscową zamianę barw. Obwódka i szwy nie mają
osobnej czarnej warstwy. Kolory zmieniają się z tęczowej palety; cztery
missiles nadal tworzą satelity. Tor i skalowanie pozostają jak w v058.

`make check` przeszło 60 testów; dodatkowo sprawdzono, że każdy fizyczny
obszar playerów może zawierać oba kolory. Pełne porównanie stereo POKEY z
oryginalnym v035 dało 8 663 688 identycznych bajtów po wyrównaniu początku.
Podgląd pochodzi z renderera 6502, nie z fizycznego Atari.

Wydanie: `releases/visual-prototype-v059.xex`, SHA-256
`2f8d761b8430e2aecb46d4a3fc6444bffab4262c0b669282ca352ada42633e9c`.
