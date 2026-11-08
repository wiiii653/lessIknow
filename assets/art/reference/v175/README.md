# Zachowane kadry v175

Wydzielone z `build/visual-prototype-v175.xex`, SHA-256:
`acb1f03deea22c6c747b5438b4dd75ad214ad834ca67be3365acbfcea0157675`.

- `arena-pan.bin`: 18 kolejnych klatek 160×64, 2 bity/piksel, 2560 B/klatkę.
  Zawartość obrazów banków loadera 19–23, bez kodu kontrolera. Używana przez
  bieżący build do zachowania dokładnego spaceru z v175.
- `encounter.bin`: sześć kadrów spotkania, 160×192, po jednym indeksie
  koloru 0–3 na piksel. Odtworzone z tabel adresów wierszy JSON i segmentów
  XEX. Referencja kompozycji; bieżący build generuje te kadry z poprawionymi
  maskami oraz torem dziewczyny prowadzącym do drzwi.

- `basketball.bin`: 12 988 B z banku loadera 1, $4B80–$7E3B. Pięć pełnych
  klatek 160×56 (2 bity/piksel), trzy łaty kozłowania 44×28 i trzy łaty
  rozbijanej tablicy 48×24. Odtwarza osiem póz postaci oraz trzy fazy szkła.
  SHA-256: c55b76ee9af23689177155f1ebc3aea84866f2733a47c82394ab17f2c009e09b.
