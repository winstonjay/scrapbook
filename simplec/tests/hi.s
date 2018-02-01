.global _start
_start:
	mov r0, #3
	mov r1, #1
	mov r2, #2
	mov r3, #3
	mul r2, r3
	mov r3, #4
	mul r2, r3
	add r1, r2
	mov r2, #2
	mov r3, #6
	add r2, r3
	mov r3, #7
	mov r4, #8
	sub r3, r4
	add r2, r3
	mov r3, #9
	mov r4, #10
	mul r3, r4
	mov r4, #11
	mul r3, r4
	add r2, r3
	mov r3, #12
	mov r4, #13
	mul r3, r4
	add r2, r3
	mov r3, #14
	mov r4, #1
	mul r3, r4
	add r2, r3
	mul r1, r2
	add r0, r1
	bl ioWrite

	mov r0, #2
	mov r1, #1
	mov r2, #2
	mov r3, #3
	mul r2, r3
	mov r3, #4
	mul r2, r3
	add r1, r2
	mov r2, #3
	mov r3, #6
	add r2, r3
	mov r3, #7
	mov r4, #8
	sub r3, r4
	add r2, r3
	mov r3, #9
	mov r4, #10
	mul r3, r4
	mov r4, #11
	mul r3, r4
	add r2, r3
	mov r3, #12
	mov r4, #13
	mul r3, r4
	add r2, r3
	mov r3, #14
	mov r4, #2
	mul r3, r4
	add r2, r3
	mul r1, r2
	add r0, r1
	bl ioWrite

	mov r0, #2
	mov r1, #1
	mov r2, #2
	mov r3, #3
	mul r2, r3
	mov r3, #4
	mul r2, r3
	add r1, r2
	mov r2, #13
	mul r1, r2
	add r0, r1
	mov r1, #14
	mov r2, #3
	mul r1, r2
	add r0, r1
	bl ioWrite

	mov r0, #0
	mov r7, #1
	swi 0
