# V169 — nowa tekstura tunelu w akcie 5

## Zmiana

W 5B tunel używa spiralnych pasm od ticku 38892. Dokładnie przy ticku
40388, w takcie 108, zmienia się w radialną siatkę gwiazd z ośmioma
wirującymi promieniami i koncentrycznymi pierścieniami. Zmiana obowiązuje
do końca zakresu 5B w ticku 41884. Granice ujęć, tempo animacji i piłka
zasłaniająca środek tunelu pozostają bez zmian.

Oba warianty współdzielą istniejące 32 klatki tunelu: 32–47 przechowują
spiralę, 48–63 nową siatkę. Są wybierane przez kompaktowy 16-bitowy
dispatcher ticków. W generatorze `tools/mosaic.py` wzory są liczone dla
tych samych czterokolorowych bitmap; nie dodano klatek ani alokacji banków.

## Pamięć i walidacja

- 64 banki nadal przydzielone; całych wolnych banków: 0.
- Potwierdzone luki w używanych bankach: nadal 31 623 B według mapy v166.
- Kod główny: 2552 B z 2560 B dostępnych przed `$1E00`; 8 B zapasu.
- Budowa `build/visual-prototype-v169.xex` zakończyła się poprawnie.
- Testów py65, porównania muzyki ani odtwarzania w Atari800/Altirrze nie
  wykonywano w tej zmianie.

SHA-256 XEX: `05f1c69517d4b1f459fec5b4183e59266392d9e169c72f4b6f4b3e35b9939b8e`.

Szczegółowa mapa przydziałów i pofragmentowanych luk: `MAPA_PAMIECI_V168.md`.
