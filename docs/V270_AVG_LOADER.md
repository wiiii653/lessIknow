# V270 — wcześniejszy ekran ładowania i diagnostyka AVG

Użytkownik zgłosił brak napisu przy starcie z AVG, na Atari z 1088 Rambo.
W v269 ekran pojawiał się dopiero po pierwszym INIT oryginalnego playera.
Ten INIT przed powrotem wykrywa 14 banków i przy niepowodzeniu nie wraca.
Brak napisu jest więc zgodny z zatrzymaniem na tej ścieżce, ale go nie dowodzi.

Warianty release 010 inicjują ten sam ekran przed pierwszym INIT, utrzymują
DMA w początkowej próbie i po błędzie tej próby wyświetlają BANK TEST FAILED.
Oddzielny mały XEX `avg-first-bank-diagnostic-001.xex` sprawdza wyłącznie tę
pierwszą próbę i kończy ekranem BANK TEST PASSED albo BANK TEST FAILED.
Nie sprawdza pozostałych 50 banków ani całego demoscenowego loadera.

[ODCZYT] Model CPU uruchomił obie ścieżki diagnostyki: 14 rozdzielonych
banków daje PASSED, pamięć aliasowana daje FAILED. Siedem testów rotatorów
na XEX stereo v270 zaliczono. Atari800 PAL/1088XE, Altirra OS: 15 795 144
identycznych bajtów stereo POKEY względem v035, cały utwór.

[OGRANICZENIE] Brak próby AVG i fizycznego Rambo. Wczesny napis i komunikat
zawężają diagnozę; nie stanowią dowodu usunięcia zgłoszonej awarii startu.
