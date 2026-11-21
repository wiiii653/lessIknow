# V362 — wspólna siatka pikseli przed areną

Chłopak i dziewczyna w zbliżeniu przy arenie korzystają z tej samej
siatki 160 × 64. Zbliżenie dziewczyny pochodzi bezpośrednio z oryginalnego
rysunku party próbkowanego do 96 × 128. Kontur, włosy, szwy i znak Fuji
mają teraz detale o szerokości jednego piksela sceny. Pozycja, skala i
kadr do pasa odpowiadają v361.

[Porównanie z Atari800](../build/v362-arena-pixel-grid.png) ·
[Wzorzec party](../assets/art/reference/v330/README.md)

## Wydania AVG

Oba pliki mają po 945 890 B. Prototyp używa 64 banków i 297 wspólnych
wierszy (11 478 B). Kod główny ma 2 542 B.

- [081 mono, jeden POKEY](../releases/less-i-know-demo-release-081-mono.xex)
  · SHA-256 `5e2161ef0467001f3988445cf3c8d8fa89b39a38fba1302b62133bdcf9dacf58`
- [080 stereo](../releases/less-i-know-demo-release-080-stereo.xex)
  · SHA-256 `862cf2d1a06a8b3b89e3e1549c4e5c59864eff90ddb9668c7c280370e1c485fd`

## Weryfikacja

Przeszło 21 testów grafiki, przejść scen, loadera i directora po Trevorze.
Porównania w Atari800 PAL, emulowane 1088 XE i Altirra OS, wykazały
różnice wyłącznie w zbliżeniu dziewczyny. W obu wydaniach 59 833
aktualizacje rejestrów POKEY odpowiadają poprzednim wydaniom 078 i 079.
Próba na fizycznym Atari i pełne `make check` pozostają niewykonane.
