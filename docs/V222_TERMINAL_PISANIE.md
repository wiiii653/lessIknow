# V222 — piszący terminal z kursorem i Enterami

Credits i greetz pojawiają się znak po znaku. Zielony blokowy kursor miga
bezpośrednio za ostatnim wpisanym znakiem. Po krótkiej pauzie zaczyna się
kolejny wiersz (`Enter`). Greetz przewijają historię dopiero po wypełnieniu
pięciu wierszy; poprzednie linie nie są przepisywane od początku. Kursor
zostaje przy ostatniej linii do rozpoczęcia następnej. Zachowano falowanie
tekstu, stałe dolne położenie chłopca i zakończenie napisów przy 59085.

Terminy kolejnych linii są zapisane w tickach playera: odstęp 112 ticków
w creditsach i 96 ticków w greetz. Jeden znak jest wpisywany co 2 ticki.
Nagłówki credits pozostają w oknach 53850 / 54847 / 55844 / 56842.
Nie przesunięto granic aktów ani muzyki. Nie dodano dźwięków klawiatury.

## Pamięć i źródła

- `tools/terminal_typing.py`: 156 B kodu pod `$EB44–$EBDF`, w powiększonej
  o 32 B rezerwie helpera intro (1824 B). Istniejący kod efektu intro nie
  zmienił się; pulę współdzielonych wierszy przesunięto o 32 B.
- Harmonogram 88 B pod `$23CE` i długości 43 B pod `$2426` wykorzystują
  nieużywany kod starego UI. Jego wejście `$23CD` zawiera teraz RTS.
  Główny callback UI został zastąpiony już w starszych wydaniach.
- `$2D00–$2D26`, stary initializer fontu z wyłączonym wywołaniem `$218F`,
  przechowuje część spakowanego strumienia. Nie wolno ponownie włączać
  starego UI/fontu bez przywrócenia jego kodu i zmiany przydziału.
- Ekran terminala: `$BF00–$BFC7`, w zwolnionym drugim buforze bitmapy.
  Cursor `$A0` to inverse-space ANTIC 2, niezależny od PMG wokół głowy.
- `$0DD8`: robocza liczba odsłoniętych znaków. Kod zachowuje X (numer wiersza)
  i przekazuje adres wiersza przez istniejące `$0DD3–$0DD4`.
- Nie zajęto nowych banków rozszerzenia. Kontrole kolizji pamięci przechodzą.

## Walidacja

[ODCZYT] V221: pełny zestaw 158 testów — OK, 113,2 s.
[ODCZYT] V222 po dopracowaniu długości linii i kursora: 44 testy terminala,
scen, PMG, budżetów i regresji — OK, 18,6 s.
[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 11 518 128
identycznych bajtów względem v035, cały utwór. To nie jest próba na
fizycznym Atari.

Build: `build/visual-prototype-v222.xex`.
Animowany podgląd rekonstrukcji CPU/ANTIC: `build/terminal-v222.gif`.
Statyczny podgląd: `build/terminal-v222-preview.png`.
