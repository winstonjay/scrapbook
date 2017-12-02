@ For Rasberry Pi etc...
@ Hello World ( Arm Assembly )
@ $ TODO

.text

.global _start
_start:
    MOV R7, #4          @ Syscall to output to screen
    MOV R0, #1          @ Monitor output stream
    MOV R2, #28         @ String Length of 28
    LDR R1, =hello      @ Load register with address of string
    MOV R7, #1          @ Exit syscall
    SWI 0

.data
hello:
    .asciz "Hello from ARM Assembly!\n"
