> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V251 — visible change of the orbit path

V250 changed mostly the radius, so the motion could still look like an unchanging
circle. Now each new terminal line selects a different shape of the elliptical
orbit: the eccentricity and the inclination of the path change. The target still
approaches gradually, one step every 16 ticks; neighbouring steps move a single
sprite by at most 4 pixels. The text clocks, scene boundaries, colours, fades
and PMG memory remain unchanged.
