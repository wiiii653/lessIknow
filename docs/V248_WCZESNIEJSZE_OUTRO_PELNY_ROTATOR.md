# V248 — pełny montaż, wcześniejsze outro

Na polecenie użytkownika przywrócono 2000 ticków montażu utracone w v240
i przesunięto cały montaż o 4000 ticków wcześniej. Trevor kończy się teraz
w 28909 zamiast 32909, zaś kadr chłopca z terminalem zaczyna się w 49850
zamiast 51850 (o 2000 ticków, ok. 10,0 s wcześniej). Zakończenie tekstu
59085, fade i czerń 59833 pozostają. Ostatni z 13 zachowanych ciosów ma
czas na całe BUM/BAM i odlot piłki; żaden nie jest ucięty na granicy.

Wirtualny zegar montażu wynosi rzeczywisty tick +4000. Sekwencja faz,
motywów, palet, piłki i satelitów odtwarza w tej samej kolejności dawne
32909–53849; fragment odpowiadający 51850–53849 przywrócono z v239.
Muzyka nie jest przesuwana, więc zdarzenia wizualne występują 4000 ticków
wcześniej względem niej. Wcześniejsze ujęcia rotatora zachowują realny zegar.
Wszystkie plansze credits/greetz i ich końcowy tick pozostają; wcześniejsze
wejście wydłuża czas dostępny na czytanie.

## Pamięć i walidacja

Główny kod zajmuje 2560 B `$1400–$1DFF`: brak zapasu do puli `$1E00`.
W banku loadera 2 helper lotu Trevora zajmuje `$6E10–$71BE`, director
`$7250–$73D6`, selektor `$7400–$744B` i zegar piłki `$7480–$74B4`.
Istniejące maski i pomocnik piłki `$7800–$7FFF` pozostają; nadal 64 banki.
Przełączenia banku zachowują PORTB, a pomocniczy zegar `$0DD3–$0DD4`
używany jest przed wejściem terminala.

[ODCZYT] Test porównuje bitmapy, fazy, pozycje PMG i palety próbek montażu
z v247 oraz przywróconej końcówki z v239. Atari800 PAL/1088XE stereo POKEY:
11 118 384 bajty identyczne z v035, pełny utwór. Nie jest to odsłuch ani
pomiar FPS z ANTIC DMA; brak testu na fizycznym Atari.

[ODCZYT] Pełne `make check`: 190/190 testów, 146,748 s.
