# Silly Venture 2026 WE — przygotowanie zgłoszenia

Stan sprawdzenia: 2026-11-11. Oficjalny regulamin v4.2.2:
https://sillyventure.eu/en/compos

- Termin zgłoszeń: 2026-11-12, 12:00 CET. Zgłoszenie przez formularz na
  stronie organizatora. W repozytorium nie ma potwierdzenia zgłoszenia.
- Kategoria do sprawdzenia na docelowej maszynie: Atari XL/XE Demo Standard.
  Organizator podaje XL/XE z Ultimate 1 MB i stereo POKEY jako konfigurację
  standardową. Lokalny test Atari800/1088XE nie dowodzi zgodności z konkretnym
  rozszerzeniem na party.
- Najnowszy numerowany XEX to release 008/v261:
  `releases/less-i-know-demo-release-008.xex` (1,111,730 B), bajtowo zgodny
  z `build/visual-prototype-v261.xex`. SHA-256:
  `fff207ea35990a0d4694e1e510f4c785fa43a7c06d3d2010733c2165b8a6d836`.
  V261 dodaje KEY-G i FALCON do greetz, zachowując FOORMAN i harmonogram.
- Pełne `make check` v261: 199/199 testów, 152.147 s. Nie wykonano po v261
  odtworzenia w Atari800 ani na fizycznym Atari. Ostatnie pełne porównanie
  stereo POKEY dotyczy v260: 16,272,720 bajtów zgodnych z v035. Testy CPU
  nie potwierdzają obrazu z DMA, FPS ani zgodności rozszerzenia pamięci.
- Pliki przygotowania konkursowego są starsze od release 008 i nie tworzą
  aktualnego pakietu v261: `releases/sv2026we-preparation/entry-draft.txt`
  opisuje v257, a `releases/less-i-know-sv2026we-v260-candidate/` oraz
  `releases/less-i-know-sv2026we-v260-candidate.zip` zawierają v260/release 007.
  Katalog jest nieśledzony, ZIP jest zachowany jako numerowany artefakt; oba
  pozostały nietknięte.
  Przed zgłoszeniem trzeba wybrać wersję i przygotować zgodny XEX, TXT,
  checksumę oraz ewentualny ZIP. Nazwy, pełne credits i szczegóły autorstwa
  wymagają potwierdzenia. Status zgłoszenia należy potwierdzić poza repozytorium.
- Aktualny montaż po Trevorze to ruchomy rotator/tunel z oczami dziewczyny;
  komiksowe przebitki v257 wycofano w v260. MP4/1920×1080/50 fps nie zostało
  przygotowane. Długie powtarzające się fragmenty mogą zostać przez
  organizatora skrócone.
- Użycie AI w demo należy jasno zgłosić w komentarzu; opis w szkicu wymaga
  potwierdzenia szczegółów.
- Regulamin zabrania wcześniejszej publikacji i całych samplowanych fragmentów
  cudzych chronionych utworów. Autor potwierdza, że użyto partytury MIDI
  i nie ma sampli z komercyjnego nagrania. Autor potwierdził, że demo było
  dotąd udostępniane wyłącznie prywatnie. Autor deklaruje posiadanie zgody
  na wykorzystanie partytury MIDI i kompozycji; sam fakt zgodności z
  playerem v035 nie dowodzi ich statusu.
- Nie zweryfikowano odbioru obrazu i dźwięku na fizycznym Atari ani zgodności
  bankowania z maszyną konkursową. Nie ogłaszać wersji compo-ready.
