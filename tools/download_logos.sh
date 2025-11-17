#!/bin/bash
# Download official console logos from Wikimedia Commons

cd "$(dirname "$0")/../assets/logos" || exit 1

# Nintendo consoles
curl -L "https://upload.wikimedia.org/wikipedia/commons/5/5f/NES_logo.svg" -o nes.svg
curl -L "https://upload.wikimedia.org/wikipedia/commons/d/d0/SNES_logo.svg" -o snes.svg
curl -L "https://upload.wikimedia.org/wikipedia/commons/0/05/Nintendo_64_wordmark.svg" -o n64.svg
curl -L "https://upload.wikimedia.org/wikipedia/commons/d/d1/Nintendo_GameCube_Official_Logo.svg" -o gamecube.svg
curl -L "https://upload.wikimedia.org/wikipedia/commons/1/12/Wii.svg" -o wii.svg
curl -L "https://upload.wikimedia.org/wikipedia/commons/6/65/WiiU.svg" -o wiiu.svg
curl -L "https://upload.wikimedia.org/wikipedia/commons/7/74/Nintendo_Game_Boy_Logo.svg" -o gameboy.svg
curl -L "https://upload.wikimedia.org/wikipedia/commons/7/7e/Gameboy_advance_logo.svg" -o gba.svg

# PlayStation consoles
curl -L "https://upload.wikimedia.org/wikipedia/commons/4/4e/Playstation_logo_colour.svg" -o playstation.svg
curl -L "https://upload.wikimedia.org/wikipedia/commons/7/73/PlayStation_5_logo_and_wordmark.svg" -o ps5.svg

# Xbox consoles
curl -L "https://upload.wikimedia.org/wikipedia/commons/d/d7/XBOX_logo_2012.svg" -o xbox.svg
curl -L "https://upload.wikimedia.org/wikipedia/commons/8/8c/Xbox_one_logo.svg" -o xboxone.svg
curl -L "https://upload.wikimedia.org/wikipedia/commons/0/00/Xbox_Series_X_logo.svg" -o xboxseriesx.svg

# Sega consoles
curl -L "https://upload.wikimedia.org/wikipedia/commons/3/3d/Dreamcast_logo.svg" -o dreamcast.svg

echo "Logo download complete"
