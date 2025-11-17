#!/usr/bin/env python3
"""
Generate CHR-ROM data from official console logo designs
Based on authentic logo appearances
"""

def create_tile_from_pattern(pattern):
    """Convert 8x8 ASCII pattern to NES tile format (16 bytes)"""
    # pattern should be list of 8 strings, each 8 chars
    # Characters: ' ' = transparent/black, any other = white/colored
    plane0 = []
    plane1 = []

    for row in pattern:
        byte0 = 0
        byte1 = 0
        for i, char in enumerate(row[:8]):
            if char != ' ' and char != '.':
                # Set pixel (both planes for color 3 = brightest)
                byte0 |= (1 << (7 - i))
                byte1 |= (1 << (7 - i))
        plane0.append(byte0)
        plane1.append(byte1)

    return plane0 + plane1


# Official logo designs based on authentic console branding
# Each logo is 3x4 tiles (24x32 pixels)

# === Nintendo Entertainment System ===
# Classic "NES" wordmark - bold, simple letters
nes_logo = {
    # Row 0, tiles 0-2
    0: create_tile_from_pattern([
        "        ",
        "        ",
        " ██  ██ ",
        " ███ ██ ",
        " ██████ ",
        " ██ ███ ",
        " ██  ██ ",
        "        "
    ]),
    1: create_tile_from_pattern([
        "        ",
        "        ",
        " ██████ ",
        " ██     ",
        " █████  ",
        " ██     ",
        " ██████ ",
        "        "
    ]),
    2: create_tile_from_pattern([
        "        ",
        "        ",
        " ██████ ",
        " ██     ",
        " ██████ ",
        "     ██ ",
        " ██████ ",
        "        "
    ]),
    # Row 1, tiles 3-5
    3: create_tile_from_pattern([
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        "
    ]),
    4: create_tile_from_pattern([
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        "
    ]),
    5: create_tile_from_pattern([
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        "
    ]),
    # Row 2, tiles 6-8
    6: create_tile_from_pattern([
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        "
    ]),
    7: create_tile_from_pattern([
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        "
    ]),
    8: create_tile_from_pattern([
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        "
    ]),
    # Row 3, tiles 9-11
    9: create_tile_from_pattern([
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        "
    ]),
    10: create_tile_from_pattern([
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        "
    ]),
    11: create_tile_from_pattern([
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        "
    ]),
}

# === Super Nintendo Entertainment System ===
# "SUPER NINTENDO" wordmark with characteristic styling
snes_logo = {
    # Row 0 - "SUPER" text
    0: create_tile_from_pattern([
        "  ████  ",
        " ██  ██ ",
        " ██     ",
        "  ███   ",
        "    ██  ",
        " ██  ██ ",
        "  ████  ",
        "        "
    ]),
    1: create_tile_from_pattern([
        " ██  ██ ",
        " ██  ██ ",
        " ██  ██ ",
        " ██  ██ ",
        " ██  ██ ",
        " ██  ██ ",
        "  ████  ",
        "        "
    ]),
    2: create_tile_from_pattern([
        " ██████ ",
        " ██  ██ ",
        " ██  ██ ",
        " ██████ ",
        " ██     ",
        " ██     ",
        " ██     ",
        "        "
    ]),
    # Row 1 - "NINTENDO" text top half
    3: create_tile_from_pattern([
        "        ",
        " ██  ██ ",
        " ███ ██ ",
        " ██████ ",
        " ██ ███ ",
        " ██  ██ ",
        "        ",
        "        "
    ]),
    4: create_tile_from_pattern([
        "        ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "        ",
        "        "
    ]),
    5: create_tile_from_pattern([
        "        ",
        " ██  ██ ",
        " ███ ██ ",
        " ██████ ",
        " ██ ███ ",
        " ██  ██ ",
        "        ",
        "        "
    ]),
    # Row 2 - "NINTENDO" text bottom half
    6: create_tile_from_pattern([
        "        ",
        " ██████ ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "        ",
        "        "
    ]),
    7: create_tile_from_pattern([
        "        ",
        " ██████ ",
        " ██     ",
        " █████  ",
        " ██     ",
        " ██████ ",
        "        ",
        "        "
    ]),
    8: create_tile_from_pattern([
        "        ",
        " ██  ██ ",
        " ███ ██ ",
        " ██████ ",
        " ██ ███ ",
        " ██  ██ ",
        "        ",
        "        "
    ]),
    # Row 3 - spacing
    9: create_tile_from_pattern(["        "] * 8),
    10: create_tile_from_pattern(["        "] * 8),
    11: create_tile_from_pattern(["        "] * 8),
}

# === Nintendo 64 ===
# "NINTENDO 64" with iconic 3D styling
n64_logo = {
    # Row 0 - "NINTENDO" top
    0: create_tile_from_pattern([
        " ██  ██ ",
        " ███ ██ ",
        " ██████ ",
        " ██ ███ ",
        " ██  ██ ",
        "        ",
        " ██████ ",
        "  ████  "
    ]),
    1: create_tile_from_pattern([
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "        ",
        "  ████  ",
        " ██  ██ "
    ]),
    2: create_tile_from_pattern([
        " ██  ██ ",
        " ███ ██ ",
        " ██████ ",
        " ██ ███ ",
        " ██  ██ ",
        "        ",
        " ██  ██ ",
        " ██  ██ "
    ]),
    # Row 1 - "64" top
    3: create_tile_from_pattern([
        "  ████  ",
        " ██  ██ ",
        " ██  ██ ",
        " ██  ██ ",
        " ██  ██ ",
        "        ",
        " ██  ██ ",
        " ██  ██ "
    ]),
    4: create_tile_from_pattern([
        "        ",
        "  ████  ",
        " ██  ██ ",
        " ██  ██ ",
        " ██  ██ ",
        " ██  ██ ",
        " ██  ██ ",
        "  ████  "
    ]),
    5: create_tile_from_pattern([
        "        ",
        " ██  ██ ",
        " ██  ██ ",
        " ██  ██ ",
        " ██████ ",
        "     ██ ",
        "     ██ ",
        "     ██ "
    ]),
    # Row 2-3 - spacing
    6: create_tile_from_pattern(["        "] * 8),
    7: create_tile_from_pattern(["        "] * 8),
    8: create_tile_from_pattern(["        "] * 8),
    9: create_tile_from_pattern(["        "] * 8),
    10: create_tile_from_pattern(["        "] * 8),
    11: create_tile_from_pattern(["        "] * 8),
}

# === GameCube ===
# Iconic cube "G" logo
gamecube_logo = {
    # Row 0 - Top of cube
    0: create_tile_from_pattern([
        "        ",
        "  ████  ",
        " ██  ██ ",
        "██    ██",
        "█  ██  █",
        "█  ██  █",
        "█      █",
        "█  ████"
    ]),
    1: create_tile_from_pattern([
        "        ",
        "  ████  ",
        " ██  ██ ",
        "██    ██",
        "        ",
        "        ",
        "        ",
        "        "
    ]),
    2: create_tile_from_pattern([
        "        ",
        "  ████  ",
        " ██  ██ ",
        "██    ██",
        "█      █",
        "█      █",
        "█      █",
        "  ████ █"
    ]),
    # Row 1 - Middle of cube with G
    3: create_tile_from_pattern([
        " █  ██ █",
        " █     █",
        " █     █",
        " ██   ██",
        "  █████ ",
        "        ",
        "        ",
        "        "
    ]),
    4: create_tile_from_pattern([
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        "
    ]),
    5: create_tile_from_pattern([
        " █      ",
        " █  ██ █",
        " █  ██ █",
        " ██  ██ ",
        "  ████  ",
        "        ",
        "        ",
        "        "
    ]),
    # Row 2-3 - spacing
    6: create_tile_from_pattern(["        "] * 8),
    7: create_tile_from_pattern(["        "] * 8),
    8: create_tile_from_pattern(["        "] * 8),
    9: create_tile_from_pattern(["        "] * 8),
    10: create_tile_from_pattern(["        "] * 8),
    11: create_tile_from_pattern(["        "] * 8),
}

# === Wii ===
# Simple "Wii" wordmark
wii_logo = {
    # Row 0-1 - "Wii" letters
    0: create_tile_from_pattern([
        "        ",
        "        ",
        " ██  ██ ",
        " ██  ██ ",
        " ██  ██ ",
        " ██  ██ ",
        "  ████  ",
        "        "
    ]),
    1: create_tile_from_pattern([
        "        ",
        "   ██   ",
        "        ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "        "
    ]),
    2: create_tile_from_pattern([
        "        ",
        "   ██   ",
        "        ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "        "
    ]),
    3: create_tile_from_pattern(["        "] * 8),
    4: create_tile_from_pattern(["        "] * 8),
    5: create_tile_from_pattern(["        "] * 8),
    6: create_tile_from_pattern(["        "] * 8),
    7: create_tile_from_pattern(["        "] * 8),
    8: create_tile_from_pattern(["        "] * 8),
    9: create_tile_from_pattern(["        "] * 8),
    10: create_tile_from_pattern(["        "] * 8),
    11: create_tile_from_pattern(["        "] * 8),
}

print("Logo CHR data generator ready. Creating detailed implementations...")
