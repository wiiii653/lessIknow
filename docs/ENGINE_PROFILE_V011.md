# Profil silnika v011

## V1 — koszt instrukcji muzyki

[ODCZYT] Wykonano pełny utwór w py65 z RuntimeMemory, wrapperem NMI v011,
oryginalnym restartem i dekoderem. 59 833 przerwania: min. 347, średnia
680,81, maks. 1427 cykli instrukcji (tick indeksowany od zera: 23933).
Maksymalna suma czterech kolejnych przerwań: 4881 cykli.
Pomiar obejmuje wejście NMI modelowane przez py65, nie obejmuje oczekiwania
WSYNC ani kradzieży cykli przez ANTIC. Nie zamyka sprzętowego profilowania V1.

## Renderer

[ODCZYT] Koszt wywołania callbacku przy ustawionym VCOUNT=124 (bez czekania
na vblank, bez DMA oraz bez wstrzykiwania NMI):

- title: 16166 cykli.
- school: 16340 cykli.
- practice1: 93424 cykli.
- practice2: 93620 cykli.
- practice3: 93601 cykli.
- solo: 93788 cykli.
- duo: 93773 cykli.
- trio: 93754 cykli.
- kaleidoscope: 19394 cykli.

[ODCZYT] Każde wywołanie w treningu i tańcu kopiuje 8192 B i buduje listę
192 LMS. Trening kopiuje ten sam atlas nawet wtedy, gdy ujęcie się nie zmienia.
PMG pozostaje wyłączone w v011.

[WNIOSEK] Pierwsza optymalizacja: zachować atlas treningu w buforach,
a statyczne listy przebudowywać przy zmianie ujęcia. W tańcu rozważyć różnice
między pozami, z uwzględnieniem zawartości każdego z dwóch buforów.
Drobne animacje przez PMG i rejestry palety wymagają mniej pracy CPU niż
kolejne pełnoekranowe kopie, ale dodatkowe DMA nadal wymaga pomiaru.

[ZAŁOŻENIE] Nie wyznaczono jeszcze gwarantowanego wolnego budżetu cykli
w każdej linii z włączonym PMG. Bez takiego pomiaru nie deklarujemy stałej
liczby wolnych cykli na dodatkowe efekty.
