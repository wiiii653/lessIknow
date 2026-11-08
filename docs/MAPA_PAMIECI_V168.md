# Raport pamięci bankowanej — v168

## Wynik

Konfiguracja docelowa udostępnia 64 banki po 16 KiB, łącznie 1 MiB pamięci
bankowanej. **Nie ma żadnego całego wolnego banku.** Potwierdzone luki
wewnątrz już używanych banków sumują się do **31 623 B (30,88 KiB)**.
To około 3,0% pojemności bankowanej, ale pamięć jest podzielona na małe
obszary z różnymi właścicielami i ograniczeniami dostępu. Nie można jej
traktować jak jednego wolnego bloku ani jako nowego banku.

V168 zmienia geometrię grafiki tunelu Trevora w istniejących bankach faz.
Nie przydziela banku ani nie zwiększa rozmiaru kodu głównego. Zestaw luk
pozostaje taki, jak w zweryfikowanej mapie v166; szczegóły generatora i
rozmiary strumieni są w `V166_PLYNNIEJSZY_TANIEC.md`.

## Rozkład potwierdzonych luk

| Właściciel / lokalizacja | Wolne bajty | Uwagi |
|---|---:|---|
| Loader index 2 — bank pomocniczy tunelu | 4 251 | Największa pojedyncza luka: `$6E0F–$77FF`, 2 545 B. Helper tunelu pozostaje w `$7800–$7FFF`. |
| Indeksy 24–31 oraz ogony 32–38 | 14 016 | Obejmuje 4 096 B w bankach aktora bocznego i 9 920 B ogonów banków z klatkami pośrednimi. |
| Sloty dawnych masek piłek | 7 212 | Dziewięć luk po 512 B oraz siedem ogonów po 372 B. Część indeksu 39 jest zajęta przez finałowego chłopca. |
| Oryginalne banki playera 9–14 | 6 144 | Po 1 024 B pod `$7C00–$7FFF` w każdym z sześciu banków tańca. |
| **Razem** | **31 623** | Rozproszone luki w używanych bankach. |

## Zajętość, której nie należy mylić z wolnym miejscem

- Indeksy loadera 0–63 są przydzielone. „Indeks loadera” oznacza numer
  wybierany przez `school_portrait_bank.bank_value()`, a nie numer PORTB
  ani numer banku z oryginalnego playera.
- Indeksy 0–7 obejmują kod/player i muzykę. Dekoder v035 wymaga ośmiu
  banków; pomysł redukcji do siedmiu nie jest dostępny.
- Banki playera 9–14 mieszczą skompaktowane klatki tańca; wolne są tylko
  wskazane ogony, a nie całe banki.
- Bank 49 zawiera ciche grafiki Trevora, kontroler szarf i finału, kod
  Trevora, dane wstęg oraz metadane. Jego nieużywane historyczne sloty nie
  są wolnym blokiem po wydaniu v166.
- XEX zapisuje pełne banki. Wolne ogony zmniejszają możliwość kolizji przy
  kolejnej alokacji, ale nie zmniejszają rozmiaru XEX proporcjonalnie do
  liczby pustych bajtów.

**Odczyt źródeł:** `AGENTS.md` (Current Memory Ownership),
`docs/V166_PLYNNIEJSZY_TANIEC.md` oraz `build/v168-allocations.json`.
W v168 nie wykonano ponownego audytu każdej komórki pamięci ani testów
sprzętowych; liczba luk bazuje na szczegółowym audycie v166, a brak zmiany
alokacji wynika z użycia istniejących slotów.
