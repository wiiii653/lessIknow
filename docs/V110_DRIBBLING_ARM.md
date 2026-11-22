# V110 — arm motion and correct dribbling buffer

Fixed the base address of the buffer used by the display list after updating
the character fragment. Previously a copy could land in one buffer while the
display list still pointed at the other. Isolated-frame tests did not catch
this bug; the new regression runs two full cycles on the same CPU and compares
the image that is actually displayed.

The boy has four drawn arm phases: contact with the ball, push, release and
return. The motion is tied to the phase of the same ball PMG; before the next
bounce the hand returns to the contact pose. The old arm was removed from the
shared graphics. The silhouette and the hall are fixed, and the updated part is
44×28 pixels and occupies 308 bytes. The three additional fragments plus one
full dribbling base together take less memory than the two former full frames.
The remaining four input frames were not changed.

[READ] 75 tests passed, including the test of two full bounces, four visible arm
positions, the fixed background and the range of writes to memory. [READ]
Atari800 PAL, 1088XE, Altirra OS, stereo: after a single alignment of the start,
5 925 960 POKEY bytes were identical to v035; the comparison covers the whole
track.

The preview `build/visual-prototype-v110-kozlowanie.gif` was made from
successive runs on the same py65 buffers. Colours and timing are approximate;
this is not an emulator recording. XEX: `build/visual-prototype-v110.xex`;
SHA-256 `dcd09eca4bb190edcbd42d0dc89899e5c7716e0ac8c390fdb02b3a42e5a55310`.
