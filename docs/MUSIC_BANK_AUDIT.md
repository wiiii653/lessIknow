# Audyt banków muzyki v035

Źródło: `less-i-know-release-v035.xex`. Banki numerowane od 1, po 16 384 B.

| Banki | Odczytane przez dekoder | Niewykorzystane |
| --- | ---: | ---: |
| 1–7 | 114 688 B łącznie | 0 B |
| 8 | 2 820 B | 13 564 B |
| 9–14 | 0 B | 98 304 B |
| Razem | **117 508 B** | **111 868 B** |

Loader rezerwuje 229 376 B (224 KiB). Dekoder wykorzystuje 114,754 KiB,
a 109,246 KiB (48,77%) pozostaje nieodczytane. Sześć całych banków daje
96 KiB do odzyskania; dodatkowe 13,246 KiB leży na końcu ósmego banku.

## Istotny szczegół końca utworu

Ostatni bajt różny od `$FF` jest pod offsetem 2818 w banku 8. Dekoder czyta
jeszcze `$FF` pod offsetem 2819 jako znacznik końca. Dopiero offsety
2820–16383 są nieużywane. Samo obcięcie wszystkich końcowych `$FF` usunęłoby
również wymagany znacznik końca.

## Jak sprawdzono

`tools/audit_music_banks.py --trace` wykonuje oryginalne procedury restartu,
dekodowania i DLI v035 w py65 z modelowanym oknem banków `$4000–$7FFF`.
Rejestruje każdy odczyt z banków aż do ustawienia flagi końca `$24C8`.
Wynik: 59 833 aktualizacje, ostatni odczyt w banku 8; banki 9–14 nieczytane.
To badanie dekodera, nie profiler ANTIC-a ani pomiar na fizycznym Atari.

Dodatkowo w testowym `build/music-padding-probe.xex` zastąpiono końcówkę
banku 8 od offsetu 2820 oraz całe banki 9–14 wartością `$55`. Porównanie
z oryginałem w Atari800 PAL/1088XE wykazało 2 941 200 zgodnych bajtów
rejestrów stereo POKEY (~819 s odtwarzania, cały utwór objęty testem).
Początkową ciszę wyrównano raz; podczas utworu nie przesuwano próbek.

Oryginalny XEX i aktualny build produkcji nie zostały odchudzone ani
zmodyfikowane przez ten audyt. Reprodukcja analizy (py65 z requirements-dev.txt):

```sh
python tools/audit_music_banks.py --trace --json build/music-bank-audit.json
```

Wniosek: v035 wymaga **ośmiu**, a nie siedmiu banków danych. Stare założenie
o siedmiu bankach w analizie v024 nie nadaje się do zastosowania w v035.
