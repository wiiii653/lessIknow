"""Map musical positions to the PAL player's integer update counter."""

# PAL is 49.86074 Hz, and the player runs four evenly spaced updates per
# frame. At 128 BPM, one four-beat bar lasts 1.875 seconds:
# 49.86074 * 4 * 1.875 = 373.95555 player updates per bar.
TICKS_PER_BAR_NUMERATOR = 37_395_555
TICKS_PER_BAR_DENOMINATOR = 100_000


def tick_at_bar(bar_numerator, bar_denominator=1):
    """Return the first whole player tick at or after a (possibly fractional) bar."""
    numerator = bar_numerator * TICKS_PER_BAR_NUMERATOR
    denominator = bar_denominator * TICKS_PER_BAR_DENOMINATOR
    return (numerator + denominator - 1) // denominator


def tick_at_beat(beat_numerator, beat_denominator=1):
    """Return the first whole player tick at or after a (possibly fractional) beat."""
    return tick_at_bar(beat_numerator, 4 * beat_denominator)
