# V244 — surowe banany i ponowne użycie banków po tytule

Właściwe odtwarzanie obu bananów korzysta teraz z surowych bitmap,
tak jak tunele. Usunięto koszt RLE z krytycznej ścieżki animacji bez
zmiany 64 obrazów, gęstości wzoru, orientacji, zoomu, palet, PMG ani timeline.

## Dlaczego pamięci wystarcza

Wszystkie 64 banki były przydzielone, lecz dziewięć banków tytułu 40–48
nie ma już pracy po ticku 2992. Ich ponowne wykorzystanie daje 144 KiB
pamięci scenowej. Osiem mieści dodatkowe surowe klatki, dziewiąty służy
jako staging. Nie zabrano rozproszonych luk z innych scen i creditsów.

| Właściciel | Przed tytułem / podczas tytułu | Po przygotowaniu |
|---|---|---|
| Loader 3–10 | 64 spakowane klatki obu bananów | 32 surowe klatki kiści |
| Loader 40–47 | Plasma, maski, przejścia i fajerwerki tytułu | 32 surowe klatki obranego banana |
| Loader 48 | Ostatnie przejście i maski tytułu | Staging klatki + szablony helperów |
| $E580–$E956 | Nieaktywna później część kodu tytułu | Worker cache |
| $EA00–$EAFF | Nieaktywne później dane tytułu | 256 B scratcha |
| $EB00–$EB1F | Nieaktywne później dane tytułu | Prywatny stan workera |

Bank 46 przechowuje szablony i bootstrap w nieużywanej końcówce fade'u:
$5400–$5BFF szablony, $6000–$63D6 worker, $6800–$6845 bootstrap. Zanim
bank 46 zostanie nadpisany, szablony są kopiowane do banku 48 pod
$6000–$67FF. Staging w banku 48 to $4000–$4EFF. Surowe banki zawierają
4 × 3840 B bitmap oraz helper 981 B pod $7C00; pozostaje po 43 B.
Łącznie 245760 B obrazów i 15696 B helperów w 16 bankach; 688 B ich
łącznych końcówek. To budżet runtime, odrębny od spakowanych danych startowych.

## Przygotowanie w tle

Bootstrap uzbraja się podczas rzeczywistego przejścia przez ticki
3072–3327. Główny callback daje workerowi jedno zadanie na wywołanie do
11775. Każde zadanie przetwarza jedną stronę 256 B. Najpierw powstają
cztery klatki obranego banana w nowym banku, potem kiść we własnym banku,
od klatki 3 do 0. Jeśli docelowy zapis mógłby przeciąć źródło bieżącej
klatki, worker rozpakowuje ją do banku 48 i dopiero potem kopiuje z powrotem.
Źródłowe wskaźniki i helper są nadpisywane dopiero po wykorzystaniu.

FLAG $0DDF: 0 = oryginalne dane, 1 = przygotowanie, 2 = pełne raw.
Przygotowanie potrzebuje 1261 małych zadań. Worker nie używa scratcha
muzyki ani strony zerowej, zachowuje PORTB, nie dotyka framebufferów,
PMG ani rejestrów publikacji obrazu. Cache i font terminala mają rozłączne
zakresy; typewriter $EB44 i director $EC20 pozostają.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS: breakpoint zakończenia workera
wypada w ticku **8609**. Pierwszy wybór rotatora/tunelu w ticku **11976**
odczytuje FLAG=2. Zapas do początku tego odcinka to około **17 sekund**,
a do pierwszych bananów 12288 około 18 sekund. To odczyt z emulatora
modelującego ANTIC, nie wniosek z samego budżetu py65.

## Płynność

| Motyw | Maks. callback po rozgrzaniu |
|---|---:|
| Kiść | 47323 cykle CPU |
| Obrany | 47402 cykle CPU |
| Tunel | 47245 cykli CPU |

[ODCZYT] Ślad kolejnych wywołań renderera w Atari800: kiść w tickach
12288–13300 wykonuje 63 zmiany faz, zawsze o jeden modulo 32 — dwa pełne
cykle bez pominiętej klatki. Obrany w 14336–14944 wykonuje 38 takich zmian,
również bez pominięć, i pokazuje wszystkie 32 fazy. Długość ujęć zachowana.
Sam pomiar instrukcji py65 nie jest FPS, dlatego osobno sprawdzono ten ślad.

## Testy i ograniczenia narzędziowe

Nowe testy wykonują pełne przygotowanie z 1122 wstrzykniętymi przerwaniami
oryginalnego playera. Wszystkie 64 surowe bitmapy są zgodne z generatorem.
Sprawdzane są banki fizyczne, PORTB, brak zapisów do obrazu/PMG i koszt obu
motywów poniżej 48000 cykli po rozgrzaniu. Najdroższe zadanie z NMI:
11462 cykle; bez NMI 10161 cykli. Pozostałe banki nie są zmieniane przez cache.

To overlay dla normalnego odtwarzania do przodu. Po wykorzystaniu banków
tytułu cofnięcie się do tytułu wymaga ponownego załadowania XEX. Duży seek
ze świeżego XEX poza okno bootstrapu zachowuje kod tytułu i korzysta z
poprzedniego RLE; taki seek nie mierzy kosztu przygotowanego odtwarzania.

[ODCZYT] Cały utwór Atari800 stereo: **10589472 bajty identyczne z v035**.
Bez próby na fizycznym Atari. XEX v244 i sprawdzony cache-work identyczne:
`4f6ab57d3919ce7bf0119607910a6a8dd931870beb2887898850925bc6e4eb5a`.
Main 2557 B ($1400–$1DFC), pozostają 3 B przed pulą wierszy $1E00.

[ODCZYT] `make check PYTHON=/tmp/finale197-venv/bin/python`: **189/189
testów**, bez pominięć, 151,2 s. Build roboczy i v244 identyczne.
