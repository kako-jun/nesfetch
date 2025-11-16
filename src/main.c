/*
 * NESfetch - neofetch風NESプログラム
 */

#define PPU_CTRL   (*(unsigned char*)0x2000)
#define PPU_MASK   (*(unsigned char*)0x2001)
#define PPU_STATUS (*(unsigned char*)0x2002)
#define PPU_SCROLL (*(unsigned char*)0x2005)
#define PPU_ADDR   (*(unsigned char*)0x2006)
#define PPU_DATA   (*(unsigned char*)0x2007)
#define OAM_ADDR   (*(unsigned char*)0x2003)
#define OAM_DMA    (*(unsigned char*)0x4014)

#define CONTROLLER1 (*(unsigned char*)0x4016)

// ボタン定義
#define BTN_A      0x01
#define BTN_B      0x02
#define BTN_SELECT 0x04
#define BTN_START  0x08
#define BTN_UP     0x10
#define BTN_DOWN   0x20
#define BTN_LEFT   0x40
#define BTN_RIGHT  0x80

// パレットデータ
const unsigned char palette[32] = {
    // 背景パレット
    0x0F, 0x00, 0x10, 0x30,  // パレット0
    0x0F, 0x16, 0x27, 0x37,  // パレット1
    0x0F, 0x1A, 0x2A, 0x3A,  // パレット2
    0x0F, 0x12, 0x22, 0x32,  // パレット3
    // スプライトパレット
    0x0F, 0x14, 0x24, 0x34,
    0x0F, 0x1B, 0x2B, 0x3B,
    0x0F, 0x11, 0x21, 0x31,
    0x0F, 0x19, 0x29, 0x39
};

// 変数
unsigned char current_logo = 0;
unsigned char total_logos = 5;
unsigned char pad1, pad1_prev;
unsigned char game_state = 0;  // 0=メニュー, 1=ロゴ表示

// ロゴ名（タイル番号として表現）
// L=0x2C, I=0x29, N=0x2E, U=0x35, X=0x38など
const unsigned char logo_names[5][16] = {
    {0x2C, 0x29, 0x2E, 0x35, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00},  // LINUX
    {0x30, 0x33, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00},  // PS
    {0x21, 0x30, 0x30, 0x2C, 0x25, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00},  // APPLE
    {0x37, 0x29, 0x2E, 0x24, 0x2F, 0x37, 0x33, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00},  // WINDOWS
    {0x2E, 0x25, 0x33, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}   // NES
};

// VBlank待機
void wait_vblank(void) {
    while ((PPU_STATUS & 0x80) == 0);
}

// PPUアドレス設定
void set_ppu_addr(unsigned int addr) {
    PPU_ADDR = (unsigned char)(addr >> 8);
    PPU_ADDR = (unsigned char)(addr & 0xFF);
}

// パレット読み込み
void load_palette(void) {
    unsigned char i;
    set_ppu_addr(0x3F00);
    for (i = 0; i < 32; i++) {
        PPU_DATA = palette[i];
    }
}

// 画面クリア
void clear_screen(void) {
    unsigned int i;
    set_ppu_addr(0x2000);
    for (i = 0; i < 960; i++) {
        PPU_DATA = 0x00;
    }
}

// テキスト描画
void draw_text(unsigned char x, unsigned char y, const unsigned char* text) {
    unsigned int addr = 0x2000 + (y << 5) + x;
    unsigned char i = 0;

    set_ppu_addr(addr);
    while (text[i] != 0x00 && i < 32) {
        PPU_DATA = text[i];
        i++;
    }
}

// タイトル
const unsigned char title_text[] = {0x2E, 0x25, 0x33, 0x26, 0x25, 0x34, 0x23, 0x28, 0x00};  // NESFETCH

// 操作説明
const unsigned char help1_text[] = {0x35, 0x30, 0x3C, 0x24, 0x2F, 0x37, 0x2E, 0x3B, 0x33, 0x25, 0x2C, 0x25, 0x23, 0x34, 0x00};  // UP-DOWN:SELECT
const unsigned char help2_text[] = {0x21, 0x3B, 0x33, 0x28, 0x2F, 0x37, 0x00};  // A:SHOW

// メニュー描画
void draw_menu(void) {
    unsigned char i;

    wait_vblank();
    PPU_MASK = 0x00;  // 描画無効

    clear_screen();

    // タイトル
    draw_text(11, 2, title_text);

    // ロゴリスト
    for (i = 0; i < total_logos; i++) {
        unsigned char row = 6 + (i << 1);

        // カーソル
        if (i == current_logo) {
            set_ppu_addr(0x2000 + (row << 5) + 8);
            PPU_DATA = 0x3D;  // > 記号
        }

        // ロゴ名
        draw_text(10, row, logo_names[i]);
    }

    // 操作説明
    draw_text(4, 22, help1_text);
    draw_text(4, 24, help2_text);

    PPU_SCROLL = 0;
    PPU_SCROLL = 0;
    PPU_MASK = 0x1E;  // 描画有効
}

// ロゴ表示
void draw_logo_screen(unsigned char logo_idx) {
    unsigned char x, y;
    unsigned char base_tile;

    wait_vblank();
    PPU_MASK = 0x00;

    clear_screen();

    // ロゴタイトル
    draw_text(12, 2, logo_names[logo_idx]);

    // ロゴタイルパターン描画
    base_tile = 0x40 + (logo_idx << 4);

    for (y = 0; y < 8; y++) {
        set_ppu_addr(0x2000 + ((8 + y) << 5) + 10);
        for (x = 0; x < 12; x++) {
            PPU_DATA = base_tile + (y * 2) + (x >> 3);
        }
    }

    // 戻る説明
    set_ppu_addr(0x2000 + (24 << 5) + 8);
    PPU_DATA = 0x22;  // B
    PPU_DATA = 0x3B;  // :
    PPU_DATA = 0x22;  // B
    PPU_DATA = 0x21;  // A
    PPU_DATA = 0x23;  // C
    PPU_DATA = 0x2B;  // K

    PPU_SCROLL = 0;
    PPU_SCROLL = 0;
    PPU_MASK = 0x1E;
}

// コントローラー読み取り
unsigned char read_controller(void) {
    unsigned char i;
    unsigned char buttons = 0;

    CONTROLLER1 = 1;
    CONTROLLER1 = 0;

    for (i = 0; i < 8; i++) {
        buttons = (buttons >> 1) | ((CONTROLLER1 & 0x01) << 7);
    }

    return buttons;
}

/* ゲームメイン */
void game_main(void) {
    unsigned char pressed;

    /* PPU初期化 */
    PPU_CTRL = 0x00;
    PPU_MASK = 0x00;

    wait_vblank();

    load_palette();
    draw_menu();

    PPU_CTRL = 0x80;  /* NMI有効 */
    PPU_MASK = 0x1E;  /* 描画有効 */

    pad1_prev = 0;

    /* メインループ */
    while (1) {
        wait_vblank();

        pad1 = read_controller();
        pressed = pad1 & ~pad1_prev;

        if (game_state == 0) {
            /* メニュー状態 */
            if (pressed & BTN_UP) {
                if (current_logo > 0) {
                    current_logo--;
                    draw_menu();
                }
            }

            if (pressed & BTN_DOWN) {
                if (current_logo < total_logos - 1) {
                    current_logo++;
                    draw_menu();
                }
            }

            if (pressed & BTN_A) {
                game_state = 1;
                draw_logo_screen(current_logo);
            }
        } else {
            /* ロゴ表示状態 */
            if (pressed & BTN_B) {
                game_state = 0;
                draw_menu();
            }
        }

        pad1_prev = pad1;

        PPU_SCROLL = 0;
        PPU_SCROLL = 0;
    }
}
