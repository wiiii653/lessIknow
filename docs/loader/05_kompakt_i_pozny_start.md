# 5. Kompaktowanie i późny start z niskiej pamięci

## 5.1. Problem

`[ODCZYT]` Baza 64 banków ma ~1 111 730 B (1.06 MiB). Duża część danych to
zera: PNG/bitmapy i nieużywane obszary banków. Poza rozmiarem problemem
jest niska pamięć: segmenty runtime `$0400–$0BFF` są wczytywane w trakcie
ładowania i nadpisują się nawzajem z buforami loaderów.

## 5.2. Czyszczenie banku przed ładowaniem (`$3A00`)

`[ODCZYT]` `tools/build_compact_xex.py`, `clear_code()`:

```
PHP / SEI / PHA / TXA / PHA / TYA / PHA
LDA #$80 / STA $3A14      ; samo-modyfikacja: starszy bajt adresu STA
LDA #0 / LDX #$40 / LDY #0
loop:  STA $8000,Y
       INY / BNE loop
       INC $3A14
       DEX / BNE loop
PLA / TAY / PLA / TAX / PLA / PLP / RTS
```

`[ODCZYT]` `INC $3A14` modyfikuje starszy bajt operandu `STA $8000,Y`;
po 64 stronach cały `$8000–$BFFF` jest wyzerowany. Kod zachowuje A/X/Y
i flagi, więc może być wywoływany jako INIT między segmentami.

`[WNIOSEK]` Dzięki zerowaniu można emitować wyłącznie niezerowe fragmenty
banku — reszta jest gwarantowanie zerowa.

## 5.3. Pomijanie ciągów zer

`[ODCZYT]` Dla każdego bloku banku narzędzie:

- pomija początkowe zera,
- emituje dane do miejsca, gdzie zaczyna się ciąg ≥16 zer,
- taki ciąg pomija i wznawia emisję od następnego niezerowego bajtu,
- krótsze ciągi (1–15 zer) zostają w segmencie, bo nagłówek kosztuje 4 B.

`[ODCZYT]` Asercja `count == 64` pilnuje, że przetworzono wszystkie banki.

`[ODCZYT]` Porównanie po dekompozycji: dane 64 banków są identyczne bajt
w bajt z pierwowzorem (potwierdzone w `docs/V273_START_AVG_RAMBO.md`).

## 5.4. Bufor niskiej pamięci (`$4000–$47FF`)

`[ODCZYT]` `tools/build_avg_late_lowram.py`, stała `LOW`:

```
(0x0400,0x07e4) (0x0800,0x08bf) (0x0900,0x0974)
(0x0980,0x09ff) (0x0a00,0x0bff)
```

Segmenty docelowo należące do tych zakresów, występujące **po ostatnim**
`$02E2`, są:

1. wycinane z bieżącego miejsca w pliku,
2. składane w bufor 2 KiB,
3. emitted jako jeden segment `$4000–$47FF` przed `$02E0`,
4. odtwarzane w bootstrapie `$4800`.

`[ODCZYT]` Bufor leży w oknie banku `$4000–$7FFF`. Oznacza to, że dane
zostaną zapisane do **aktualnie wybranego** banku. Bootstrap czyta z tego
samego mapowania, więc para „segment $4000 + INIT $4800” musi wystąpić bez
zmiany PORTB pomiędzy nimi.

`[ZAŁOŻENIE]` Bufor zajmuje 2 KiB w jednym z banków 1 MB. Jeśli trafi
w bank używany przez demo, nadpisze jego pierwsze 2 KiB. Na testowanym
sprzęcie nie powoduje to widocznego błędu; przy zmianie kolejności
segmentów wymaga sprawdzenia.

## 5.5. Bootstrap `$4800`

`[ODCZYT]` 116 bajtów:

```
78              SEI
A9 00 8D 0E D4  NMI off
```

Potem kolejno kopiuje strony z bufora:

| Cel | Źródło | Bajty |
| --- | --- | ---: |
| `$0400` | `$4000` | 256 |
| `$0500` | `$4100` | 256 |
| `$0600` | `$4200` | 256 |
| `$0700` | `$4300` | 229 (`$07E4`) |
| `$0800` | `$4400` | 192 (`$08BF`) |
| `$0900` | `$4500` | 117 (`$0974`) |
| `$0980` | `$4580` | 128 (`$09FF`) |
| `$0A00` | `$4600` | 256 |
| `$0B00` | `$4700` | 256 |

Na końcu:

```
4C E0 13        JMP $13E0
```

`[WNIOSEK]` Bootstrap jest **ostatnim** INIT-em i nigdy nie wraca. Od tej
chwili działa wyłącznie kod runtime.

## 5.6. Dlaczego to działa

`[WNIOSEK]` Trzy rzeczy zmieniły się względem starszych buildów:

1. plik jest mniejszy niż 1 MiB (935 472 B zamiast 1 111 730 B);
2. niska pamięć nie jest nadpisywana w trakcie ładowania — jest odtwarzana
   na końcu;
3. start nie zależy od RUNAD, tylko od `JMP $13E0` w bootstrapie.

`[OGRANICZENIE]` Nie ustalono, która z tych zmian była warunkiem
koniecznym — wszystkie trzy weszły razem.

## 5.7. Pułapki przy modyfikacji

- Nie dodawaj segmentów do `$0400–$0BFF` po ostatnim `$02E2` bez
  rozszerzenia `LOW` i bootstrapu — zostaną utracone.
- Nie zmieniaj PORTB między segmentem `$4000–$47FF` a INIT-em `$4800`.
- Nie zwiększaj bufora powyżej `$47FF` bez sprawdzenia, co leży dalej.
- `clear_code` modyfikuje własny operand pod `$3A14` — nie przenoś kodu
  bez aktualizacji tego adresu.
