# V167 — tęczowy cykl refleksów tunelu

Po scenie Trevora kolor jasnych refleksów tunelu zmienia się wraz z każdą
nową fazą animacji. Rejestr koloru `$D018` przechodzi przez 16 kolejnych
barw z istniejącej palety, zachowując wysoką jasność. Faza zmienia się co
16 ticków playera. Krótka przebitka tunelu w akcie 3 nadal ma biały błysk;
żółta barwa kiści bananów przed tunelem pozostaje stała. Nie zmieniono scen,
ticków, animacji obrazu ani przydziału pamięci.

Zmiana jest w `tools/mosaic.py`. Oczekiwanie w istniejącym teście koloru
rotatora i tunelu zaktualizowano w `tests/test_mosaic.py`; testów w tej
zmianie nie uruchamiano.

## Wydanie

XEX zbudowano poleceniem `python3 tools/build_bitmap_sequence.py --output
build/visual-prototype-v167.xex`. Budowa zakończyła się poprawnie; główny
callback nadal ma 2546 B. Odtwarzanie na Atari800/Altirrze i odsłuch nie
były w tej zmianie weryfikowane.

SHA-256: `fe7e0408d324f57649d0a2d0e796dcb1dc58242177b646ad194d07ba8d5fe4d0`.
