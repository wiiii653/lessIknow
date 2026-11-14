# v347 — dymki i kontrola tablicy

Przywrócono boczne dymki z v340, wyłączone omyłkowo w v346. Render PMG w py65 pokazuje cztery dymki przy wieku 56 i 72 ticków; w ujęciu oczu wybierana jest piłka. Wygląd na sprzęcie nie został zweryfikowany.

Bank wsadu w v347 jest identyczny bajt po bajcie z v330. Porównanie py65 wszystkich 94 faz wsadu, z PMG, nie wykazało różnic w pikselach względem v330. Nie zidentyfikowano w ten sposób przyczyny zgłoszonych artefaktów na tablicy; potrzebny jest obraz problemu. Dwa testy sceny wsadu przeszły. Test directora wymaga stałego zasłonięcia środka tunelu także w ujęciu oczu, gdzie piłka celowo się przemieszcza, i zgłosił tam błąd; pozostałe trzy testy przeszły.

Build stereo `build/visual-prototype-v347.xex`; SHA-256 `51be93153eb50a50ac6c2dab90e9dc3555c523d6c093c9d46cc1db60cfc99641`. Generator: 298 współdzielonych wierszy i 2560 B kodu. Nie uruchamiano emulatora ani fizycznego Atari.
