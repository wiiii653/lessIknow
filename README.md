# The Less I Know The Better — Atari XE demo

Projekt stereo dla Atari XE z 1 MB RAM, oparty na playerze v035 i oryginalnej aranżacji POKEY.

## Stan projektu

Ostatnie wydanie produkcyjne to **v330 / stereo release 058**. Kandydat v352
przywraca loader v330, animuje kropki postępu ładowania banków i zachowuje tor
ósemki piłki w ujęciu oczu oraz końcówkę v330:

- XEX: `releases/less-i-know-demo-release-058-stereo.xex` (936 240 B)
- SHA-256: `f3c14bc36b96220ead8fbe24df2e0dfc7ef5d30371d5cd83d11f808b62706b8f`
- źródłowy build: `build/visual-prototype-v330.xex`
- kandydat v352: `build/visual-prototype-v352.xex`
- SHA-256: `b3031752e9615e3f69c7ab877cb115c1d798b39efdb500e1b0ee00d63f795d1d`
- paczka zgłoszeniowa: `releases/less-i-know-sv2026we-v330-submission/` i ZIP obok
- v352 trwa ok. 4:20.7; terminal od ticku 41884, końcowa karta od ticku 51980

Director steruje pierwszymi rotatorami, tunelem przed wsadem i montażem po
Trevorze. BUM/BAM z dymkami pojawia się na ostatnich bananach przed oczami i po nich.
Szczegóły: [montaż](docs/AKTUALNY_MONTAZ_V330.md) i [notatka v352](docs/V352_BANANY_PRZED_OCZAMI.md).

## Budowanie i weryfikacja

`make` tworzy zastępowany build roboczy `build/visual-prototype-dev.xex`.
`make check PYTHON=/ścieżka/do/venv/bin/python` uruchamia aktualny zestaw
py65. Szczegóły ograniczeń oraz zweryfikowany stan wydania są w
[statusie projektu](docs/PLAN_STATUS.md) i [przygotowaniu SV](docs/SV2026WE_PRZYGOTOWANIE.md).

v330: 28 ukierunkowanych testów py65 zaliczonych; pełnego `make check` nie
uruchomiono. Użytkownik potwierdził poprawny przebieg v330 na Atari 1088
Rambo z kartą AVG. v352 zbudowano jako stereo (298 współdzielonych wierszy,
2542 B kodu); szczegóły kontroli są w [notatce v352](docs/V352_BANANY_PRZED_OCZAMI.md).

## Zasady pracy

Wydania numerowane są niezmienne. Buduj wyłącznie stereo; wariant mono jest
wycofany. Nie zakładaj wolnych banków: wszystkie 64 banki są przydzielone.
Zachowuj historię wydań i sprawdzaj aktualny allocator przed zmianami pamięci.
