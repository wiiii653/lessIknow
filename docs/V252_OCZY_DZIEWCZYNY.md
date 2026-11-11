# V252 — oczy dziewczyny w montażu

[ODCZYT] W tickach 39379–40126, w istniejącym montażu po Trevorze,
pojawia się czterofazowe zbliżenie oczu: spojrzenia w boki i mrugnięcie.
Kolejna faza co 32 ticki. Zachowany jest dotychczasowy cykl barw i piłka
PMG z satelitami na pierwszym planie. Granice scen i zegar muzyki bez zmian.
Podgląd `build/v252-eyes-preview.png` przedstawia grafikę źródłową w
umownych barwach, bez PMG; nie jest obrazem z emulatora.

[ODCZYT] Cztery bitmapy zajmują dotychczasowe sloty 60–63 organicznego
tunelu w loader banku 18. Poza ujęciem oczy te ID są mapowane na fazy 56–59;
ostatnie cztery fazy organicznego tunelu zastąpiono więc powtórzeniem
wcześniejszych faz, również w krótkim ujęciu tunelu po wyrzucie. Nie jest to
odtworzenie tunelu bajt w bajt. Mapper w banku 2 zaczyna się w `$7500`, a
trampolina w RAM pod OS w `$EC04`. Jest sprawdzanie kolizji przy instalacji.
Bez dodatkowego banku; główny kod pozostaje 2560 B.

[ODCZYT] Testy wybranych callbacków sprawdzają cztery bitmapy, granice okna,
przywrócenie PORTB oraz wybór pozostałych klatek. Próba pełnego porównania
stereo w Atari800 nie wystartowała: lokalny AppImage wymaga niedostępnego FUSE.
Nie sprawdzono płynności obrazu ani odsłuchu na fizycznym Atari.

[ODCZYT] Późniejsze porównanie v253, zawierającego scenę oczu, z v035 w
Atari800 przeszło dla całego utworu (stereo POKEY); patrz dokument v253.
