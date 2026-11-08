# V173 — dopracowanie przejść solówki

## Zmiana

Przerobiłem cztery pozy, które weszły w v171/v172 pośrodku końcowej fazy
solówki. Teraz odpowiadają konkretnemu ruchowi między poprzednią klatką
pośrednią a następnym akcentem: opadaniu ręki, obrotowi tułowia, wstawaniu
z przysiadu i otwarciu skrzyżowanych nóg do szerokiego rozkroku. Pozy dłoni
są liczone z nowej grafiki, więc kolorowe szarfy nadal trafiają do rąk.

Nowy arkusz zawiera dziewięć póz; cztery pierwsze są używane przez scenę.
Pozostałe sceny, długość solówki, ticki i wyrzut dziewczyny nie zmieniły się.
Każda nowa bitmapa nadal zajmuje jeden z ogonów banków 32–35, w których
znajduje się właściwy dekoder. Rozmiary strumieni: 983, 1006, 986 i 970 B.
Wolne luki banków: 27 323 B.

- Grafika: `assets/art/source/act2_ribbon_inbetweens_v173.png`.
- Prompt: `assets/art/source/act2_ribbon_inbetweens_v173.prompt.txt`.
- Podgląd czterech przejść: `build/v173-solo-transition-contact.png`.
  Pokazuje bitmapowe kompozycje i przybliżoną paletę; to nie jest zrzut z Atari
  ani zapis wykonania callbacka 6502.

## Wydanie

`build/visual-prototype-v173.xex`, 309 współdzielonych wierszy, 2552 B kodu.
SHA-256: `d113a29be0b2bf391ffe39aef4d9b31c0b9339af45efc66816da56048877e70c`.

Nie uruchamiałem testów py65 ani emulatora w tej iteracji; `py65` nie jest
zainstalowany w środowisku. Odtwarzanie v173 należy jeszcze potwierdzić.
