# nesfetch

neofetch にインスパイアされた、実際の NES で動作するゲーム機ロゴビューア。29種類のゲーム機のドット絵ロゴをNESコントローラーで閲覧できる。

## スクリーンショット

> ビルド後に Mesen や FCEUX で実行。メニュー画面でロゴを選択し、24×32ピクセルのドット絵を表示。

## 収録ロゴ（29種）

| メーカー | 機種 |
|---|---|
| **Nintendo** (11) | NES, SNES, N64, GameCube, Wii, Wii U, Switch, Game Boy, GBA, DS, 3DS |
| **PlayStation** (7) | PS1, PS2, PS3, PS4, PS5, PS Vita |
| **SEGA** (3) | Genesis, Saturn, Dreamcast |
| **Xbox** (4) | Xbox, Xbox 360, Xbox One, Xbox Series X/S |
| **その他** (4) | Atari, PC Engine, Neo Geo, Steam Deck, WonderSwan |

## 操作方法

| 操作 | 機能 |
|------|------|
| 十字キー上下 | メニュー選択（スクロール対応） |
| Aボタン | 選択中のロゴを表示 |
| Bボタン | メニューに戻る |

メニューは10項目ずつ表示。ページ番号が画面下部に表示される。

## ビルド

[CC65](https://cc65.github.io/cc65/) v2.19 以上が必要。

### Docker ビルド（推奨）

```bash
docker build -t nesfetch .
docker run --rm -v $(pwd):/workspace nesfetch
```

### ローカルビルド

```bash
# CC65 をインストール後
make
```

CHR-ROM（フォント＋ロゴのタイルデータ）は `tools/create_chr.py` で自動生成される。

## 動作確認済みエミュレータ

| エミュレータ | 精度 | 推奨度 |
|---|---|---|
| [Mesen](https://www.mesen.ca/) | 高精度 | ★★★ |
| [FCEUX](https://fceux.com/) | 標準 | ★★☆ |
| [Nestopia](http://nestopia.sourceforge.net/) | 標準 | ★★☆ |

実機の場合は EverDrive-N8 等のフラッシュカートリッジで動作。

## 技術仕様

- **ROM形式**: iNES (Mapper 0 / NROM)
- **PRG-ROM**: 32KB (2バンク)
- **CHR-ROM**: 8KB (1バンク)
- **ミラーリング**: 垂直
- **コントローラー**: 標準NESパッド（1P）
- **ロゴサイズ**: 24×32ピクセル（3×4タイル、4色パレット）
- **フォント**: カスタム8×8ピクセルフォント（A-Z, 0-9, 記号）
- **開発言語**: C (CC65) + 6502アセンブリ

## CI/CD

- **build.yml**: プッシュ時に自動ビルド、ROMをArtifactsにアップロード
- **release.yml**: タグ付きプッシュでGitHub Releaseを作成

## ライセンス

MIT
