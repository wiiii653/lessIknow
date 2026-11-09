# V198 — tęczowe kolory obiektów w finale

Gwiazdy, nuty i klucz wiolinowy orbitujące wokół głowy dostają żywą, cykliczną
paletę 19 kolorów GTIA. Cztery obiekty mają przesunięte fazy, więc kolory
płyną niezależnie przez pełne spektrum. Paleta współpracuje z dotychczasowym
wygaszeniem.

Zmieniły się wyłącznie bajty palety: 19 B w danych banku 49. Orbita, rytm
przełączania gwiazdek i nut, maski PMG, bitmapa, wygaszenie oraz kod pozostają
jak w v197. Build: `build/visual-prototype-v198.xex`, para dev zaktualizowana.

[ODCZYT] Dziesięć testów finału przechodzi. Test palety sprawdza pełne 19
kolorów, co najmniej 16 odcieni oraz poprawną jasność do nałożenia fade'u.
