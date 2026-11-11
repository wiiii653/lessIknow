# V272 — śledzenie INIT pełnego dema

[ODCZYT użytkownika] Test RUNAD pokazał INIT OK oraz RUN OK. Sam wektor
RUN działa; brak wyniku wcześniejszych diagnostyk nie dowodził jego awarii.

`releases/avg-full-demo-init-trace-001.xex` instrumentuje 66 INIT-ów pełnej
wersji stereo 011. Pokazuje numer, adres i ENTER przed wywołaniem oraz
RETURN po powrocie. Wrapper zachowuje A/X/Y i flagi. Tymczasowe $1200
jest nadpisywane końcowymi segmentami obrazu wykonawczego jak w źródle.
Lista etapów: pasujący plik `.stages.txt`. Ten plik służy do diagnozy,
nie zastępuje wydania produkcyjnego. Nie potwierdzono działania na AVG.

Uwaga do wcześniejszego raportu: CHBASE jest pod $D409, a $D018 to COLPF2.
Zmiana $D018 nie zmienia adresu fontu; błędny komentarz w źródle poprawiono.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS: cały utwór, 15 965 064
identycznych bajtów stereo POKEY względem v035. To kontrola regresji
emulatora, nie potwierdzenie zachowania fizycznego loadera AVG.
