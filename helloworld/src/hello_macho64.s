; Hello World ( Assembly Mac osx )
; $ nasm -f macho64 -o hello_macho64.s hello_macho64.s
; $ ld -o hello_macho64 hello_macho64.o
; $ hello_macho64.s

global  start

section .text
start:
        mov     rax, 0x2000004      ; syscall num for write
        mov     rdi, 1              ; file descriptor (stdout)
        mov     rsi, msg            ; address of string to output
        mov     rdx, msg.len        ; number of bytes
        syscall

        mov     rax, 0x2000001      ; sys call for exit
        mov     rdi, 0              ; exit code
        syscall


section .data
msg:    db      "Hello, world!", 0xa ; 0xa is newline
.len:   equ     $ - msg