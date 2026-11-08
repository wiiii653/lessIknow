# V177 — produkcyjna grafika postaci

Zastąpiłem próbne grafiki postaci w otwarciu i sekwencji koszykówki nowymi
źródłami RGBA:

- Chłopiec: portret na przezroczystej warstwie, patrzy w lewo, mruga i gwiżdże.
- Dziewczyna: arkusz 2×2 czterech póz chodu w lewo, w kurtce z emblematem Fuji.
- Koszykarz: sześć pełnych póz do kozłowania, nabrania rozpędu i wsadu.

Prawdziwe kanały alfa tworzą od nowa maski postaci. Usunąłem prowadzące
wielokąty, które wybierały elementy postaci i tablicy ze starych teł. Koszykarz
jest teraz składany bezpośrednio na płycie hali, a obręcz i tablica są rysowane
osobno na tej płycie. Pęknięcie tablicy, lot piłki i satelity korzystają z
tych samych faz oraz ticków.

Źródła:

- `assets/art/source/act1_boy_whistle_v177.png`
- `assets/art/source/act1_girl_walk_cycle_v177.png`
- `assets/art/source/act3_basketball_hero_v177.png`

Podglądy złożenia bitmapowego (nie są zrzutami emulatora):

- `build/v177-opening-cast-preview.png`
- `build/v177-arena-walk-preview.png`
- `build/v177-basketball-preview.png`

Build:

- XEX: `build/visual-prototype-v177.xex`
- 292 z 309 współdzielonych wierszy; 10 919 B danych skanlinii
- 2 552 B kodu głównego
- Banki i timeline bez zmian
- SHA-256: `2d867354e852762a20ef3e6119a851021353514012963efb883920305048172b`
- Budowa zakończona powodzeniem. Testów i odtwarzania emulatorowego nie
  uruchomiono.
