# V239 — kiść i banan obrany do połowy, wymiennie

Kiść pozostaje. Co drugie widoczne wejście bananowego rotatora pokazuje
pojedynczy owoc obrany do połowy: jasny miąższ, żółtą dolną część oraz
trzy wywinięte płaty skórki. Zmiana motywu następuje przy kolejnym wejściu,
bez przełączania w trakcie obrotu. Oba warianty zachowują **32 klatki,
pełne 360° i zegar jednej klatki na 16 ticków**. Brak ditheringu.

| Tick wejścia | Motyw |
|---:|---|
| 12288 | Kiść |
| 14336 | Obrany |
| 32909 | Kiść — cały odcinek do 35900 |
| 43008 | Obrany |
| 45056 | Kiść |
| 47104 | Obrany |
| 49152 | Kiść |
| 51200 | Obrany |
| 53248 | Kiść |

Wariant wynika z położenia na timeline, więc szukanie i ponowne wejście
dają ten sam obraz. Nie ma zależnego od historii licznika wejść. W całym
32909–35900 wymuszana jest kiść: globalny bit czasu nie przełączy jej
w środku sceny. Granice ujęć, tunele, piłka i satelity pozostają zachowane.

## Pamięć

Oba zestawy to łącznie 64 bitmapy po 3840 B, czyli 245760 B bez pakowania.
Zostały umieszczone w **dotychczasowych ośmiu bankach bananów** (loader
3–10). Każdy bank zawiera cztery fazy kiści i cztery odpowiadające im
fazy obranego owocu. Nie zabrano luk z innych banków ani rezerwy credits.

- Grafika RLE: **111114 B**.
- Kod i tablice: **1256 B na bank**, razem 10048 B.
- Łączne zajęcie: **121162 B ze 131072 B**.
- Pozostaje **9910 B = 9,68 KiB** rozproszonych luk w tych bankach.
- Względem v236 odzysk netto 9902 B, mimo dodania drugiego pełnego motywu.
- Główny kod nadal 2521 B; liczba wszystkich banków nie wzrasta.

Obrany wariant zaczyna w przeciwnej fazie obrotu i zoomu, aby duże/gęste
klatki obu motywów nie wypadały w tym samym banku. To przesunięcie całego
cyklu, bez skracania liczby klatek ani naruszania jego ciągłości.

## Dekoder i bufory

Wstępne LZ w roboczych v237/v238 mieściło grafikę, lecz przekraczało
dotychczasowy koszt CPU. W v239 zastosowano prostsze RLE: literalne bajty
oraz powtórzenia jednego bajtu. Dekoder kopiuje serie od końca przez
DEY/BPL; brak zależności między bajtami pozwala uniknąć kosztu testowania
dodatkowego licznika. Nie korzysta ze strony zerowej ani scratcha NMI.
Upakowanie dobiera próg powtórzeń w ramach limitu każdego banku, przeznaczając
wolne bajty na szybszy strumień dla najdroższych klatek.

Wejście $7C00 pozostało dla głównego callbacku. Helper bananowy jest pod
$7840–$7BFE, kopia/wybór źródła $7C80–$7C9B, dekoder $7D00–$7D90,
osiem par wskaźników $7F80–$7F8F. Dane kończą się najpóźniej pod $7840.
W banku 0 wypełniają tę przestrzeń dokładnie; assert chroni granicę kodu.

Wariant ma prywatny klucz $0DDD i cache $0DDE. Po wyjściu wspólny klucz
$83FA jest unieważniany, więc nie może udawać cache szkoły lub klatek
szarf o tych samych wartościach. Przed pominięciem kopiowania sprawdzana
jest również własność aktywnej display listy. Rozpakowywany jest wyłącznie
nieaktywny framebuffer; PORTB nadal zachowuje istniejący wrapper NMI.

## Weryfikacja

[ODCZYT] Nowe testy porównują wszystkie 64 działające klatki z generatorem,
pilnują limitu 90000 cykli, braku zapisów do frontu, naprzemienności wejść,
braku zmiany w środku aktu 5 oraz skoków między motywami/szkołą/szarfami.
Przerwania oryginalnego dekodera muzyki są wstrzykiwane podczas rozpakowania;
po każdym wraca ten sam bank, a gotowa bitmapa pozostaje prawidłowa.

[ODCZYT] Pomiar CPU przy 32 kolejnych fazach: pierwsze dwie klatki kiści
87875/88112 cykli; późniejsze maks. 78748. Obrany wariant maks. 78599
po przygotowaniu układu. To koszt CPU bez ANTIC DMA, nie pomiar FPS.

[ODCZYT] Osiem banków obu tuneli identycznych bajtowo z v236.
Atari800 PAL/1088XE, stereo POKEY: **11 570 400 identycznych bajtów**
względem v035, cały utwór. Bez próby na fizycznym Atari.

Podglądy CPU/PMG: `build/banana-v239-variants.png`,
`build/banana-v239-bunch.gif` i `build/banana-v239-peeled.gif`.

[ODCZYT] Pełna regresja: **181/181 testów**, bez pominięć, 133,7 s.
Build roboczy i v239 są identyczne. SHA-256:
`37cd975c936cadf7e1a4e6a3e4167af0441471d72f0324692335234a36a9c7dd`.
