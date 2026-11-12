# 11. Mozaiki, scena szkolna i banany — analiza

Analiza tylko-do-odczytu: nie zmieniono kodu, builda ani narzędzi.
Pomiary: py65 na `build/visual-prototype-v294.xex`, callback wywoływany jak
w `tests/test_sequence.py`, bez modelowania DMA ANTIC.

Legenda: `[ODCZYT]`, `[WNIOSEK]`, `[ZAŁOŻENIE]`, `[OGRANICZENIE]`.

---

## 1. Ważna korekta nazw scen

`[ODCZYT]` Tick 8992 (bar 24) to **nie scena szkolna**, tylko początek
bocznego tańca z szarfą (Act 2, 8975–11966). Wcześniejsza analiza
przypisała jego koszt scenie szkolnej.

`[ODCZYT]` Rzeczywiste koszty ciepłego callbacku:

| Scena | Tick | Cykle | Ramki (23 712) |
| --- | ---: | ---: | ---: |
| ujęcie szkolne (Act 1) | 4416 | **807** | 0,03 |
| praktyka | 6096 | **757** | 0,03 |
| boczny taniec | 9496 | **69 302** | 2,92 |
| szarfy (typ) | 15008 | 44 469 | 1,88 |
| szarfy (akcent) | 14992 | 91 376 | 3,85 |
| rotator | 32928 | 47 297 | 1,99 |
| tunel | 35920 | 47 312 | 2,00 |
| tytuł | 1504 | 11 997 | 0,51 |
| outro | 49868 | 10 915 | 0,46 |
| finał | 59104 | 10 203 | 0,43 |

`[WNIOSEK]` Scena szkolna jest **bardzo tania** (807 cykli) — nie ma tam
czego optymalizować. Wąskie gardła to boczny taniec, szarfy i mozaiki
(rotator/tunel).

---

## 2. Gdzie dokładnie idzie czas

`[ODCZYT]` Podział cykli według adresu PC (callback, zimny start):

**Boczny taniec (80 840 cykli):**

| Obszar | Cykle | Udział |
| --- | ---: | ---: |
| `$0C00–$0F3F` — kopiowanie + kompozytor | 49 765 | 61 % |
| `$5400–$5CCF` — kontroler szarf | 30 542 | 38 % |
| `$1400–$1DFF` — kod główny | 405 | 0,5 % |

**Rotator / tunel (58 731 cykli):**

| Obszar | Cykle | Udział |
| --- | ---: | ---: |
| `$0C00–$0F3F` — kopiowanie ramki | 38 786 | 66 % |
| `$7C00–$7FFF` — helper mozaiki (DL, paleta, swap) | 11 984 | 20 % |
| `$7800–$7BFF` — helper piłki/PMG | 7 314 | 12,5 % |

**Szarfy, szczyt (91 376 cykli):**

| Obszar | Cykle | Udział |
| --- | ---: | ---: |
| `$5CD0–$5FFF` — kontroler finału/szarf | 60 987 | 67 % |
| `$5400–$5CCF` — kompozytor | 29 523 | 32 % |

---

## 3. Jak działa kopiowanie (główne źródło kosztu)

`[ODCZYT]` `tools/engine_effects.py`, `runtime_helper()`:

- kopiuje `5*X` stron po 256 B z banku (`$4000+`) do niebankowanego
  bufora (`$9000+`),
- w jednej iteracji pętli kopiuje **5 bajtów równolegle** (po jednym
  z każdej strony), czyli ~11 cykli na bajt,
- `X=2` dla sceny szkolnej/tanga (2560 B), `X=3` dla mozaiki (3840 B).

`[ODCZYT]` Dlaczego nie można wyświetlać wprost z banku `$4000`:
NMI muzyki przełącza PORTB na bank muzyczny cztery razy na ramkę.
ANTIC czyta wtedy ten sam bank co CPU, więc obraz z `$4000–$7FFF`
mrugałby na czas każdego NMI. Bufor w niebankowanym RAM jest więc
**wymagany**, a nie przypadkowy.

`[WNIOSEK]` Kopiowanie można przyspieszyć tylko w obrębie tego samego
schematu — np. przez samomodyfikujące się `STA abs` (4 cykle zamiast
`STA abs,Y` 5 cykli) i większe rozwinięcie pętli.

---

## 4. Propozycje dla mozaik (rotator/tunel)

| # | Zmiana | Szacowany zysk | Ryzyko |
| ---: | --- | ---: | --- |
| M1 | `STA abs` samomodyfikujące zamiast `STA abs,Y` w kopiowaniu (−16 %) | ~6 200 cykli | niskie: kod w `$0C00`, bez zmian danych |
| M2 | Prekompilacja wpisów DL dla 192 wierszy na fazę i podmiana wskaźnika | ~6 400 cykli | średnie: tabela w banku, klucze cache |
| M3 | Helper piłki: aktualizować PMG tylko przy zmianie fazy | ~3 000 cykli | niskie |
| M4 | Kopiować tylko wiersze zmienione między klatkami | 0–15 000 cykli | wysokie: rotacja zmienia cały obraz |

`[WNIOSEK]` M1+M2+M3 dają ~15 600 cykli, czyli rotator/tunel
z 47 297 → ~31 700 cykli (1,99 → 1,34 ramki). Bez zmiany mapy banków.

---

## 5. Propozycje dla bocznego tańca i szarf

| # | Zmiana | Szacowany zysk | Ryzyko |
| ---: | --- | ---: | --- |
| T1 | Kopiowanie jak M1 (2560 B → −16 %) | ~4 500 cykli | niskie |
| T2 | Overlay aktora: scalić piksel+maska w jeden bajt z bitem przezroczystości (2 operacje zamiast 4) | ~10 000 cykli | średnie: nowy format danych w bankach 24–39 |
| T3 | Ograniczyć overlay do rzeczywistego bounding boxu pozy | ~5 000 cykli | średnie: metadane pozy |
| T4 | Kontroler szarf: pomijać przebudowę, gdy faza się nie zmieniła | ~5 000 cykli | niskie |

`[WNIOSEK]` T1+T2 dają ~14 500 cykli: boczny taniec 69 302 → ~55 000
(2,92 → 2,3 ramki), a szczyty szarf z 91 376 → ~77 000.

---

## 6. Scena szkolna — brak potrzeby optymalizacji

`[ODCZYT]` 807 cykli ciepło, 17 500 zimno. To 3 % budżetu ramki.
`[WNIOSEK]` Nie warto tu nic zmieniać; ryzyko regresji wizualnej byłoby
większe niż zysk.

---

## 7. Banany: naprzemienny obrót pod koniec dema

### 7.1. Jak działa teraz

`[ODCZYT]` `tools/post_trevor_director.py`:

- zegar montażu = `tick + 4000` (poza montażem bez przesunięcia),
- motyw: bit 10 zegara (`(clock>>5)&32`) — 0 = banany, 1 = tunel,
  naprzemiennie co 1024 ticki,
- faza banana: `(clock>>4)&31` — 32 faz, krok 16 ticków, **zawsze w jedną
  stronę**,
- wariant (kiść/obrany banan): `banana_variants.variant_at()` — bit 11
  zegara, zmienia się co 2048 ticków.

`[ODCZYT]` Po `CYCLE_START` (ostatnia trzecia montażu) banany używają
pełnych 32 faz (0–31); wcześniej część klatek obranych korzysta z 16 faz.

### 7.2. Co proponuję

`[WNIOSEK]` Bit 11 zegara i tak zmienia się przy **każdym kolejnym**
oknie bananów (okna co 2048 ticków), więc można go użyć jako przełącznika
kierunku bez dodatkowego licznika:

```
faza = (clock >> 4) & 31
if clock >= PROG and ((clock >> 11) & 1):
    faza = 31 - faza          ; lustro = obrót w przeciwną stronę
```

gdzie `PROG` to np. `CYCLE_START` (37984 w zegarze montażu, czyli ostatnia
trzecia część) albo `tick_at_bar(112)`.

`[WNIOSEK]` Efekt: kiść obraca się w jedną stronę, obrany banan w drugą,
naprzemiennie przy każdym pojawieniu się owocu. Przejście wypada
w momencie, gdy banan znika (motyw zmienia się na tunel), więc **nie widać
skoku fazy**.

### 7.3. Koszt i implementacja

| Element | Koszt |
| --- | --- |
| Kod w banku 2 (`bank_helper`) | ~15–20 B |
| RAM | 0 B (bez nowego stanu) |
| Banks | 0 |
| CPU na klatkę | ~30 cykli |
| Klucze cache `$83fa` | bez zmian (ID klatek 0–31) |

`[ODCZYT]` Miejsce jest: helper dyrektora kończy się przed `$7250`
(asercja `BANK_ENTRY+len(data)<=0x7250`), a w banku 2 są wolne obszary.

### 7.4. Wariant z ciągłością fazy

`[ZAŁOŻENIE]` Jeśli mirrorowanie okaże się zbyt „skokowe” przy dłuższych
oknach, można dodać licznik okien i bazę fazy (jak dla tuneli w
`timeline()`): `faza = (base + dir*elapsed) mod 32`. Koszt: +1 bajt stanu
i ~20 B kodu. Zysk wizualny: ruch zaczyna się tam, gdzie poprzednio się
skończył.

### 7.5. Czego nie ruszać

- `frame_at()` (Python, podglądy) i `bank_helper()` (6502) muszą liczyć
  fazę **identycznie**, inaczej podglądy i build się rozjadą.
- ID 32–59 (tunel/organiczny) i 60–63 (oczy) pozostają bez zmian.
- Warianty banana (banki 40–48, zasoby 46/48) i klucz `$83fa` bez zmian.
- `banana_variants.variant_at()` wybiera bank wariantu niezależnie od
  fazy — mirrorowanie nie może zmienić wyboru wariantu.

---

## 8. Kolejność prac i weryfikacja

1. **M1 + T1** (szybsze kopiowanie) — najmniejsze ryzyko, ~10 000 cykli.
2. **M2** (prekompilowane DL) — średnie ryzyko, ~6 400 cykli.
3. **T2/T3** (overlay) — większa zmiana danych, ~15 000 cykli.
4. **Banany** (naprzemienny obrót) — niezależne od powyższych.

Weryfikacja po każdej zmianie:

```sh
PYTHONPATH=tests:tools /tmp/opencode/tliktb-venv/bin/python -m unittest discover -s tests
ATARI_TEST_XEX=build/visual-prototype-v294.xex PYTHONPATH=tests:tools \
  /tmp/opencode/tliktb-venv/bin/python -c "from test_sequence import execute; \
  print(execute(32928).processorCycles)"
```

`[OGRANICZENIE]` Pomiary py65 nie modelują DMA ANTIC; realny zysk na
sprzęcie może być inny. Zmiany w kopiowaniu wymagają porównania obrazu
klatka w klatka z obecnym buildem.
