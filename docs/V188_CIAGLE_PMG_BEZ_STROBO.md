# V188 — usunięta przerwa w wyświetlaniu nut

## Przyczyna i poprawka

Główna ścieżka `colors` zerowała GRACTL ($D01D) i wyłączała DMA PMG
przez zapis $22 do DMACTL ($D400), zanim wywołała renderer nut. Ten
przygotowywał drugi bufor i czekał na następną bezpieczną fazę blankingu.
W efekcie buforowanie działało, ale poprzedni obraz był już wyłączony.

Ślad instrukcji v187 z poruszającym się VCOUNT pokazał wyłączenie PMG
na 267–313 linii, czyli niemal całą klatkę PAL. Statyczne podglądy oraz
dotychczasowe testy sprawdzały stan po zakończeniu callbacku i pomijały
ten okres. To był błąd kolejności sterowania DMA, niezależny od nut i masek.

V188 omija te dwa resety w scenach gwizdu 10–11. Poprzedni bufor nut
pozostaje aktywny podczas budowania następnego i oczekiwania na blanking.
Po przygotowaniu obrazu następuje przełączenie PMBASE i rejestrów.
Przy wyjściu do sceny 12 resety nadal działają i melodia kończy się przy
drzwiach. Rozmiary, kolory, kształty i tory v187 pozostają zachowane.

## Dowody i testy

- `build/v187-whistle-raster-audit.json`: okresy wyłączenia 267–313 linii.
- `build/v188-whistle-raster-audit.json`: zero wyłączeń GRACTL/DMACTL
  podczas ciągłego gwizdu.
- Nowy `tests/test_whistle_raster.py` odtwarza błąd na v187:
  `build/v187-whistle-raster-regression.log`.
- Na v188 przechodzi 48 przypadków: 3 ticki (w tym zmiana bitmapy),
  8 początkowych pozycji rastra i warianty z opóźnieniem 0/5000 cykli.
  Test śledzi wszystkie zapisy w trakcie callbacku: brak wyłączeń DMA,
  nietknięty stary bufor, publikacja wyłącznie po ukończeniu nowego
  i w dolnym blankingu, zachowane PORTB.
- Osobny test potwierdza wyłączenie melodii przy drzwiach.
- 19 ukierunkowanych testów zaliczonych, łącznie z dotychczasowymi testami
  nut, masek, panoramy, piłki i przesuwającego się rastra tunelu.
  Log: `build/v188-focused-check.log`.
- Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 16 336 440 identycznych
  bajtów względem v035, cały utwór. `build/v188-playback-check.log`.
- `make check`: 142 testy, 129 zaliczonych, 10 niezaliczonych,
  3 pominięte z powodu braku v126. Zestaw nazw niezaliczonych testów jest
  identyczny jak w v186; dotyczą wcześniej opisanych testów koszykówki,
  szarf, pamięci, progu CPU i starego progu aktu 5.
  Log: `build/v188-check.log`; szczegóły wcześniejszych usterek w raporcie v186.

Śledzenie VCOUNT jest symulacją czasu CPU z syntetycznym opóźnieniem,
nie pełnym modelem DMA ANTIC. Nie wykonano oceny na fizycznym Atari.
Zgodność POKEY nie stanowi dowodu płynności rastra.

## Build i pamięć

- `build/visual-prototype-v188.xex` i JSON; dev identyczny.
- SHA-256: `172e97bd75b3c188b6bf815e3dbc5b116b311ad15a75bb5f10bdec16605de6b1`.
- Poprawka zajmuje ostatnie 8 B głównego kodu: 2560 B w $1400–$1DFF.
  Przed pulą wierszy $1E00 nie ma już zapasu.
- Bank 0 zawierający nuty jest identyczny bajt w bajt z v187. Wywołania
  pomocnicze w innych bankach mają przeliczone adresy etykiet przesuniętych
  w kodzie głównym. Przydział banków oraz 298 wierszy / 11 480 B bez zmian.
