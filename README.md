# The Less I Know The Better — Atari XE demo

Projekt stereo dla Atari XE z 1 MB RAM, oparty na playerze v035 i oryginalnej aranżacji POKEY.

## Stan projektu

Zatwierdzona wersja po party to **v390 / stereo 133**.
[Plik XEX](releases/less-i-know-demo-release-133-stereo.xex).
Wzorzec sprawdzony z karty AVG na Atari 1088 Rambo to stereo 058 / v330.

Demo trwa około pięciu minut. Terminal wchodzi w ticku 41 884,
a końcowa karta w ticku 51 980. Rotator używa oryginalnych tekstur z wydania 119.
Obrót i zoom obejmują całą mozaikę. [Montaż](docs/AKTUALNY_MONTAZ_V330.md).

## Budowanie i weryfikacja

Po zainstalowaniu `requirements-dev.txt` w środowisku wirtualnym:

```sh
make all PYTHON=/ścieżka/do/venv/bin/python
make check PYTHON=/ścieżka/do/venv/bin/python
```

Build roboczy tworzy prototyp oraz `build/hardware-dev.xex` z miksem stereo
z wydania 133, werblem przed halą, narastaniem perkusji w treningu
i akcentem basowym przed wejściem tancerki. Aby zapakować
bieżący prototyp z tym miksem, użyj nowej ścieżki wyjściowej:

```sh
python3 tools/build_hardware_xex.py build/visual-prototype-dev.xex /tmp/less-i-know-stereo.xex --approved-music --earlier-percussion
```

Sumę SHA-256 i wyniki prób zawiera [status projektu](docs/PLAN_STATUS.md).
Pakowanie sprzętowe opisuje [kontrakt loadera](docs/HARDWARE_LOADER_CONTRACT.md).

## Zasady pracy

Wydania numerowane są niezmienne. Buduj wyłącznie stereo; wariant mono jest
wycofany. Nie zakładaj wolnych banków: wszystkie 64 banki są przydzielone.
Zachowuj historię wydań i sprawdzaj aktualny allocator przed zmianami pamięci.
