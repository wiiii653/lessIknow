# V252 — the girl's eyes in the montage

[READ] In ticks 39379–40126, in the existing montage after Trevor,
a four-phase close-up of the eyes appears: glances to the sides and a blink.
The next phase every 32 ticks. The existing colour cycle and the PMG ball with
satellites in the foreground are retained. Scene boundaries and the music clock are unchanged.
The preview `build/v252-eyes-preview.png` shows the source graphics in
conventional colours, without PMG; it is not an image from an emulator.

[READ] The four bitmaps occupy the existing slots 60–63 of the organic
tunnel in the bank 18 loader. Outside the shot these eye IDs are mapped to phases 56–59;
the last four phases of the organic tunnel were therefore replaced by a repetition of
earlier phases, also in the short tunnel shot after the throw. This is not
a byte-for-byte reconstruction of the tunnel. The mapper in bank 2 starts at `$7500`, and
the trampoline in RAM under the OS at `$EC04`. There is a collision check during installation.
No additional bank; the main code remains 2560 B.

[READ] Tests of selected callbacks check the four bitmaps, the window boundaries,
PORTB restoration and the selection of the remaining frames. The full stereo comparison
attempt in Atari800 did not start: the local AppImage requires an unavailable FUSE.
Image smoothness and listening on a physical Atari were not checked.

[READ] A later comparison of v253, containing the eyes scene, with v035 in
Atari800 passed for the whole track (stereo POKEY); see the v253 document.
