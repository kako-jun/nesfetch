# nesfetch

NESエミュレータで動作するneofetch風ゲーム機ロゴ表示ROM

## 機能

- 29種類のゲーム機ロゴを表示
- スクロール対応メニュー
- 十字キーで選択、Aボタンで表示、Bボタンで戻る

## 対応ロゴ

**Nintendo (11種)**: NES, SNES, N64, GameCube, Wii, Wii U, Switch, Game Boy, GBA, DS, 3DS

**PlayStation (7種)**: PS1〜PS5, PS Vita

**SEGA (3種)**: Genesis, Saturn, Dreamcast

**Xbox (4種)**: Xbox, 360, One, Series X/S

**その他 (4種)**: Atari, PC Engine, Neo Geo, Steam Deck, WonderSwan

## ビルド

### Docker（推奨）

```bash
docker build -t nesfetch .
docker run --rm -v $(pwd):/workspace nesfetch
```

### ローカル

```bash
# CC65が必要
make
```

## 実行

`nesfetch.nes` を以下のエミュレータで実行:

- [FCEUX](https://fceux.com/) (推奨)
- [Mesen](https://www.mesen.ca/)
- [Nestopia](http://nestopia.sourceforge.net/)

## 操作

- **十字キー上下**: メニュー選択
- **Aボタン**: ロゴ表示
- **Bボタン**: メニューに戻る

## 技術仕様

- **ROM形式**: iNES (Mapper 0)
- **PRG-ROM**: 32KB
- **CHR-ROM**: 8KB
- **ロゴサイズ**: 24×32ピクセル（3×4タイル）

## ライセンス

MIT
