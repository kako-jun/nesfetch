.PHONY: all clean
.SUFFIXES:

# ターゲットファイル名
TARGET = nesfetch

# コンパイラとツール
CC65 = /usr/local/bin/cc65
CA65 = /usr/local/bin/ca65
LD65 = /usr/local/bin/ld65

# ソースファイル
C_SOURCES = src/main
ASM_SOURCES = src/header src/reset

# オブジェクトファイル
C_OBJS = $(addsuffix .o,$(C_SOURCES))
ASM_OBJS = $(addsuffix .o,$(ASM_SOURCES))
ALL_OBJECTS = $(ASM_OBJS) $(C_OBJS)

# フラグ
CFLAGS = -Oi -t nes
ASFLAGS = -t nes
LDFLAGS = -C nes.cfg

all: $(TARGET).nes

# C -> アセンブリ
$(C_SOURCES).s: $(C_SOURCES).c
	$(CC65) $(CFLAGS) -o $@ $<

# アセンブリ -> オブジェクト（Cから生成）
$(C_SOURCES).o: $(C_SOURCES).s
	$(CA65) $(ASFLAGS) -o $@ $<

# アセンブリ -> オブジェクト（直接）
src/header.o: src/header.s
	$(CA65) $(ASFLAGS) -o $@ $<

src/reset.o: src/reset.s
	$(CA65) $(ASFLAGS) -o $@ $<

# CHRデータ生成
chr.bin:
	python3 tools/create_chr.py

# CHRデータをアセンブリに変換
src/chr.s: chr.bin
	echo '.segment "CHR"' > $@
	echo '.incbin "chr.bin"' >> $@

src/chr.o: src/chr.s
	$(CA65) $(ASFLAGS) -o $@ $<

# リンク
$(TARGET).nes: $(ALL_OBJECTS) src/chr.o
	$(LD65) $(LDFLAGS) -o $@ $(ALL_OBJECTS) src/chr.o /usr/local/share/cc65/lib/nes.lib

clean:
	rm -f $(C_SOURCES).s $(ALL_OBJECTS) src/chr.s src/chr.o $(TARGET).nes chr.bin
