# Credits i greetz — aktualny tekst v261

**Status:** credits i greetz wdrożone. V261 ma siedem wierszy terminala
(status + sześć tekstu), szybkie pisanie całych plansz i pauzy na czytanie.
Prompt `>_`, kursor miga również w czasie pisania. Dodano KEY-G i FALCON;
pisownia FOORMAN i liczba stron pozostają bez zmian.
V235 dodaje dwie linie o tworzeniu z LLM/AI (`V235_LLM_AI_W_CREDITS.md`).
Komunikat otwierający pozostaje propozycją i nie jest wyświetlany.

## 1. Komunikat otwierający

Proponowany disclaimer przed intro:

```text
THIS DEMO IS NOT INTENDED TO PROMOTE VIOLENCE.
IT IS SOLELY A DEMONSTRATION OF THE
POWER AND CAPABILITIES OF THE ATARI XE.

ANY RESEMBLANCE BETWEEN CHARACTERS
IN THIS DEMO AND OTHER DEPICTIONS
IS PURELY COINCIDENTAL AND
WAS NEVER INTENDED.
```

Preferowane miejsce to krótka plansza przed tickiem 0, tak aby nie przesuwać
muzycznych granic intro; wydłużyłaby ona jednak całkowity czas prezentacji.
Alternatywą jest czytelna nakładka na początkową plazmę, bez przesuwania ticków.
Wybór sposobu i długości wyświetlania pozostaje do zatwierdzenia po podglądzie.

## 2. Zarezerwowane okna

| Sekwencja | Ticki | Czas | Tło / ograniczenia |
|---|---:|---:|---|
| 8A — credits | 49850–52850 | około 15 s | Stały kadr chłopca, trzy szybko wpisywane plansze z pauzą. |
| 8B — greetz | 52850–59085 | około 31,2 s | To samo tło; pięć plansz, osobno każdy akapit, bez scrollowania podczas czytania. |
| 8C — finał | 59085–59833 | 3,75 s | Oddzielny finałowy kadr i fade. Żaden tekst credits/greetz nie może wejść w ten zakres. |

Granice są zgodne z `TLIKTB_Atari_Timeline_v2.md`. W v197 finał 8C
naprzemiennie pokazuje orbitujące gwiazdki oraz nuty/klucz wiolinowy; tekst
greetz znika w ticku 59085 i nie ingeruje w ten efekt. V240 przesunęło
terminal do 51850, a v248 dalej przeniosło go do 49850 razem z montażem.
Obecne początki ośmiu stron to 49850, 50850, 51850, 52850, 54097, 55344,
56591 i 57838.

## 3. Tekst ekranowy w v261

Tekst ekranowy jest po angielsku. Poniższe wiersze odpowiadają aktualnym
stronom w `tools/outro_text.py`; nagłówki statusu terminala nie są częścią
treści credits/greetz.

### 8A — Credits

Trzy strony, około 5 sekund na stronę; po szybkim wpisaniu każda pozostaje
widoczna do następnej granicy.

**Plansza 1 — autor / grupa**

```text
THE LESS I KNOW THE BETTER
AN ATARI XE 1 MB DEMO
BY OGNJEN
MADE WITH OPENAI CODEX
HUMAN VISION / LLM CODE
```

**Plansza 2 — muzyka**

```text
SONG / TAME IMPALA
THE LESS I KNOW THE BETTER
POKEY / OGNJEN / CODEX
MIDI / MIDISHOW 200337
```

**Plansza 3 — wydarzenie**

```text
MADE FOR
SILLY VENTURE 2026
AI TOOLS / ATARI SOUL
```

### 8B — Greetz

Pięć plansz pokazuje te akapity osobno; wiersze są szybko wpisywane, po czym
pozostają nieruchome do następnej strony.

```text
GREETINGS TO ALL MY CHOOMS!
ESPECIALLY MY SON VICVIP AND HIS
MUM, MY MUM AND DAD,
AND THE REST OF MY FAMILY.
```

```text
I TOLD MUM: "IT'S AN ATARI DEMO."
SHE SAID: "I CAN HEAR THAT!"
SHE'D HEARD AN ATARI XE
ABOUT 30 YEARS AGO.
```

```text
TO MY FRIENDS AND NEIGHBOURS -
SPECIAL THANKS TO D3CKER,
WHO INTRODUCED ME TO AI AGENTS,
AND BLASPH, WHO GAVE ME THE IDEA:
TAME IMPALA ON THE ATARI!
```

```text
VIRUS / FOORMAN / MAQ / KEY-G
FALCON / ATARIONLINE.PL / PTODT
```

```text
ALL THE GUESTS AT SILLY VENTURE,
THE WHOLE SILLY VENTURE CREW,
AND EVERYONE WATCHING -
EACH OF YOU, PERSONALLY!
```

## 4. Wskazówki do realizacji obrazu

- Zachować aktualne ticki 49850, 52850 i 59085; nie skracać finału 8C.
- Najpierw przygotować podgląd nakładki tekstowej na istniejącym tle leżącego
  chłopca. Postać zajmuje dużą część kadru, a wokół głowy poruszają się obiekty
  PMG, więc nie umieszczać tekstu na twarzy ani na orbicie gwiazdek/nut.
- Dla credits sprawdzić trzy plansze o wysokim kontraście. Dla dłuższych greetz
  każdy akapit stanowi osobną planszę; po szybkim wpisaniu zostawić pauzę
  na czytanie, bez ruchu liter i historii w tym czasie.
- Zachować czytelność nad jasnymi fragmentami stroju: rozważyć niewielki,
  ciemny pas/podkład lub obrys liter. Nie zakładać, że tekst będzie czytelny
  bezpośrednio na całym obrazie.
- Przed kolejną edycją potwierdzić pisownię uchwytów i nazw grup; obecne strony
  nie zawierają dodatkowych slotów `[NAME]`.
- Wszystkie 64 banki są przydzielone. Przed dodaniem fontu, danych lub kodu
  sprawdzić aktualną mapę pamięci w `AGENTS.md` i nie zakładać, że historyczne
  luki nadal są wolne. Zachować własność banków, podwójne bufory PMG i istniejący
  kontroler finału.

## 5. Źródło muzyki i zakres potwierdzonych informacji

- Projekt używa oryginalnej muzyki z playera v035; dokumentacja opisuje utwór
  jako **Tame Impala — “The Less I Know The Better”**.
- OGNJEN wskazuje, że MIDI z Midishow było głównym źródłem partytury do dalszej
  adaptacji na POKEY, wykonanej przez niego z pomocą agenta Codex.
- Podany odnośnik źródłowy: <https://www.midishow.com/en/midi/the-less-i-know-the-better-midi-download-200337>.
  Próba odczytu strony w trakcie przygotowania szkicu zwróciła HTTP 403;
  uploadera i licencji MIDI nie udało się zweryfikować. Nie przypisujemy więc
  autorstwa MIDI ani statusu licencji bez dodatkowego potwierdzenia.
- Ekran pokazuje skrócony opis `MIDI / MIDISHOW 200337`; pełny link pozostaje
  w dokumentacji, bo źródło i licencja nie zostały niezależnie zweryfikowane.

## 6. Walidacja przed włączeniem do wydania

1. Przed zgłoszeniem obejrzeć v261 na Atari800/Altirrze oraz, jeśli dostępne,
   na docelowym Atari; testy automatyczne nie zastępują oceny A/V.
2. Sprawdzić, że pięć stron greetz mieści się w oknie 8B, a przy ticku 59085
   pozostaje wyłącznie planowany finał 8C.
3. Po zmianach tekstu uruchomić testy granic scen i terminala. V261 przechodzi
   pełne `make check` (199/199); po v261 nie wykonano odtworzenia emulatorowego
   ani testu sprzętowego.
4. Nie traktować testów CPU jako potwierdzenia czytelności, płynności rastra ani
   działania na fizycznym sprzęcie.
