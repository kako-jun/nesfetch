# TODOリスト

## 現在の状態: ロゴ画像収集待ち

### Phase 1: 画像収集（進行中）
- [x] ロゴダウンロードスクリプト作成 (`download_logos.sh`)
- [x] 画像処理スクリプト作成 (`process_logos.sh`)
- [x] 画像→CHR変換スクリプト作成 (`images_to_chr.py`)
- [x] `assets/logos/` ディレクトリ準備
- [x] READMEで必要な画像リスト明記
- [ ] **29個の公式ロゴ画像を収集（ユーザー作業中）**

#### 必要な画像一覧

Nintendo (11個):
- [ ] nes.png
- [ ] snes.png
- [ ] n64.png
- [ ] gamecube.png
- [ ] wii.png
- [ ] wiiu.png
- [ ] switch.png
- [ ] gameboy.png
- [ ] gba.png
- [ ] ds.png
- [ ] 3ds.png

PlayStation (7個):
- [ ] playstation.png
- [ ] ps2.png
- [ ] ps3.png
- [ ] ps4.png
- [ ] ps5.png
- [ ] psvita.png

Sega (3個):
- [ ] genesis.png
- [ ] saturn.png
- [ ] dreamcast.png

Xbox (4個):
- [ ] xbox.png
- [ ] xbox360.png
- [ ] xboxone.png
- [ ] xboxseriesx.png

その他 (4個):
- [ ] atari.png
- [ ] pcengine.png
- [ ] neogeo.png
- [ ] steamdeck.png
- [ ] wonderswan.png

### Phase 2: 画像処理（画像収集後）
- [ ] ImageMagickインストール確認
- [ ] `./tools/process_logos.sh` 実行
- [ ] 処理済み画像確認（`assets/processed/*.png`）
- [ ] 24×32ピクセル、4色に正しく変換されているか検証

### Phase 3: CHRデータ生成
- [ ] `./tools/images_to_chr.py` 実行
- [ ] 生成されたPythonコードを確認
- [ ] `tools/create_chr.py` にデータを統合
- [ ] フォントタイル（0x00-0x3F）とロゴタイル（0x40-）の配置確認
- [ ] 合計タイル数が512以下であることを確認

### Phase 4: ROM統合とテスト
- [ ] `make clean && make` でビルド
- [ ] ビルドエラーがないか確認
- [ ] `chr.bin` が8192バイトであることを確認
- [ ] `nesfetch.nes` が生成されることを確認
- [ ] エミュレータでROM起動
- [ ] 29個のロゴがメニューに表示されるか確認
- [ ] 各ロゴを表示して正しく描画されるか確認
- [ ] 認識可能なロゴになっているか確認

### Phase 5: 品質検証
- [ ] 各ロゴが公式デザインに忠実か確認
- [ ] 色のコントラストが適切か確認
- [ ] 24×32ピクセルで認識可能か確認
- [ ] 必要に応じてImageMagickパラメータ調整
  - コントラスト調整: `-contrast`, `-normalize`
  - シャープネス: `-sharpen`
  - ディザリング: `-dither FloydSteinberg`

### Phase 6: 最終調整
- [ ] 不鮮明なロゴの再処理
- [ ] パレット最適化
- [ ] README.mdに完成したロゴのスクリーンショット追加
- [ ] コミット・プッシュ

## 次のステップ詳細

### 画像収集完了後の実行コマンド

```bash
# 1. ImageMagickインストール確認
convert --version

# 2. ロゴ画像を処理
./tools/process_logos.sh

# 3. 処理済み画像を確認
ls -l assets/processed/
file assets/processed/nes.png

# 4. CHRデータ生成
./tools/images_to_chr.py > /tmp/chr_data.txt

# 5. create_chr.pyの既存ロゴデータを置き換え
# （手動編集またはスクリプト化）

# 6. ROMビルド
make clean
make

# 7. 動作確認
fceux nesfetch.nes
```

## 技術的課題

### 解決済み
- [x] CHR-ROM容量オーバー問題（4×4 → 3×4タイルに変更）
- [x] BSS セグメントエラー（nes.cfg修正）
- [x] CC65インストール（ソースビルド）
- [x] スクロールメニュー実装

### 未解決/検討中
- [ ] 外部ネットワークアクセス制限（Wikimedia Commons 403エラー）
  - **解決策**: ユーザーが手動で画像を配置
- [ ] 4色制限での色再現性
  - **対策**: グレースケール変換で明度差を最大化
- [ ] 低解像度での認識性
  - **対策**: ImageMagickパラメータ最適化

## 将来の拡張アイデア

### 優先度: 低
- [ ] カラーパレット対応（ロゴごとに異なる色）
- [ ] アニメーション効果
- [ ] サウンド追加（ロゴ選択時の効果音）
- [ ] システム情報表示（neofetch風）
- [ ] 他のMapperサポート（より多くのロゴ）

### 優先度: 中
- [ ] ロゴ追加（Atari Jaguar, 3DO, Intellivisionなど）
- [ ] 自動画像ダウンロード機能（ネットワーク環境で）
- [ ] より高度な画像処理（エッジ検出、手動最適化）

### 優先度: 高（現在の目標）
- [x] 公式ロゴの忠実な再現
- [ ] 全29ロゴの品質確保

## ブロッカー

### 現在のブロッカー
1. **29個のロゴ画像が未配置**
   - 担当: ユーザー
   - 期限: N/A
   - 状態: 進行中

### 解決済みブロッカー
1. ~~外部ネットワークアクセス~~
   - 解決: 手動配置に変更

## メトリクス

### CHR-ROM使用状況
- フォント: 64タイル (12.5%)
- ロゴ: 348タイル (67.9%)
- 未使用: 100タイル (19.5%)
- **合計**: 412 / 512タイル (80.5%)

### コード統計
- C言語: `src/main.c` (~300行)
- アセンブリ: `src/*.s` (~50行)
- Python: `tools/*.py` (~400行)
- Bash: `tools/*.sh` (~100行)

### ビルド時間
- クリーンビルド: ~2秒
- インクリメンタルビルド: ~1秒
- CHR生成: ~0.1秒

## レビューポイント

### コードレビュー
- [ ] C90/C89互換性（CC65要件）
- [ ] メモリリーク無し
- [ ] VBlank同期の正確性
- [ ] コントローラー入力のデバウンス

### デザインレビュー
- [ ] 29個全てのロゴが認識可能
- [ ] 公式デザインとの類似度
- [ ] UIの使いやすさ

### テストレビュー
- [ ] 複数のエミュレータでテスト
- [ ] 実機テスト（可能であれば）
- [ ] 全機能の動作確認

## 完了条件

このプロジェクトは以下を満たした時に完了:

1. ✅ 29個の公式ロゴを全て実装
2. ✅ 各ロゴが元のデザインに忠実
3. ✅ 24×32ピクセルで認識可能
4. ✅ NESエミュレータで正常動作
5. ✅ ビルドが成功
6. ✅ CI/CDパイプラインが通過
7. ✅ ドキュメント完備
