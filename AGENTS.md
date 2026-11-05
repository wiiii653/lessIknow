# Repository Guidelines

## Project Structure & Module Organization

This project is an Atari XE 1 MB audiovisual demo for “The Less I Know The Better.” The current checkout contains planning documents and a prebuilt player:

- `TLIKTB_Atari_Timeline_v2.md`: act boundaries, musical events, and player tick synchronization.
- `TLIKTB_Technical_Constraints.md`: hardware limits, memory layout, proposed asset formats, and verification tasks V1–V7.
- `less-i-know-release-v035.xex`: the supplied executable.

There are currently no source, test, or asset directories. The referenced `TLIKTB_Asset_List.md` and older v024 executable are absent; do not assume they are available.

## Build, Test, and Development Commands

No build scripts, dependency manifests, or automated test commands are provided. Document the assembler, dependencies, and exact commands when introducing a source pipeline.

- `ls -lh *.xex`: inspect available executables and sizes.
- `sha256sum less-i-know-release-v035.xex`: record the binary checksum before comparisons.

To run locally, load the XEX in Altirra configured for 65XE, PAL, 1 MB expanded RAM, and stereo POKEY. Record the memory expansion configuration used.

## Coding Style & Naming Conventions

Preserve the existing Markdown structure and Polish terminology when updating the specifications. Use `$` hexadecimal notation for Atari addresses, such as `$D301`.

No formatter, linter, or source indentation standard is configured. Establish consistent formatting when adding code. The proposed asset convention uses `snake_case` with act prefixes, for example `act2_hearts_tile.bin`; formats include `.bin`, `.pal`, `.pmg`, `.fnt`, and compressed `.zx0` files.

## Testing Guidelines

Validation currently relies on emulator checks; no automated framework or coverage threshold exists. Complete and document V1–V7 before building the video engine. Verify v035 addresses instead of reusing v024 addresses without checking.

Test each build in the target configuration and listen for missed music ticks throughout playback. Record results under the relevant V-number, distinguishing direct observations (`[ODCZYT]`), inferences (`[WNIOSEK]`), and assumptions (`[ZAŁOŻENIE]`).

## Commit & Pull Request Guidelines

Git history is unavailable in this checkout, so existing commit conventions cannot be established. Use concise, imperative subjects describing one change.

Pull requests should explain the change, affected acts or memory regions, and validation results. Include screenshots for visual changes and playback observations for timing changes.

## Timing & Memory Constraints

Use the player tick counter for scene synchronization. Preserve four evenly spaced music updates per PAL frame. Verify PORTB restoration and bank ownership before changing memory use. Obtain human confirmation before changing act boundaries, tick positions, or production priorities.
