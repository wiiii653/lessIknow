> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# v348 — director from the first rotators

The director changes tempo and direction in the first rotators (ticks 11967–14958), in the tunnel before the insert (20942–21689) and in the montage after Trevor (29656–41883). The cuts of the story scenes remain unchanged. The eyes are at ticks 39379–40126; BUM/BAM with side speech bubbles is active only on the bananas after that shot. The bananas last until tick 41135, after which the tunnels return.

Stereo build `build/visual-prototype-v348.xex`: SHA-256 `1a30a191f06580a8662dc16bb9d4be682b3f9820db3de505983fd5c7da9c2f65`. Generator: 298 shared rows, 2542 B of code. Five director tests and two tunnel/insert transition tests passed in py65. Separately checked on two bars: BUM, BAM and all four speech-bubble buffers, disabling the overlay in the eyes and PORTB preservation. Not checked in an emulator or on physical Atari. The previously reported artifacts of the insert board were not fixed; see [audit](AUDIT_DUNK_PMG_V347.md).
