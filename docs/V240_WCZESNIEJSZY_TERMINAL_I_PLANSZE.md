# V240 — wcześniejszy terminal, szybki wydruk i czas na czytanie

Na wyraźne polecenie użytkownika terminal i leżący chłopiec zaczynają się
w **51850 zamiast 53850** — o 2000 ticków, około 10 s wcześniej. Koniec
tekstu 59085, fade od 59705 i trwała czerń od 59833 pozostają zachowane.
Dolny kadr, orbita PMG i siedmiowierszowy układ terminala nie zmieniają się.

## Pisanie i prompt

- Prefix każdego wpisu to `>`. Przed rozpoczęciem tekstu widać `>_`.
- Podkreślnik jest cienkim kursorem na dolnej linii znaku, zamiast bloku.
- Kursor **zawsze miga** podczas działania terminala: zarówno przy
  wpisywaniu, jak i podczas pauzy po zakończonej planszy. Bit 6 zegara
  daje około 0,32 s na stan i około 0,64 s na pełny cykl.
- Pisanie: 1 znak na tick; prompt i Enter mają po 4 ticki. Zniknęły długie
  pauzy przed/po każdym pojedynczym wierszu.
- Cała plansza powstaje w 55–180 tickach (około 0,28–0,90 s), po czym
  pozostaje nieruchoma przez 667–900 ticków (około 3,34–4,51 s).

## Plansze

Każdy akapit greetz jest osobną planszą; żaden wpis nie został usunięty.
Nie ma już ciągłego przewijania historii podczas czytania.

| Start | Treść | Wpisanie / pauza w tickach |
|---:|---|---:|
| 51850 | Autor, Codex, LLM | 166 / 834 |
| 52850 | Muzyka | 147 / 853 |
| 53850 | Silly Venture / AI | 100 / 900 |
| 54850 | Rodzina | 133 / 714 |
| 55697 | Anegdota o mamie | 131 / 716 |
| 56544 | Przyjaciele, D3cker, Blasph | 180 / 667 |
| 57391 | Grupy i portale | 55 / 792 |
| 58238 | Ekipa i goście Silly Venture | 136 / 711 |

## Pamięć i synchronizacja

55 wpisów czasu (110 B) i 54 długości ładowane są razem z fontem, do
nieużywanych glyphów kontrolnych: $C828–$C895 i $C8A8–$C8DD. Znaki
drukowalne zaczynają się dopiero od $C900. Nie ma statycznych insertów
do używanego wcześniej drugiego bufora bitmapy.

Wyłączone UI $23CE–$2450 jest teraz całe dostępne dla stagingu; wykorzystano
49 B. Łączny staging ma 1914 B, zasoby po kompresji 1832 B. Loader nadal
373 B i kończy się $3FCC, przed zasobami $3FCE. $23CD pozostaje RTS,
router $2451 i żywe zmienne playera od $249C nie są naruszane.

Typewriter ma 172 B w $EB44–$EBEF, o 23 B mniej. Director rotatora/tunelu
zatrzymuje się w 51850: po odcięciu nieużywanych późniejszych punktów ma
60 cue i 301 B w $EC20–$ED4C. Rezerwy obu helperów pozostają, więc nie
przesunięto wspólnej puli wierszy. Główny kod nadal 2521 B.

Nie wykorzystano dodatkowych banków ani ich luk. **Wszystkie 64 banki
payloadu są identyczne bajtowo z v239**. Cztery muzyczne DLI zachowują
pozycje 1/79/157/235; dodatkowy split palety pozostaje w 57.

## Weryfikacja

[ODCZYT] 59 testów ukierunkowanych zaliczonych: kompletność ośmiu plansz,
szybkie pisanie i nieruchoma pauza, miganie kursora również w trakcie
pisania, dokładny prompt/podkreślnik, nowa granica sceny i zachowane
bufory, orbita PMG, DLI i PORTB.

[ODCZYT] Atari800 PAL/1088XE, stereo POKEY: **11 175 336 identycznych
bajtów** względem v035, cały utwór. Bez próby na fizycznym Atari.

Podglądy CPU/ANTIC/PMG: `build/terminal-v240.png`,
`build/terminal-v240.gif` (szybki wydruk pierwszej planszy i pauza z kursorem).

[ODCZYT] Pełna regresja: **183/183 testy**, bez pominięć, 133,5 s.
Build roboczy i v240 są identyczne. SHA-256:
`b72619f7da4a364b5f13099411b31530d10fd4ceda32ebe75cfce6fe6fa5dcb7`.
