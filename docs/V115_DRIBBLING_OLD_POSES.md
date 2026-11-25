> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V115 — natural arm from earlier illustrations

Two original dribbling poses from the v024 source and from the v100 XEX graphics
bank were compared: the indexed pixels of both illustrations are identical. The
arm drawn from simple segments was reverted. The new animation uses contours of
the arm, elbow, wrist and fingers cut from the earlier drawings. Two intermediate
phases are built from the same shapes. The contact, push, release and return
phases still use the same PMG ball phase.

The shared background and body remain constant. Remnants of the old abandoned
arm, which could previously remain under the raised palm, were removed. Each
change still copies a 44×28 fragment, i.e. 308 bytes. The correct address of both
buffers from v110 is retained.

The Trevor ordering fix was also kept: during the entrance there are only calm
poses. The first wind-up begins in the action part, and the punch 32 ticks later.
Trevor's silhouette remains registered relative to the tunnel; his phase does not
accidentally shift the character. The last punch does not announce another,
non-existent hit.

[READ] 77 tests passed, including the continuous playback of two bounces, the
range of background writes and the order of all 40 Trevor hits.
[READ] A comparison of the source frames with v100 gave 0 differing pixels.
[READ] Atari800 PAL, 1088XE, Altirra OS, stereo: the POKEY dump matched v035 for
5,899,680 bytes after a single alignment of the start; it covers the whole song.
The software preview replays two consecutive bounces on the same CPU and
buffers; colours and tempo are approximate.

XEX: `build/visual-prototype-v115.xex`; preview:
`build/visual-prototype-v115-kozlowanie.gif`; SHA-256
`a9514828e9340c7b0d6a985204ce01e26f5899eddc0e0152f9810e47ebb7a2c7`.
