def generate_assembly(ir_code, output_file="output1.asm"):
    import re

    # Register pool (naive allocation)
    available_registers = ['eax', 'ebx', 'ecx', 'edx']
    register_map = {}  # Map temporaries to registers
    register_in_use = {reg: None for reg in available_registers}

    def allocate_register(temp):
        if temp in register_map:
            return register_map[temp]
        for reg in available_registers:
            if register_in_use[reg] is None:
                register_map[temp] = reg
                register_in_use[reg] = temp
                return reg
        raise RuntimeError("Out of registers")

    def free_register(temp):
        for reg, t in register_in_use.items():
            if t == temp:
                register_in_use[reg] = None
                del register_map[temp]
                break

    asm = [] 
    data_section = [] 
    bss_section = [] 
    text_section = [] 

    temp_map = {}  # Map temporaries like t0, t1, t2 to memory locations
    label_counter = 0

    asm.append("section .data")
#   data_section.append('malloc_space dd 0\n\n    extern malloc\n    extern free')
    data_section.append('newline db 10')  # newline for printing

    asm.append("section .bss")
    bss_section.append("buffer resb 256")  # buffer for printing strings

    asm.append("section .text")
    asm.append("global _start")
    text_section.append("_start:")

    def ensure_temp(temp_name):
        if temp_name not in temp_map:
            bss_section.append(f"{temp_name} resd 1")
            temp_map[temp_name] = temp_name

    for line in ir_code:
        tokens = line.split()

        if not tokens:
            continue

        if tokens[0].endswith(':'):
            text_section.append(tokens[0])  # already single colon now
            continue

        # Handle assignment: t0 = 5
        if len(tokens) == 3 and tokens[1] == '=':
            target = tokens[0]
            value = tokens[2]
            ensure_temp(target)

            if value.isdigit():
                text_section.append(f"    mov dword [{target}], {value}")
            elif value.startswith('"'):
                label = f"str{label_counter}"
                label_counter += 1
                string_content = value.strip('"')
                data_section.append(f'{label} db "{string_content}", 0')
                ensure_temp(target)
                text_section.append(f"    mov dword [{target}], {label}")
            else:
                ensure_temp(value)
                text_section.append(f"    mov eax, [{value}]")
                text_section.append(f"    mov [{target}], eax")

        # Handle print
        elif tokens[0] == "print":
            arg = tokens[1]
            if arg.startswith('"'):
                label = f"str{label_counter}"
                label_counter += 1
                string_content = arg.strip('"')
                data_section.append(f'{label} db "{string_content}", 0')
                text_section.append(f"    mov eax, 4")
                text_section.append(f"    mov ebx, 1")
                text_section.append(f"    mov ecx, {label}")
                text_section.append(f"    mov edx, {len(string_content)}")
                text_section.append(f"    int 0x80")
            else:
                ensure_temp(arg)
                text_section.append(f"    mov eax, 4")
                text_section.append(f"    mov ebx, 1")
                text_section.append(f"    mov ecx, [{arg}]")
                text_section.append(f"    mov edx, 4")
                text_section.append(f"    int 0x80")

        # Handle conditional jumps: ifFalse t2 goto Lt3
        elif tokens[0] == "ifFalse":
            cond = tokens[1]
            label = tokens[3]
            ensure_temp(cond)
            text_section.append(f"    mov eax, [{cond}]")
            text_section.append(f"    cmp eax, 0")
            text_section.append(f"    je {label}")

        # Handle goto
        elif tokens[0] == "goto":
            text_section.append(f"    jmp {tokens[1]}")

        # Handle binary operations: t2 = x != y
        elif len(tokens) == 5 and tokens[1] == '=' and tokens[3] in ['+', '-', '*', '/', '!=', '==', '<', '>', '<=', '>=']:
            target = tokens[0]
            left = tokens[2]
            op = tokens[3]
            right = tokens[4]
            ensure_temp(target)
            ensure_temp(left)
            ensure_temp(right)

            text_section.append(f"    mov eax, [{left}]")
            text_section.append(f"    cmp eax, [{right}]")

            if op == '!=':
                text_section.append(f"    sete al")
            elif op == '==':
                text_section.append(f"    sete al")
            elif op == '<':
                text_section.append(f"    setl al")
            elif op == '>':
                text_section.append(f"    setg al")
            elif op == '<=':
                text_section.append(f"    setle al")
            elif op == '>=':
                text_section.append(f"    setge al")
            else:
                raise NotImplementedError(f"Operator {op} not supported")

            text_section.append(f"    movzx eax, al")
            text_section.append(f"    mov [{target}], eax")

    # Exit syscall
    text_section.append("    mov eax, 1")
    text_section.append("    mov ebx, 0")
    text_section.append("    int 0x80")

     # Final assembly code — ordered correctly
    asm = []
    asm.append("section .data")
    asm.extend(data_section)

    asm.append("section .bss")
    asm.extend(bss_section)

    asm.append("section .text")
    asm.append("global _start")
    asm.extend(text_section)

    # Write to file
    with open(output_file, "w") as f:
        for line in asm:
         f.write(line + "\n")

    
    