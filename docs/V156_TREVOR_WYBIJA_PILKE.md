# V156 — Trevor wybija piłkę co trzecim ciosem

Co trzecie uderzenie (3., 6., 9., …) zachowuje zwykły początek BANG/BAM,
a po napisie wypuszcza dużą neonową piłkę z tunelu. Zastępuje ona chmurkę
players w wieku uderzenia 80–135 ticków, leci w górę/prawo i obraca się.
Pozostałe ciosy zachowują dotychczasowy rozpad. Missiles nadal rysują iskry
i odłamki. Nie zmieniono ani jednego ticka ciosu, długości efektu czy granicy aktu.

To dokładnie geometria dużej piłki z `tunnel_ball.masks()`, cztery fazy
0/4/8/12, po 32 podwójne linie. Dwie pary players składają lewą i prawą
połowę, cztery nasycone barwy nadal cyklicznie się zmieniają. Nie jest to
mniejsza piłka rzutu ani nowa bitmapa tła.

## Pamięć

[ODCZYT] Każdy z 16 banków akcji loadera 24–39 otrzymuje 512 B masek
w dotąd pustym `$5E00–$5FFF`. Zajętość masek 8192 B. Dane są wspólne
logicznie, powielone fizycznie, aby renderować bez przełączania banku
w środku kontrolera. Obszar nie koliduje z boczną tancerką ani finałową bitmapą.

Bank 49 nie dostaje masek: jego `$5CD0–$5FFB` zajmuje kontroler końcowego
chłopca. Instalator wpisuje piłkę wyłącznie do banków akcji.

Helper Trevora urósł z 2395 do **2556 B**, kończy się na `$69FB` i ma już
**tylko 4 B** do danych od `$6A00`. W 17 kopiach helpera daje to +2737 B.
Łączny koszt +10 929 B; odzysk netto względem v141: 12 905 B (12,60 KiB).
Nadal 64 banki. Główny kod i jego 14 B zapasu pozostają bez zmian.

## Walidacja

Test co trzeciego ciosu porównuje wszystkie cztery płaszczyzny z maskami
piłki tunelu w pięciu momentach lotu i trzech uderzeniach. Zachowano
regresje zwykłych chmurek, BANG/BAM oraz odłamków. Testy nieaktywnego
bufora i ruchomego VCOUNT obejmują również lot piłki; wstrzykiwanie NMI
muzyki wykonuje się teraz podczas tego lotu.

[ODCZYT] `make check`: 118 testów, 115 zaliczonych, 3 pominięte
(brak archiwalnego v126), 87,140 s.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
14 403 384 identyczne bajty względem v035 przez cały utwór.
Nie wykonano odsłuchu ani testu na fizycznym Atari. Testy py65 nie modelują
DMA ANTIC i nie ustalają rzeczywistego FPS ani stabilności rastra na sprzęcie.

## Wydanie i podglądy

`build/visual-prototype-v156.xex` i JSON.
`build/v156-ball-punch.gif` oraz `build/v156-ball-punch.png` pokazują napis,
pojawienie się piłki i lot. Podglądy po callbacku 6502, z przybliżoną paletą
i tempem; nie są nagraniem emulatora.

SHA-256 XEX: `6e8d3a2e2a2c7916804507081a166b21da4183b816e74bd5afcd22ff29b1a616`.
Numerowane XEX/JSON są identyczne z plikami roboczymi dev.
