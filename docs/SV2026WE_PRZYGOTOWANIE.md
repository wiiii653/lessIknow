# Silly Venture 2026 WE — przygotowanie zgłoszenia

Stan sprawdzenia: 2026-11-12. Oficjalny regulamin v4.2.2:
https://sillyventure.eu/en/compos

- Termin zgłoszeń: 2026-11-12, 12:00 CET. Zgłoszenie przez formularz na
  stronie organizatora. W repozytorium nie ma potwierdzenia zgłoszenia.
- Kategoria do sprawdzenia na docelowej maszynie: Atari XL/XE Demo Standard.
  Organizator podaje XL/XE z Ultimate 1 MB i stereo POKEY jako konfigurację
  standardową. Lokalny test Atari800/1088XE nie dowodzi zgodności z konkretnym
  rozszerzeniem na party.
- Najnowszy numerowany stereo XEX to release 052/v319:
  `releases/less-i-know-demo-release-052-stereo.xex` (936,106 B), zbudowany
  dla AVG i 1 MB RAM/stereo POKEY. SHA-256:
  `0e1fd31bdb9a666bda5783b5f4f3fbffb83e1fc154f9357dfd463f24c1f5e8fa`.
- W v319 poprawiono maskę przy lewym ramieniu i przedramieniu kozłującego
  zawodnika. Test porównujący maskę z release 001 przechodzi. Najnowszego
  wydania nie uruchomiono na fizycznym Atari; wcześniejsze
  wydania uruchamiały się z AVG na konfiguracji 1088 Rambo. Testy CPU nie
  potwierdzają obrazu z DMA, FPS ani zgodności z konkretną maszyną party.
- Pełne porównanie całego utworu stereo POKEY z oryginalnym v035 dotyczy
  starszego builda v260: 16,272,720 bajtów zgodnych. Release 048 nie został
  ponownie porównany przez Atari800.
- Aktualny pakiet zgłoszeniowy dla release 052 znajduje się w
  `releases/less-i-know-sv2026we-v319-submission/` i w ZIP obok. Starsze
  szkice v257/v260 zachowano bez zmian. Formularz organizatora wymaga pliku
  TXT i wykonywalnego pliku; film MP4 1920×1080/50 fps jest opcjonalny,
  zalecany przez organizatora i nie został dołączony. Pakiet nie został
  wysłany przez formularz; status zgłoszenia trzeba potwierdzić poza repo.
- Aktualny montaż po Trevorze to ruchomy rotator/tunel z oczami dziewczyny;
  komiksowe przebitki v257 wycofano w v260. MP4/1920×1080/50 fps nie zostało
  przygotowane. Długie powtarzające się fragmenty mogą zostać przez
  organizatora skrócone.
- Użycie AI opisano w `info.txt`: programowanie i grafika były wspomagane
  przez AI, a produkcja obejmowała dwa tygodnie intensywnej pracy dzień i noc
  z agentami AI (deklaracja autora).
- Regulamin zabrania wcześniejszej publikacji i całych samplowanych fragmentów
  cudzych chronionych utworów. Autor potwierdza, że użyto partytury MIDI
  i nie ma sampli z komercyjnego nagrania. Autor potwierdził, że demo było
  dotąd udostępniane wyłącznie prywatnie. Autor deklaruje posiadanie zgody
  na wykorzystanie partytury MIDI i kompozycji; sam fakt zgodności z
  playerem v035 nie dowodzi ich statusu.
- Nie zweryfikowano odbioru obrazu i dźwięku na fizycznym Atari ani zgodności
  bankowania z maszyną konkursową. Nie ogłaszać wersji compo-ready.
