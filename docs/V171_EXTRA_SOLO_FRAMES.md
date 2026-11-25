> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V171 — additional solo frames

> **Release v171 is defective and should not be played.** The streams of
> compressed frames went into the image banks without a decoder. The v172 fix
> moves them to banks 32–35, which contain the decoder.

## Animation change

I added four new movement phases to the central solo shot: on the pose change
6→7, 7→8, 8→9 and 9→8. They fall at 3/4 of the transition, about 34–35 ticks
after the previous accent. The existing intermediate frame remains at the
middle of the transition, and the new frames shorten its final gaps to about
11–12 ticks. I did not change the scene length, the musical accents, the side
shot, the group dance or the girl's throw.

## Graphics and memory

The new poses come from a 3×3 sheet, of which four frames are used. Each was
composed at the original solo scale, reduced to the native 160×64 bitmap and
aligned to the hand anchors. The data is fast LZ and was verified by local
reconstruction of the streams before assembling the banks.

- Source: `assets/art/source/act2_ribbon_inbetweens_v171.png`.
- Generation description: `assets/art/source/act2_ribbon_inbetweens_v171.prompt.txt`.
- In the original v171 the four frames occupied 3805 B in the tails of banks 8–11 from
  `$7C00`. That location did not contain a decoder and caused a playback error.
- The selector grows from 1015 to 1370 B, uses `$4040–$4599`; the first stream
  still starts at `$4600`.
- The main code and the non-banked runtime keep their sizes. The corrected bank
  routing is described in [V172](V172_DANCE_DECODER_FIX.md).

All the remaining frames and their anchors return to the previous selection on
the next accent. The dance banks are loaded without a change in their size, and
the data of the new frames occupies previously free tails.

## Validation scope

The first XEX release built, but the build itself did not check for the presence
of the decoder in the selected bank. The playback problem was fixed in v172.
