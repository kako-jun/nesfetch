#!/usr/bin/env python3
"""
Convert processed logo images (24x32 PNG) to NES CHR tile data
Reads from assets/processed/ and generates CHR data for create_chr.py
"""

import os
from PIL import Image

PROCESSED_DIR = "assets/processed"

# Logo order matching main.c
LOGO_ORDER = [
    "nes", "snes", "n64", "gamecube", "wii", "wiiu", "switch",
    "gameboy", "gba", "ds", "3ds",
    "playstation", "ps2", "ps3", "ps4", "ps5", "psvita",
    "genesis", "saturn", "dreamcast",
    "xbox", "xbox360", "xboxone", "xboxseriesx",
    "atari", "pcengine", "neogeo", "steamdeck", "wonderswan"
]


def image_to_tiles(img_path):
    """Convert 24x32 image to NES tile format (12 tiles in 3x4 grid)"""
    img = Image.open(img_path).convert('L')  # Convert to grayscale

    if img.size != (24, 32):
        print(f"Warning: {img_path} is {img.size}, expected (24, 32)")
        img = img.resize((24, 32), Image.NEAREST)

    tiles = []

    # Process 4 rows of 3 tiles each
    for tile_row in range(4):
        for tile_col in range(3):
            # Extract 8x8 tile
            tile_x = tile_col * 8
            tile_y = tile_row * 8

            plane0 = []
            plane1 = []

            for y in range(8):
                byte0 = 0
                byte1 = 0

                for x in range(8):
                    pixel = img.getpixel((tile_x + x, tile_y + y))

                    # Convert grayscale to 2-bit value
                    # 0-63 = color 0 (transparent/black)
                    # 64-127 = color 1 (dark gray)
                    # 128-191 = color 2 (light gray)
                    # 192-255 = color 3 (white)
                    if pixel >= 192:
                        color = 3
                    elif pixel >= 128:
                        color = 2
                    elif pixel >= 64:
                        color = 1
                    else:
                        color = 0

                    # Set bits in plane0 and plane1
                    if color & 1:
                        byte0 |= (1 << (7 - x))
                    if color & 2:
                        byte1 |= (1 << (7 - x))

                plane0.append(byte0)
                plane1.append(byte1)

            # NES tile format: 8 bytes plane0, 8 bytes plane1
            tiles.append(plane0 + plane1)

    return tiles


def generate_chr_code():
    """Generate Python code for create_chr.py with all logo data"""

    print("Generating CHR data from processed images...")
    print()

    all_logos_data = {}

    for idx, logo_name in enumerate(LOGO_ORDER):
        img_path = os.path.join(PROCESSED_DIR, f"{logo_name}.png")

        if not os.path.exists(img_path):
            print(f"Warning: Missing {img_path}, using blank tiles")
            tiles = [[0] * 16 for _ in range(12)]
        else:
            print(f"Processing {logo_name}...")
            tiles = image_to_tiles(img_path)

        all_logos_data[logo_name] = tiles

    print()
    print("=" * 60)
    print("Copy the following code into create_chr.py:")
    print("=" * 60)
    print()

    # Generate Python dictionary code
    for logo_name, tiles in all_logos_data.items():
        print(f"{logo_name}_logo = [")
        for tile_idx, tile_data in enumerate(tiles):
            # Format as hex bytes
            hex_bytes = ", ".join(f"0x{b:02X}" for b in tile_data)
            print(f"    [{hex_bytes}],  # Tile {tile_idx}")
        print("]")
        print()

    # Generate all_logos list
    print("all_logos = [")
    for logo_name in LOGO_ORDER:
        print(f"    {logo_name}_logo,")
    print("]")


if __name__ == "__main__":
    if not os.path.exists(PROCESSED_DIR):
        print(f"Error: {PROCESSED_DIR} directory not found")
        print("Please run process_logos.sh first")
        exit(1)

    generate_chr_code()
