.global _start
_start:
	mov r0, #1
	mov r1, #1
	add r0, r1
	bl ioWrite

	mov r0, #0
	mov r7, #1
	swi 0
