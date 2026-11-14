# v350 — wolniejszy dolot piłek Trevora

Dolot każdej piłki trwa 48 zamiast 32 ticków. Ta sama droga 32 kroków jest
rozłożona na dłuższy czas; uderzenia, pozy ciosów i terminy BUM/BAM pozostają
na dotychczasowych tickach muzyki. Pierwszy dolot rozpoczyna wejście w tło
akcji 16 ticków wcześniej. Odloty po uderzeniu pozostają bez zmian.

Tablica 49 przeliczeń jest w banku 19 pod `$7250–$7280`, za kodem panoramy
kończącym się pod `$7245`. Generator sprawdza, czy zajmowane miejsce jest
puste. Kod lotu zajmuje 2041 B pod `$6800–$6FF8`.

Stereo `build/visual-prototype-v350.xex` (1 115 783 B), SHA-256
`2ff0dff063ceedce22953b7c7d481cd875171ceb6f1340d901cdee3354a6eca1`.
Generator: 298 współdzielonych wierszy, 2542 B kodu głównego. Testy py65
obejmują doloty i odloty wszystkich ciosów, przerwania muzyki, bufor PMG,
granice wejścia oraz director. Nie uruchamiano emulatora ani fizycznego Atari.
Wcześniej zgłoszone artefakty tablicy wsadu nadal wymagają naprawy.
