# V181 — spacer i kadrowanie z v175

[ODCZYT] Przywrócono wszystkie 18 bocznych klatek dziewczyny bezpośrednio
z zachowanego XEX-a v175: kierunek, proporcje postaci, położenie kamery i
przesunięcia tła są identyczne. Źródło klatek zachowano w
`assets/art/reference/v175/arena-pan.bin`; generator ponownie pakuje je
w dotychczasowe pięć banków panoramy, z bieżącym kontrolerem.

Ujęcia chłopca i dziewczyny wróciły do kolejności i skal z v175. W sekwencji
oddalania skorygowano położenia dziewczyny: środek jej stóp dochodzi do
lewych drzwi areny, w pobliżu logicznego punktu (82,52). Poprzedni punkt
końcowy (64,48) wypadał przy słupie obok wejścia. Duży pierwszy plan oraz
portret chłopca zachowują swoje kadrowanie. Maska kurtki obejmuje całe
wnętrze prowadzącego konturu tułowia; czarne włosy nadal są kryjące.

Znormalizowano też podgląd nut do faktycznego wyświetlania szkolnego ujęcia:
każdy logiczny wiersz jest powtarzany trzykrotnie, jak w display liście.
Wygląd nut w XEX-ie pozostaje taki jak przed tą normalizacją.

## Build i sprawdzenie

- `build/visual-prototype-v181.xex` i odpowiadający JSON.
- SHA-256: `c43fb25f554f3c48d02041b9b2fb90852cbaaad0079d3a3900d4cc9e7f8324cb`.
- 275 współdzielonych wierszy, 10 630 B danych wierszy, 2552 B kodu.
- Bez zmiany ticków, granic aktów oraz przydziału banków; dłuższy tunel v180
  pozostaje aktywny.
- Porównanie 64 banków z v180: zmieniły się wyłącznie banki panoramy 19–23;
  pozostałe 59 banków jest identyczne bajt w bajt.
- Sześć testów zaliczonych: 18 klatek panoramy po callbacku, porównanie
  z archiwalnymi bankami v175, krycie włosów/kurtki w obu pozach chłopca,
  kompozycja spotkania, kadrowanie pierwszego planu oraz zbieżność toru
  dziewczyny do wejścia.
- Podgląd po wykonaniu callbacków 6502: `build/v181-opening-preview.png`.
  py65 nie modeluje DMA ANTIC ani rzeczywistego FPS.
- Próba porównania stereo POKEY w Atari800 zakończyła się przed startem
  emulatora: zainstalowane AppImage wymaga niedostępnego FUSE. W tym wydaniu
  nie potwierdzono odtwarzania emulatorowego ani sprzętowego.
