# nesfetch - NESエミュレータで動作するneofetch風ゲーム機ロゴ表示ROM

## プロジェクト概要

NESエミュレータ上で動作する、ゲーム機の公式ロゴを表示するROMプログラム。
neofetchのようにメニューから選択してロゴを切り替えられる。

## 目的

- NESエミュレータで動作する実行可能なROMファイルを作成
- 歴代の有名ゲーム機29種の**公式ロゴ**を忠実に再現
- メニューベースのナビゲーション（十字キー + Aボタン）
- 実機でも動作可能なiNES形式のROMファイル

## コンセプトの変遷

### 初期バージョン
- 5つのロゴ（Linux, PlayStation, Apple, Windows, NES）
- 抽象的なシンボリックパターン
- 2×2タイル（16×16ピクセル）のロゴ

### 第1拡張
- 20個のロゴに拡張
- スクロール可能なメニュー実装

### 第2拡張
- 28→29個のロゴ（WonderSwan追加）
- 3×4タイル（24×32ピクセル）にアップグレード
- CHRタイル容量最適化（512タイル制限内に収める）

### 現在の目標（第3拡張）
- **公式ロゴの忠実な再現**
- 実際の公式ロゴ画像を取得
- ImageMagickで24×32ピクセルに縮小
- ドット絵として自然に見える変換処理
- CHR-ROMデータとして組み込み

## 対象コンソール（29種）

### Nintendo (11種)
1. NES / Famicom
2. SNES / Super Famicom
3. Nintendo 64
4. GameCube
5. Wii
6. Wii U
7. Nintendo Switch
8. Game Boy
9. Game Boy Advance
10. Nintendo DS
11. Nintendo 3DS

### PlayStation (7種)
12. PlayStation / PS1
13. PlayStation 2
14. PlayStation 3
15. PlayStation 4
16. PlayStation 5
17. PlayStation Vita

### Sega (3種)
18. Sega Genesis / Mega Drive
19. Sega Saturn
20. Dreamcast

### Xbox (4種)
21. Xbox
22. Xbox 360
23. Xbox One
24. Xbox Series X/S

### その他 (4種)
25. Atari
26. PC Engine / TurboGrafx-16
27. Neo Geo
28. Steam Deck
29. WonderSwan

## 技術的特徴

- **開発環境**: CC65ツールチェーン（C → 6502アセンブリ）
- **ROM形式**: iNES Mapper 0
- **PRG-ROM**: 32KB（プログラム領域）
- **CHR-ROM**: 8KB（グラフィックス領域、512タイル）
- **入力**: NESコントローラー（十字キー、A/Bボタン）
- **表示**: PPU経由でタイルベースグラフィックス
- **CI/CD**: GitHub Actions自動ビルド
- **コンテナ**: Docker対応

## デザイン方針

### 以前のアプローチ（問題あり）
- プログラマが想像で作成した抽象的なロゴ
- 実際の公式ロゴとは異なるデザイン
- 色やフォントが不正確

### 新しいアプローチ（目標）
- 公式ロゴ画像を入手（Wikimedia Commonsなど）
- ImageMagickで正確に縮小処理
- ドット絵化しても認識可能な形を維持
- NESの4色パレット制限内で最適化

## ユーザー体験

1. ROM起動
2. 29個のロゴメニューが表示（1ページ10個、スクロール可能）
3. 十字キー上下で選択
4. Aボタンでロゴ表示
5. Bボタンでメニューに戻る
6. ページインジケータ表示（例: "Page 1/3"）
