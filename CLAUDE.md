# nesfetch 開発者向けドキュメント

NES で動作する neofetch 風ゲーム機ロゴビューア。CC65 v2.19 + C言語 + 6502アセンブリ。

## プロジェクト構造

```
nesfetch/
├── src/
│   ├── main.c       # メインプログラム（PPU制御、メニュー、入力）
│   ├── header.s     # iNESヘッダー（Mapper 0、PRG 32KB、CHR 8KB）
│   └── reset.s      # 6502ブートストラップ（RAM初期化、NMIハンドラ）
├── tools/
│   └── create_chr.py  # CHR-ROM生成（フォント＋29ロゴ）
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
- 0x40+: ロゴデータ（29ロゴ × 12タイル = 348タイル）
- 合計412 / 512タイル使用（80.5%）

### タイル番号とASCIIの対応
- A=0x21, B=0x22, ..., Z=0x3A
- 0=0x10, 1=0x11, ..., 9=0x19
- 記号: ':'=0x3B, '-'=0x3C, '>'=0x3D, '▲'=0x3E

### ページ番号表示
- 十の位: `value / 10 + 0x10`（0x10が"0"タイル）
- 一の位: `value % 10 + 0x10`
