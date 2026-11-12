# 10. Analiza optymalizacji (bez zmian w kodzie)

Dokument opisuje **możliwości** optymalizacji obecnego dema. Powstał w trybie
tylko-do-odczytu: nie zmieniono żadnego pliku produkcyjnego, builda ani
narzędzia. Wszystkie liczby pochodzą z pomiarów wykonanych na obecnym
buildzie (`build/visual-prototype-v294.xex`, `releases/less-i-know-demo-release-031-stereo.xex`).

Legenda: `[ODCZYT]`, `[WNIOSEK]`, `[ZAŁOŻENIE]`, `[OGRANICZENIE]`.

---

## 1. Metryki wejściowe

| Miara | Wartość |
| --- | ---: |
| Baza 64 banków (`visual-prototype-v294.xex`) | 1 111 760 B |
| Release 031 stereo | 941 515 B |
| Segmentów w release | 1 770 |
| Dane w oknie banków | 886 177 B |
| Pozostałe dane (runtime) | 48 256 B |
| Nagłówki segmentów (4 B × 1770) | 7 080 B |
| Banki 16 KiB | 64 (1 048 576 B) |
| Zera w bankach | 335 472 B (32,0 %) |
| Unikalne banki | 64 z 64 (brak duplikatów) |
| Współdzielone wiersze | 298 (`row_storage_bytes` 11 494 B) |
| Kod główny | 2 560 B (`$1400–$1DFF`) — brak zapasu |

`[ODCZYT]` INIT-y w release 031: `$38A0`×1, `$3900`×66, `$3A00`×64,
`$4800`×1; RUN `$13E0` (niewykorzystywany do startu).

---

## 2. Budżet czasu CPU

`[ODCZYT]` Ramka PAL: 312 linii × 76 cykli ≈ **23 712 cykli**.
Przy czterech wywołaniach callbacku na ramkę budżet na jedno wywołanie
wynosi **5 928 cykli** (dla 50 fps).

`[ODCZYT]` Zmierzone koszty callbacku (py65, bez DMA, po rozgrzaniu
cache; kolejne ticki na tym samym CPU):

| Scena | Cykle | Ile ramek |
| --- | ---: | ---: |
| tytuł | 11 997 | 0,51 |
| boczny taniec (Act 2) | **69 302** | **2,92** |
| szarfy | 44 469 | 1,88 |
| Trevor | 443 | 0,02 |
| rotator | 47 297 | 1,99 |
| tunel | 47 312 | 2,00 |
| outro | 10 915 | 0,46 |
| finał | 10 203 | 0,43 |
| ujęcie szkolne (Act 1) | 807 | 0,03 |
| praktyka | 757 | 0,03 |

`[ODCZYT]` Korekta: w pierwszej wersji tego dokumentu sceną „szkoła” nazwano
tick 8992, który należy do bocznego tańca. Prawdziwe ujęcia szkolne Act 1
kosztują ~807 cykli i nie wymagają optymalizacji. Szczegóły i profile
adresowe: [11_mozaiki_szkola_i_banany.md](11_mozaiki_szkola_i_banany.md).

`[WNIOSEK]` Sceny bocznego tańca, rotatora, tunelu i szarf przekraczają budżet
jednej ramki kilkukrotnie. Muzyka pozostaje w taktcie, bo NMI działa
niezależnie, ale odświeżanie obrazu w tych scenach jest ograniczone CPU.
`[OGRANICZENIE]` py65 nie modeluje DMA ANTIC ani rzeczywistych terminów
rastera; na sprzęcie koszt będzie jeszcze wyższy.

`[ODCZYT]` Koszt „na zimno” (świeży CPU, puste cache) jest znacznie
większy: tytuł 131 812, boczny taniec 81 018, outro 192 825 cykli. To tłumaczy,
dlaczego pierwsze wywołanie po zmianie sceny jest drogie.

---

## 3. Koszt loadera (czas ładowania)

`[ODCZYT]` Zmierzone emulacją fragmentów kodu z release:

| Etap | Cykle | Na 64 banki |
| --- | ---: | ---: |
| Czyszczenie banku (`$3A00`) | 164 535 | **5,94 s** |
| Kopiowanie 16 KiB (`$1000`) | 230 409 | **8,30 s** |
| Sondowanie i wybór banków | ~30 tys./bank | ~1,9 s `[ZAŁOŻENIE]` |
| **Razem narzut CPU loadera** | | **~16 s** |

`[WNIOSEK]` Około 16 s ładowania to czysta praca 6502, niezależna od SIO.
Czyszczenie i kopiowanie to 86 % tego czasu.

`[ODCZYT]` Czyszczenie działa w `SEI`; pojedynczy bank to blok ~93 ms bez
przerwań. Nie wpływa na muzykę (jeszcze nie gra), ale wydłuża ładowanie.

---

## 4. Analiza rozmiaru pliku

`[ODCZYT]` Zera to 32 % danych banków. Obecny próg pomijania ciągów zer
w `tools/build_compact_xex.py` wynosi **16 B**. Symulacja dla obecnego
zbioru banków (wraz z nagłówkami i kodem czyszczącym):

| Próg | Rozmiar banków + clear | Oszczędność vs 16 B | Segmenty danych |
| ---: | ---: | ---: | ---: |
| 4 B | 838 734 B | +30 137 B | 14 235 |
| 8 B | 848 405 B | +20 466 B | 4 675 |
| **16 B (obecnie)** | **868 871 B** | — | 1 401 |
| 32 B | 883 744 B | −14 873 B | 532 |

`[WNIOSEK]` Zejście do progu 8 B daje **~20 KB mniej** przy +3 274
segmentach. Próg 4 B daje kolejne ~10 KB, ale liczba segmentów rośnie
do 14 235, co wydłuża obsługę pliku przez loader plików.

`[ODCZYT]` Brak duplikatów banków — deduplikacja nic nie da.
`[ODCZYT]` Żaden bank nie mieści się w pierwszych 8 KiB (ostatni niezerowy
bajt ≥ `$27FF`), więc skrócenie banku do 8 KiB nie jest możliwe bez
przeprojektowania układu.

`[ODCZYT]` Dane runtime to tylko 48 KB — kompresja tej części da co najwyżej
kilka KB i komplikuje start.

---

## 5. Kandydaci optymalizacji

### A. Czas ładowania — największy potencjał

| # | Pomysł | Zysk | Ryzyko | Zależności |
| ---: | --- | ---: | --- | --- |
| A1 | Czyszczenie tylko zakresów pominiętych (nie całych 16 KiB) | ~4,0 s | średnie | nowy kod/tablica zakresów; `$3A00` i jego self-mod `$3A14` |
| A2 | Rozwinięte `STA abs` zamiast pętli `STA abs,Y` | ~2,5 s | niskie | rozmiar kodu czyszczenia; zachowanie A/X/Y/flags |
| A3 | Rozwinięte kopiowanie (`LDA abs,Y` × N / `STA abs,Y` × N) | ~1,7 s | niskie | `school_portrait_bank.loader`, długość kodu INIT |
| A4 | Ładowanie banków bezpośrednio do `$4000` (jak w innym demie 1 MB) | ~8,3 s + 2 KiB RAM | wysokie | cała struktura XEX, compact pass, brak bufora `$8000` |
| A5 | Sondowanie banków tylko raz i zapis tabeli na stałe do builda | ~1,9 s | wysokie | przenośność między klonami; test `avg-bank-map-diagnostic-003` |

`[WNIOSEK]` A1–A3 nie zmieniają formatu pliku i mogą dać łącznie **~8 s**
krótsze ładowanie przy zachowaniu wszystkich niezmienników.
A4 to największy zysk, ale wymaga przepisania loadera i ponownej walidacji
całego startu.

### B. Rozmiar pliku

| # | Pomysł | Zysk | Ryzyko |
| ---: | --- | ---: | --- |
| B1 | Próg zer 16 → 8 B | ~20 KB | niskie |
| B2 | Próg zer 8 → 4 B | ~10 KB | średnie (14 tys. segmentów) |
| B3 | Kompresja danych runtime | ~2–5 KB | wysokie (dekoder, RAM) |
| B4 | Deduplikacja banków | 0 B | — |

`[ODCZYT]` B1 nie wymaga zmian w kodzie 6502 — tylko w narzędziu
kompaktującym. `[OGRANICZENIE]` Zmiana progu zmienia liczbę segmentów
i czasy obsługi pliku; trzeba powtórzyć porównanie POKEY i test startu.

### C. CPU w czasie odtwarzania

| Scena | Koszt | Propozycja |
| --- | ---: | --- |
| boczny taniec | 69 302 | kopiowanie szybsze (M1/T1); overlay aktora (T2/T3) |
| rotator/tunel | ~47 300 | ograniczyć kopiowanie do brudnych stron (już 5 376 B z 7 936 B); rozważyć podwójny bufor i podmianę LMS |
| szarfy | 44 469 | komponować tylko obszar aktora; ograniczyć czyszczenie PMG do aktywnych zakresów |
| tytuł | 11 997 | cache kompozycji plazmy; odświeżać tylko zmienione wiersze |
| outro/finał | ~10 200 | tanie jak na razie; nie priorytet |

`[WNIOSEK]` Redukcja kosztu szkoły o połowę dałaby ~1,5 ramki zapasu
i najbardziej poprawiła płynność. To jednak zmiana w generatorach scen,
nie w loaderze.

### D. Pamięć i kod główny

- `[ODCZYT]` Kod główny 2 560 B w `$1400–$1DFF` — **zero zapasu**.
  Uwolnienie miejsca wymaga scalenia trampolin `compare_tick`/`compare_tick16`
  albo przeniesienia części logiki do banku.
- `[ODCZYT]` Pula 298 wierszy / 11 494 B jest już deduplikowana.
  Dalszy zysk tylko przez współdzielenie wierszy między scenami
  (wymaga zmiany kluczy cache).
- `[ZAŁOŻENIE]` Sprawdzenie, które wiersze są używane tylko w jednej scenie,
  mogłoby wskazać kandydatów do usunięcia po zmianach artystycznych.

---

## 6. Zależności loadera — czego nie wolno ruszać

`[ODCZYT]` Poniższe elementy są ze sobą sprzężone; zmiana jednego wymaga
sprawdzenia pozostałych.

### 6.1. Adresy stałe

| Adres | Rola | Uwaga |
| --- | --- | --- |
| `$3800–$3877` | ekran ładowania | nie może kolidować z segmentami runtime |
| `$3880–$388A` | display lista | musi leżeć w jednej stronie 1 KiB |
| `$38A0–$38DC` | INIT ekranu | ustawia CHBASE `$D409` i kolory |
| `$3900–$398B` | wrapper INIT (diagnostyka) | opcjonalny; usuwa się przez pominięcie etapu 2 |
| `$3A00–$3A24` | czyszczenie banku | **self-mod pod `$3A14`** |
| `$4000–$47FF` | bufor niskiej pamięci | w oknie banku |
| `$4800–$4873` | bootstrap + `JMP $13E0` | musi być ostatnim INIT |

### 6.2. Niezmienniki

1. Między segmentem `$4000–$47FF` a INIT-em `$4800` **nie wolno zmieniać
   PORTB** — bootstrap czyta ten sam bank.
2. `LOW` w `build_avg_late_lowram.py` musi odpowiadać rzeczywistym
   segmentom niskiej pamięci; dodanie zakresu wymaga nowej pętli kopiowania.
3. Tabele selektorów: `$24B3–$24B5` i `$08C3–$08F1`; `bank_value()` musi
   zgadzać się z loaderem i wszystkimi konsumentami.
4. 64 banki dokładnie; banki 0/1 są liczone arytmetycznie bez weryfikacji.
5. Bank 39 trzyma bitmapę finału i aktora bocznego; bank 49 kontrolery.
6. Banki 40–48 pełnią rolę overlayu (plazma, fajerwerki, banany 46/48).
7. Kolejność INIT: ekran → 14 banków v035 → 50 banków wideo → segmenty
   runtime → bufor `$4000` → bootstrap.
8. Start: `JMP $13E0` z bootstrapu; RUNAD istnieje, ale nie jest używany.
9. Kod czyszczenia zakłada, że cały `$8000–$BFFF` jest zerowany przed
   danymi banku — zmiana progu zer w kompaktorze nie może tego złamać.
10. `SEI` w czyszczeniu: nie dodawaj tam kodu zależnego od NMI.

### 6.3. Miejsca czytające `$D301`

`[ODCZYT]` `run_stub`, `school_portrait_bank.loader`, `banana_cache`,
`banked_effects`, `ribbon_copy`. Na testowanym sprzęcie odczyt działa,
ale nie jest przenośny. Każda optymalizacja tych bloków powinna albo
zachować wzorzec `PHA/PLA`, albo wprowadzić shadow w RAM.

---

## 7. Priorytety

| Priorytet | Zmiana | Zysk | Ryzyko | Wpływ na loader |
| ---: | --- | ---: | --- | --- |
| 1 | A1 + A2 (czyszczenie) | ~6 s | średnie | kod `$3A00`, self-mod `$3A14` |
| 2 | A3 (kopiowanie) | ~1,7 s | niskie | `school_bank_loader`, długość INIT |
| 3 | B1 (próg zer 8 B) | ~20 KB | niskie | compact pass, liczba segmentów |
| 4 | C boczny taniec | ~0,6 ramki | średnie | kompozytor, cache |
| 5 | C rotator/tunel | ~1 ramka | średnie | renderery mozaiki |
| 6 | A4 (ładowanie do banków) | ~8 s | wysokie | cała struktura XEX |

`[WNIOSEK]` Najlepszy stosunek zysku do ryzyka: **A2 + A3 + B1**.
Nie ruszają mapy banków, kolejności INIT ani startu.

---

## 8. Czego nie da się poprawić tanio

- `[ODCZYT]` Deduplikacja banków — brak duplikatów.
- `[ODCZYT]` Skrócenie banków do 8 KiB — dane sięgają końca 16 KiB.
- `[ODCZYT]` Kompresja runtime — tylko 48 KB, zysk nieproporcjonalny
  do ryzyka dekodera w pamięci podstawowej.
- `[OGRANICZENIE]` Zmniejszenie kodu głównego bez refaktoru — 2 560 B
  jest dokładnie wypełnione.

---

## 9. Jak weryfikować zmiany

1. `make check` — 200/200.
2. Porównanie struktury XEX: liczba banków 64, INIT-y `$38A0/$3900/$3A00/$4800`.
3. Ponowne porównanie stereo POKEY w Atari800 1088XE z v035.
4. Test startu na fizycznym Atari (AVG, Rambo 1 MB).
5. Pomiar czasu ładowania na sprzęcie (stoper) przed i po.
6. Pomiar ciepłych cykli callbacku w py65 dla scen: boczny taniec, rotator, tunel.

`[OGRANICZENIE]` Punkty 1–3 i 6 nie potwierdzają płynności ani zachowania
fizycznego loadera AVG.
