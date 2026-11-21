# Stały kontrakt loadera AVG / 1088 Rambo

Zapisane 2026-11-17 po zgłoszeniu kolejnej awarii na fizycznym Atari.
Przeczytaj przed każdą zmianą bankowania, loadera lub pakowania XEX.
Nie zastępuj tego dokumentu starymi założeniami z notatek Vxxx.

## Wzorzec i fakty

Ostatni pełny przebieg potwierdzony przez użytkownika: v330, stereo release
058, AVG, Atari 1088 Rambo. PAL/NTSC oraz fizyczna konfiguracja drugiego
POKEY nie zostały podane w tym zgłoszeniu; nie dopisywać ich jako faktów.

Plik: `releases/less-i-know-demo-release-058-stereo.xex`, 936 240 B.
SHA-256: `f3c14bc36b96220ead8fbe24df2e0dfc7ef5d30371d5cd83d11f808b62706b8f`.
Nie nadpisywać wzorca ani innych numerowanych wydań.

Release 059 i 060 wcześniej nie wystartowały na sprzęcie użytkownika.
Release 061 ma identyczne ze wzorcem 058 wszystkie 51 procedur `$1000`
(50 banków wideo + kopia RAM pod ROM), ekran, 66 wrapperów, kod zerowania
i bootstrap. Zatem samą różnicą tych procedur nie można wyjaśnić awarii 061.
Użytkownik doprecyzował, że najnowsza awaria dotyczyła prototypu v353.

Prototyp v353 ma 1 115 800 B, pełne obrazy banków, ekran `$0600/$0700/$0780`,
bez wrapperów `$3900`, czyszczenia `$3A00` i bootstrapu `$4800`.
Nowe procedury banków dodatkowo piszą postęp do `$0641–$0643` i `$06FF`.
Jest to inna ścieżka ładowania niż działające wydanie sprzętowe. Nie ustalono,
która pojedyncza różnica wywołuje fizyczną awarię; nie przedstawiać hipotezy
jako potwierdzonej diagnozy.

## Reguły obowiązkowe

- Ekran podczas ładowania: tekst `$3800`, lista ANTIC `$3880`, INIT `$38A0`.
- Zachować oryginalną detekcję banków v035 i selektory 50 dodatkowych banków.
  Nie zmieniać mapy ani kolejności na podstawie samego emulatora.
- 66 INIT-ów przechodzi przez wrapper `$3900`, w kolejności ze wzorca 058.
  Wrapper zachowuje rejestry i flagi wokół odświeżenia ekranu.
- Przed każdym z 64 obrazów wyzerować bufor `$8000–$BFFF` przez INIT `$3A00`.
  Dopiero potem wczytać niezerowe fragmenty. Odtworzone 64 obrazy muszą być
  identyczne bajtowo z surowym prototypem, łącznie z obrazem RAM pod ROM.
- Nie wczytywać końcowych danych runtime `$0400–$0BFF` do obszarów roboczych
  loadera w trakcie ładowania. Odłożyć je do `$4000–$47FF` i odtworzyć na końcu.
- Zachować zakresy kopii 058: `$0400–$07DF`, `$0800–$08BF`, `$0900–$0976`,
  `$0980–$09FF`, `$0A00–$0BFF`. Krótszy helper v353 uzupełnić dwoma zerami.
  Wzrost poza te zakresy wymaga ponownego audytu, a nie cichej zmiany bootstrapu.
- Nie zmieniać PORTB między buforem `$4000` a bootstrapem. Bootstrap `$4800`
  wyłącza IRQ/NMI, odtwarza niską RAM i wykonuje `JMP $13E0`, bez powrotu
  do loadera i bez zależności od obsługi RUNAD przez AVG.
- Zachować rozmiar poniżej 1 MiB jako warunek zgodności ze sprawdzoną ścieżką.
  Nie twierdzić, że sam limit rozmiaru jest dowiedzioną przyczyną awarii.
- Nie przenosić kropek postępu do niskiej RAM w loaderze sprzętowym.
  Samo porównanie adresów i liczby INIT-ów nie wystarcza.

## Budowanie i weryfikacja

`make all PYTHON=/path/to/python` buduje prototyp i `build/hardware-dev.xex`.
`make hardware PYTHON=/path/to/python` odświeża sam cel sprzętowy wraz
z zależnościami. Do numerowanego, nowego kandydata:

```sh
python3 tools/build_hardware_xex.py build/visual-prototype-v353.xex releases/less-i-know-demo-release-062-stereo.xex
```

Narzędzie odmawia nadpisania numerowanego pliku, sprawdza SHA-256 wzorca,
odrzuca nieznane zmiany procedur oraz porównuje pełny kod loadera ze wzorcem.
Nie zmienia grafiki, scen, alokacji 64 banków ani playera runtime.

2026-11-17 wykonano cztery testy `test_hardware_loader`: odtworzenie całego
058 z prototypu v330 bajt w bajt, zgodność wszystkich 64 obrazów v353,
odrzucenie zmienionego kodu banku i wykonanie bootstrapu w py65 z kontrolą
odtworzenia danych runtime oraz przejścia do `$13E0`.
py65 nie modeluje ANTIC DMA ani fizycznych terminów rastrowych.
Potwierdzenie na emulatorze nie zastępuje próby na AVG / 1088 Rambo.

Kandydat 062: 945 676 B, SHA-256
`0699c0ac764e03ca82c00d971b33d0e70571ae1699574d60fcad77db48d859ac`.
`make hardware PYTHON=python3` wygenerował identyczny plik.
Atari800 PAL / emulowane 1088 XE / Altirra OS / stereo: porównanie 062
z surowym v353 dało 5 174 424 identyczne bajty POKEY, ok. 1441,4 s
emulowanych. Bez wizualnej oceny, fizycznej próby i pełnego `make check`.

Historia działającego rozwiązania: [V273](V273_START_AVG_RAMBO.md).
Szczegóły dawnego potoku: [loader](loader/README.md). W razie sprzeczności
stosować bieżący kontrakt i narzędzie `build_hardware_xex.py`.

## Szybkie czyszczenie w kandydatach 100 i 101

Flaga `--fast-clear` wybiera eksperymentalną procedurę. Domyślny build,
w tym `make hardware`, weryfikuje loader bajt w bajt względem 058.
Wariant najpierw przechodzi tę samą weryfikację, a potem podmienia
wyłącznie zawartość 64 segmentów procedury `$3A00`. Wszystkie 64 INIT-y
czyszczenia wciąż zerują całe `$8000–$BFFF`. Procedura zachowuje
A, X, Y i flagi oraz nie dotyka PORTB.

Procedura próbna zajmuje `$3A00–$3AD3`. Budowanie sprawdza, że zakres
nie nakłada się na ładowane dane przed ostatnim zerowaniem i zostaje
w całości pokryty przez późny segment runtime przed bootstrapem
`$4800`. Wydanie 058 pozostaje wzorcem sprzętowym. Wyniki porównania
i odnośniki do kandydatów są w [analizie optymalizacji](loader/10_analiza_optymalizacji.md).
