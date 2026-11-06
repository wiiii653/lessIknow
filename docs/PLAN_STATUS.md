# Status planu dema — stan po v126

Legenda: ✅ wykonane w buildzie lub potwierdzone; 🟡 częściowo wykonane / ograniczone do prototypu albo emulatora; ⬜ niezaimplementowane lub nieweryfikowane. Ticki pozostają zgodne z zatwierdzonym timeline’em.

## Timeline i akty

| Akt / zakres z timeline’u | Status | Co mamy teraz |
|---|---|---|
| **Act 1 — School Days**, takty 0–24, ticki 0–8975 | ✅ | Szkoła zewnętrzna, wejście dziewczyny, ujęcia chłopca i dziewczyny, sala gimnastyczna oraz animowana piłka. Cheerleaderki wchodzą kolejno w tickach 8975, 9723 i 10471; cztery pozy, animowane cienie i akcenty PMG. |
| **Act 2 — Crush**, takty 24–56, ticki 8975–20942 | ✅ | Taniec, kalejdoskop z cyklem kolorów, cztery zbliżenia podczas występu z mruganiem i włosami. Granice podscen wykorzystują muzyczne ticki. |
| **Act 3 — Basketball Hero**, takty 56–64, ticki 20942–23934 | ✅ | Kozłowanie z animowanym chłopcem, piłką i ramieniem; następnie czteroetapowy wsad, obracająca się tęczowa piłka i błysk. Tło sali przy kozłowaniu pozostaje statyczne. |
| **Act 4 — Trevor Awakens**, takty 64–88, ticki 23934–32909 | ✅ | Ciche wejście, zamach przed każdym ciosem, naprzemienne kombinacje i BANG z osobną fazą pustej chmurki oraz dłuższym rozpryskiem. Zachowano moment powrotu energii w ticku 26925. |
| **Act 5 — Psychedelic Breakdown**, takty 88–120, ticki 32909–44875 | 🟡 | Od ticku 32909 działa kalejdoskop. Zaplanowane przejścia do tunelu w 38892, zmiany tekstury w 40388, mozaika w 41884 i sekwencja oczu od 43379 nie są jeszcze ułożone jako ten akt. Część efektów mozaiki/tunelu istnieje w innych miejscach dema. |
| **Act 6 — Love Triangle**, takty 120–128, ticki 44875–47867 | ⬜ | Brak zaplanowanych kadrów komiksowych i pojedynku Trevora z koszykarzem w tym zakresie. |
| **Act 7 — Trevor Wins**, takty 128–144, ticki 47867–53850 | ⬜ | Brak osobnej kulminacji z gigantycznym Trevorem, flashem i wskazanym narastaniem neonów. |
| **Act 8 — Outro**, takty 144–160, ticki 53850–59833 | ⬜ | Brak creditsów, greetzów i końcowego fade’u w zaplanowanych zakresach. |

Intro TAME IMPALA / album title z plazmą i ditheringiem działa w tickach 0–2992 przed ujęciami szkoły. Kolory liter zmieniają się co uderzenie. To późniejszy dodatek, który zastępuje początkowe logo szkoły z timeline’u; dalsze granice nie przesunięto.

## Zadania weryfikacyjne V1–V7

| Zadanie | Status | Ustalenie |
|---|---|---|
| **V1 — profil ticka muzyki** | 🟡 | Są profile instrukcji py65 i pomiary kosztów callbacku. To nie obejmuje pełnego pomiaru cykli z DMA ANTIC ani potwierdzenia czasu linii na Atari/Altirrze. |
| **V2 — przywracanie PORTB** | ✅ | Wrapper NMI zachowuje i odtwarza bank foreground. Testy przełączeń banków i przerwań przechodzą; odtwarzanie stereo POKEY w Atari800 zgadza się z oryginałem. Nie jest to test fizycznego rozszerzenia. |
| **V3 — odczyty banków muzyki** | ✅ | Ślad dekodera i Atari800 potwierdziły 8 wymaganych banków dla v035; banki 9–14 nie są czytane przez dekoder. Po INIT te banki są wykorzystywane na wideo. |
| **V4 — pauza zatrzymuje licznik** | ⬜ | Brak dedykowanego testu START/pauza i sprawdzenia, czy `$24A7–$24A9` stoi podczas pauzy. |
| **V5 — porównanie v024/v035** | 🟡 | Potwierdzono adresy i zachowanie używanego v035. Pliku v024 nie ma w repozytorium, więc pełnego porównania obu playerów nie da się wykonać. |
| **V6 — równe odstępy DLI** | ⬜ | Produkcja zachowuje cztery ticki na klatkę w dotychczasowym układzie, ale nie ma eksperymentu przesuwającego DLI i oceny wpływu na rytm. |
| **V7 — przycięcie loadera do 7 banków** | 🚫 | Nie wykonywać według obecnego planu: dla strumienia v035 dekoder czyta znacznik końca w banku 8, więc potrzeba 8 banków. Banki 9–14 można wykorzystać dopiero po inicjalizacji, co demo już robi. |

## Pozostałe decyzje i walidacja

- ⬜ GTIA 9 w akcie 5 oraz konkretne źródła i paleta.
- ⬜ Decyzja, czy zachować UI playera; część UI/fontu jest już wyłączona, by zwolnić RAM dla scen.
- ⬜ Ustalenie zasad compo: PAL, dopuszczalny interlace/flicker, rozmiar i konfiguracja sprzętu.
- 🟡 Testy pełnego utworu i porównanie stereo POKEY wykonywane są w Atari800 PAL/1088XE z Altirra OS; potwierdzają, że wideo nie zmieniło strumienia muzyki. Nie zastępują kontroli obrazu, odsłuchu A/V na Altirrze ani próby na fizycznym Atari.
- ⬜ Walidacja na fizycznym Atari 65XE 1 MB ze stereo POKEY oraz pomiar zapasu CPU w najcięższych scenach.

Źródła statusu: `TLIKTB_Atari_Timeline_v2.md`, `TLIKTB_Technical_Constraints.md`, bieżący `README.md` oraz notatki w `docs/` (m.in. audyt banków, profil silnika i wydania V117–V125).
