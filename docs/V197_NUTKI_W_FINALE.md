# V197 — nutki wokół głowy w finale

Leżącemu chłopcu wirują wokół głowy na przemian cztery gwiazdki i cztery
symbole melodii: nuty oraz klucz wiolinowy z początkowego gwizdania.
Zmiana następuje co 256 ticków gracza (około 1,28 s). Zachowane są orbita,
zmiany kolorów, przygotowanie masek w nieaktywnym buforze PMG i końcowe
wygaszenie. Kształty melodii zachowują oryginalne sylwetki; dla mniejszego
kadru finałowego używają pojedynczych wierszy i zwykłej szerokości PMG.

Build: `build/visual-prototype-v197.xex` i odpowiadający JSON; para dev
zaktualizowana. Granice scen bez zmian. Kod główny nadal 2560 B.
Kontroler finału: 809 B przy $5CD0; dane 48 B przy $69C4 oraz 95 B przy
$7FA0 w istniejącym banku 49. Instalator sprawdza, że wszystkie zajmowane
miejsca były puste. Łącznie 952 B wobec 812 B w v196: dodatkowe 140 B.

[ODCZYT] Dziewięć testów `test_story_finale.py` zaliczonych: maski wszystkich
czterech obiektów przez cztery przełączenia, brak pozostałości w buforach,
orbita, raster, zachowanie NMI i PORTB oraz trwała czerń po zakończeniu.
[ODCZYT] Atari800 PAL / 1088XE / stereo POKEY: 6 125 832 identyczne bajty
w porównaniu z v035; porównanie obejmuje cały utwór.
[WNIOSEK] Testy CPU potwierdzają maski i moment publikacji rejestrów;
nie stanowią oceny wyglądu na fizycznym Atari.

[ODCZYT] Pełny `make check` zgłasza wcześniejsze błędy testów dotyczące
odzyskanych slotów Trevora, klatek pośrednich szarf i budżetu rastera.
Pięć zgłoszonych testów uruchomiono osobno na archiwalnym XEX v196:
wszystkie pięć również kończy się niepowodzeniem. Nie wynikają z masek finału.
Pełny wynik: 148 testów, 5 błędów potwierdzonych również na v196,
3 pominięte. Dziewięć testów finału przechodzi także w pełnym zestawie.
