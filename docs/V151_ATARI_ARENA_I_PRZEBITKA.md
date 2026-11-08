# V151 — ATARI ARENA, przebitka i szybki wsad

## Zatwierdzony montaż

Użytkownik poprosił o krótką przebitkę tunelu z piłką po wyrzucie,
z zachowaniem długości wyrzutu, oraz o skrócenie rozciągniętej sceny wsadu.
Przebudowano wnętrze aktu 3 bez przesunięcia wejścia Trevora ani muzyki:

| Ticki (koniec wyłączny) | Takty | Długość nominalna | Obraz |
|---|---|---|---|
| 17950–20942 | 48–56 | 15 s | Dotychczasowy taniec i pojedynczy wyrzut; bez zmiany długości i faz lotu |
| 20942–21690 | 56–58 | 3,75 s | Przebitka spiralnego tunelu z neonową piłką v150 |
| 21690–23186 | 58–62 | 7,5 s | Kozłowanie we wnętrzu ATARI ARENA |
| 23186–23934 | 62–64 | 3,75 s | Pojedynczy wsad, pęknięcie i rozpad tablicy |
| od 23934 | od 64 | bez zmiany | Ciche wejście Trevora |

Wsad trwa o połowę krócej: jego faza rośnie co 8 ticków, dawniej co 16.
Sekwencja pozostaje kompletna: przygotowanie, dwa etapy lotu, kontakt,
pęknięcie, rozpad i opadanie piłki. Nie wycięto końca rozbicia tablicy.
Przebitka wykorzystuje wszystkie 32 fazy istniejącego tunelu i piłkę v150;
nie zajmuje nowych banków na kolejne bitmapy.

## Grafika i logo

Fikcyjna ATARI ARENA zastępuje szkołę w istniejących ujęciach zewnętrznych
2992–5984. Fasada jest inspirowana owalną bryłą ERGO ARENY, z pasami szkła,
niskim dachem, dużym napisem i Fuji nad wejściem. Chłopiec, ruch dziewczyny,
przewijanie planów i odchodzenie w głąb zachowują dotychczasową choreografię.
Na plecach dziewczyny duże Fuji zastępuje NORTH; mniejszy znak jest też
na kurtce w bocznym ujęciu.

W akcie 3 nowe wnętrze ma duże trybuny, kratownicę dachu i podwieszony ekran
ATARI ARENA. Dalsze rzędy widowni są uspokojone przy redukcji do palety Atari,
żeby postać pozostała czytelna. Zawodnik i kosz pochodzą z dotychczasowych
ilustracji, z oddzielnymi maskami; animowane ramię nadal korzysta z tego
samego niewielkiego patcha. Po wybiciu tablicy odsłania się właściwe tło areny.

Źródła architektury: oficjalna [fasada ERGO ARENY](https://ergoarena.pl/wp-content/uploads/2024/07/Rectangle-14.jpg)
i [wnętrze podczas koszykówki](https://ergoarena.pl/wp-content/uploads/2024/09/Arena-Glowna5.jpg).
To inspiracja ilustracji, nie dokumentalna rekonstrukcja obiektu.

Obie ilustracje wykonano wbudowanym `image_gen.imagegen`:

- [Fasada](../assets/art/source/act1_atari_arena_exterior_v151.png),
  [pełny prompt i referencje](../assets/art/source/act1_atari_arena_exterior_v151.prompt.txt).
- [Wnętrze](../assets/art/source/act3_atari_arena_interior_v151.png),
  [pełny prompt i referencje](../assets/art/source/act3_atari_arena_interior_v151.prompt.txt).

Źródła pozostają w repozytorium, stare ilustracje są zachowane.
`tools/arena_art.py` wykonuje docelową kwantyzację, compositing i nakładanie
małych znaków Fuji. Makefile przygotowuje dwa surowe wejścia RGB.

## Pamięć i kod

[ODCZYT] Nadal 64 banki. Bitmapy areny zastępują dotychczasowe dane
w istniejących strukturach, a przebitka współdzieli banki tunelu i piłki.

- Główny kod: 2546 B (`$1400–$1DF1`), +31 B; **14 B** przed pulą `$1E00`.
- Helper hero w banku loadera 1: 2652 B (`$4000–$4A5B`), +15 B.
  Do danych od `$4B80` pozostają 292 B. Dane i trzy patche rozbicia tablicy
  nadal kończą się na `$7E3B`.
- Wspólne wiersze: 279 zamiast 277; spakowane zajmują **10 927 B** zamiast
  10 998 B, czyli oszczędzają 71 B. Liczba wpisów tablic scen nie rośnie.
- Zmiana netto względem v150: +31 +15 −71 = **−25 B zajętości**.
  Odzysk względem v141: **23 671 B = 23,12 KiB**. Nie oznacza wolnego banku.

Bankowany hero przekazuje początkowe dwa takty do niebankowanej trampoliny,
która uruchamia normalny renderer tunelu. Zagnieżdżone powroty odtwarzają
PORTB. Wybór fazy uwzględnia oba bajty ticka, także przejście przez `$xxFF`.
Cztery aktualizacje muzyki na klatkę PAL i układ DLI są zachowane.

## Walidacja

[ODCZYT] `make check`: **116 testów, 113 zaliczonych, 3 pominięte**
(brak archiwalnego v126), 86,535 s. Testy obejmują niezmieniony koniec
wyrzutu, granice przebitki/kozłowania/wsadu, wszystkie pozy i fazy
rozbicia tablicy, zgodność buforów z grafiką, duże Fuji, PORTB,
wstrzykiwanie NMI oraz późny VCOUNT piłki.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
**15 154 704 identyczne bajty** względem v035; objęty cały utwór.
Końcowy rebuild jest identyczny z binarnym plikiem objętym porównaniem.
Nie wykonano odsłuchu ani testu na fizycznym Atari. Testy py65 nie modelują
DMA ANTIC i nie ustalają rzeczywistego FPS ani stabilności rastra na sprzęcie.

## Wydanie i podglądy

- `build/visual-prototype-v151.xex` z odpowiadającym JSON.
- `build/v151-arena-exterior.gif` — cały odcinek przed areną.
- `build/v151-launch-tunnel-dunk.gif` — koniec wyrzutu, przebitka i akt 3.
- `build/v151-atari-arena.png` — fasada, duże Fuji i wnętrze.

GIF-y odtwarzają się jednokrotnie; powstają z callbacku 6502 z krokiem
16 ticków. Kolory i tempo są przybliżone; to nie nagranie emulatora.

SHA-256 XEX: `52c99b69e13b70fc8b3d8af9d591b8aa34ce4de68b6fba956ee4f5325a0bf52f`.
Numerowane XEX/JSON są identyczne z roboczymi `visual-prototype-dev`.
