# V191 — wycentrowane BUM i dymki przy pięściach

BUM miało zachowane wyrównanie dawnego czteroliterowego BNG!, dlatego
trzy litery były przesunięte w lewo. Oba słowa, BUM i BAM, mają teraz
24-pikselowe pole wycentrowane w 32-pikselowym dymku: przesunięcie +4.

Każdy z 40 ciosów otrzymuje pseudolosowy punkt, obliczony generatorem
xorshift i zapisany w tablicy. Rozrzut ogranicza się do ±6 logicznych
pikseli poziomo i ±3 podwójnych wierszy PMG (±6 linii obrazu) pionowo
wokół kotwicy właściwej pięści. W przebiegu występuje 16 różnych punktów
dla jednej ręki i 18 dla drugiej. Pozycja jest stała podczas jednego
ciosu; napis, dymek i rozprysk korzystają z tego samego początku.
Sekwencja jest powtarzalna między odtworzeniami i nie zużywa czasu CPU
na losowanie w trakcie rastra. Piłki odbijane przez Trevora zachowują tory.

- XEX: `build/visual-prototype-v191.xex`; dev identyczny.
- SHA-256: `218d1ab3524b13cb78d5e7486306f8bb6dbacb5295790e263a9f699d885d11ad`.
- Trevor helper: 2500 B, 60 B zapasu do $6A00; main 2560 B bez zapasu.
- 24 testy zaliczone: centrowanie obu słów, wszystkie 40 kotwic i stałość
  przez cios, rozrzut we właściwym obszarze, napisy, bufory PMG i sceny
  Trevora. Log: `build/v191-focused-check.log`.
- Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 16 037 712 identycznych
  bajtów z v035, cały utwór. `build/v191-playback-check.log`.
- Podgląd po callbackach 6502: `build/v191-impact-preview.png`.
  Nie jest przechwyceniem emulatora i nie modeluje DMA ANTIC.
- Nie ponawiano pełnego zestawu testów; wcześniejsze niezwiązane
  rozbieżności są opisane przy v189. Bez nowej oceny na fizycznym Atari.
