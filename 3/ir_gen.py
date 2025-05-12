temp_counter = 0
ir_code = []

def new_temp():
    global temp_counter
    temp = f"t{temp_counter}"
    temp_counter += 1
    return temp

def generate_ir(node):
    if node.type == "Program":
        for child in node.children:
            generate_ir(child)

    elif node.type == "Literal":
        temp = new_temp()
        ir_code.append(f"{temp} = {node.value}")
        return temp

    elif node.type == "Identifier":
        return node.value

    elif node.type == "Assign":
        rhs = generate_ir(node.children[0])
        ir_code.append(f"{node.value} = {rhs}")

    elif node.type == "BinOp":
        left = generate_ir(node.children[0])
        right = generate_ir(node.children[1])
        result = new_temp()
        ir_code.append(f"{result} = {left} {node.value} {right}")
        return result

    elif node.type == "Print":
        expr = generate_ir(node.children[0])
        ir_code.append(f"print {expr}")

    elif node.type == "If":
        cond = generate_ir(node.children[0])
        label_else = f"L{new_temp()}"
        label_end = f"L{new_temp()}"

        ir_code.append(f"ifFalse {cond} goto {label_else}")
        generate_ir(node.children[1])  # then
        ir_code.append(f"goto {label_end}")
        ir_code.append(f"{label_else}:")
        generate_ir(node.children[2])  # else
        ir_code.append(f"{label_end}:")

    elif node.type in ["Then", "Else"]:
        for stmt in node.children:
            generate_ir(stmt)

    elif node.type == "FunctionDecl":
        ir_code.append(f"func {node.value}:")
        for stmt in node.children:
            generate_ir(stmt)
        ir_code.append(f"end func {node.value}")
