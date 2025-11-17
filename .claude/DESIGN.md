# 技術設計書

## アーキテクチャ

### ファイル構成

```
nesfetch/
├── src/
│   ├── main.c          # メインプログラム（C言語）
│   ├── header.s        # iNESヘッダー（アセンブリ）
│   └── reset.s         # リセットベクタ（アセンブリ）
├── tools/
│   ├── create_chr.py            # CHR-ROM生成（現在：手動デザイン）
│   ├── download_logos.sh        # ロゴダウンロードスクリプト
│   ├── process_logos.sh         # ImageMagick画像処理
│   ├── images_to_chr.py         # 画像→CHRデータ変換
│   └── create_chr_from_logos.py # 新バージョン（未完成）
├── assets/
│   ├── logos/          # 元画像（SVG/PNG）
│   └── processed/      # 処理済み画像（24×32 PNG）
├── nes.cfg             # リンカー設定
├── Makefile            # ビルドシステム
└── .github/workflows/  # CI/CD設定
```

### ビルドフロー

```
元画像 → ImageMagick処理 → CHRデータ生成 → ROMビルド
  ↓           ↓                ↓              ↓
SVG/PNG    24x32 4色      chr.bin (8KB)  nesfetch.nes
```

## NES技術仕様

### メモリマップ

| アドレス | サイズ | 内容 |
|---------|--------|------|
| $0000-$07FF | 2KB | RAM |
| $2000-$2007 | 8B | PPUレジスタ |
| $4016 | 1B | コントローラー1 |
| $8000-$FFFF | 32KB | PRG-ROM |

### CHR-ROMレイアウト

```
タイルID 用途
-------------------------------------
$00-$3F   フォント (64タイル)
$40-$1FF  ロゴタイル (29ロゴ × 12タイル = 348タイル)

合計: 64 + 348 = 412タイル (< 512タイル上限)
```

### ロゴタイルレイアウト（3×4タイル = 24×32ピクセル）

```
各ロゴは12タイルで構成:
[0] [1] [2]   ← Row 0
[3] [4] [5]   ← Row 1
[6] [7] [8]   ← Row 2
[9][10][11]   ← Row 3

タイルID計算式:
  base_tile = 0x40 + (logo_index * 12)
  tile_at(row, col) = base_tile + (row * 3) + col
```

### PPU描画シーケンス

```c
// VBlank待機
wait_vblank();

// PPUアドレス設定
PPU_ADDR = 0x20;  // ネームテーブル上位
PPU_ADDR = offset; // オフセット下位

// タイル書き込み
for (row = 0; row < 4; row++) {
    for (col = 0; col < 3; col++) {
        PPU_DATA = tile_id;
    }
}

// 描画有効化
PPU_CTRL = 0x80;
PPU_MASK = 0x1E;
```

## 画像処理パイプライン

### Step 1: 公式ロゴ取得

**ソース候補:**
- Wikimedia Commons
- 公式プレスキット
- ブランドガイドライン

**形式:**
- SVG（ベクター、推奨）
- PNG（透過背景）
- JPG（非推奨、背景処理が必要）

### Step 2: ImageMagick処理

```bash
convert input.svg \
  -background white \      # 透過部分を白に
  -flatten \               # レイヤー統合
  -resize 24x32! \         # 24×32に強制リサイズ
  -colorspace Gray \       # グレースケール化
  -depth 2 \               # 2ビット色深度（4色）
  -colors 4 \              # 4色に減色
  -type Grayscale \        # グレースケールタイプ
  output.png
```

**出力:**
- サイズ: 24×32ピクセル
- 色数: 4色（2ビット）
- 形式: グレースケールPNG

### Step 3: PNG → CHR変換

```python
# 画像読み込み（PIL）
img = Image.open("logo.png").convert('L')

# 8×8タイルに分割（3×4 = 12タイル）
for tile_row in range(4):
    for tile_col in range(3):
        # タイル抽出
        tile = extract_tile(img, tile_col * 8, tile_row * 8)

        # NES形式に変換（16バイト/タイル）
        chr_data = convert_to_nes_format(tile)
```

**NESタイル形式:**
```
各タイル = 16バイト
  Byte 0-7:  Plane 0 (下位ビット)
  Byte 8-15: Plane 1 (上位ビット)

ピクセル色 = (Plane1 bit << 1) | (Plane0 bit)
  00 = 色0（透明/黒）
  01 = 色1（濃いグレー）
  10 = 色2（薄いグレー）
  11 = 色3（白）
```

## コントローラー入力

### ハードウェア仕様

```
$4016書き込み: 1 → 0 でラッチ
$4016読み込み: ボタン状態（1ビット/読み込み）

読み込み順序:
1. A
2. B
3. Select
4. Start
5. Up
6. Down
7. Left
8. Right
```

### 実装

```c
#define BUTTON_A      0x01
#define BUTTON_B      0x02
#define BUTTON_UP     0x10
#define BUTTON_DOWN   0x20

unsigned char read_controller() {
    unsigned char i, result = 0;

    *((unsigned char*)0x4016) = 1;  // ラッチ
    *((unsigned char*)0x4016) = 0;  // 読み込み開始

    for (i = 0; i < 8; i++) {
        result <<= 1;
        result |= (*((unsigned char*)0x4016) & 1);
    }

    return result;
}
```

## メニューシステム

### 状態管理

```c
// グローバル変数
unsigned char selected_logo = 0;   // 選択中のロゴ (0-28)
unsigned char scroll_pos = 0;      // スクロール位置
unsigned char current_state = 0;   // 0=メニュー, 1=ロゴ表示
unsigned char prev_buttons = 0;    // 前フレームのボタン状態
```

### スクロールアルゴリズム

```c
#define ITEMS_PER_PAGE 10

// 選択位置がスクロール範囲外なら調整
if (selected_logo < scroll_pos) {
    scroll_pos = selected_logo;
}
if (selected_logo >= scroll_pos + ITEMS_PER_PAGE) {
    scroll_pos = selected_logo - ITEMS_PER_PAGE + 1;
}
```

### 表示更新

```c
// メニュー再描画
for (i = 0; i < ITEMS_PER_PAGE; i++) {
    logo_index = scroll_pos + i;
    if (logo_index >= total_logos) break;

    // カーソル表示
    if (logo_index == selected_logo) {
        draw_text("> ");
    }

    // ロゴ名表示
    draw_text(logo_names[logo_index]);
}

// ページ番号表示
current_page = selected_logo / ITEMS_PER_PAGE + 1;
total_pages = (total_logos + ITEMS_PER_PAGE - 1) / ITEMS_PER_PAGE;
draw_text("Page X/Y");
```

## パフォーマンス最適化

### VBlank同期

```c
// VBlank待機（1フレーム = 約16.7ms）
void wait_vblank() {
    while (!(PPU_STATUS & 0x80));  // VBlankフラグ待機
}
```

### 差分更新

- メニュー: カーソル移動時のみ再描画
- ロゴ: 表示切替時のみ再描画
- 不要なPPU書き込みを最小化

## ビルドシステム

### Makefile主要ターゲット

```makefile
all: nesfetch.nes

chr.bin: tools/create_chr.py
    python3 tools/create_chr.py

nesfetch.nes: src/*.c src/*.s chr.bin
    cc65 -Oi -t nes -o src/main.s src/main.c
    ca65 -t nes -o src/main.o src/main.s
    ld65 -C nes.cfg -o nesfetch.nes src/*.o
    cat chr.bin >> nesfetch.nes

clean:
    rm -f src/*.s src/*.o nesfetch.nes chr.bin
```

### CI/CD (GitHub Actions)

```yaml
- name: Install CC65
  run: |
    wget https://github.com/cc65/cc65/archive/V2.19.tar.gz
    tar xzf V2.19.tar.gz && cd cc65-2.19
    make && sudo make install

- name: Build ROM
  run: make

- name: Upload Artifact
  uses: actions/upload-artifact@v2
  with:
    name: nesfetch.nes
    path: nesfetch.nes
```

## デバッグ

### エミュレータ推奨

- **FCEUX**: デバッグ機能、メモリビューア
- **Mesen**: 高精度、詳細なデバッガ
- **Nintaco**: クロスプラットフォーム

### デバッグ戦略

1. タイルビューアでCHRデータ確認
2. ネームテーブルビューアで配置確認
3. PPU/CPUレジスタ監視
4. ブレークポイント設定

## 既知の制約

1. **CHR-ROM容量**: 8KB (512タイル)
   - フォント: 64タイル
   - ロゴ: 348タイル
   - 残り: 100タイル

2. **色数制限**: 1パレット = 4色
   - ロゴはモノクロ表現

3. **解像度**: 24×32ピクセル/ロゴ
   - 詳細な表現には限界

4. **リアルタイム処理**: 60fps
   - 複雑な処理は困難
