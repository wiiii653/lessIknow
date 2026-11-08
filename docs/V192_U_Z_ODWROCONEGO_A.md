# V192 — U z odwróconego A

Glif U w BUM jest wyliczany z rzeczywistego A używanego w BAM:
odwrócenie w pionie i zastąpienie wiersza poprzeczki bocznymi kreskami.
Wiersze logiczne U: CC CC CC CC CC CC 78. Podwojenie wierszy PMG,
szerokość komórki i położenie napisu pozostają takie jak w v191.

- `build/visual-prototype-v192.xex` i JSON; dev identyczny.
- SHA-256: `c6e8921b7fc3f12ec7a92c380da8e48e9371e7eb668b3c41b30e377783cb1cfa`.
- 12 testów zaliczonych: odwrócenie A i brak poprzeczki także w faktycznych
  danych PMG, centrowanie BUM/BAM, rozrzut przy pięściach i animacja dymków.
  Log: `build/v192-focused-check.log`.
- Bez zmiany kodu Atari, przydziału banków i synchronizacji. Nie wykonano
  nowego porównania muzyki ani pełnego zestawu po zmianie pojedynczego glifu.
