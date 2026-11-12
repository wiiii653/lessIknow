"""Artwork and GTIA palettes for the opening story and gym sequences."""

# The original source classification preserves jacket and pavement details.
# The sampled school and warmer gym colours describe the intended display.
SCHOOL_PALETTE = ((0, 0, 0), (157, 80, 88), (66, 111, 167), (222, 152, 138))
ART_PALETTE = ((0, 0, 0), (255, 50, 160), (0, 220, 255), (255, 190, 150))
GYM_PALETTE = ((0, 0, 0), (142, 69, 66), (166, 112, 66), (194, 137, 112))

# GTIA colour/luminance bytes for the matching scene families.
SCHOOL_GTIA = (0x38, 0x88, 0x2c)
GYM_GTIA = (0x38, 0x68, 0x2a)
# Deep petrol balances the warm brick, amber and peach gym colours.
PRACTICE_WALL_GTIA = 0x96
