# V250 — płynne orbity na nowe linie terminala

Każda z 34 wypisywanych linii credits/greetz wybiera nowy kształt orbity
gwiazdek i nut. Cel różni się zarówno od bieżącego kształtu, jak i od
poprzedniego celu. Promienie w poziomie i pionie zmieniają się po jednym stopniu co
16 ticków, bez skokowej zamiany pozycji. Powtórny callback w tym samym
ticku nie przyspiesza zmiany. Po ostatniej linii orbity nadal krążą; fade,
kolory, bitmapa chłopca, treść i wszystkie granice scen są zachowane.

## Pamięć i weryfikacja

Helper, czasy 34 linii i tablice ośmiu kształtów zajmują 600 B w banku 49
`$66A0–$68F7`, po helperze Trevora kończącym się `$6697`. Bieżące pozycje
i stan są w `$69B8–$69C3`, przed istniejącymi danymi `$69C4`. Instalator
sprawdza oba obszary. Helper używa `$0DD8–$0DD9` jako scratch przed osobnym
wywołaniem terminala, który następnie wykorzystuje te same bajty. Kontroler
finału ma 700 B, nadal mieści się w swoim
dotychczasowym zakresie; main pozostaje 2560 B, liczba banków 64. Dane PMG
są przygotowywane w nieaktywnym buforze i publikowane w oknie blankingu.

[ODCZYT] Test modeluje wszystkie teksty, tempo zmian, powtórne callbacki,
powrót do sceny i pozycje czterech duszków. Pozostałe testy obejmują kształty
PMG, fade, wyjście do czerni, VCOUNT oraz muzyczne NMI.

[ODCZYT] W 128 callbackach od wejścia finału, po odrzuceniu inicjalizacji,
średni koszt wzrósł z 10 295 do 10 978 cykli py65; maksimum z 10 371 do
11 054. Jest to koszt CPU bez ANTIC DMA, nie pomiar FPS.

[ODCZYT] Atari800 PAL/1088XE stereo POKEY: 16 306 560 bajtów identycznych
z v035 przez cały utwór. Bez odsłuchu ani testu na fizycznym Atari.

[ODCZYT] Pełne `make check`: 192/192 testy, 151,229 s. Dodatkowy test
maksymalnego przesunięcia między sąsiednimi kształtami zaliczono osobno.
