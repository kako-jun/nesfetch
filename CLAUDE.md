# nesfetch 開発者向けドキュメント

NESエミュレータで動作するneofetch風ゲーム機ロゴ表示ROM。CC65 + C言語。

## コンセプト

- 29種類のゲーム機ロゴをNES上で表示
- neofetchのようなメニューベースのUI
- 公式ロゴに忠実なドット絵（24×32px、4色）

## プロジェクト構造

```
nesfetch/
├── src/
│   ├── main.c       # メインプログラム
│   ├── header.s     # iNESヘッダー
│   └── reset.s      # リセットベクタ
├── tools/
│   └── create_chr.py  # CHRデータ生成
├── assets/
│   ├── logos/       # 元画像
│   └── processed/   # 処理済み画像
├── nes.cfg          # リンカー設定
├── Makefile
└── Dockerfile
```

## メモリマップ

| アドレス | サイズ | 内容 |
|---------|--------|------|
| $0000-$07FF | 2KB | RAM |
| $2000-$2007 | 8B | PPUレジスタ |
| $4016 | 1B | コントローラー |
| $8000-$FFFF | 32KB | PRG-ROM |

## CHR-ROMレイアウト

```
タイルID 0x00-0x3F: フォント（64タイル）
タイルID 0x40-0x1FF: ロゴ（29ロゴ × 12タイル = 348タイル）
合計: 412 / 512タイル（80.5%使用）
```

## ロゴタイル配置（3×4 = 12タイル）

```
[0] [1] [2]   ← Row 0
[3] [4] [5]   ← Row 1
[6] [7] [8]   ← Row 2
[9][10][11]   ← Row 3

base_tile = 0x40 + (logo_index * 12)
```

## PPU描画

```c
// VBlank待機
void wait_vblank(void) {
    while ((PPU_STATUS & 0x80) == 0);
}

// PPUアドレス設定
void set_ppu_addr(unsigned int addr) {
    PPU_ADDR = (unsigned char)(addr >> 8);
    PPU_ADDR = (unsigned char)(addr & 0xFF);
}
```

## コントローラー読み取り

```c
#define BTN_A      0x01
#define BTN_B      0x02
#define BTN_UP     0x10
#define BTN_DOWN   0x20

unsigned char read_controller(void) {
    unsigned char i, buttons = 0;
    CONTROLLER1 = 1;
    CONTROLLER1 = 0;
    for (i = 0; i < 8; i++) {
        buttons = (buttons >> 1) | ((CONTROLLER1 & 0x01) << 7);
    }
    return buttons;
}
```

## 状態管理

```c
unsigned char current_logo = 0;   // 選択中のロゴ (0-28)
unsigned char menu_scroll = 0;    // スクロール位置
unsigned char game_state = 0;     // 0=メニュー, 1=ロゴ表示
```

## メニューシステム

- 1ページ10項目表示
- 選択位置に応じて自動スクロール
- ページインジケーター表示（例: "01/29"）
- 上下矢印でスクロール可能を示す

## パレット

```c
const unsigned char palette[32] = {
    // 背景パレット
    0x0F, 0x00, 0x10, 0x30,  // パレット0
    0x0F, 0x16, 0x27, 0x37,  // パレット1
    0x0F, 0x1A, 0x2A, 0x3A,  // パレット2
    0x0F, 0x12, 0x22, 0x32,  // パレット3
    // スプライトパレット（未使用）
    ...
};
```

## ビルドフロー

```
元画像 → ImageMagick処理 → CHRデータ生成 → ROMビルド
  ↓           ↓                ↓              ↓
SVG/PNG    24x32 4色      chr.bin (8KB)  nesfetch.nes
```

## ビルドコマンド

```bash
make          # ビルド
make clean    # クリーンアップ
```

## NESタイル形式

```
各タイル = 16バイト
  Byte 0-7:  Plane 0 (下位ビット)
  Byte 8-15: Plane 1 (上位ビット)

ピクセル色 = (Plane1 bit << 1) | (Plane0 bit)
  00 = 色0（透明/黒）
  01 = 色1
  10 = 色2
  11 = 色3
```

## 画像処理（ImageMagick）

```bash
convert input.svg \
  -background white \
  -flatten \
  -resize 24x32! \
  -colorspace Gray \
  -depth 2 \
  -colors 4 \
  output.png
```

## 対応ロゴ一覧（29種）

| カテゴリ | ロゴ |
|---------|------|
| Nintendo | NES, SNES, N64, GameCube, Wii, Wii U, Switch, Game Boy, GBA, DS, 3DS |
| PlayStation | PS1, PS2, PS3, PS4, PS5, PS Vita |
| SEGA | Genesis, Saturn, Dreamcast |
| Xbox | Xbox, 360, One, Series X/S |
| その他 | Atari, PC Engine, Neo Geo, Steam Deck, WonderSwan |

## 制約

- CHR-ROM: 8KB（512タイル）
- 色数: 1パレット4色（モノクロ表現）
- 解像度: 24×32ピクセル/ロゴ
- リアルタイム: 60fps

## 拡張予定

- 公式ロゴ画像からの自動変換パイプライン
- カラーパレット対応（ロゴごとに異なる色）
- サウンド効果
