# NESfetch

NESエミュレータで動くneofetch風システム情報表示プログラム

## 機能

- neofetch風のロゴ表示（Linux、PlayStation、Apple、Windows、NESなど）
- 十字キーでメニュー選択
- Aボタンでロゴ切り替え

## ダウンロード

最新のROMファイルは[Releases](https://github.com/kako-jun/nesfetch/releases)ページからダウンロードできます。

## ビルド方法

### 方法1: Dockerを使用（推奨）

```bash
# Dockerイメージをビルド
docker build -t nesfetch .

# ROMをビルド
docker run --rm -v $(pwd):/workspace nesfetch

# または docker-compose を使用
docker-compose up
```

### 方法2: ローカル環境

CC65が必要です：

```bash
# CC65をソースからビルド
cd /tmp
wget https://github.com/cc65/cc65/archive/refs/tags/V2.19.tar.gz
tar xzf V2.19.tar.gz
cd cc65-2.19
make
sudo make install PREFIX=/usr/local

# nesfetchをビルド
cd /path/to/nesfetch
make
```

### 方法3: GitHub Actions

このリポジトリをGitHubにプッシュすると、GitHub Actionsが自動的にビルドします。
ビルドされたROMは「Actions」タブの「Artifacts」からダウンロードできます。

## 実行方法

生成された `nesfetch.nes` を以下のNESエミュレータで実行してください：

- **FCEUX** (推奨) - Windows/Linux/Mac
- **Nestopia** - Windows/Mac
- **Mesen** - Windows/Linux
- **RetroArch** - マルチプラットフォーム

## 操作方法

- **十字キー上下**: メニュー選択
- **Aボタン**: 選択したロゴを表示
- **Bボタン**: メニューに戻る

## 対応ロゴ（20種類）

### 任天堂
1. NES/ファミコン
2. Super Nintendo/スーパーファミコン
3. Nintendo 64
4. GameCube
5. Wii
6. Game Boy
7. Game Boy Advance
8. Nintendo DS

### Sony PlayStation
9. PlayStation 1
10. PlayStation 2
11. PlayStation 3
12. PlayStation 4

### SEGA
13. Genesis/Mega Drive
14. Saturn
15. Dreamcast

### その他
16. Xbox
17. Xbox 360
18. Atari 2600
19. PC Engine/TurboGrafx-16
20. Neo Geo

## プロジェクト構成

```
nesfetch/
├── src/
│   ├── main.c         # メインプログラム
│   ├── header.s       # iNESヘッダー
│   └── reset.s        # リセット/初期化コード
├── tools/
│   └── create_chr.py  # CHRデータ生成ツール
├── Makefile           # ビルド設定
├── nes.cfg            # リンカー設定
├── Dockerfile         # Docker設定
└── docker-compose.yml
```

## 開発環境

- **CC65**: NES用Cコンパイラ
- **Python 3**: CHRデータ生成スクリプト用
- **NESエミュレータ**: FCEUX、Nestopiaなど推奨

## ライセンス

MIT License

## 技術情報

- **ROM形式**: iNES (Mapper 0)
- **PRG-ROM**: 32KB (2 x 16KB)
- **CHR-ROM**: 8KB
- **ミラーリング**: Vertical
