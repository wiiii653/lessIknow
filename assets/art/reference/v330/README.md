> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../../../../docs/README.md) for active instructions.

# Party-Version Girl Reference

The [reference frames captured from Atari800](opening.png) come from
archival stereo release 058 / v330. The top row shows three positions from the
side panorama. The bottom row shows a rear close-up and two views on the path
to the entrance. These six frames are pixel-identical in release 061 / v352.

Reference XEX: [stereo 058](../../../../releases/less-i-know-demo-release-058-stereo.xex).
SHA-256: `f3c14bc36b96220ead8fbe24df2e0dfc7ef5d30371d5cd83d11f808b62706b8f`.

- The rear view comes from [act1_north_girl.png](../../source/act1_north_girl.png).
  `school_story.party_girl()` returns the original 48×64 artwork with its mask
  and Fuji emblem. Positions and scale come from `GIRL_PLACEMENTS`.
- The walk cycle comes from [arena-pan.bin](../v175/arena-pan.bin).
  `school_parallax.party_frames()` returns all 18 frames with three profile
  corrections already present in the party version.

Use these frames as the source reference for opening-scene refinements. Since
v362, `school_story.foreground_girl()` derives the close-up from the same
drawing directly on the scene grid. Side-panorama retouching is stored
separately in `PROFILE_POLISH`. Tests check the original v330 hashes.
