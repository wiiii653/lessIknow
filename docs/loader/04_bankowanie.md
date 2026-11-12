# 4. Bankowanie pamięci

## 4.1. PORTB — podstawy

`[ODCZYT]` Rejestr `$D301` (PORTB) na Atari XL/XE ma 8 bitów:

| Bit | Znaczenie w standardzie 130XE |
| ---: | --- |
| 0 | 1 = ROM OS widoczny, 0 = RAM pod ROM |
| 1 | 1 = BASIC widoczny |
| 2–3 | wybór banku CPU w oknie `$4000–$7FFF` |
| 4–5 | wybór banku ANTIC |
| 6–7 | nieużywane |

`[ODCZYT]` Rozszerzenia 1 MB muszą zaadresować 64 banki po 16 KiB, czyli
potrzebują **6 bitów** numeru banku. Klony (Rambo 1 MB, Newell, Compy-Shop,
Ultimate 1 MB) robią to różnie — bit 1, 4 lub 7 mogą być przejęte na numer
banku. Ta sama wartość `$D301` znaczy więc co innego na różnych maszynach.

`[ODCZYT]` Na testowanym klonie działa zestaw bitów **1, 2, 3, 5, 6, 7**,
z bitem 0 = 1 i bitem 4 = 0. Potwierdza to test sprzętowy
`avg-bank-map-diagnostic-003.xex` (`BANK MAP PASSED`, 64 rozdzielone banki).

## 4.2. 64 selektory używane przez loader

`[ODCZYT]` `tools/school_portrait_bank.py`, etykieta `candidates`:

```
81 83 85 87 89 8B 8D 8F   A1 A3 A5 A7 A9 AB AD AF
C1 C3 C5 C7 C9 CB CD CF   E1 E3 E5 E7 E9 EB ED EF
01 03 05 07 09 0B 0D 0F   21 23 25 27 29 2B 2D 2F
41 43 45 47 49 4B 4D 4F   61 63 65 67 69 6B 6D 6F
```

To 8 grup × 8 wariantów: bity 5–7 wybierają grupę, bity 1–3 numer w grupie.

## 4.3. Wykrywanie banków przez oryginalny player (v035)

`[ODCZYT]` Pierwszy INIT playera (`$2000`) wykonuje:

1. `PHP/SEI`, wyłącza DMA (`$D400=0`), zeruje `$249C/$249D`;
2. `LDA #$FF / STA $D301` — ROM OS widoczny;
3. zapamiętuje bajt spod `$4000` w `$249E`;
4. z tabel `$2734/$2737` pobiera wskaźnik i kopiuje **14 selektorów**
   do `$26FC–$2709`;
5. dla każdego selektora: ustawia PORTB, zapisuje numer do `$4000`,
   przełącza i sprawdza, czy odczyt się zgadza;
6. przy niezgodności skacze do `$20BB` (w buildach AVG podmienionym na
   ekran diagnostyczny).

`[ODCZYT]` Tabele selektorów leżą w **RAM-ie** załadowanym z segmentu XEX
`$24BD–$28BC`, a nie w ROM-ie. `$2734`/`$2737` to tablice wskaźników do
właściwych list selektorów.

`[ODCZYT]` 14 wykrytych wartości dla tej konfiguracji:

```
81 83 85 87 89 8B 8D 8F A1 A3 A5 A7 A9 AB
```

## 4.4. Dodatkowe banki wideo (`school_portrait_bank.loader`)

`[ODCZYT]` `tools/school_portrait_bank.py`, funkcja `loader(frame, index)`.
Wywoływana jest 50 razy, z indeksami 0–49.

### Indeksy 0 i 1 — wyliczane bez testu

```
LDX $26FC          ; pierwszy wykryty selektor
CPX #$81
BEQ two            ; typowa konfiguracja 1088XE
LDA #4*(index+1)
JMP add
two: LDA #2*(index+1)
add: CLC
     ADC $2709     ; ostatni wykryty selektor (baza)
     STA $D301
     AND #$FE
     STA $24B3+index
```

`[WNIOSEK]` To jedyne dwa banki, których unikalność **nie jest sprawdzana**.
Dla konfiguracji z pierwszym selektorem `$81` dają `$AD` i `$AF`.

### Indeksy 2–49 — sondowanie

Dla każdego kandydata z listy 64:

1. wybierz bank, zapisz do `$4000` znacznik `$55`;
2. dla wszystkich już znanych banków sprawdź, czy któryś czyta `$55`;
3. jeśli tak, wpisz `$AA` i sprawdź ponownie — zgodność oznacza alias;
4. przy aliasie przejdź do następnego kandydata;
5. po znalezieniu wolnego banku zapisz `selektor & $FE` do
   `bank_value(index)`.

`[ODCZYT]` `bank_value(index)`:

```
index < 3   → $24B3 + index
index >= 3  → $08C0 + index
```

Czyli selektory trafiają do `$24B3–$24B5` oraz `$08C3–$08F1`.

### Ścieżka błędu

```
no_bank:
    LDA #$32
    STA $D01A      ; COLBK = $32
    JMP no_bank
```

`[ODCZYT]` Brak banku objawia się **wyłącznie zmianą koloru tła** i pętlą.
Nie ma tekstu ani numeru indeksu. `[WNIOSEK]` To najgorszy możliwy objaw
diagnostyczny — wygląda jak zawieszenie dema.

### Kopiowanie zawartości

`[ODCZYT]` Po wyborze banku loader kopiuje `len(frame)/256` stron:

```
LDA $8000,Y
STA $4000,Y
INY / BNE ...
INC źródło+1 / INC cel+1 / DEX / BNE ...
```

Źródłem jest segment XEX w `$8000–$BFFF`, celem wybrany bank w
`$4000–$7FFF`. Po kopiowaniu PORTB jest przywracany ze stosu.

`[ODCZYT]` `LDA $D301 / PHA` na początku i `PLA / STA $D301` na końcu
zakładają, że PORTB da się odczytać. Na testowanym sprzęcie działa;
na klonach z nieczytelnym PORTB to miejsce wymaga zmiany.

## 4.5. Weryfikacja na sprzęcie

`[ODCZYT]` `releases/avg-bank-map-diagnostic-003.xex` (485 B) sprawdza
wszystkie 64 selektory: każdemu przypisuje unikalny znacznik w jego banku
i drugim przebiegiem sprawdza brak aliasów. Wynik na Atari:
**`BANK MAP PASSED`**.

`[WNIOSEK]` Mapa bitów jest poprawna dla tego klonu; problem nie leżał
w liście selektorów.

## 4.6. Znane ryzyka

- `[ODCZYT]` Indeksy 0/1 nie są weryfikowane — przy innym klonie arytmetyka
  może trafić w zajęty bank.
- `[ODCZYT]` `no_bank` nie raportuje błędu na ekranie.
- `[ZAŁOŻENIE]` Fałszywe trafienie testu `$55`/`$AA` jest możliwe, jeśli
  znany bank ma taki bajt pod `$4000`; wpływa to tylko na wybór banku,
  nie na poprawność danych.
- `[ZAŁOŻENIE]` Test unikalności nie sprawdza, czy bank istnieje fizycznie —
  wykrywa wyłącznie aliasy.
