# V273 — start na fizycznym Atari z AVG i 1088 Rambo

[ODCZYT użytkownika, 2026-11-12] Dwa ostatnie pliki diagnostyczne pełnego
dema wystartowały na fizycznym Atari z rozszerzeniem 1088 Rambo i AVG:

- `releases/avg-compact-late-start-001.xex`;
- `releases/avg-final-segment-trace-001.xex`.

[ODCZYT] Kompaktowa postać wycina długie ciągi zer z danych ładowanych do
bufora banków. Przed każdym takim blokiem bufor jest zerowany; odtworzone
dane 64 banków porównano bajt w bajt z pierwowzorem. W pierwszej wersji
niska pamięć wykonawcza jest odkładana do bufora i przywracana przez ostatni
INIT, który przechodzi bezpośrednio do playera. Druga dodaje znaczniki
końcowych segmentów. Obie mieszczą się poniżej 1 MiB.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS: cały utwór stereo zgodny z v035:
16 517 736 bajtów dla wersji late-start i 15 539 688 dla final-segment-trace.
Osobne wykonanie kodu 6502 potwierdziło zgodność pięciu kopiowanych zakresów
niskiej pamięci.

[OGRANICZENIE] Potwierdzenie fizyczne dotyczy startu obu wskazanych plików.
Nie otrzymano potwierdzenia pełnego przebiegu, odsłuchu, płynności ani
wersji mono. Przyczyna awarii wcześniejszych plików pozostaje hipotezą:
równocześnie zmieniono rozmiar pliku i sposób końcowego ładowania.
