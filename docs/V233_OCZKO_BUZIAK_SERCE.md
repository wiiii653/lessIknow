# V233 — oczko, buziak i przestrzenne serce w wyrzucie

## Obraz i synchronizacja

- 20615–20661: przedostatnia faza zbliżenia — zamknięte jedno oko,
  drugie otwarte, lekki uśmiech.
- 20662–20941: końcowe zbliżenie — otwarte oczy i dziubek; jedno serce
  wylatuje z ust, rośnie ku widzowi i odlatuje po skosie w prawo/górę.
- 20942: dotychczasowa przebitka tunelu z piłką. Żadna granica sceny
  ani czas wyrzutu nie zostały zmienione.

Poprawiono tylko wnętrze twarzy w dwóch istniejących bitmapach. Włosy,
sylwetka, ręce, kostium, tancerki pod spodem i kadrowanie pozostają.
Nie są potrzebne kolejne pełne klatki postaci.

Serce ma osiem faz co 32 ticki; ostatnia trwa do istniejącego cięcia.
Maski przedstawiają dwa wyraźne płaty i dolny czubek, różowy przód,
białe odbicie światła oraz fioletowy wyciągnięty bok. Zmienna perspektywa
lekko obraca powierzchnię, a kolejne fazy zwiększają rozmiar. Punkt
startu (82,67 w przestrzeni 160×192) odpowiada dolnej wardze.

W samej fazie buziaka wszystkie cztery players składają serce; zachowane
cztery osobno animowane smugi missiles utrzymują pęd po obu bokach.
Wcześniejsze fazy wyrzutu nadal mają dotychczasowe player wind/fireworks.
Nie dodano pętli oczka, buziaka ani kolejnych serc.

## Pamięć i bezpieczeństwo

[ODCZYT] Przed zmianą sześć banków tańca miało po 1024 B wolnego ogona,
łącznie 6144 B. `launch_kiss.py` wykorzystuje **992 B jednego ogona**:
$7C00–$7FDF, indeks 10 w oryginalnej tabeli banków playera (trzeci bank
bitmap szarf, kompozycje 12–17). Pozostaje **5152 B** tych samych ogonów.
Brak nowych banków rozszerzenia i nowych pełnych bitmap.

- 31 B niebankowanego trampolinu: $0F00–$0F1E, rezerwa do $0F3F.
  Początek regionu wspólnych wierszy przesunięto na $0F40.
- Prywatny scratch foreground: $0DDB/$0DDC.
- Kontroler szarf: 2252 B, $5400–$5CCB, +6 B. Finał nadal od $5CD0.
- Główny kod: 2551 B, +27 B na paletę serca; 9 B przed $1E00.
- Same maski serca: 512 B w powyższych 992 B. Każda faza ma cztery
  8×16 strumienie; większe fazy podwajają wiersze i szerokość sprzętowo.

Przygotowanie kasuje i wypełnia wyłącznie nieaktywny PMG. Nie dotyka
aktywnej bitmapy. Własny trampolin zachowuje PORTB na stosie; muzyczne
NMI przywraca aktualnie wybrany bank. Istniejący helper palety przywraca
cztery odcienie serca po muzycznym DLI, bez bankowania i wspólnego scratcha.
Zegar i cztery aktualizacje muzyki na PAL frame pozostają.

## Weryfikacja

[ODCZYT] 29 testów ukierunkowanych zaliczonych, następnie 4/4 testy serca
po dodaniu prób późnego rastra i przerwań NMI. Sprawdzono wszystkie osiem
masek w działającym 6502, skalowanie, pozycje, połysk, rozdzielone płaty,
wyjście do tunelu i powrót do tańca. Wstrzykiwanie NMI obejmuje początek,
środek i ostatnią fazę serca; zapisy rejestrów mieszczą się w wczesnym blank.

[ODCZYT] Atari800 PAL/1088XE, stereo POKEY: **11 608 128 identycznych
bajtów** względem v035, cały utwór. Bez próby na fizycznym Atari.

[ODCZYT] Pełny zestaw v233: **172/172 testy zaliczone**, bez pominięć,
118,6 s. Numerowane XEX i robocze `visual-prototype-dev` są identyczne.
SHA-256: `81b78b474a360dd8bc9659eebc40afcb14186ef84c3160c9900308fb7a9d8ad0`.

Podgląd CPU/PMG, z przybliżoną paletą PAL: `build/launch-kiss-v233.gif`
i `build/launch-kiss-v233.png`. Nie jest pomiarem FPS ani nagraniem sprzętu.
