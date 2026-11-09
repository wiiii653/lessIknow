# Wstępny szkic credits i greetz

**Status:** credits i greetz wdrożone; v240 ma stały terminal z siedmioma
wierszami (status + sześć tekstu), szybkim pisaniem całych plansz i pauzami
na czytanie. Prompt `>_`, kursor miga również w czasie pisania.
V235 dodaje dwie linie o tworzeniu z LLM/AI (`V235_LLM_AI_W_CREDITS.md`).
Komunikat otwierający
i dodatkowe `[NAME]` pozostają propozycjami i nie są wyświetlane.

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
| 8A — credits | 51850–54850 | około 15 s | Stały kadr chłopca, trzy szybko wpisywane plansze z pauzą. |
| 8B — greetz | 54850–59085 | około 21,25 s | To samo tło; pięć plansz, osobno każdy akapit, bez scrollowania podczas czytania. |
| 8C — finał | 59085–59833 | 3,75 s | Oddzielny finałowy kadr i fade. Żaden tekst credits/greetz nie może wejść w ten zakres. |

Granice są zgodne z `TLIKTB_Atari_Timeline_v2.md`. W v197 finał 8C
naprzemiennie pokazuje orbitujące gwiazdki oraz nuty/klucz wiolinowy; tekst
greetz znika w ticku 59085 i nie ingeruje w ten efekt. V240 przyspiesza
start terminala/chłopca o 2000 ticków na wyraźne polecenie użytkownika.

## 3. Proponowany tekst ekranowy

Tekst ekranowy jest po angielsku. Pisownię uchwytów zachowano w formie podanej
przez OGNJENA. Drobne zmiany łamania wierszy będą potrzebne po wyborze kroju i
rozmiaru fontu.

### 8A — Credits

Trzy krótkie plansze, odpowiadające wstępnie `logo_group`, `logo_music` i
`logo_sv` — około 5 sekund na planszę, bez przesuwania granic 8A.

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
ORIGINAL SONG
TAME IMPALA — THE LESS I KNOW THE BETTER
POKEY ADAPTATION BY OGNJEN
WITH OPENAI CODEX
MIDI SCORE REFERENCE: MIDISHOW #200337
```

**Plansza 3 — wydarzenie**

```text
MADE FOR
SILLY VENTURE 2026
AI TOOLS / ATARI SOUL
```

### 8B — Greetz

Poniższy wariant zachowuje osobistą dedykację i wszystkie dotychczas wskazane
osoby oraz grupy. V240 pokazuje pięć osobnych plansz akapitów: szybkie
wpisanie wszystkich wierszy, potem nieruchomy tekst do czytania.

```text
GREETINGS TO ALL MY CHOOMS!

Especially my son Vicvip and his mum,
my mum and dad,
and the rest of my family.

I told Mum: “It’s an Atari demo.”
She said: “I can hear that!”
She’d heard an Atari XE
about 30 years ago.

To my friends and neighbours —
special thanks to D3cker,
who introduced me to AI agents,
and Blasph, who gave me the idea:
Tame Impala on the Atari!

Virus · Foorman · Maq
atarionline.pl · PTODT

All the guests at Silly Venture,
the whole Silly Venture crew,
and everyone watching —
each of you, personally!

[MORE CHOOMS: NAME · NAME · NAME]
```

## 4. Wskazówki do realizacji obrazu

- Zachować aktualne ticki 51850, 54850 i 59085; nie skracać finału 8C.
- Najpierw przygotować podgląd nakładki tekstowej na istniejącym tle leżącego
  chłopca. Postać zajmuje dużą część kadru, a wokół głowy poruszają się obiekty
  PMG, więc nie umieszczać tekstu na twarzy ani na orbicie gwiazdek/nut.
- Dla credits sprawdzić trzy plansze o wysokim kontraście. Dla dłuższych greetz
  każdy akapit stanowi osobną planszę; po szybkim wpisaniu zostawić pauzę
  na czytanie, bez ruchu liter i historii w tym czasie.
- Zachować czytelność nad jasnymi fragmentami stroju: rozważyć niewielki,
  ciemny pas/podkład lub obrys liter. Nie zakładać, że tekst będzie czytelny
  bezpośrednio na całym obrazie.
- Przed implementacją uzupełnić dodatkowe sloty `[NAME]` i potwierdzić pisownię
  wszystkich uchwytów oraz nazw grup.
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
- Krótki napis ekranowy `MIDISHOW #200337` jest tylko propozycją identyfikacji
  źródła; pełny link warto zachować w dokumentacji lub metadanych wydania.

## 6. Walidacja przed włączeniem do wydania

1. Obejrzeć podgląd 8A/8B z tekstem, chłopcem i aktualnym PMG.
2. Sprawdzić, że scroll zaczyna się i kończy w oknie 8B, a przy ticku 59085
   pozostaje wyłącznie planowany finał 8C.
3. Uruchomić testy granic scen i buforów PMG; następnie obejrzeć pełne
   odtwarzanie na Atari800/Altirrze oraz docelowym Atari, jeśli jest dostępne.
4. Nie traktować testów CPU jako potwierdzenia czytelności, płynności rastra ani
   działania na fizycznym sprzęcie.
