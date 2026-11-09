# V225 — paleta terminala z DLI i wejście Trevora

## Terminal

Przyczyną mrugania były zapisy COLPF2 przez foreground, zależne od czasu
rysowania napisów i PMG. ANTIC 2 współdzielił hue tła/znaków z kolorem
skóry bitmapy. Usunięto polling VCOUNT/WSYNC z renderera napisów.

Terminal używa teraz ANTIC 4: litery są rysowane kolorem COLPF0, a puste
piksele i otoczenie mają prawdziwy COLBK `$00`. Nowy font terminalowy 3×7
mieści 40 kolumn. Kursor `$5F` jest pełnym blokiem w tym samym zielonym
kolorze. Nie ma zielonego tła/pasa ani zielonej ramki.

Display lista oznacza ostatni wiersz tekstu jako `$C4`, dodając DLI po
linii 41. Router NMI `$2451–$248F` (63 B) przy pierwszym DLI ustawia zielone
litery, a przy dodatkowym DLI przywraca kolor bitmapy. Dodatkowe DLI nie
uruchamia dekodera muzyki: zdejmuje adres powrotu JSR, przywraca Y/X/A i
wykonuje RTI. Nie przełącza banku. Cztery muzyczne DLI pozostają przy
liniach 1/79/157/235, czyli co 78 linii. COLPF1 i COLPF2 nie są zmieniane
przez terminal; kolor skóry pozostaje pod kontrolą rendererera postaci.

Router zajmuje dalszą część wyłączonego kodu starego UI/fontu. Nie wolno
przywracać starego UI/fontu bez zmiany jego własności pamięci. Pakiet
napisów: 1691 B, loader: 351 B. Brak nowych banków.

## Trevor

Oba ujęcia wejścia mają podstawową paletę z bicia:
COLPF0 `$48`, COLPF1 `$68`, skóra `$2A`. Usunięto przyciemnianie pierwszego
ujęcia i inną barwę skóry drugiego ujęcia. Animacja, timing i palety samych
ciosów pozostają zachowane. NOP-y utrzymują rozmiar i położenie helpera.

## Weryfikacja

[ODCZYT] V223 (zmiana terminala): 158/158 testów, 114,6 s.
[ODCZYT] V225 (terminal, font i paleta wejścia): 47 testów scen, NMI,
terminala, kolorów, granic i regresji — OK, 18,8 s. Test dodatkowego NMI
sprawdza niezmieniony licznik muzyki, rejestr banku i kolor skóry.
[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 11 329 632 identyczne
bajty względem v035, cały utwór. Brak próby na fizycznym Atari.

Build: `build/visual-prototype-v225.xex`.
Rekonstrukcja podglądu CPU/ANTIC: `build/terminal-v225-preview.png`.
