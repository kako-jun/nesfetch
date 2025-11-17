#!/bin/bash
# Process logo images with ImageMagick
# Converts logos to 24x32 pixel, 2-bit grayscale for NES CHR conversion

set -e

LOGO_DIR="assets/logos"
PROCESSED_DIR="assets/processed"

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "ImageMagick is not installed. Installing..."
    apt-get update && apt-get install -y imagemagick
fi

mkdir -p "$PROCESSED_DIR"

# Process each logo file
for logo in "$LOGO_DIR"/*.{svg,png,jpg,jpeg}; do
    if [ ! -f "$logo" ]; then
        continue
    fi

    filename=$(basename "$logo")
    name="${filename%.*}"
    output="$PROCESSED_DIR/${name}.png"

    echo "Processing $filename -> ${name}.png"

    # Convert to 24x32 pixels, 2-bit grayscale (4 colors for NES)
    # -background none: preserve transparency
    # -flatten: composite onto white background
    # -resize 24x32: scale to NES tile size (3x4 tiles)
    # -depth 2: reduce to 2-bit color depth (4 colors)
    # -colors 4: limit to 4 colors
    # -type Grayscale: convert to grayscale
    convert "$logo" \
        -background white \
        -flatten \
        -resize 24x32\! \
        -colorspace Gray \
        -depth 2 \
        -colors 4 \
        -type Grayscale \
        "$output"

    echo "  Created: $output"
done

echo ""
echo "Logo processing complete!"
echo "Processed images are in: $PROCESSED_DIR"
