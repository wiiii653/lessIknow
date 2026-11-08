# V185 — wcześniejszy gwizd i dłużej widoczne nuty

Gwizd zaczyna się w ticku 4862, po ujęciu mijania chłopca w pierwszym planie
(4488). Poza z dziubkiem i lecące nuty pozostają aktywne w scenach 10–12,
aż do początku ćwiczeń w ticku 5984. Cała melodia jest widoczna przez około
5,6 s, zamiast 2,3 s w v184. Początek wypada około 3,3 s wcześniej.

Dziewczyna nadal oddala się po torze do drzwi w dotychczasowych skalach.
Jej ostatnia pozycja ponownie zaczyna się w oryginalnym ticku 5610,
niezależnie od początku gwizdu. Chłopiec najpierw patrzy przed siebie,
w 4488 ogląda się za nią i dopiero w 4862 zaczyna gwizdać.

Jedna faza lotu trwa teraz osiem ticków zamiast czterech. Pojedynczy znak
unosi się przez około 2,56 s. W całym ujęciu faza nie zawija 8-bitowego
zegara, więc kolejne nuty nie znikają przy ponownym naliczaniu opóźnienia
emisji. Zachowano buforowanie PMG i ślady missiles.

## Build i sprawdzenie

- `build/visual-prototype-v185.xex` i JSON; dev identyczny.
- SHA-256: `5df7b3c2d811ac8cd9c33da8737428269d1c524d78ba73fbe0b791382e56760d`.
- 316 wierszy, 12 174 B danych wierszy, 2552 B kodu głównego.
- Helper PMG 839 B w $6A00–$6D46 banku loadera 0; bez nowych banków.
- 14 testów zaliczonych: emisja, czas i kierunek lotu, ciągłość w scenach
  10–12, zachowanie przy granicy dawnego zawijania zegara, bufory PMG,
  wyłączenie w 5984, maski, panorama v175, kompozycja i regresje piłki.
- `build/v185-whistle.gif` pokazuje całą melodię po wykonaniu callbacków
  6502. Nie modeluje DMA ANTIC. Nie wykonano nowej walidacji emulatorowej
  ani sprzętowej.
