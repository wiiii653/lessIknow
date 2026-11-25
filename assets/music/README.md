# Music Data from v035

`v035/` contains the fourteen original 16 KiB blocks loaded through
`$8000–$BFFF` by `less-i-know-release-v035.xex`, in their original load order.
Recreate them with:

```sh
python3 tools/extract_music.py less-i-know-release-v035.xex assets/music/v035
```

Choose a new output directory if `v035/` already exists. The manifest records
the original XEX and bank SHA-256 hashes. Banks 9–14 contain only `$FF`; bank 8
contains data followed by `$FF`. Keep all banks until their playback reads have
been verified. See [the music-bank audit](../../docs/MUSIC_BANK_AUDIT.md).

The source banks preserve the original player data. The post-party stereo build
uses the v035 player with four music updates per PAL frame. The hardware dev
target uses release 122 music with the opening kick muted. See the Makefile
for the active options. Build instructions and evidence are in the
[project README](../../README.md) and
[project status](../../docs/PLAN_STATUS.md).

## v035 Display-List Inspection

Run `python3 tools/inspect_display_list.py less-i-know-release-v035.xex` to
inspect static XEX contents. The list at `$3300` schedules DLIs on lines 0, 78,
156 and 234 relative to its start, then jumps back to `$3300` with JVB. It
accounts for 235 scanlines before JVB; ANTIC controls the remaining frame time.
A replacement list must preserve the four DLI positions relative to the PAL
frame. This inspection does not execute INIT/RUN or establish whether the
player changes the list at runtime.
