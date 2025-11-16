; Reset and initialization code

.export _main
.import _game_main
.importzp sp

.segment "STARTUP"

_main:
    ; Disable interrupts
    sei
    cld

    ; Disable APU frame IRQ
    ldx #$40
    stx $4017

    ; Set up stack
    ldx #$FF
    txs

    ; Disable NMI and rendering
    inx  ; now X = 0
    stx $2000
    stx $2001

    ; Wait for first vblank
:   bit $2002
    bpl :-

    ; Clear RAM
    txa
clear_ram:
    sta $0000, x
    sta $0100, x
    sta $0200, x
    sta $0300, x
    sta $0400, x
    sta $0500, x
    sta $0600, x
    sta $0700, x
    inx
    bne clear_ram

    ; Wait for second vblank
:   bit $2002
    bpl :-

    ; Initialize stack pointer for C
    lda #$00
    sta sp
    lda #$06
    sta sp+1

    ; Call C main function
    jsr _game_main

    ; Infinite loop
forever:
    jmp forever

; NMI handler
.export _nmi
_nmi:
    rti

; IRQ handler
.export _irq
_irq:
    rti

.segment "VECTORS"
.word _nmi
.word _main
.word _irq
