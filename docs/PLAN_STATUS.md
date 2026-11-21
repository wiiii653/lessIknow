# Stan projektu — kandydat po party v388

Terminal wchodzi w takcie 112 (tick 41884), zgodnie z wydaniem stereo 112.
Usunięto dodatkowe trzy takty rotatora. Napisy kończą się w ticku 51232,
a karta końcowa wchodzi w ticku 51980. W Atari800 PAL (1088 XE, Altirra OS,
stereo) pierwsze zaobserwowane wejście w scenę przypadło w obu wydaniach
na tick 41892. Porównanie z wydaniem 125 dało 4 696 416 identycznych bajtów
POKEY. Pełne `make check` zaliczyło 206 testów.

[Wydanie stereo 126](../releases/less-i-know-demo-release-126-stereo.xex)
ma 952 239 B. SHA-256
`dc4e3b5d00456b3d46999b09d8cc010c943baa3cfd95e885f1434b45089a86bd`.
Próba na fizycznym Atari pozostaje niewykonana.

## Przywrócenie oryginalnych tekstur bananów


Wydanie 125 przywraca oryginalną złotą kiść i obrany owoc z wydania 119.
Cała mozaika obraca się i skaluje wspólnie. Wszystkie 64 klatki odpowiadają
archiwum piksel w piksel. Zachowano wszystkie 46 cięć directora i 24 pola
czasowe z wydania 124. Pełne `make check` obejmuje 206 zaliczonych testów.
Kod główny ma 2542 B. Pula współdzielona ma 298 wierszy.
Atari800 PAL (1088 XE, Altirra OS, stereo) zarejestrował 3 051 000 bajtów
POKEY identycznych z wydaniem 124.

[Wydanie stereo 125](../releases/less-i-know-demo-release-125-stereo.xex)
ma 952 257 B. SHA-256
`dca3fff3b56b7d072e4a5c87ac3f5743ebf196e2488de6f65ee471c71c049b43`. Próba na fizycznym Atari pozostaje niewykonana.

## Niezależny obrót kiści

Wydanie 124 zachowuje reżyserię i 32 fazy kamery wydania 119. Każda kiść
ma własny ośmiobitowy kąt aktualizowany co 16 ticków playera. Pełny obrót
zajmuje 4096 ticków, około 20,5 s PAL. Renderer składa kąt lokalny z kątem
kamery i wybiera jedną z 64 orientacji. Środki leżą na wspólnej siatce zoomu.
Banki 17–24 zawierają atlasy i kod rysujący do nieaktywnego bufora. Kod
główny zajmuje 2503 B, pula wspólna ma 298 wierszy.

Przed oczami i po nich złota kiść ma pięć owoców (wcześniej trzy), obrana
trzy (wcześniej jeden). W tickach 41884–43004 dochodzą cztery złote kiście.
W zależności od fazy kamery widać środki 5–13 kiści, a przy krawędziach
mogą być widoczne fragmenty kolejnych. Wszystkie przesunięcia scen względem
123 wynoszą zero. Oczy wchodzą w ticku 39379, terminal w 43005, finał w
51232, karta końcowa w 51980.

Przeszło pełne `make check` (207 testów). Porównanie wszystkich 372 stanów
bananów z montażu w py65 dało zgodność piksel w piksel z rendererem
referencyjnym. W pomiarze Atari800 PAL, 1088 XE, Altirra OS, stereo,
zarejestrowano 49 różnych kroków animacji w ostatnich trzech taktach,
wobec 70 w identycznym pomiarze wydania 123. Każda przechwycona bitmapa
wydania 124 odpowiadała oczekiwanemu stanowi. W tej scenie renderer
gubi część faz kamery. Porównanie POKEY objęło 4 238 856 identycznych
bajtów względem 123. Przebieg na fizycznym Atari pozostaje do sprawdzenia.

[Wydanie stereo 124](../releases/less-i-know-demo-release-124-stereo.xex)
ma 928 974 B. SHA-256
`838391be995454515856c8c44377dd039a95b1d01496c1e15da4efc117821448`.
Powtórne pakowanie dało identyczny XEX. Ostatnie wydanie potwierdzone na
fizycznym Atari 1088 Rambo z AVG to stereo 058 / v330.

## Powolny obrót tekstury bananów

Wydanie 123 zachowuje 32 klatki kamery każdego motywu z wydania 119.
Lokalny kąt kafla zmienia się sinusoidalnie od −10° do +10°, przeciwnie
dla sąsiadów. Maksymalny krok to 1,96° na fazę. Obie tekstury mieszczą się
w dotychczasowych bankach 17–24. Kod główny zajmuje 2542 B, pula ma
298 wierszy. Porównanie z v384 wykazało zmiany tylko w ośmiu bankach grafiki.

[Wydanie stereo 123](../releases/less-i-know-demo-release-123-stereo.xex),
953 134 B, SHA-256 `6d33f3374d26bcc56147da69577c10e7c448d761a8100f915d045037afa6aa13`.
Atari800 PAL, 1088 XE, Altirra OS i stereo dały 4 192 992 identyczne
bajty POKEY względem 122. Ostatnie potwierdzenie pełnego przebiegu na
fizycznym Atari 1088 Rambo z AVG dotyczy wydania 058.

Pełne `make check` przeszło: 207 testów. Zaktualizowano oczekiwania
dotyczące palety, tekstu loadera, faz tunelu i publikacji PMG w sekwencji
BUM/BAM. Po wyłączeniu lokalnego obrotu wszystkie 64 klatki rotatora
odtworzyły piksele wydania 119.

Powtórne zbudowanie XEX z polecenia w README dało identyczny plik.
Przed archiwizacją wersji źródłowej trzeba uwzględnić narzędzia pakowania
i dane końcówki muzyki: `tools/build_hardware_xex.py`,
`tools/build_audio_revision.py` i `assets/music/v035-unfaded-ending.bin`
są wymagane przy odtwarzaniu wydania.

## Historia wcześniejszych wersji


## Oryginalne klatki rotatora z animowaną teksturą

Przywrócono projekcję, zoom, fazę obu motywów i powtarzanie tekstury z wydania 119.
Wewnątrz tekstury sąsiednie kafle obracają się przeciwnie. Próba z wyłączonym
obrotem lokalnym odtworzyła wszystkie 64 oryginalne klatki piksel w piksel.
Zmieniły się dane banków 17–24. Przeszło 21 ukierunkowanych testów.
Atari800 PAL (1088 XE, Altirra OS, stereo) zarejestrował 2 172 600 bajtów
POKEY identycznych z 119. Próba na fizycznym Atari pozostaje niewykonana.

- Stereo 122 · SHA-256 `fb19ccf0c1cad0b5a9950fb44ee36e577ac6af84e774782629d6763d8e11c0d4`

## Wspólne skalowanie i obrót siatki bananowej

W obu motywach cała siatka 3×3 obraca się wokół środka ekranu
i zmienia skalę razem z odstępami między kaflami. Banany nadal
obracają się wokół własnych środków w przeciwnych kierunkach
na sąsiednich polach. Symetria siatki domyka pętlę po 32 klatkach.
Zmieniono wyłącznie zawartość ośmiu banków bananowych, a ich
spakowane klatki zajmują 80 809 B. Kod główny ma 2542 B, pula
298 współdzielonych wierszy i wszystkie 64 banki są przydzielone.

Przeszły 22 ukierunkowane testy grafiki, montażu i loadera.
Wydanie 121 zachowuje loader 058. Atari800 PAL na emulowanym 1088 XE
z Altirra OS i stereo zarejestrował 2 307 960 identycznych bajtów
POKEY względem 120. Próba na fizycznym Atari pozostaje niewykonana.

- Stereo 121 · SHA-256 `d6840ac305df1b574cdae8ca89e2571e5165cbeae3f9ef3d981f926ee0432b55`

## Lokalne obroty kafli bananowych

W montażu po Trevorze oba motywy bananowe używają siatki 3×3. Każdy
kafel obraca się wokół własnego środka, a sąsiedzi w poziomie i pionie
obracają się przeciwnie. Każdy motyw mieści pełny obrót w 32 klatkach.
Zmiana obejmuje dane ośmiu banków bananowych. Kod główny zajmuje 2542 B,
pula ma 298 współdzielonych wierszy, a wszystkie 64 banki pozostają
przydzielone.

Stereo 120 korzysta ze ścieżki sprzętowej 058 i końcówki muzyki ze 119.
Przeszło 21 testów obrotu, odtwarzania obu motywów, montażu i loadera.
Szersza próba ujawniła tę samą rozbieżność testu palety tuneli co w v381.
Atari800 w trybie PAL, na emulowanym 1088 XE z Altirra OS i stereo,
zarejestrował 1 507 680 identycznych bajtów POKEY w porównaniu z 119.
Próba na fizycznym Atari pozostaje niewykonana.

- Stereo 120 · SHA-256 `79590c05aeb7135f25065ab62c5bf4fb14dc319dc3042e9ecfd69786ceb55183`

## Plansza o reżyserii scen

Piąta plansza końcowa opisuje cięcia sterowane tickami muzyki
i zachowanie fazy przy zmianie kierunku rotatorów. Pięć plansz
zapętla się z wygaszaniem. Przeszło 30 testów, w tym przejście przez
przepełnienie licznika NMI. Atari800 PAL (1088 XE, Altirra OS, stereo)
potwierdził 59 833 aktualizacje POKEY zgodne z 118. Próba sprzętowa
pozostaje niewykonana.

- Stereo 119 · SHA-256 `3392bf91d86aba47529ceb8ca7af04e2c005f149ff28f85b44adc925c5db445e`

## Dłuższe rotatory bananowe przed terminalem

Trzy dodatkowe takty bananów od 112 do 115 dają około 5,6 s.
Terminal wchodzi w ticku 43 005. Osiem stron zachowuje całą treść,
a strony pozdrowień mają krótszą ekspozycję. Karta końcowa wchodzi
w takcie 139. Przeszło 40 testów. Atari800 PAL (1088 XE, Altirra OS,
stereo) potwierdził 59 833 aktualizacje POKEY zgodne z 117.
Próba sprzętowa pozostaje niewykonana.

- Stereo 118 · SHA-256 `9b904a3eb9888c96084827276023bb167aae2cee6a1d6341694739d4d033b54d`

## Stały nagłówek terminala

Usunięto zapis migającego ukośnika na końcu wiersza statusu
`[XE-OS] LINK:ONLINE // SV2026 [OK]`. Test pierwszego wiersza
odtworzył problem na v378 i przeszedł na v379. Łącznie przeszło 30
testów. Atari800 PAL (1088 XE, Altirra OS, stereo) potwierdził
identyczne 59 833 aktualizacje POKEY względem 116. Próba sprzętowa
pozostaje niewykonana.

- Stereo 117 · SHA-256 `e6fa9550141690a994b551e8ecf38f0b1b53ae044949e3d574555cd463711047`

## Pierwszy wiersz terminala bez kursora

Migający kursor pojawia się tylko poniżej pierwszego widocznego wiersza
terminala. Wydanie stereo 116 zachowuje końcówkę muzyki z 115. Atari800
PAL (1088 XE, Altirra OS, stereo) potwierdził identyczny przebieg wszystkich
59 833 aktualizacji POKEY. Przeszło 29 testów terminala, sceny końcowej
i loadera. Próba sprzętowa pozostaje niewykonana.

- Stereo 116 · SHA-256 `64eddcb8196b36c676c08c0a04e92036b8f8155f37fd797ed3d5168af74b27e2`

## Odtworzona końcówka bez fade

Stereo 115 korzysta z ponownego renderu ostatnich sześciu uderzeń aranżacji
v035 z wyłączonym wyciszeniem całości. Render kontrolny odtworzył wszystkie
etapy od v018 do v035 bajt w bajt. Zmiany zaczynają się od aktualizacji 59 277
(licząc od zera). Zachowano pauzy partytury i osiem końcowych aktualizacji
ciszy. Atari800 PAL, 1088 XE, Altirra OS i stereo potwierdziły zgodność
wszystkich 59 833 aktualizacji z nowym miksem. Przywrócono 220 wcześniej
niesłyszalnych aktualizacji głosów. Przeszło 17 testów sceny końcowej
i loadera. Próba na fizycznym Atari pozostaje niewykonana.

- Stereo 115 · SHA-256 `6389166058d6b741d699527be8baa4f3bc43e008c6e6a65dcd7fb147715b7900`

```sh
python3 tools/render_unfaded_ending.py ../impala-lessIknow/remix/releases /tmp/v035-unfaded-ending.bin
cmp /tmp/v035-unfaded-ending.bin assets/music/v035-unfaded-ending.bin
python3 tools/build_audio_revision.py build/visual-prototype-v377.xex releases/less-i-know-demo-release-115-stereo.xex --fast-clear --unfaded-ending
```

## Końcówka utworu bez wyciszenia całości

W stereo 114 skompensowano sześciouderzeniowe wyciszenie v035 w
końcowych rejestrach głośności POKEY. Poziomy odtworzono w przybliżeniu
z 4-bitowych wartości, z ograniczeniem do wcześniejszego poziomu
głosu. Próbki o zerowej głośności zachowano. Atari800 PAL (1088 XE,
Altirra OS, stereo) potwierdził wszystkie 59 833 aktualizacje,
identyczny przebieg przed aktualizacją 59 310 (licząc od zera)
i zachowane końcowe 29 aktualizacji ciszy. Przeszło 17 testów
sceny końcowej i loadera. Weryfikacja na sprzęcie pozostaje otwarta.

- Stereo 114 · SHA-256 `8f65d1abdcfece8fbef58cc09b862df9ca950e30b400bba266efc3e9444f947d`

## Gwiazda po ostatniej nucie

Zegar NMI `$24AA` steruje 32 klatkami gwiazdy i pierścieni także po
zakończeniu utworu. Strony tekstowe nadal się zmieniają. W Atari800
(PAL, 1088 XE) obie wersje odtworzyły wszystkie 59 833 aktualizacje
POKEY (około 5:00), z przebiegami zgodnymi z 110/111. Zarejestrowano
pełny obrót po zakończeniu utworu. Przeszły 22 testy sceny końcowej,
tekstu i programu ładującego. Próba sprzętowa pozostaje niewykonana.
[Podgląd](../build/v377-star-after-music.gif).

- Stereo 112 · SHA-256 `221098004350c2aa3bec12b392d1a6af4f2d4227ba4950d037dd1398cc83dbb0`
- Mono 113 · SHA-256 `91a925591abe56785685b6a63b628dc74d8c55e5369981dd194abb9995a837c1`

## Czytelna cyfra 4

Cyfra 4 w terminalu i na planszach końcowych ma nowy glif 3 × 7.
Przeszły 24 testy. Atari800 pokazał czytelną cyfrę i ślady POKEY
zgodne z 108/109. [Podgląd](../build/v376-ending-digit-4.png).

- Stereo 110 · SHA-256 `a0951aea5de28387c673ea1a63cd1df64088a560d85a3805652a300d9458f1df`
- Mono 111 · SHA-256 `1a31eac872b0127bd9d610270308156ddd299ce65397e546cee0c0b06e280d06`

## Zmienne plansze końcowe

Pod gwiazdą zapętlają się cztery strony z podpisem, odtwarzaczem v035,
trybami ANTIC/GTIA i sprzętowymi efektami PMG oraz DLI. Każda trwa około
5,1 s w PAL. Tekst gaśnie do czerni, zmienia się i ponownie rozjaśnia.
Gwiazda dalej animuje się w 32 fazach. Tekst używa osobnego koloru
COLPF3 i pamięci `$BF80–$BFF7`. Zegar stron to licznik NMI `$24AA/$24AB`.

Przeszło 29 testów. Atari800 potwierdził cztery strony, osiem stopni
jasności i pełne ślady POKEY zgodne z 106/107. Próba sprzętowa pozostaje
niewykonana. [Podgląd](../build/v375-final-card-pages.gif).

- Stereo 108 · SHA-256 `538028b0bad5c65b0016351c09f18e941a915bd4028042b7c4a76459cb6cbaee`
- Mono 109 · SHA-256 `ea96a8aa471116abd95c3c59fecbe02bbb90959a5d07543bb62169ff471f86c9`

## Notka autora w terminalu

Pierwsza plansza kredytów podaje początek vibecodingu w lipcu 2026
i informuje, że to pierwsza praca Ognjena na Atari. Zapis tekstów
w naturalnej długości mieści się w istniejącej pamięci terminala.
Przeszło 28 testów. Atari800 pokazał czytelny tekst w obu wersjach
i ślady POKEY zgodne z 104/105. Próba sprzętowa pozostaje niewykonana.
[Widok terminala](../build/v374-terminal-author-credits.png).

- Stereo 106 · SHA-256 `dd592257cf15997c1f5e6b019d79a9fbc7a1cff04de205c5c10b9e8bd229d1ef`
- Mono 107 · SHA-256 `0e0be57a2015c6007009dd4609fd81c7b19dc524a528782f5478e03bba292a81`

## Ciągły obrót szybkich tuneli

Dziesięć ujęć tuneli na taktach 36, 38, 84, 85, 88, 89, 96, 97, 100
i 101 wykonuje jeden krok co 16 ticków. Poprzednio co drugi obraz fazy
był pomijany. Kierunki obrotu, momenty cięć i prędkości bananów pozostały
takie jak w v372. Przeszło 13 testów directora i loadera. Ślady POKEY
w Atari800 PAL odpowiadają 102/103. Próba sprzętowa pozostaje niewykonana.
[Porównanie tuneli](../build/v373-tunnel-motion.gif).

- Stereo 104 · SHA-256 `2204699000ac34f6633ae42338fbb0262954fae040b6660f8cc68b7d45b5a3ba`
- Mono 105 · SHA-256 `e370c50914b05a3355cb12a7f13647c2d7f7752635641777774506e30c72b273`

## Szybka animacja gwiazdy na planszy końcowej

Gwiazda ma mocniejszy obrót faset, dwa pierścienie wirują w przeciwnych
kierunkach, a białe refleksy biegną wzdłuż orbit. Pętla ma 32 klatki
i trwa 0,64 s w PAL. Klatki znajdują się w bankach wideo 20–23
pod `$6800–$6FFF`. Kopiowanie odbywa się od VCOUNT 124 do 143.

Przeszło 21 testów. Atari800 PAL pokazał wszystkie 32 kolejne fazy
w obu wersjach oraz identyczne ślady POKEY względem 100/101.
Oba wydania używają opcji `--fast-clear`. Próba sprzętowa pozostaje
niewykonana. [Podgląd Atari800](../build/v372-final-star.gif).

- Stereo 102 · SHA-256 `849d88ab936dec5511798cf7f7e91a5172eebf363079227c028abe9c71ec1f19`
- Mono 103 · SHA-256 `77257de64a843fb98725739235d9b8d79db3cd59ed8d8ce6e64198b24a813730`

## Kandydaci z szybszym ładowaniem

Stereo 100 i mono 101 używają rozwiniętej pętli czyszczenia banków.
W Atari800 PAL start skrócił się z 17,81 do 14,53 s. Przeszło 6 testów
loadera, a pełne ślady POKEY odpowiadają 098 i 099. Wariant wymaga
flagi `--fast-clear`. Wyniki i SHA-256 są w
[analizie optymalizacji](loader/10_analiza_optymalizacji.md).

## Kolor na każdej linii rastra terminala

Czcionka ANTIC 4 przypisuje kolejnym liniom liter trzy różne kolory.
Dwa krótkie DLI zmieniają odcienie przed tekstem i przywracają kolory
bitmapy pod nim. Tekst zaczyna się 10 linii niżej, a cztery muzyczne
DLI występują w swoich dotychczasowych miejscach. Plansza końcowa
korzysta z oryginalnej czcionki.

Przeszło 27 testów terminala, planszy końcowej i loadera. Atari800 PAL
potwierdził różne kolory sąsiednich linii liter i 59 833 aktualizacje POKEY
zgodne z 096/097. Próba sprzętowa pozostaje niewykonana.
[Podgląd z powiększeniem](../build/v371-terminal-scanline-colors.gif).

- Stereo 098 · SHA-256 `3076ef3d0c6c1f53eafcd9f356d407e6f3c9c709f82e8a18eaa7f748a3780e93`
- Mono 099 · SHA-256 `a322e5d4e2df4f014b113e6d1803b1309e2ec6cbca059ad7ad60dd28e1d73be0`

## Częstsze kroki czterech tuneli

Pierwsze cztery ujęcia wykonują jeden krok obrotu co 16 ticków
(około 80 ms w PAL). Wersja v369 trzymała każdą fazę przez 32 ticki.
Tunele organiczne wykonują pojedyncze kroki, a cięcia i kierunki
obrotu zachowują dotychczasowe pozycje. [Porównanie Atari800](../build/v370-opening-tunnels.gif).

Przeszło 11 testów directora i loadera. W Atari800 PAL zarejestrowano
krótsze postoje obrazu i pełne ślady POKEY zgodne z 094/095.
Próba sprzętowa pozostaje niewykonana.

- Stereo 096 · SHA-256 `6f70748133fab7a6bb2d86cb9d9a47ed036ae4acbc105accec8ee2246397d7d0`
- Mono 097 · SHA-256 `2c63ec8de9626d7b279e73e2eb5b9c472bf4648e87819eb5d5617417771e90e4`

## Przepływ kolorów w terminalu

Siedem kolorów przesuwa się w dół o jeden wiersz co 32 ticki.
Pętla trwa około 1,12 s w PAL. Kod fazy i tabela zmieściły się
w RAM pod ROM przy `$FF94`. Lista ANTIC zachowuje dotychczasowe DLI.
W emulatorze pierwsze dwie linie rastra liter zachowują odcień
poprzedniego wiersza, tak jak w wydaniu 092.

Przeszły 22 testy terminala, planszy końcowej i loadera. Atari800 PAL
pokazał pełną rotację w obu wydaniach i czyste wejście do terminala.
W obu wydaniach wszystkie 59 833 aktualizacje POKEY odpowiadają 092/093.
Próba sprzętowa pozostaje niewykonana. [Podgląd animacji](../build/v369-terminal-color-flow.gif).

- Stereo 094 · SHA-256 `6aeb1c1f2412059f0c62cbb38af4a3a17aa3dade7c38d6e5ca0774c182bf2cf9`
- Mono 095 · SHA-256 `359465005c70875880bef4e543b0050094eb1b8d39ad208bd371c87f21798454`

## Czyste przejście do terminala

Lista tunelu pozostawała aktywna podczas nadpisywania jej bitmapy.
V368 wygasza kolory i PMG przed kopiowaniem i przywraca je przy
publikacji gotowej listy terminala. Zachowano cztery aktualizacje muzyki
na ramkę. Atari800 PAL potwierdził czyste przejście w obu wersjach
i 59 833 aktualizacje POKEY zgodne z 090/091. Przeszło 20 testów.
Próba sprzętowa pozostaje niewykonana. [Porównanie](../build/v368-terminal-entry.png).

- Stereo 092 · SHA-256 `c62fd83318755f487495518ff5ad3cd0fa4e6fa36ed7afe7b837e20b73a9377b`
- Mono 093 · SHA-256 `5a6ed653e2b09691b0be60cd88b816de39816e0d4d0ae832fe54a087f816d2b3`

## Animacja gwiazdy na planszy końcowej

Gwiazda kołysze się, a przerwy dwóch pierścieni przesuwają się w przeciwnych
kierunkach. Pętla ma 16 klatek i trwa około 2,56 s w PAL.
W v367 klatki są w banku wideo 0 od `$4A00`. Kopia 168 B do fontu
następuje we wczesnym wygaszaniu z zachowaniem PORTB. Wcześniejsza próba
v366 (088/089) dawała uszkodzony obraz po pełnym odtworzeniu w Atari800.

Przeszło 20 testów. Atari800 PAL pokazał wszystkie 16 klatek w obu
wydaniach i identyczne ślady POKEY względem 086/087. Próba sprzętowa
pozostaje niewykonana. [Podgląd animacji](../build/v367-animated-star.gif).

- Stereo 090 · SHA-256 `2fa85ffb6c8af33cb92d2c33e33a73de1cd8f63c4f750262ada0224b2559f5f8`
- Mono 091 · SHA-256 `4330d0f4c6207a4238a1f22816eb8c7376cd0f318d2f33da8d665cd85d840fd0`

## Siedem kolorów terminala

Każdy wiersz terminala ma własny odcień GTIA. Lista ANTIC uruchamia
zmiany koloru bez dodatkowego taktowania muzyki. Atari800 pokazał siedem
kolorów i potwierdził identyczne ślady POKEY względem 084/085.
Przeszły 22 z 23 testów. Test palety wejścia Trevora daje tę samą
rozbieżność w v364 i v365. Próba na sprzęcie pozostaje niewykonana.

- Stereo 086 · SHA-256 `7be92c27a132fdaf541efcff0f2455a14b1241b12a94274748f83576fa659c41`
- Mono 087 · SHA-256 `255f4bcda8391b3489a3e67dceed1306b0adf2700d842de5e71c2139cca138a0`

## Wolniejsze pierwsze cztery tunele

Pierwsze cztery ujęcia mają krok co 32 ticki zamiast ruchu o jedną lub
dwie fazy co 16 ticków. Zachowano kierunki i cięcia na taktach 32–35.
Przeszło 11 testów directora i loadera. Atari800 PAL potwierdził
identyczne ślady POKEY względem 082/083. Próba na sprzęcie pozostaje niewykonana.

- Stereo 084 · SHA-256 `41438acb8aea4d83478fc88845832ae2d29fd860f376e9038977ffe593f004cb`
- Mono 085 · SHA-256 `edd9f834fb0e35d1047d7750b50e57d7164c430b85b667bd4aadd0a4dd227d60`

## Naszywka XL⚡XE

W zbliżeniu przy arenie kurtka ma napis XL⚡XE, a w dalszych ujęciach
samą błyskawicę. Oryginalne kadry party pozostają w katalogu wzorców.
Przeszło 12 testów, a Atari800 potwierdził zgodność śladów POKEY z 080/081.
Fizyczna próba AVG pozostaje niewykonana.

- Stereo 082 · SHA-256 `281bd1a093b2c346053953575920ed40302294ff00b8159759432f3d5a86fd0a`
- Mono 083 · SHA-256 `bbe9221dab7cc8047e41667ece210081a063f93f272ca1ccfe5bb9a132f3fb32`

## Wspólna siatka pikseli w zbliżeniu przy arenie

W v362 zbliżenie dziewczyny używa tej samej siatki 160 × 64 co chłopak.
Grafika źródłowa z party jest próbkowana bezpośrednio w rozmiarze
96 × 128, z zachowaniem dotychczasowego kadru do pasa.
Wydania AVG, porównanie i sumy SHA-256 są w [notatce v362](V362_SIATKA_PIKSELI_ARENA.md).

## Dziewczyna z wersji party

Kandydaci AVG to stereo 078 i mono 079. Powróciła oryginalna grafika
dziewczyny oraz 18 klatek panoramy z wydania party. Poprawki dotyczą
pasm włosów w zbliżeniu i czterech pikseli profilu na klatkę.
Szczegóły, wyniki testów i SHA-256 są w [notatce v361](V361_DZIEWCZYNA_Z_PARTY.md).
Kadry v330 są zapisane jako [wzorzec do dalszej pracy](../assets/art/reference/v330/README.md).

## Twarz tancerki i postawa w otwarciu

Kandydaty AVG: stereo 076 i mono 077. V360 używa w zbliżeniu rysunku twarzy
i loków tancerki ze wstążkami, a w bocznym kroku przesuwa głowę nad barki.
Strój codzienny pozostaje jak w v359. 21 testów przeszło, pełne ślady stereo
i mono w Atari800 odpowiadają 074 i 075. Kadry i SHA-256: [v360](V360_TWARZ_TANCERKI_I_POSTAWA.md).

## Strój codzienny i profil z odniesieniem do tancerek

Najnowsze kandydaty AVG to stereo 074 i mono 075. Dziewczyna ma jasne loki
i profil inspirowany tancerkami oraz codzienny strój na spacer. Kadr obok
chłopaka, chód i porównanie z postaciami: [v359](V359_CHEERLEADERKA_STROJ_CODZIENNY.md).
21 testów przeszło. W Atari800 pełne ślady 074/075 odpowiadają 072/073.

## Nowa dziewczyna i cykl chodu w otwarciu

Najnowsze kandydaty AVG: stereo 072 i mono 073. V358 rysuje od nowa duży
portret i dalsze pozy dziewczyny oraz 18 klatek bocznej panoramy z nowym
cyklem chodu. Kadry i GIF porównują 058, 070 i 072. Przeszło 21 testów.
Pełny ślad POKEY obu wydań w Atari800 odpowiada odpowiednio 070 i 071.
Szczegóły, SHA-256 i zakres próby: [v358](V358_NOWA_CHEERLEADERKA.md).

## Tunele przed walką, banany po Trevorze

V357 ma wyłącznie tunele spiralne i organiczne w pierwszych rotatorach
(takty 32–39). Wejście bananów następuje w ticku 29656, zaraz po Trevorze.
Dalszy montaż i miks wydań 068/069 zachowują swoje role. Zmienia się tylko
tabela directora w banku wideo 2, w procedurze od `$6E20`.

- Stereo `releases/less-i-know-demo-release-070-stereo.xex`, 945 968 B,
  SHA-256 `476974632f4d126404b76f6d925447e3d8eb9fb6aa5bae6899b6e20b3673c8a6`.
- Mono `releases/less-i-know-demo-release-071-mono.xex`, 945 968 B,
  SHA-256 `e049fcfba31a02fe4109c5a00237ccdcca2e0b5b6721e07f26254a304b1bfc4e`.

13 testów directora, granic scen i loadera przeszło. Atari800 PAL, 1088 XE,
Altirra OS: 59 833 aktualizacje stereo identyczne z 068 i 59 833 aktualizacje
mono identyczne z 069. Obejrzano trzy kadry z emulatora (`build/v357-tunnels-then-bananas.png`).
Nie wykonano fizycznej próby nowych plików ani pełnego `make check`.

## Korekta miksu po audycie POKEY

Najnowsze kandydaty na AVG to stereo 068 i mono 069. Stereo wyrównuje
strój basu, mono zachowuje ciągłość aktywnych głosów, oba ograniczają
głośne nakładki. Pełne ślady POKEY są zgodne z nowymi miksami, a czas
utworu wynosi 5:00. Pliki, skróty i zakres zmian: [068/069](V356_MIKS_AUDIO_068_069.md).
Użytkownik potwierdził, że mono 069 brzmi dobrze na fizycznym Atari z jednym
POKEY. Stereo 068 nadal ma tylko walidację w emulatorze.

## Szlif obrazu v356

Nowy kandydat stereo `releases/less-i-know-demo-release-066-stereo.xex`.
Profil dziewczyny w otwarciu, podwójny bufor piłki i odłamków w akcie 3
oraz gwiazda z orbitami na końcowej karcie. 29 testów przeszło. Pełny ślad
POKEY w Atari800 zgodny z 064. Próba fizyczna pozostaje niepotwierdzona.
Rozkład pamięci, wynik śladu i SHA-256: [v356](V356_GWIAZDA_I_STABILNY_WSAD.md).

Wariant v356 na jeden POKEY: `releases/less-i-know-demo-release-067-mono.xex`,
945 964 B. SHA-256 `12a0bbc6ea8d873b8c07edff360cdfec19cb96b5b71e7dfeb60544def0e1c864`.
`tools/make_mono.py --merge` składa obie strony 066 tak jak w 065.
Różnią się wyłącznie segmenty playera `$2000–$24B2` i `$2C00–$2C80`.
Atari800 PAL, 1088 XE, Altirra OS i jeden POKEY potwierdziły 59 833 identyczne
z 065 aktualizacje mono przez 5:00. Próby na fizycznym Atari nie wykonano.

## Wariant na jeden POKEY — 18 listopada 2026

Osobny kandydat `releases/less-i-know-demo-release-065-mono.xex`, 945 628 B,
SHA-256 `eb913aa8f492a28c1668a43370c17da851fa4b9006ad193b2580e69f67bb7058`.
`tools/make_mono.py --merge` składa obie strony 064 na jeden układ. Bas
łączy poziomy obu głosów i korzysta z lewego stroju. Dwie pozostałe pary
korzystają z głośniejszego aktywnego głosu. Jeden układ nie zagra dwóch
różnych wysokości jednocześnie w jednym kanale.

Zmiana obejmuje tylko `$2000–$24B2` (wyłączenie zapisów na drugi POKEY)
i `$2C00–$2C80` (miks rejestrów). Układ XEX, loader i grafika odpowiadają
064. Atari800 PAL, 1088 XE, Altirra OS, z jednym i dwoma emulowanymi POKEY:
porównano 59 833 aktualizacji z oczekiwanym miksem 064. Wszystkie zgodne,
ok. 300 s. Po starcie player zapisuje wyłącznie na pierwszy POKEY.
Odtwarzanie na fizycznym Atari wymaga próby.

## Tempo muzyki na końcowej karcie

Kandydat stereo `releases/less-i-know-demo-release-064-stereo.xex`, 945 628 B,
SHA-256 `0da2f621e0ff4b35f6f284fbbf14f6fa1f99d053e635898eacac0f62eeb37d5b`.
Względem 063 plik różni się jednym bajtem listy ANTIC końcowej karty. Zmiana
`$F0` → `$70` zachowuje osiem pustych linii i usuwa piąte przerwanie muzyki.
Cztery prawidłowe DLI wypadają na liniach 0, 78, 156 i 234 listy.

Ślad pojedynczych zapisów POKEY w Atari800 PAL, 1088 XE, Altirra OS, stereo
pokazał problem w 058 i 063 od ok. 4:20. Te same pakiety obu POKEY przechodziły
w 063 w 292,13 s zamiast ok. 300 s. W 064 ślad potwierdził 59 834 kompletne
pakiety (w tym wyciszenie startowe), identyczne w kolejności i wartościach z
v035, w 300,00 s. Odstępy ustabilizowane na karcie to 8890–8894 cykli wokół
nominalnych 8892. Sześć skupionych testów list, finału i loadera przeszło.

Wcześniej w demie pojedynczy pakiet zajmuje do 287 cykli magistrali, wobec
151–152 dla v035 i 216–219 dla Starfish Motion v5 4×. Ślad wyklucza utratę
pakietów w emulatorze. Nie ustala przyczyny różnicy słyszalnej na fizycznym
Atari przed końcową kartą. Kandydat 064 oczekuje na próbę fizyczną.

## Nowy rysunek dziewczyny w otwarciu

V354 rysuje od podstaw dziewczynę idącą do areny: profil, włosy, kurtkę
z logo Fuji i krok. Zachowuje istniejącą paletę, tło i pozycje kamery.
Kandydat stereo `releases/less-i-know-demo-release-063-stereo.xex`, 945 628 B,
SHA-256 `baa7e8940986879de0a7871a2bb9fc7a811c037fbd15fc343aed10da39932d43`.
Pakowanie według kontraktu 058. Build mieści 299 współdzielonych wierszy
(11 487 B) i 2542 B kodu głównego. Sześć testów kompozycji i loadera przeszło.
Podgląd czterech ujęć: `build/opening-girl-v354-preview.png`.
Atari800 PAL, emulowane 1088 XE, Altirra OS, dwa POKEY: 063 kontra 062,
7 724 448 identycznych bajtów rejestrów stereo, ok. 2151,7 s emulowanych.
Pomiar rejestrów nie obejmuje analogowego dźwięku ani sprzętowego odtwarzania.
Kandydat 063 oczekuje na próbę sprzętową.

## Naprawa pakowania po awarii v353 na Atari

Użytkownik potwierdził, że na fizycznym Atari nie działa **v353**. Surowy
prototyp omijał kompaktowanie, wysoki ekran loadera i późne odtworzenie
niskiej RAM z działającego release 058. To regresja ścieżki pakowania;
nie ustalono pojedynczego mechanizmu fizycznej awarii.

Nowy kandydat: `releases/less-i-know-demo-release-062-stereo.xex`, 945 676 B,
SHA-256 `0699c0ac764e03ca82c00d971b33d0e70571ae1699574d60fcad77db48d859ac`.
Zachowuje grafikę i runtime v353 oraz procedury ładowania z 058.
Nie jest jeszcze potwierdzony na fizycznym Atari. v330/058 pozostaje
ostatnim wydaniem z potwierdzonym pełnym przebiegiem.

Trwałe reguły: [kontrakt loadera](HARDWARE_LOADER_CONTRACT.md), podpięty
także w `AGENTS.md`. `make all` buduje teraz dodatkowo `build/hardware-dev.xex`.
Sześć ukierunkowanych testów loadera i alokacji pamięci przeszło, w tym
odtworzenie całego 058 z v330 bajt w bajt, zgodność 64 obrazów banków v353
i wykonanie bootstrapu w py65. Pełnego `make check` nie powtarzano.
`make hardware PYTHON=python3` przeszedł: 297 współdzielonych wierszy,
2542 B kodu głównego; wynik identyczny SHA-256 z release 062.
Atari800 PAL / emulowane 1088 XE / Altirra OS / dwa POKEY, bez obrazu
i dźwięku: release 062 kontra prototyp v353, 5 174 424 identyczne bajty
stereo, ok. 1441,4 s emulowanych. Nie jest to próba fizycznego loadera AVG
ani nowa deklaracja pełnej zgodności z playerem v035.

## Archiwalny stan wydań v330–v360

- Stereo release 058: `releases/less-i-know-demo-release-058-stereo.xex`
- Rozmiar: 936 240 B; SHA-256: `f3c14bc36b96220ead8fbe24df2e0dfc7ef5d30371d5cd83d11f808b62706b8f`
- Najnowszy prototyp: `build/visual-prototype-v360.xex`, SHA-256 `9ba948ef56c068062fbdc1733b3005a475c6829cc4f38a500f57eed18c98847c`. Aktualny montaż: [v357](AKTUALNY_MONTAZ_V330.md).
- Poprzedni kandydat stereo: `build/visual-prototype-v352.xex`; SHA-256: `b3031752e9615e3f69c7ab877cb115c1d798b39efdb500e1b0ee00d63f795d1d`.
- Ostatnie wydanie produkcyjne pozostaje stereo release 058 / v330. Źródło v330: `build/visual-prototype-v330.xex`; paczka SV v330 pozostaje w `releases/less-i-know-sv2026we-v330-submission/` oraz ZIP obok.
- Czas v352: ok. 4:20.7; terminal od ticku 41884, tekst do 51232, fade od 51852, końcowa karta od 51980.
- Trevor kończy się przy ticku 29656. Director przejmuje sterowanie na pierwszym callbacku po nim, bez resetu fazy bananów. Od taktu 80 zmienia motyw, kierunek i prędkość na granicach taktów. Oczy dziewczyny: 39379–40126.
- Director steruje także rotatorami od ticku 11967 i tunelem od 20942 do 21689. BUM/BAM i dymki pojawiają się na ostatnich bananach przed oczami oraz na bananach po nich. Szczegóły: [v352](V352_BANANY_PRZED_OCZAMI.md).
- V349 dodaje mniejszy dymek, wygaszenie i niezależną szeroką ósemkę: [notatka](V349_BUM_BAM_OSEMKA.md).
- V350 wydłuża dolot piłek Trevora z 32 do 48 ticków, zachowując momenty uderzeń: [notatka](V350_PILKI_TREVORA.md).
- V351 poprawia dolne piksele cyfry 7 w foncie creditsów: [notatka](V351_CYFRA_7.md).
- V352 włącza BUM/BAM od taktu 104 na bananach przed oczami, zachowując ujęcie oczu z piłką i satelitami.

Zmiany v331 obejmowały większe serce; wadliwy dodatkowy parallax chmur został usunięty w v333, bo przesuwał górę głowy idącej dziewczyny. V332 dodawał ruch stopy leżącego chłopaka co beat; animację wycofano w v335 i przywrócono statyczną pozę z v330. V334 rozjaśnia i nasyca paletę serca. V336 wyrównuje jasność klatek ciosu Trevora. V338 przełącza późne rotatory bananowe na BUM/BAM, pozostawiając piłkę w tunelach: [notatka v338](V338_BUM_BAM_W_BANANACH.md). V339 przywrócił loader i końcówkę z v300, co przesunęło finał o ok. 40 sekund i usunęło kartę końcową. V340 poprawił ósemkę BUM/BAM, satelity i serce: [notatka v340](V340_BUM_BAM_OSEMKA_I_SERCE.md). V341 przywrócił timing i kartę końcową v330 oraz tor piłki w ujęciu oczu: [notatka v341](V341_OCZY_OSEMKA_FINAL_V330.md). V342 przywrócił tekst loadera v330; v343 dodaje postęp kropek po kolejnych bankach bez przesuwania napisu: [notatka v343](V343_LOADER_PROGRESS_DOTS.md). Szczegóły wcześniejszych zmian: [v331](V331_CHMURY_I_SERCE.md), [v332](V332_STOPA_W_RYTMIE.md), [v333](V333_NAPRAWA_PANORAMY.md), [v334](V334_PALETA_SERCA.md), [v335](V335_STOPA_STATYCZNA.md), [v336](V336_PALETA_TREVORA.md).

Aktualny timeline po Trevorze: [montaż v330](AKTUALNY_MONTAZ_V330.md). Zmiana wydania produkcyjnego: [v330](V330_KROTSZY_MONTAZ_I_DIRECTOR.md). Szczegółowa historia pozostaje w notatkach Vxxx; bieżący stan podaje początek tego pliku.

## Historyczna walidacja v330–v353

- v353: build stereo i kontrola nakładania pamięci przeszły; 297 współdzielonych wierszy, 11 486 B puli, 2542 B kodu głównego, nadal 64 banki. 34 ukierunkowane testy przeszły. Pełne `make check`: 200 testów, 32 porażki i 1 błąd; nie jest zielone. Niezmieniony kod/testy HEAD z prototypem v352 dały te same 33 wpisy porażek/błędu (198 testów). Nie naprawiano ich w ramach szlifu grafiki.
- Atari800: PAL, emulowane 1088 XE, dwa POKEY, Altirra OS, tryb bez obrazu i dźwięku z rejestracją rejestrów. v353 kontra v352: 10 721 808 identycznych bajtów stereo, ok. 2986,6 s emulowanych. Porównanie z oryginalnym playerem v035 dla obu wersji kończy się pierwszą różnicą na bajcie 935 784, ok. 260,7 s; nie deklarować pełnej zgodności z v035. Fizycznego Atari ani pełnego wizualnego odtwarzania v353 nie sprawdzano. Znany artefakt tablicy wsadu pozostaje nierozwiązany.
- 28 ukierunkowanych testów py65 dla rotatorów, granic scen, timeline’u i creditsów zaliczyło v330.
- Pełnego `make check` po ostatnich zmianach nie uruchomiono. Nie należy deklarować, że cały zestaw testów przechodzi. Usunięto nieaktualne porównanie z XEX v198, test wydzielonego projektu pomponów oraz dawne asercje cyklu rotatora zastąpione testami aktualnego directora.
- Użytkownik potwierdził, że v330 działa bez zarzutu z karty AVG na Atari 1088 Rambo. To pozytywna próba pełnego przebiegu na docelowym sprzęcie; nie wykonano osobnego pomiaru FPS ani nowego porównania stereo POKEY.
- v352 zbudowano jako stereo (298 współdzielonych wierszy, 2542 B kodu). Siedem testów directora i dziewięć testów Trevora przeszło w py65. Piłkę i PMG w oczach porównano z v351 w pięciu momentach. Emulatora ani Atari nie uruchamiano; v330 pozostaje ostatnią wersją sprawdzoną na sprzęcie.
- Ostatnie pełne porównanie ścieżki stereo z playerem v035 dotyczy starszego buildu v260. Nie powtarzano go dla v330.
- Wszystkie 64 banki są przydzielone. Nie wnioskować o wolnej pamięci ze starszych raportów odzysku; przed zmianą sprawdzać bieżący allocator i JSON buildu.
- Budujemy wyłącznie stereo. Wariant mono jest wycofany.

## Stan na koniec przygotowań do party

Główne sceny i montaż są ukończone. Próba release 058 na Atari 1088 Rambo z kartą AVG została potwierdzona jako bezproblemowa. Termin zgłoszeń Silly Venture 2026 WE minął; w repo nie ma potwierdzenia wysłania formularza. Nie deklarować zgłoszenia ani gotowości konkursowej bez takiego potwierdzenia.

Status paczki i autorstwa muzyki: [przygotowanie SV](SV2026WE_PRZYGOTOWANIE.md). Pierwotne cele audytu V1–V7 i dokumenty `TLIKTB_*` są materiałem projektowym/historicznym, nie listą blokującą release.

## Release 061 i AVG

Kandydat stereo `releases/less-i-know-demo-release-061-stereo.xex` (v352), SHA-256 `90426fde4adcbfc83f7e52c8ec93265112da518ee85f8464d54a88b5e819e433`. Paczka: `releases/less-i-know-sv2026we-v352-release061-submission.zip`. Release 059 i 060 nie uruchomiły się na sprzęcie użytkownika (AVG, Atari 1088 Rambo); nie używać ich do zgłoszenia. Release 061 zawiera ekran loadera, 66 wrapperów INIT i bootstrap identyczne bajtowo z działającym release 058; liczby INIT i adresy porównano z release 058. Start release 061 na fizycznym Atari pozostaje niepotwierdzony.
