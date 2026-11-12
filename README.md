# The Less I Know The Better — Atari XE demo

Projekt stereo dla Atari XE z 1 MB RAM, oparty na playerze v035 i oryginalnej aranżacji POKEY.

## Stan projektu

Aktualnym wydaniem jest **v330 / stereo release 058**:

- XEX: `releases/less-i-know-demo-release-058-stereo.xex` (936 240 B)
- SHA-256: `f3c14bc36b96220ead8fbe24df2e0dfc7ef5d30371d5cd83d11f808b62706b8f`
- źródłowy build: `build/visual-prototype-v330.xex`
- paczka zgłoszeniowa: `releases/less-i-know-sv2026we-v330-submission/` i ZIP obok
- długość: ok. 4:20.7; czarny ekran od ticku 51980

Po Trevorze director przejmuje rotatory na pierwszym callbacku. Od taktu 80
muzycznie zmienia motyw, kierunek i prędkość. Oczy dziewczyny pozostają w
zakresie 39379–40126. Szczegóły zmian: [montaż v330](docs/AKTUALNY_MONTAZ_V330.md)
i [notatka wydania](docs/V330_KROTSZY_MONTAZ_I_DIRECTOR.md).

## Budowanie i weryfikacja

`make` tworzy zastępowany build roboczy `build/visual-prototype-dev.xex`.
`make check PYTHON=/ścieżka/do/venv/bin/python` uruchamia aktualny zestaw
py65. Szczegóły ograniczeń oraz zweryfikowany stan wydania są w
[statusie projektu](docs/PLAN_STATUS.md) i [przygotowaniu SV](docs/SV2026WE_PRZYGOTOWANIE.md).

v330: 28 ukierunkowanych testów py65 zaliczonych. Pełnego `make check` po
ostatnich zmianach nie uruchomiono. Użytkownik potwierdził poprawny pełny
przebieg v330 na Atari 1088 Rambo uruchomionym z karty AVG.

## Zasady pracy

Wydania numerowane są niezmienne. Buduj wyłącznie stereo; wariant mono jest
wycofany. Nie zakładaj wolnych banków: wszystkie 64 banki są przydzielone.
Zachowuj historię wydań i sprawdzaj aktualny allocator przed zmianami pamięci.
