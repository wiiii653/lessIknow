> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V120 — memory and code review

[READ] In banks 24–39 the code selects only Trevor's action poses, and before the impacts it selects bank 49 with two entry poses. The duplicated frames in those banks were not being read. 16 areas of 2560 bytes each ($4A00–$53FF) were freed in the action banks, and three areas of 2560 bytes each ($5400–$5DFF, $6A00–$73FF, $7400–$7DFF) were freed in the entry bank: 48 640 bytes in total for future use. The same banks are still occupied; the XEX stores full bank segments.

[READ] The plasma code reservation was reduced from 2048 to 1792 bytes. The generator still rejects exceeding this limit, and checks the neighbouring areas for overlap. 256 bytes of space under the ROM were recovered for shared image rows.

[CONCLUSION] The plasma composition remains time-expensive: it can skip animation phases. The freed bank fragments are not a contiguous block and require checking bank selection and PORTB restoration before use. Scene boundaries and the music update rate were not changed.
