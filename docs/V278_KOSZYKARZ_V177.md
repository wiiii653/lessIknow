# V278 — koszykarz v177 w kozłowaniu i wsadzie

Sześć póz z warstwy RGBA v177 jest składanych na istniejącym tle ATARI
ARENA. Kozłowanie korzysta z trzech pełnych póz: pozycja wyjściowa,
druga pozycja, przysiad i powrót przez drugą pozycję. Wsadowi przypadają
przysiad, dwie fazy lotu i finałowa poza. Czas ujęć i piłki nie zmienia się.

Wersja v177 używała zbyt małej łaty dla całych póz. W v278 dwie dodatkowe
pełne klatki (2 × 2240 B) zajmują wcześniej puste `$4A00–$52BF` i
`$5300–$5BBF` w banku loadera 0. Helper `$EC80–$ECDC` kopiuje je do
nieaktywnego bufora; zachowuje i przywraca bank. Osobne łaty pęknięć tablicy
uwzględniają piksele postaci. Nie dodano banku. Kod banku koszykarza zajmuje
2926 B (`$4000–$4B6D`), kończąc przed danymi `$4B80`.

[ODCZYT] Testy ukierunkowane obejmują wszystkie pozy podczas kozłowania,
klatki wsadu i tablicy, bufor niewidoczny, oraz przerwania muzyki w trakcie
kopiowania. Atari800 PAL/1088XE: 16 302 960 identycznych bajtów stereo POKEY
względem v035, pełen utwór.
[ODCZYT] Pełny zestaw: 200/200 testów w 145,144 s. Dodatkowy test przerwań
podczas pełnego kopiowania również zaliczony.

[OGRANICZENIE] CPU/py65 nie modeluje obciążenia DMA ANTIC i nie jest pomiarem
FPS. Nie wykonano odsłuchu ani oceny obrazu na fizycznym Atari. Bufor jest
większy niż stara łata ręki, więc rzeczywistą płynność należy ocenić na
docelowym sprzęcie.
