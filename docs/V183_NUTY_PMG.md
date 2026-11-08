# V183 — nuty wylatujące z ust na PMG

Znaki wyglądające jak oczy nad wejściem były kluczami wiolinowymi z bitmapy.
Rysowano je dla 192 linii, po czym szkolny display list pobierał tylko co
trzecią linię. To usuwało większość kształtu. Bitmapową melodię usunięto.

Od ticku 5610, gdy dziewczyna dochodzi do drzwi, cztery players wyświetlają
nuty, parę nut oraz klucz wiolinowy. Emitowane są kolejno sprzed ust chłopca,
unoszą się w górę i w lewo, lekko kołyszą oraz zmieniają barwy. Cztery
missiles tworzą krótkie oderwane ślady pod znakami. Kadry spotkania i
panorama v175 oraz rytm dalszych scen pozostają zachowane.

Kod powstaje w `tools/whistle_pmg.py`. Zajmuje 835 B w dotąd wolnej luce
banku loadera 0, $6A00–$6D42. Wywołanie dodaje 10 B do bankowego dispatchera
efektów. Nie dodano banku ani kodu głównego. Renderer buduje nieaktywny
bufor PMG i publikuje go w dolnym blankingu; przełącza istniejące buforowanie
$0980–$0BFF / $8980–$8BFF. Nuty są wyłączane w następnym ujęciu (5984).

## Wynik

- `build/visual-prototype-v183.xex` i JSON; dev jest identyczny.
- SHA-256: `c98aad7de93b23c7cb8456bf89c7698ee3cc7cef53f6024b726930438ddb3ad5`.
- 316 wspólnych wierszy, 12 158 B danych wierszy, 2552 B kodu głównego.
- Porównanie banków z v182: zmieniony wyłącznie bank loadera 0; pozostałe
  63 banki są identyczne bajt w bajt.
- 13 testów CPU/renderowania zaliczonych: emisja przy ustach, ruch w górę,
  ślady missiles, naprzemienne bufory i zachowanie poprzedniego obrazu,
  brak bitmapowych nut na budynku, wyłączenie efektu po cięciu, reakcja
  chłopca, maski, dokładność panoramy v175 i regresje piłki.
- `build/v183-whistle.gif` i `build/v183-whistle-preview.png`: podglądy
  po wykonaniu kodu 6502, z nałożonym PMG. Nie modelują DMA ANTIC ani FPS.
- Nie uruchamiano ponownie emulatora; instalacja Atari800 ma znaną
  przeszkodę FUSE opisaną przy v181. Brak nowej walidacji sprzętowej.
