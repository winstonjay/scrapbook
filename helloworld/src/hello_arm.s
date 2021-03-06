@ Hello World ( Assembly Raspberry Pi ARM )
@ $ as -o tmp/hello_arm.o hello_arm.s
@ $ ld -o bin/hello_arm tmp/hello_arm.o
@ $ ./bin/hello_arm

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
