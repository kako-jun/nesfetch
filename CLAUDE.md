# nesfetch 開発者向けドキュメント

NES で動作する neofetch 風ゲーム機ロゴビューア。CC65 v2.19 + C言語 + 6502アセンブリ。

## プロジェクト構造

```
nesfetch/
├── src/
│   ├── main.c       # メインプログラム（PPU制御、直接切替UI、入力）
│   ├── header.s     # iNESヘッダー（Mapper 0、PRG 32KB、CHR 8KB）
│   └── reset.s      # 6502ブートストラップ（RAM初期化、NMIハンドラ）
├── tools/
│   └── create_chr.py  # CHR-ROM生成（フォント＋16ロゴ[PT0] / 13ロゴ[PT1準備済]）
├── nes.cfg          # CC65リンカー設定
├── Makefile
├── Dockerfile
└── docs/            # 仕様書
```

## ビルド

```bash
make          # CHR生成 → コンパイル → リンク → nesfetch.nes
make clean    # クリーンアップ
```

## UI仕様

- メニュー画面は廃止。起動直後からロゴ表示
- 上下キーで直接ロゴを切替（A/Bボタン不要）
- 先頭↔末尾でラップアラウンド（循環）
- ページ番号「NN」を表示（現在位置のみ）
- ナビゲーション矢印（▲▼）は常時表示
- フリッカー低減：2回目以降の描画は変更行のみクリア

## ロゴ収録状況

- **PT0（有効・16種）**: NES, SNES, N64, GameCube, Wii, Wii U, Switch, Game Boy, GBA, NDS, 3DS, PS1, PS2, PS3, PS4, PS5
- **PT1（create_chr.py準備済・main.c未対応・13種）**: PSVita, Genesis, Saturn, Dreamcast, Xbox, Xbox360, XboxOne, XSX, Atari, PCEngine, NeoGeo, SteamDeck, WonderSwan

## 技術メモ

### NMI/VBlank同期
- NMIハンドラが `nmi_ready` フラグをセット
- `wait_vblank()` はNMI有効時にフラグベースで待機（ポーリングとのレース回避）
- 描画更新はVBlank中にPPU_MASK=0で安全に実行

### ネームテーブル
- $2000-$23BF: タイルマップ（32×30 = 960バイト）
- $23C0-$23FF: 属性テーブル（64バイト、2×2タイル単位のパレット選択）
- `clear_screen()` は属性テーブル含む1024バイトをクリア

### CHR-ROMレイアウト
- 0x00-0x3F: フォント（A-Z, 0-9, 記号）
- 0x40+: ロゴデータ（PT0: 16ロゴ × 12タイル = 192タイル）
- PT1用にcreate_chr.pyで13ロゴ分のデータ生成済み（main.c側の切替未実装）

### タイル番号とASCIIの対応
- A=0x21, B=0x22, ..., Z=0x3A
- 0=0x10, 1=0x11, ..., 9=0x19
- 記号: ':'=0x3B, '-'=0x3C, '>'=0x3D, '▲'=0x3E

### ページ番号表示
- 十の位: `value / 10 + 0x10`（0x10が"0"タイル）
- 一の位: `value % 10 + 0x10`
