> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V130 — Trevor entrance mask

[READ] The earlier close entrance pose contained a separate shot of the room with a large
black area behind the head and shoulders. When switching from the distant pose, fragments
of the wall and door disappeared. The shot did not use a mask cutting out the figure.

[READ] A contour of the close pose was added, along with separate openings under the arms.
The close Trevor is composited over the distant shot. Black remnants of the
backing were cleaned at the edge, preserving the outline and details inside the silhouette.
Composition happens during asset building; the playback code and the pose
change moments remain as before.

Finished file: `build/visual-prototype-v130.xex`.
Raster comparison v128/v130: `build/v130-entrance-preview.png`.
V129 was an intermediate contour variant; v130 additionally cleans the backing
at the mask edges.

A check was added for the shared room behaviour outside the mask and for the face behaviour.

[READ] Final build: 20 Trevor, BANG and optimisation regression tests OK.
Atari800 PAL/1088XE: 3 527 496 identical stereo POKEY bytes,
about 982.6 s of emulation, the whole track.

[READ] Full `make check` on the final build: 84/84 tests OK, 99.982 s.
