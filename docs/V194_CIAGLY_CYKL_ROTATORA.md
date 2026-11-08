# V194 — ciągły cykl rotatora i tunelu

## Znaleziony krótki fragment

Po takcie 112 (tick 41884) dispatcher przechodził na globalną fazę 64 klatek.
Zegar znajdował się wtedy na końcówce fazy bananowej: klatki 25–31 pokazywały
banany tylko do ticku 41984, czyli przez 100 ticków / około 0,5 sekundy.
Następnie cykl przechodził do spiralnego tunelu.

## Korekta

Granica uruchomienia globalnego cyklu została wyrównana do ticku 41984 —
początku pełnej fazy tunelu. Organiczny tunel utrzymuje się przez tick 41983,
a potem cykl wznawia się od spiralnego tunelu. Pozostały harmonogram v193,
w tym pełny rotator 32909–35900 i wejście chłopca w 53850, jest zachowany.

Zmiana dotyczy wyłącznie ticka dispatchera. Nie zmieniano grafiki, faz
animacji efektów, rendererów ani przydziału pamięci.

## Walidacja

Zbudowano `build/visual-prototype-v194.xex` oraz pasujący JSON. Build ma
298 współdzielonych wierszy i 2560 B kodu głównego. 10 ukierunkowanych testów
granic motywów, scen i finału przechodzi; test obejmuje ticki 41884, 41983
i 41984. Nie wykonywano pełnego porównania audio ani próby na fizycznym Atari.
