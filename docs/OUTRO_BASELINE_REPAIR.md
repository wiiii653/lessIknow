# Zabezpieczenie bazy przed creditsami

- Kontrola przydziałów obejmuje teraz `$9000–$AEFF` i `$B000–$CEFF`.
  Statyczny blok pod `$C000` jest odrzucany przed utworzeniem pliku.
- Model `quarter_at` respektuje bramkę połowy kroku występującą w działającym
  selektorze 6502. Nie zmieniono selektora ani momentów odtwarzania w XEX.
  Raportowana wcześniej „ćwierć” jest w aktualnym odtwarzaniu wybierana od
  połowy kroku; to opis stanu, a nie poprawka dynamiki animacji.
- Testy uwzględniają wszystkie strumienie współdzielące banki 32–35 i faktyczne
  położenie dodatkowych czterech strumieni za danymi tych samych banków.
- Limit regresji CPU scen 10–11: 25000 cykli wobec pomiaru 23954.
  To próg regresji CPU z zapasem poniżej 5%, nie gwarancja ramki z ANTIC DMA.
- Porównania między wydaniami opierają się na dostępnej v198. Sprawdzają
  bitmapy, oba bufory PMG, rejestry GTIA, powroty PORTB i koszt callbacków.
- [ODCZYT] Build `/tmp/visual-prototype-memory-guard.xex` jest bajt w bajt
  identyczny z archiwalną v198 (`cmp`).
- [ODCZYT] Dwa testy kolizji pamięci oraz trzy porównania z v198 przechodzą.

Credits/greetz nadal nie są podłączone; eksperymentalnej v199 nie wydawać.
- [ODCZYT] Pełny przebieg: 149 testów, zero błędów, 3 historyczne pominięcia
  porównań z v126 (106,5 s). Po zastąpieniu tych porównań trzema testami v198
  ich osobny przebieg również zakończył się powodzeniem; nowe dwa testy
  kontroli kolizji przeszły osobno.
