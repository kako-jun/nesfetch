# Console Logo Assets

このディレクトリに各コンソールの公式ロゴ画像を配置してください。

## 必要なファイル (29個)

以下の名前でロゴ画像を配置してください（PNG、SVG、JPEGに対応）：

### Nintendo
- `nes.png` または `nes.svg` - Nintendo Entertainment System
- `snes.png` - Super Nintendo Entertainment System
- `n64.png` - Nintendo 64
- `gamecube.png` - GameCube
- `wii.png` - Wii
- `wiiu.png` - Wii U
- `switch.png` - Nintendo Switch
- `gameboy.png` - Game Boy
- `gba.png` - Game Boy Advance
- `ds.png` - Nintendo DS
- `3ds.png` - Nintendo 3DS

### PlayStation
- `playstation.png` - PlayStation / PS1
- `ps2.png` - PlayStation 2
- `ps3.png` - PlayStation 3
- `ps4.png` - PlayStation 4
- `ps5.png` - PlayStation 5
- `psvita.png` - PlayStation Vita

### Sega
- `genesis.png` - Sega Genesis / Mega Drive
- `saturn.png` - Sega Saturn
- `dreamcast.png` - Dreamcast

### Xbox
- `xbox.png` - Xbox
- `xbox360.png` - Xbox 360
- `xboxone.png` - Xbox One
- `xboxseriesx.png` - Xbox Series X/S

### その他
- `atari.png` - Atari
- `pcengine.png` - PC Engine / TurboGrafx-16
- `neogeo.png` - Neo Geo
- `steamdeck.png` - Steam Deck
- `wonderswan.png` - WonderSwan

## 画像配置後の手順

1. **画像を処理** (24x32ピクセル、4色に変換):
   ```bash
   ./tools/process_logos.sh
   ```

2. **CHRデータを生成**:
   ```bash
   ./tools/images_to_chr.py > chr_data.txt
   ```

3. **生成されたデータを`tools/create_chr.py`に統合**

4. **ROMをビルド**:
   ```bash
   make clean && make
   ```

## 推奨される画像ソース

- Wikimedia Commons (https://commons.wikimedia.org/)
- 各コンソールメーカーの公式プレスキット
- 高解像度の公式ロゴ画像

## 注意事項

- 背景が透明なPNGまたはSVGが推奨
- 可能な限り公式ロゴを使用
- ロゴの色は自動的に4色グレースケールに変換されます
