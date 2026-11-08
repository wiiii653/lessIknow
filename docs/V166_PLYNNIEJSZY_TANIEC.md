# V166 — rzeczywiste klatki pośrednie tańca

## Efekt i synchronizacja

Trzy późniejsze ujęcia tańca ze szarfami mają 14 nowych kompozycji
pośrednich. Dziewięć nowych anatomicznych póz bohaterki jest wykorzystywanych
w różnych skalach i układach grupy. Oryginalne pozy wchodzą na swoich
niezmienionych tickach `STEPS`, a nowe w połowie odstępów 46/47 ticków.
Daje to kolejne fazy ruchu co 23/24 ticki, około 0,117 s, bez zwalniania
choreografii i bez wydłużania scen.

Przejście między dwiema pozami wykorzystuje ten sam obraz pośredni także
w drugą stronę. Sześć obrazów dotyczy pierwszej grupy, cztery solówki,
cztery grupy przed wyrzutem. Identyczne kolejne pozy i cięcia między
ujęciami pozostają bez sztucznej interpolacji. Szybkie przygotowanie,
wyrzut i zbliżenie z góry zachowują wcześniejsze klatki i ticki.

Boczne ujęcie pozostaje bez zmian. Szarfy zachowują wcześniejsze ciągłe
maski i tęczowe DLI, natomiast kotwice dłoni pośrednich póz odpowiadają
nowym obrazom. Bitmapa i PMG są przygotowywane w nieaktywnych buforach;
na ekran trafia kompletny obraz z odpowiadającymi mu szarfami.

## Grafika źródłowa

Użyto wbudowanego narzędzia `imagegen`, zgodnie ze skillem imagegen,
na podstawie oryginalnego arkusza `act2_ribbon_dancer_v136.png`.
Nowy arkusz 3×3 zachowuje bohaterkę, strój i styl; przedstawia dziewięć
nowych faz ruchu pomiędzy używanymi pozami. Oryginalnego arkusza nie zmieniono.

- Źródło: [act2_ribbon_inbetweens_v166.png](../assets/art/source/act2_ribbon_inbetweens_v166.png).
- Pełny prompt: [act2_ribbon_inbetweens_v166.prompt.txt](../assets/art/source/act2_ribbon_inbetweens_v166.prompt.txt).
- Makefile przygotowuje `build/ribbon-inbetweens-v166.rgb`, siatkę 1329×1329.
- `ribbon_dance.actor(..., mid=True)` korzysta z tej samej skali i metody
  próbkowania, ochrony czarnych detali i keyline co wcześniejsze obrazy.
- Nowe kompozycje są zapisane jako natywne czterokolorowe bitmapy 160×64.

## Szybki format i banki

14 pełnych obrazów wymagałoby 35 840 B. Nowy prosty LZ przechowuje je
w **16 886 B**. Strumień zawiera dosłowne odcinki 1–128 B albo odwołania
wstecz do już odtworzonej bitmapy. Kopiowanie odcinka odbywa się w szybkiej
pętli indeksowanej Y. Encoder preferuje dopasowania co najmniej ośmiobajtowe:
mniejsze pliki z mnóstwem krótkich dopasowań zużywały więcej czasu CPU.
Każdy strumień jest przy budowie odtwarzany i porównywany z bitmapą.

[ODCZYT] Nowe dane mieszczą się w dotychczas wolnych lukach:

| Właściciel | Zakres | Zajętość |
|---|---|---:|
| Bank loadera 2: selektor, timingi, kotwice, deskryptory | `$4040–$4436` | 1015 B |
| Bank 2: pierwsze cztery obrazy | `$4600–$5AA6` | 5287 B |
| Bank 2: obrazy 4–6 | `$6000–$6E0E` | 3599 B |
| Banki 32–38: obrazy 7–13 | od `$4A00` w każdym | 8000 B |
| Bank 2 i 32–38: dekodery | `$5E00–$5E8B` w każdym | 8 × 140 B |

Razem **19 021 B wypełnionych dawnych luk bankowych**. Kontroler szarf
rośnie o 9 B: 2246 B, `$5400–$5CC5`, z 10 B przed kontrolerem finału
pod `$5CD0`. Główny kod pozostaje identyczny, 2546 B, z 14 B przed `$1E00`.
Liczba banków nadal 64. XEX przechowuje stałe pełne banki, więc mniejsza
zajętość danych w bankach nie oznacza analogicznego zmniejszenia XEX-a.

Niebankowany runtime pozostaje w swojej dotychczasowej rezerwacji
`$0C00–$0EFF`. Dodany wrapper/entry używa `$0D60–$0DB9` (90 B, razem
z wyrównaniem), prywatny workspace `$0DC0–$0DCF` (16 B), a dotychczasowy
kompozytor pod `$0E00` dostaje 11 B routingu. Nie rozszerzono runtime
ani puli głównego kodu. Właściciele luk są zaktualizowani w `AGENTS.md`.

[ODCZYT] Pozostałe potwierdzone luki w bankach:

| Obszar | Wolne |
|---|---:|
| Bank 2, poniżej oryginalnego helpera tunelu | 4251 B |
| Ogony bocznych aktorów i pozostałe części slotów 32–38 | 14 016 B |
| Pozostałości slotów starych masek piłek | 7212 B |
| Ogony sześciu oryginalnych banków tańca | 6144 B |
| **Łącznie** | **31 623 B = 30,88 KiB** |

Największa pojedyncza luka banku 2 to `$6E0F–$77FF`, 2545 B.
Nie traktować całego dawnego 14 KiB ani całych slotów Trevora jako wolnych.
Dokładne rozmiary każdego skompresowanego obrazu:
`build/v166-allocations.json`. Starsze „odzyski netto vs v141” dotyczą
historycznych bilansów, a nie pełnej bieżącej mapy wolnej pamięci.

## Wywołania, kotwice i cache

Oryginalne ID obrazów 0–35 i specjalne ID finału 36 pozostają niezmienione;
nie powiększano tabel w ciasnym głównym kodzie. Pythonowe ID 37–50 służą
opisowi/podglądowi nowych kompozycji. Runtime przechowuje w `$83ED` bazowy
numer starego obrazu, a w `$83E5` flagę `$80` klatki pośredniej.

Wrapper z `$0D60` zachowuje bank na stosie i wywołuje selektor banku 2.
Ten wybiera właściwy strumień i przygotowuje osiem kotwic. Po powrocie
wrapper przywraca bank kontrolera i aktualizuje jego metadane. Zwykłe
pozy zawsze odzyskują swoje oryginalne kotwice z niezmienionej kopii.
Cache uwzględnia flagę pośrednią, więc stara i nowa poza nie kolidują.

Kompozytor rozpoznaje flagę przed zwykłym kopiowaniem. Dla nowej klatki
wybiera bank strumienia i uruchamia lokalny dekoder; wyjście przechodzi
przez dotychczasowy niebankowany trampoline, który przywraca bank
kontrolera. Dla starych klatek, bocznego aktora i finału pozostaje poprzednia
ścieżka. NMI muzyki zachowuje wybrany bank, a kolory szarf korzystają
z dotychczasowego prywatnego stosu.

## Walidacja

[ODCZYT] Testy właściwe dla tańca: 24 zaliczone, 16,206 s.
[ODCZYT] Pełne `make check`: **132 testy, 129 zaliczonych,
3 pominięte** (brak archiwalnego v126), 101,725 s.

Sprawdzono wszystkie nowe kompozycje po callbackach 6502, timingi midpoint,
oryginalne akcenty i cięcia, pełną zgodność dekompresji, dopasowanie kotwic,
powroty do starych kotwic, cache, własność nieaktywnych bitmap/PMG,
przywrócenie PORTB, późny VCOUNT i wstrzykiwane prawdziwe NMI muzyki podczas
dekompresji zarówno z banku 2, jak i banku akcji. Maski szarf nadal mają
ciągłe pionowe odcinki bez brakujących wierszy.

[ODCZYT] Wszystkie sześć oryginalnych banków tańca i osiem bocznych
aktorów pixel/mask są identyczne z v165. Porównano też 32 kolejne próbki
bocznego ujęcia: identyczna bitmapa, aktywne PMG i wszystkie rejestry GTIA.
Zmieniły się banki loadera 2, 32–38 oraz 49 i używane luki runtime.
Główny kod jest identyczny z v165.

[ODCZYT] Najdroższy z 14 sprawdzonych callbacków nowej klatki:
**91 282 cykle CPU**; pozostałe 75 583–80 959. Trzymana klatka pośrednia
wykorzystuje cache i mieści się w 25 000 cykli. To koszty CPU w py65,
bez ANTIC DMA; nie są pomiarem FPS ani opóźnienia prezentacji w emulatorze.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
**15 057 720 identycznych bajtów** względem v035, około 4194,4 s emulacji,
obejmujące cały utwór. To porównanie danych rejestrów, bez odsłuchu.
Bez testu na fizycznym Atari; wyniki nie są deklaracją gotowości compo.

## Podglądy

- `build/v166-dance-v166.gif`: trzy nowe ujęcia po jednym cyklu tańca.
- `build/v166-dance-v165.gif`: te same ticki i ujęcia przed zmianą.
- `build/v166-inbetween-contact.png`: stara → pośrednia → stara poza.

Podglądy są wynikiem rzeczywistych callbacków 6502, z przybliżonym tempem
i paletą, bez emulacji DMA. Nie są nagraniem Atari800.

## Wydanie

`build/visual-prototype-v166.xex` i odpowiadający JSON są identyczne
z plikami dev. Po pełnych testach poprawiono wyłącznie raportowane pola
wolnej pamięci w JSON; ponowna budowa dała identyczny XEX, potwierdzony SHA-256.
Wcześniejsze wydania zachowane.

SHA-256 XEX: `edafa81faca46c2335cf2e21e9f2cc29d99da1060c6f3fd7ebbe3b27ff6489c1`.
