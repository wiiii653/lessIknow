# v346 — BUM/BAM i oczy

Ujęcie oczu wybierane jest przed przydziałem PMG, co przywraca tam renderer piłki. Na bananach używany jest ten sam kod BUM/BAM co u Trevora, z pozycją na ósemce. Po 80 tickach PMG jest czyszczone: osobna animacja odlatującej piłki i satelitów ze sceny Trevora nie została dołączona do rotatorów.

Build stereo: `build/visual-prototype-v346.xex`, SHA-256 `7752e3feecbfebe786c7e598a328ec7480887c00c7ecacea637388f693ae07f9`. Generator: 298 wierszy i 2560 B. Trzy z czterech testów directora przeszły; czwarty przerwał import z powodu braku `RuntimeMemory` w `test_sequence`. Nie sprawdzono w emulatorze ani na Atari.
