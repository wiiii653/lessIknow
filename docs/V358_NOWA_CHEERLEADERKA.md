# V358 — nowa cheerleaderka w ujęciach przed areną

Punkty odniesienia: ujęcia z 058 (v330, paczka party), 061 (v352) i 070
(v357). Obejrzano je w Atari800. W 070 bliski kadr dziewczyny powielał
próbki siatki 48×64, podczas gdy twarz chłopaka miała kontury na docelowej
siatce 160×64. Boczny spacer nadal używał wcześniejszego korpusu i ruchu rąk.

Dziewczyna jest narysowana od podstaw w palecie areny. Z bliska ma pojedyncze
kolumny konturu, podobny do chłopaka różowy cień na twarzy, ciemne włosy
z kokardą i kurtkę z Fuji. Dalsze kadry używają osobnych póz i skal.
Boczna panorama pokazuje sylwetkę ze spódnicą, skarpetami i butami. Osiem
faz chodu daje przetoczenie stopy, uniesienie pięty, zmianę kolana i ruch
rąk przeciwny do kroku. Fazy wypełniają 18 istniejących klatek od ticku 3553.
Tło areny nadal przesuwa się w przeciwnym kierunku. Kadry po spojrzeniu
chłopaka pozostają cięciami na kolejne pozy oddalającej się dziewczyny.

Porównania rzeczywistych kadrów emulatora: `build/v358-opening-comparison.png`
i 18-klatkowy `build/v358-walk-comparison.gif` (058, 070, 072).
Kadr chłopaka na prawo od linii kompozycji, jego reakcje i ticki scen są
zachowane. Początkowe tunele i wejście bananów po Trevorze odpowiadają v357.

## Pamięć i loader

Nowe klatki panoramy zmieniają pięć obrazów stagingowych o indeksach 33–37
(licząc od zera), bez przydzielania kolejnego banku. Pula współdzielona
zawiera 297 wierszy i 11 481 B; kod główny ma 2542 B. Generator ogranicza
pule od `$0400` i `$0900` do ostatnich bajtów odtwarzanych przez bootstrap
058 (`$07DF` i `$0976`). Zachowane są wszystkie 64 obrazy i kontrakt loadera.

## Pliki i sprawdzenie

- Stereo `releases/less-i-know-demo-release-072-stereo.xex`, 945 059 B,
  SHA-256 `4a4399db47153d5d8a2c938a05b8b25f4633a20e7e9604c4309156e22b3f4251`.
- Mono `releases/less-i-know-demo-release-073-mono.xex`, 945 059 B,
  SHA-256 `9291792352a01006bdfa85044505e6b6418c8023ebd2cf65bf33cc0c7f9e6b48`.

21 ukierunkowanych testów kompozycji, panoramy, scen i loadera przeszło.
W Atari800 PAL, 1088 XE, Altirra OS porównano po 59 833 aktualizacje: 072
z dwoma POKEY daje wartości identyczne z 070, a 073 z jednym POKEY daje
wartości identyczne z 071. Pełny utwór trwa 5:00. Obejrzano kadry emulatora.
Nie wykonano fizycznej próby tych plików ani pełnego `make check`.
