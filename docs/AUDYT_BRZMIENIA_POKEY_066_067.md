# Audyt brzmienia POKEY — stereo 066 i mono 067

18 listopada 2026. Użytkownik zgłosił źle brzmiące instrumenty lub patterny
na rzeczywistym Atari. Brak nagrania, informacji o wybranym pliku i dokładnej
konfiguracji z tej próby. Poniżej są wyniki analizy programu, bez przypisywania
konkretnemu Atari objawów, których nie zmierzono.

## Błąd miksu mono 067

Mikser w `$2C00` wybiera głośniejszą stronę osobno dla kanałów 3 i 4 przy każdej
aktualizacji (około 5,014 ms). Porównanie 59 833 pełnych aktualizacji potwierdziło
zgodność śladu mono z tym algorytmem. Ustalono przypadki, w których oba źródła
były aktywne, a ich dzielniki i tryby pozostały takie same między dwiema
aktualizacjami. W tych miejscach zmieniał się wyłącznie wybór strony.

| Czas od startu muzyki | Kanał | Przykład |
| --- | --- | --- |
| 0:07,737–0:07,747 | 3, perkusja | Przełączenie prawego `$82` z dzielnikiem `$05` na lewy `$C1` z dzielnikiem `$57`, mimo że oba źródła nadal grają. Powtarza się około 0:08,213 i 0:08,684. |
| 0:45,873 | 4, organ | Dzielnik zmienia się z `$55` na `$AA` przy zmianie poziomu z 5 na 6. To skok o prawie oktawę. |
| 0:47,121–0:47,136 | 4, organ i ozdobnik | Powrót na lewo, przejście na prawo i powrót na lewo w ciągu około 15 ms. |

W całym utworze są 807 takich zmian na kanale 4 (579 organ/organ, 228
organ/ozdobnik), wszystkie ze skokiem co najmniej pięciu półtonów. Na kanale 3
jest 126 zmian w trakcie stałych dzielników obu źródeł, każda zmienia tryb
generatora. Najwięcej skoków melodii w oknach 7,5 s zaczynających się przy
3:00, 3:07,5 i 4:07,5. To wada redukcji głosów w 067, obecna już w 065.
Przy poprawce oprzeć wybór melodii o atak i ciągłość frazy, a perkusji o atak
i priorytet uderzenia. Zmiana poziomu obwiedni sama nie powinna przełączać głosu.

## Stereo 066

Cały aktywny zapis 066 jest bajtowo zgodny ze strumieniem aranżacji v035 z
repozytorium muzyki. Są wszystkie aktualizacje, również na karcie końcowej.
Rozbieżności miksu 067 nie występują w śladzie dwóch POKEY 066.

- **Stereo XEX uruchomiony z jednym POKEY.** Atari800 z wyłączoną opcją
  `STEREO_POKEY` potwierdził 59 833 aktualizacje, w których druga seria zapisów
  nadpisuje pierwszą. Lewa perkusja jest od początku aktywna, a prawa zaczyna
  dopiero przy 0:07,737. Na stockowym dekodowaniu adresów to tłumaczy brak
  perkusji na otwarciu przy uruchomieniu wersji stereo na jednym układzie.
- **Na dwóch POKEY.** Już od startu bas jest rozstrojony między stronami o
  około pięć centów. Przy sumowaniu odsłuchu może pulsować. Suma zadanych
  poziomów na lewym chipie osiąga 30 w 34 aktualizacjach. Pierwszy przypadek
  przy 0:45,477 nakłada poziom 10 basu, 13 perkusji i 7 organu. Wcześniej
  maksimum wynosi 26. Suma poziomów jest górnym ograniczeniem chwilowego
  sygnału, a nie pomiarem przesterowania. Nieliniowość analogowa jest możliwa,
  szczególnie przy kumulacji głosów, ale nie wyjaśnia sama całego otwarcia.

## Podstawa

Atari800 PAL, 1088 XE, Altirra OS, emulator z rejestracją pojedynczych zapisów
POKEY. `066-full` dla dwóch układów, `067-full` i `066-one-pokey` dla jednego.
Czasy z indeksu pakietu i częstotliwości 199,443 aktualizacji/s.
Źródła ról `voice-roles.bin` i stanów `registers.bin` z archiwum v035.
Dla interpretacji analogowej: [Altirra Hardware Reference, Appendix E](https://www.virtualdub.org/downloads/Altirra%20Hardware%20Reference%20Manual.pdf).
Nie wykonano odsłuchu ani pomiaru na fizycznym Atari.
