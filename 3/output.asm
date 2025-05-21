section .data
newline db 10
section .bss
buffer resb 256
t0 resd 1
x resd 1
t1 resd 1
y resd 1
t2 resd 1
t5 resd 1
t6 resd 1
section .text
global _start
_start:
    mov dword [t0], 5
    mov eax, [t0]
    mov [x], eax
    mov dword [t1], 20
    mov eax, [t1]
    mov [y], eax
    mov eax, [x]
    cmp eax, [y]
    setl al
    movzx eax, al
    mov [t2], eax
    mov eax, [t2]
    cmp eax, 0
    je Lt3
    mov eax, 4
    mov ebx, 1
    mov ecx, [t5]
    mov edx, 4
    int 0x80
    jmp Lt4
Lt3:
    mov eax, 4
    mov ebx, 1
    mov ecx, [t6]
    mov edx, 4
    int 0x80
Lt4:
    mov eax, 1
    mov ebx, 0
    int 0x80
