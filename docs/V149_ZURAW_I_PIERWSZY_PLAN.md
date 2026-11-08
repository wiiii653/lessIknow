# V149 — zwarty Żuraw i fajerwerki przed obrazem

## Zmiana

Na życzenie użytkownika lewa baszta historycznego Żurawia jest połączona
z korpusem ciągłą ścianą bramną. Zlikwidowano szczelinę z ruchomą plazmą.
Całą sylwetkę zmniejszono z 40×32 do 36×29 pikseli źródłowych na siatce
80×64; położenie (22,35) zachowuje wyśrodkowanie i nabrzeże na dole.
Pozostają dwie murowane baszty, dachy, drewniana część wysięgowa i kontrast
chłodnego muru z ciepłymi dachami oraz obrysem.

Fajerwerki obu plansz intro mają teraz cztery przesunięte w fazie cykle:
wznoszenie rakiety z ogonem, centralny rozbłysk, promienisty rozkwit,
opadające i zanikające fragmenty. Missiles mają dłuższy pionowy zakres
śladów. Kolory nadal cyklicznie się zmieniają i podlegają wygaszeniu planszy.

Usunięto przycinanie kształtów do napisów, ich cieni i sylwetki Żurawia.
Kompletne players i missiles są przed plazmą, literami oraz budynkiem,
z `PRIOR=$C1`, bez trybu piątego playera. To świadomie zastępuje ochronę
napisów i budynku z v140/v144. Kolejność wejść I KNOW → THE BETTER → THE LESS,
końcowy układ tekstu i wszystkie ticki scen pozostają bez zmian.

## Pamięć i kod

[ODCZYT] Banki loadera 40 i 41 mają ten sam kontroler i kształty:

- Kod 1356 B: `$6C00–$714B`, wejście publikacji `$7000`.
- Kotwice pionowe: `$73F8–$73FC` (5 B), przeniesione sprzed starego końca danych.
- Kształty: `$7400–$7FFF` (3072 B). Cztery players po 16×32 wiersze;
  wspólna płaszczyzna missiles 16×64 wiersze, z osobną tabelą adresów.
- Instalator sprawdza rozdzielenie kodu, kotwic i danych oraz pustą przestrzeń
  docelową. Nowe kształty nie dopisują nic poza końcem banku.

[ODCZYT] Koszt względem v148: 2×(512 B kształtów + 32 B tabel) = 1088 B.
Nadal 64 banki. Odzysk netto względem v141 wynosi **23 683 B = 23,13 KiB**.
Grafika Żurawia mieści się w istniejących klatkach plazmy. Główny kod nadal
2515 B (`$1400–$1DD2`), z 45 B przed pulą od `$1E00`.

Przygotowanie efektu zachowuje nieaktywny bufor PMG, a publikacja odbywa
się w ograniczonym oknie VCOUNT 124–127. Cztery aktualizacje muzyki na
klatkę PAL i przywracanie PORTB są zachowane.

## Walidacja

[ODCZYT] Testy intro sprawdzają ciągłość połączenia lewej baszty, rozmiar
budynku, zachowaną kolejność napisów, pełne kształty w obu bankach,
nakładanie na litery i Żurawia, opadanie/kurczenie późnych iskier, własność
buforów PMG, PORTB oraz publikację przy ruchomym VCOUNT.

[ODCZYT] `make check`: **115 testów, 112 zaliczonych, 3 pominięte**
(brak archiwalnego v126), 90,781 s.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: **15 348 384
identyczne bajty** względem v035; objęty cały utwór.

Podglądy po wykonaniu callbacku 6502: `build/v149-intro.gif` (oba napisy,
jednokrotne odtworzenie) i `build/v149-zuraw-fireworks.png`. Paleta i tempo
podglądów są przybliżone. Nie jest to nagranie emulatora, pomiar FPS ani
sprawdzenie rastra na fizycznym Atari. Porównanie POKEY nie zastępuje odsłuchu.

## Wydanie

`build/visual-prototype-v149.xex` z odpowiadającym JSON; identyczne
z plikami roboczymi `visual-prototype-dev`.

SHA-256 XEX: `f57e236d15a2fd910c84a4a50ef1d6b5a1391ea63bb1fb2c4f43737ab9f35465`.
