# V120 — przegląd pamięci i kodu

[ODCZYT] W bankach 24–39 kod wybiera wyłącznie pozy akcji Trevora, a przed uderzeniami wybiera bank 49 z dwiema pozami wejścia. Powielone w tych bankach klatki nie były odczytywane. Zwolniono 16 obszarów po 2560 bajtów ($4A00–$53FF) w bankach akcji i trzy obszary po 2560 bajtów ($5400–$5DFF, $6A00–$73FF, $7400–$7DFF) w banku wejścia: razem 48 640 bajtów do wykorzystania w przyszłości. Nadal zajęte są te same banki; XEX przechowuje pełne segmenty banków.

[ODCZYT] Rezerwację kodu plazmy zmniejszono z 2048 do 1792 bajtów. Generator nadal odrzuca przekroczenie tego limitu, a sąsiednie obszary sprawdza pod kątem nakładania. Odzyskano 256 bajtów przestrzeni pod ROM-em dla współdzielonych wierszy obrazu.

[WNIOSEK] Kompozycja plazmy pozostaje kosztowna czasowo: może pomijać fazy animacji. Zwolnione fragmenty banków nie są ciągłym blokiem i przed użyciem wymagają sprawdzenia wyboru banku oraz przywracania PORTB. Nie zmieniono granic scen ani częstotliwości aktualizacji muzyki.
