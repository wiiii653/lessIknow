# V170 — chłopak puszcza oko i gwiżdże

## Ujęcie i grafika

W pierwszym ujęciu szkolnej fasady chłopak ma wyraźne przymrużone oko,
patrzy w lewo i gwiżdże za dziewczyną. Krótki, pikselowy ślad melodii
zawiera dwa klucze wiolinowe i dwie nuty. Symbole są komponowane w
rozdzielczości 160×192, zamiast polegać na detalach, które znikają przy
zmniejszeniu całego obrazu. Melodia jest warstwą tła; w pierwszym przejściu
dziewczyna zasłania ją zgodnie z głębią sceny.

Nowy obraz źródłowy zastępuje portret w `build/school-front.rgb`.
Oryginalny `act1_boy_front.png` pozostaje zachowany.

- Źródło: `assets/art/source/act1_boy_front_v170.png` (1619×971).
- Prompt: `assets/art/source/act1_boy_front_v170.prompt.txt`.
- Przetwarzanie źródła: cel 160×64, istniejąca maska portretu i paleta
  sceny; melodia dodana przez `school_story.whistle_melody`.
- Podglądy po kompozycji tła i portretu: `build/school-v170-1-preview.png`
  oraz `build/school-v170-2-preview.png` (drugie ujęcie z dziewczyną).

## Pamięć i synchronizacja

- Ticki i granice aktu 1 bez zmian.
- Banki bez zmian; liczba całych wolnych banków nadal 0, znane luki
  bankowane nadal 31 623 B.
- Wiersze współdzielone: 279 → 309; pamięć wierszy: 10 764 → 11 913 B
  (+1 149 B). Wiersze pozostają w dotychczasowych obszarach RAM.
- Kod główny: 2552 B, osiem bajtów przed limitem `$1E00`.
- Testów nie uruchamiano. Podglądy sprawdzają kompozycję grafiki, nie
  nagranie z Atari800.

XEX zbudowano poleceniem `python3 tools/build_bitmap_sequence.py --output
build/visual-prototype-v170.xex`.

SHA-256: `a439cbe3e2fc94cff35ccf941d5a11df21c8c79618328da034909d4fad12ac5c`.
