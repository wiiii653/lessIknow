# V193 — pełny rotator i wcześniejsze tło outro

## Zmiana timeline’u

- Takty 88–92 (ticki 32909–34404): pierwsza połowa istniejącego rotatora
  bananowego.
- Takty 92–96 (34404–35900): druga połowa tego rotatora.
- Takty 96–108 (35900–40388): tunel spiralny.
- Takty 108–112 (40388–41884): istniejąca organiczna tekstura tunelu.
- Granice dalszych ujęć Act 5 w taktach 112 i 116 pozostają bez zmian.
- Od taktu 144 / ticku 53850 pojawia się leżący chłopiec z orbitującymi
  gwiazdkami jako przewidziane tło okien credits i greetz. Samych napisów
  credits/greetz jeszcze nie ma.
- Takt 158 / tick 59085 nadal rozpoczyna końcowe dwutaktowe domknięcie do
  czerni; koniec pozostaje w takcie 160 / ticku 59833.

## Zakres techniczny

Zmieniono granicę przejścia z bananowego rotatora do tunelu z taktu 92 na 96
w `tools/build_bitmap_sequence.py`. `tools/final_boy.py` uruchamia istniejący
kadr od taktu 144, zachowując dotychczasowe dane, animację gwiazdek i koniec.
Nie zmieniano grafiki, generatorów efektów ani przydziału pamięci.

Build: `build/visual-prototype-v193.xex` i odpowiadający mu JSON.
298 współdzielonych wierszy, 2560 B kodu głównego.

## Walidacja

10 testów granic scen, motywów Act 5 i finału zaliczonych. Testy sprawdzają
przejścia w tickach 34404, 35900, 40388 i 53850 oraz zachowanie pełnego kadru
końcowego. Bez porównania pełnego audio i bez testu na fizycznym Atari.
