# V136 — trzy ujęcia tańca ze wstęgami

## Zawartość i synchronizacja

[ODCZYT] Cztery dawne ilustracje występu w 14959–20942 zastąpiono trzema
ujęciami: grupa 40–44, solówka 44–48, grupa z przygotowaniem i wyrzutem
bohaterki 48–56. Końcowy wyrzut ma cztery pozycje wznoszenia. Zegar playera
wybiera pozy według tablicy 128 granic półuderzeń; oddzielny cykl 16 kształtów
wstęg wynika ze spójnej kopii ticka. Nie zmieniono granic aktów ani czterech
aktualizacji muzyki na ramkę. Zmianę treści i trzy ujęcia zatwierdził użytkownik.

[ODCZYT] Osiem źródłowych póz komponuje 16 klatek 160×64, powtarzanych
trzykrotnie przez ANTIC. Tło przedstawia wspólną salę; postacie używają
czterech kolorów, a cztery players i cztery missiles tworzą wstęgi oraz
cienkie akcenty. To adaptacja choreografii i strojów, nie rotoskopia teledysku.

## Pamięć i prezentacja

[ODCZYT] Nadal 64 banki. Wykorzystano potwierdzone wolne sloty:

- Banki 24–39: `$4A00–$53FF`, 16 × 2560 B = 40 960 B bitmap.
- Bank 49: kontroler `$5400`, 1412 B; szarfy `$6A00–$7DFF`, 5120 B;
  pozycje zaczepienia `$7E00–$7E7F`, 128 B. Oryginalne pozy/kod Trevora
  pozostają w swoich obszarach; instalator odrzuca nadpisanie niezerowych danych.
- Nowy niebankowany trampoline kopii ma 25 B. PORTB zachowywany jest
  także przez NMI muzyki.
- Bufory PMG: `$0980–$0BFF` i `$8980–$8BFF`. Drugi obszar wydzielono
  z puli statycznych wierszy i ponownie rozłożono te wiersze podczas budowy.
  Przy zapisie działa poprzedni PMG; PMBASE przełącza się wraz z rejestrami
  pozycji w ograniczonym oknie rastra. Bitmapa również powstaje w nieaktywnym
  buforze `$9000` / `$B000`.

[ODCZYT] Dawne portrety usunięto z wynikowego banku 8; muzyka poniżej
`$4B10` i trening powyżej `$6000` są zachowane. Nowa scena zużywa więcej
danych niż stare cztery statyczne ilustracje, lecz mieści się w dotychczasowej
konfiguracji bez dokładania banków.

## Walidacja

[ODCZYT] Pełny `make check`: 90 testów, 87 zaliczonych, 3 pominięte
z powodu braku archiwalnego v126; 81,307 s. Nowe/regulowane testy obejmują
128 kroków, skoki między ujęciami, ruch szarf przy zatrzymanej pozie,
brak zapisów do aktywnego PMG/bitmapy, bezpieczne zatwierdzanie przy różnych
pozycjach rastra oraz kopiowanie z rzeczywistymi NMI dekodera i odtwarzaniem
PORTB. Symulacja VCOUNT nie modeluje DMA ANTIC ani terminów na sprzęcie.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 14 744 880
identycznych bajtów względem v035, cały utwór. To porównanie rejestrów,
nie odsłuch na fizycznym Atari ani pomiar płynności obrazu.

Podgląd `build/v136-ribbon-dance.gif` pochodzi z 250 kolejnych wykonań callbacku
6502; odstęp 24 ticki, około 30 sekund. Tempo i paleta są przybliżone;
GIF nie uwzględnia DMA, czasu kopiowania ani pomijania faz w emulatorze.
Do oceny artystycznej oraz docelowej płynności pozostaje odtworzenie XEX-a.

## Źródła grafiki

Built-in imagegen, referencja stroju z materiału projektanta:
https://www.behance.net/gallery/31604763/Tame-Impala-Textile-Design

- Grafika: `assets/art/source/act2_ribbon_dancer_v136.png`.
- Pełny prompt: `assets/art/source/act2_ribbon_dancer_v136.prompt.txt`.
- Generator i renderer: `tools/ribbon_dance.py`.
- Wydanie: `build/visual-prototype-v136.xex`.
