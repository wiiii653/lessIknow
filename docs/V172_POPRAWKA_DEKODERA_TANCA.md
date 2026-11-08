# V172 — poprawka routingu dekodera tańca

## Przyczyna błędu v171

Nowe klatki solówki były skompresowane i umieszczone w ogonach banków 8–11,
które należą do sześciu banków bitmap tańca. Selektor po ich wyborze uruchamiał
dekoder pod `$5E00`, ale w tych bankach ten adres zawiera grafikę, a nie kod
dekodera. Procesor wykonywał więc bajty obrazu jako instrukcje. To był błąd
adresowania banku, nie wyczerpanie pamięci.

## Poprawka

Cztery strumienie pozostały w szybkiej postaci LZ, ale zostały przeniesione do
wolnych ogonów loader indices 32–35, bezpośrednio za dotychczasowymi
kompozycjami. Te banki już zawierają dekoder pod `$5E00`. Selektor, ID klatek,
timingi i bitmapy pozostają te same. Oryginalne banki 8–13 znów zachowują
niezmienione sześć klatek i pełny, wolny ogon 1 KiB każdy.

Nowe dane zajmują 970, 940, 889 i 1006 B. Końce payloadów pozostają poniżej
`$5400`; sterownik każdego banku nadal mieści dekoder pod `$5E00–$5E8B`.
Łączne potwierdzone wolne luki: 27 463 B. Długość sceny i wszystkie ticki
pozostają bez zmian.

## Wydanie i walidacja

Poprawiony XEX: `build/visual-prototype-v172.xex`.

Budowa zakończyła się poprawnie, 309 współdzielonych wierszy, 2552 B kodu.
Próba uruchomienia testów py65 nie doszła do wykonania: środowisko nie ma
zainstalowanego `py65`, więc moduł testowy nie może zaimportować `TrackedMemory`.
Nie potwierdzono jeszcze odtwarzania w emulatorze ani na Atari.
