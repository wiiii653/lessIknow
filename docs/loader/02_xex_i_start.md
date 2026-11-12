# 2. Format XEX i start programu

## 2.1. Czym jest XEX

Plik XEX (Atari DOS binary) to nagłówek `FF FF`, a potem ciąg segmentów:

```
start_lo start_hi end_lo end_hi <dane>
```

Znaczenie specjalnych adresów:

| Adres | Znaczenie |
| --- | --- |
| `$02E0–$02E1` | RUNAD — adres startowy programu |
| `$02E2–$02E3` | INITAD — adres procedury wywoływanej **natychmiast** po wczytaniu tego segmentu |

`[ODCZYT]` Loader OS po wczytaniu wszystkich segmentów skacze pod RUNAD.
Program może też nigdy nie wrócić z INIT-a i wtedy RUNAD nie ma znaczenia.

## 2.2. Kolejność w naszym pliku

`[ODCZYT]` Release 018 (1775 segmentów) ma następującą strukturę logiczną:

1. ekran ładowania: `$3800` (tekst), `$3880` (DL), `$38A0` (INIT), `$02E2`;
2. oryginalne segmenty v035: `$2000–$24B2` (kod playera), `$24BD–$28BC`
   (tabele), `$3300`/`$3400` (DL i ekran playera);
3. 50× loader banku wideo: segment `$8000–$BFFF`, INIT `$1000`
   (opakowany w `$3900`), `$02E2`;
4. 64× czyszczenie banku: INIT `$3A00` przed danymi każdego banku;
5. segmenty runtime: `$1400–$1DFF`, `$0C00–$0F3F`, PMG, display listy,
   `$9000`/`$B000` (bitmapy) itd.;
6. bufor niskiej pamięci `$4000–$47FF`;
7. bootstrap `$4800` + `$02E2=$4800`;
8. `$02E0=$13E0` (RUNAD, nieużywany do startu w tym wariancie).

`[ODCZYT]` Licznik INIT-ów w release 018:

| INIT | Liczba | Rola |
| --- | ---: | --- |
| `$38A0` | 1 | ekran ładowania |
| `$3900` | 66 | wrapper diagnostyczny każdego INIT-a |
| `$3A00` | 64 | czyszczenie `$8000–$BFFF` przed bankiem |
| `$4800` | 1 | bootstrap + bezpośredni start |

## 2.3. Dlaczego start jest „późny”

`[ODCZYT]` Bootstrap `$4800` kończy się rozkazem `JMP $13E0`, a nie `RTS`.
Oznacza to, że program **nie wraca** do loadera OS i nie czeka na RUNAD.

`[ODCZYT]` `$13E0` to stub startowy (`tools/os_ram.py`, `run_stub()`):

```
78              SEI
A9 00 8D 0E D4  LDA #0 / STA $D40E   ; NMI off
AD 01 D3        LDA $D301             ; odczyt PORTB
29 FE           AND #$FE              ; OS ROM off
8D 01 D3        STA $D301
4C 46 21        JMP $2146             ; wejście playera
```

`[WNIOSEK]` Dzięki temu start nie zależy od tego, czy loader plików
(AVG/DOS) wykona RUNAD. To była jedna z rzeczy zmienionych względem
wcześniejszych, niedziałających buildów.

`[OGRANICZENIE]` Stub czyta `$D301`. PORTB jest rejestrem zapisywalnym;
odczyt na XL/XE zwykle zwraca ostatnio zapisaną wartość, ale nie jest to
gwarantowane na każdym klonie. Na testowanym sprzęcie działa. Jeśli
pojawi się losowe zachowanie, pierwszy kandydat do zmiany to zastąpienie
`LDA $D301 / AND #$FE` stałą wartością.

## 2.4. Kopia OS pod ROM

`[ODCZYT]` Przed startem INIT `$1000` (`tools/os_ram.py`, `loader()`) kopiuje
14 KiB obrazu OS do RAM pod ROM:

- regiony źródłowe: `$8000–$BFFF` (obraz ROM z XEX),
- cele: `$C000–$CFFF` i `$D800–$FFFF`,
- w tym samym kroku tabela selektorów muzyki `$26FC–$2709` jest maskowana
  przez `AND #$FE` (bity 0 wyłączone),
- wektor NMI `$FFFA` ustawiany jest na `$2210` (oryginalny handler DLI),
- na końcu przywracany jest PORTB i `$D400=$40`.

`[WNIOSEK]` Runtime pracuje z **wyłączonym ROM-em OS** i korzysta z kopii
w RAM. Dlatego selektory banków zapisywane do tabel mają bit 0 = 0.

## 2.5. Co się dzieje, gdy loader nie wykona INIT-a

`[ODCZYT]` Jeśli któryś INIT nie wróci (np. pętla błędu), OS nigdy nie
dojdzie do kolejnych segmentów ani do RUNAD. Objaw: ekran zatrzymany na
ostatnim stanie, brak dalszego ładowania. Dlatego każda ścieżka błędu w
loaderze banków powinna być widoczna na ekranie — obecny `no_bank`
tego nie robi (patrz [04_bankowanie.md](04_bankowanie.md)).

## 2.6. Różnica względem wersji 1.06 MiB

| Cecha | Stare buildy (008–011) | Obecny (012+) |
| --- | --- | --- |
| rozmiar | 1 111 730 B (1.06 MiB) | 935 472 B |
| start | RUNAD `$13E0` | `JMP $13E0` z bootstrapu `$4800` |
| niska pamięć | ładowana segmentami w trakcie | buforowana i kopiowana na końcu |
| dane banków | pełne 16 KiB | tylko niezerowe fragmenty, bank zerowany |

`[OGRANICZENIE]` Nie ustalono, która z tych zmian była konieczna na
testowanym sprzęcie — zmieniono je jednocześnie.
