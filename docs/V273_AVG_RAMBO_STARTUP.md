> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V273 — startup on physical Atari with AVG and 1088 Rambo

[READ from the user, 2026-11-12] The last two diagnostic files of the full
demo started on a physical Atari with a 1088 Rambo expansion and AVG:

- `releases/avg-compact-late-start-001.xex`;
- `releases/avg-final-segment-trace-001.xex`.

[READ] The compact form cuts long runs of zeros from the data loaded into the
bank buffer. Before each such block the buffer is zeroed; the reconstructed
data of the 64 banks was compared byte for byte with the original. In the first
version the low execution memory is deferred to a buffer and restored by the last
INIT, which goes directly to the player. The second adds markers for the
final segments. Both fit below 1 MiB.

[READ] Atari800 PAL/1088XE, Altirra OS: the whole stereo tune matches v035:
16 517 736 bytes for the late-start version and 15 539 688 for final-segment-trace.
A separate run of the 6502 code confirmed that the five copied
low-memory ranges match.

[LIMITATION] The physical confirmation concerns the startup of the two indicated files.
No confirmation of a full run, listening, smoothness or the
mono version was received. The cause of the failure of the earlier files remains a hypothesis:
the file size and the final loading method were changed at the same time.
