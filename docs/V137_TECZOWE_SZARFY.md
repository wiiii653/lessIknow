# V137 — tęczowe szarfy i lecące iskry

[ODCZYT] Cztery players zmieniają kolory w cyklu 16 odcieni. Istniejące
cztery DLI muzyczne wywołują dodatkowo niebankowany helper palety **po**
zakończeniu ticka dekodera, wyłącznie w scenie 14. Daje to szerokie pasy
tęczy wzdłuż szarf oraz zmianę barw w czasie. Nie dodano DLI ani ticków
muzycznych; nie przesunięto scen. Helper palety używa wyłącznie stosu jako
pamięci tymczasowej i może zostać przerwany przez NMI bez utraty kontekstu.

[ODCZYT] Cztery missiles były już wykorzystywane w v136. Zastąpiono ich
oscylujące akcenty strumieniem iskier: cztery przesunięte fazy narodzin,
ruch w górę z wyhamowaniem, rozrzut poziomy i krótki, zanikający ogon.
Kolor piątego gracza również bierze udział w cyklu, przy wysokiej jasności.

[ODCZYT] Bitmapy choreografii i wielkość tablic PMG nie zmieniły się.
Podwójne bufory PMG i bitmap nadal chronią aktywny obraz. Zachowano
64 banki; dodatkowa pamięć to kod i niewielkie tablice, bez kolejnych klatek.

## Sprawdzenie

[ODCZYT] Testy palety uruchamiają kod 6502 dla czterech pasów i czterech faz
zegara, przy wybranym banku wideo: sprawdzają wszystkie pięć kolorów,
zachowanie banku i stosu oraz brak zapisów do buforów obrazu. Test iskier
sprawdza zmianę masek i pozycji przy zatrzymanej pozie tancerki.
Testy ochrony buforów, późnego rastra oraz NMI muzyki również przechodzą.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 15 113 088
identycznych bajtów względem v035; cały utwór. Nie jest to odsłuch sprzętowy
ani pomiar dokładnych linii przejść palety.

Podgląd `build/v137-rainbow-dance.gif` to sekwencyjne wykonanie callbacku
w py65 z przybliżoną paletą i idealnymi pozycjami pasów DLI. W emulatorze
granice pasów uwzględniają czas dekodera muzyki; GIF nie modeluje tej latencji,
DMA ani pomijania faz. Grafika pozy pochodzi z v136, bez nowej generacji AI.

XEX: `build/visual-prototype-v137.xex`.

[ODCZYT] Pełny `make check`: 92 testy, 89 zaliczonych, 3 pominięte
z powodu braku archiwalnego v126; 81,817 s. Build roboczy identyczny z v137.
SHA-256: `0b6a15875e0933d5cbc049058dcc86d9b285be0501c918e2e386e90c0e17324e`.
Dodatkowy kod i tablice zajmują 496 B względem v136 (381 B niebankowanego
kodu/tablic i 115 B w kontrolerze sceny).
