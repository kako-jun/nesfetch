; iNES header for NES ROM

.segment "HEADER"

.byte $4E, $45, $53, $1A  ; "NES" followed by MS-DOS end-of-file
.byte $02                  ; Number of 16KB PRG-ROM banks
.byte $01                  ; Number of 8KB CHR-ROM banks
.byte $01, $00             ; Mapper 0, vertical mirroring
.byte $00, $00, $00, $00   ; Unused padding
.byte $00, $00, $00, $00
