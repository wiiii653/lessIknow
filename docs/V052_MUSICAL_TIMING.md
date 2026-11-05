# V052 — poprawa mapowania taktów na ticki

## Zmiana

Silnik używał wcześniej przybliżenia 374 ticków na takt. Ponieważ zegar playera
pracuje z częstotliwością 199,44296 Hz, a takt przy 128 BPM trwa 1,875 s,
rzeczywista średnia wynosi 373,95555 ticka na takt. Błąd starego przeliczenia
kumulował się do około 7 ticków (35,7 ms) pod koniec utworu.

`tools/music_timing.py` wyznacza teraz próg taktu `n` jako
`ceil(n × 37 395 555 / 100 000)`, liczony zawsze od początku utworu. Oznacza to
pierwszy cały tick nie wcześniejszy niż zaplanowany moment muzyczny. Granice
aktów i przebitek oraz akcenty taneczne korzystają ze wspólnej funkcji. Ujęcia
mozaiki zmieniają paletę zgodnie z rytmem połówek taktu o długości 186 lub 187
ticków.

| Granica | V051 | V052 |
| ---: | ---: | ---: |
| Takt 24 — taniec | 8976 | 8975 |
| Takt 32 — kalejdoskop | 11968 | 11967 |
| Takt 56 — koszykówka | 20944 | 20942 |
| Takt 64 — Trevor | 23936 | 23934 |
| Takt 72 — uderzenie | 26928 | 26925 |
| Takt 88 — zmiana aktu | 32912 | 32909 |
| Takt 160 — koniec | 59840 | 59833 |

## Wynik budowania

`make all` zbudowało `build/visual-prototype-v052.xex`. Kopia wydania
`releases/visual-prototype-v052.xex` ma tę samą sumę SHA-256:

`94fb15c9162f05a2b43587f0ec7eec79e07b52afcbd27e76c74cf82d2a23c008`

Testów automatycznych i pełnego odsłuchu na emulatorze w tej zmianie nie
wykonywano.

W v052 pozostał jeszcze próg wewnętrznej zmiany pozy Trevora przy takcie 68,
oparty na starym dodawaniu `4 × 374` do startu aktu. Poprawiono go w v053; suma
wydania v052 powyżej dotyczy wersji sprzed tej ostatniej korekty.
