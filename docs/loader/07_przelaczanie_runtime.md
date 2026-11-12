# 7. Przełączanie banków w czasie odtwarzania

## 7.1. Zasada ogólna

`[ODCZYT]` W kodzie runtime każdy blok, który czyta lub pisze do banku,
stosuje ten sam wzorzec:

```
LDA $D301     ; zapamiętaj bieżący PORTB
PHA
LDA <selektor>; z tabeli $24B3+ / $08C3+
STA $D301
JSR <kod w banku>
PLA
STA $D301     ; przywróć
RTS
```

`[WNIOSEK]` Dzięki temu przerwania (NMI muzyki) działają w spójnym
mapowaniu: handler nie może trafić na bank podmieniony przez foreground.

## 7.2. Główne miejsca przełączania

`[ODCZYT]` `tools/build_bitmap_sequence.py`:

| Etykieta / linia | Co robi |
| --- | --- |
| `banked_effects` (~729) | wybiera bank efektów (`BANK_VALUE`) i woła `BALL_ENTRY` |
| `hero` (~279) | wybiera bank koszykarza (`HERO_BANK`) |
| `crush` (~292) | wybiera `$08F1` (bank 49) dla kontrolera szarf |
| `final_boy` (~269) | wybiera `$08F1` dla kontrolera finału |
| `ribbon_copy` (~759) | wybiera bank klatki z `$26FC+X` albo `$08C0+39` |
| `banana_bootstrap` (~769) | wybiera bank zasobów banana (`bank_value(46)`) |
| `hero_cutaway` (~722) | wybiera bank 2 (Trevor) przez `post_trevor_director` |

`[ODCZYT]` Wybór klatki szarfy (`ribbon_copy`, `build_bitmap_sequence.py`
~759–767):

```
LDA $D301 / PHA
LDX $83ED                  ; numer klatki
CPX #FRAME_KEY (36)        ; klatka finałowa?
BNE ribbon_frame_bank
LDA $08C0+39               ; bitmapa finałowa w banku 39
STA $D301
LDA #(BITMAP_SOURCE>>8)
JMP ribbon_source_ready
ribbon_frame_bank:
LDY ribbon_banks,X         ; tabela: 8 + i//6
LDA $26FC,Y                ; selektor banku muzyki
STA $D301
LDA ribbon_sources,X       ; strona źródła (A) dla kompozytora
...
```

`[ODCZYT]` `ribbon_banks` to tabela `8 + i//6` dla `i` w `0..35`, czyli
sześć klatek na bank w bankach 8–13 (oryginalne banki muzyki).

## 7.3. Banki 24–39 i kompozytor boczny

`[ODCZYT]` `ribbon_dance.install_side_actor` umieszcza w każdym z 16
banków (24–39) po jednej fazie aktora bocznego. Wybór banku:

```
LDA $83E0        ; faza/scena
...              ; (SCENE)
LDA $08C0+24+phase
STA $D301
```

`[ODCZYT]` Bank 39 zawiera dodatkowo bitmapę finałowego chłopca
(`final_boy.install_bitmap`), więc nie wolno go czyścić.

## 7.4. Banki 40–48 (plazma, fajerwerki, banany)

`[ODCZYT]` `title_plasma` wybiera banki 40/41 dla dwóch plansz tytułowych,
a `title_fireworks` dokłada kontroler i kształty w wolne końcówki tych
samych banków.

`[ODCZYT]` `banana_cache` używa:

- `RESOURCE_BANK = 46` — skompresowane źródła klatek,
- `SPARE = 48` — tymczasowy bufor dla klatek, które nakładają się
  ze źródłem,
- banki 40–47 stają się surowymi klatkami banana po zakończeniu tytułu
  (overlay czasowy).

`[ODCZYT]` Przełączenie na bank zasobów banana ma własny trampoline
(`banana_bootstrap`), który zachowuje PORTB i działa tylko wtedy, gdy
starszy bajt ticka wynosi `$0C` (tick 3072–3327).

## 7.5. Bank 49 — kontrolery

`[ODCZYT]` Bank 49 zawiera:

- kontroler szarf i fajerwerków (`ribbon_dance.install_control`),
- kontroler finałowego chłopca (`final_boy.install_control`),
- tabele kotwic, kształty wiatru i finałowe orbity.

`[ODCZYT]` Wybór: `LDA $08F1 / STA $D301` (bo `bank_value(49) = $08C0+49
= $08F1`).

## 7.6. NMI muzyki

`[ODCZYT]` `music_entry` (w głównym kodzie) robi:

```
PHA / TXA / PHA / TYA / PHA
JSR outro_palette      ; router palety terminala
LDA $D301
STA $83FE              ; zapis shadow
LDY $24A5
LDA $26FC,Y
STA $D301              ; bank muzyki wg oryginalnej tabeli
JMP $2218              ; oryginalny handler
```

`[ODCZYT]` `music_exit` przywraca PORTB z `$83FE` i obsługuje dodatkowe
kolory tylko w scenie 14.

`[WNIOSEK]` Bank muzyki jest wybierany **w handlerze NMI**, a nie w
foregroundzie — dlatego foreground musi przywracać PORTB przed powrotem.

## 7.7. Ryzyka

- `[ODCZYT]` Wszystkie przełączenia polegają na `LDA $D301`; na klonie
  z nieczytelnym PORTB trzeba by trzymać własny shadow w RAM.
- `[ODCZYT]` Bank 39 i bank 49 są współdzielone przez kilka systemów —
  nie wolno ich nadpisywać.
- `[OGRANICZENIE]` Testy py65 nie modelują wpływu DMA ANTIC na czas
  przełączeń; stabilność rastra potwierdza tylko sprzęt.
