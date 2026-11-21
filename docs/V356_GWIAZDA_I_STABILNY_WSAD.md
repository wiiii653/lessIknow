# V356 — gwiazda finału i stabilna publikacja wsadu

W otwarciu pojawiło się oko, cień żuchwy i chłodna krawędź włosów dziewczyny.
Profil pozostaje czytelny w dużym kadrze oraz w ujęciach oddalających postać.
Paleta areny i pozycje kamery odpowiadają montażowi v355.

W akcie 3 piłka, satelity i odłamki są przygotowywane na niewidocznej stronie
PMG. Ukończona lista ANTIC i PMG przechodzą na ekran razem z ich pozycjami
w wygaszaniu. Wybór bufora przechowuje bank wsadu, bez odczytu PMBASE.
Niewidoczny bufor jest czyszczony w zakresie `$0980–$0BFF` albo `$8980–$8BFF`.
Zostają istniejące klatki, trajektorie i momenty trzech pęknięć tablicy.
To usuwa zapis do widocznego PMG wskazany w audycie v347. Przyczyna
obserwowanego na fizycznym Atari artefaktu pozostaje do potwierdzenia.

Finał zamyka fasetowana gwiazda przecięta dwiema orbitami, złożona z kafli
ANTIC 5. Znak podejmuje motyw czterech gwiazd znad leżącego chłopaka.
Listę końcową zaprojektowano z czterema DLI na liniach 0, 78, 156 i 234.
Znak korzysta z nieużywanych znaków fontu i ekranu pod `$BF00` po wygaśnięciu
terminala. Karta nadal wchodzi przy ticku 51980, a muzyka kończy się po 5:00.

## Obszary pamięci

- Zmiana kodu wsadu w banku wideo 1, `$4000–$4B7F`. Sprawdzenie rozmiaru
  pilnuje granicy danych bitmapy pod `$4B80`.
- Karta w banku sterującym 49. Lista startuje pod `$5C60`, kod i kafle mieszczą
  się w przerwach przed `$5CD0`, `$6000` i stanem orbit pod `$69B8`. Żadna
  część nie korzysta z zakresu strumienia wstążek `$6A00–$7DFF`.
- Tylko obrazy stagingowe indeksów 15 i 63 (licząc od zera) różnią się od v355.
  Pula współdzielona ma 299 wierszy i 11 491 B. Kod główny ma 2542 B;
  wszystkie 64 banki pozostają przydzielone.

## Plik i weryfikacja

`releases/less-i-know-demo-release-066-stereo.xex`, 945 964 B.
SHA-256 `2369853082b52dc69ebb03d88101722e3246f9a1a669c8d48a3bbde40a8f6fdd`.
Pakowanie według loadera 058, z kontrolą pełnych 64 obrazów i bootstrapu.

Przeszło 29 ukierunkowanych testów wsadu, postaci, finału, list ANTIC i loadera.
Test ruchomego VCOUNT sprawdził publikację oraz brak zapisów do widocznego
PMG przy różnych fazach wsadu i wejściach w ramkę. Pełnego `make check`
nie uruchamiano.

Atari800 PAL, 1088 XE, Altirra OS, dwa POKEY. Cały przebieg dał 59 834
identyczne z 064 pakiety rejestrów w tej samej kolejności, łącznie z wyciszeniem
startowym. W scenie wsadu zarejestrowano 543 publikacje PMBASE, na przemian
`$08` i `$88`, na liniach 248–256 w emulacji. Obejrzano wybrane kadry,
zapisane w `build/v356-kadry-atari800.png` i `build/v356-karta-finalowa.png`.
Nie przeprowadzono fizycznej próby AVG, pomiaru FPS ani odsłuchu analogowego.
