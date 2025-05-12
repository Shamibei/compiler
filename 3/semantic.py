class SymbolTable:
    def __init__(self):
        self.stack = [{}]  # Stack of scopes
        self.functions = {}  # Store function declarations separately

    def enter_scope(self):
        self.stack.append({})

    def exit_scope(self):
        self.stack.pop()

    def declare(self, name, value_type):
        if name in self.stack[-1]:
            raise Exception(f"Variable '{name}' already declared in this scope.")
        self.stack[-1][name] = value_type

    def lookup(self, name):
        for scope in reversed(self.stack):
            if name in scope:
                return scope[name]
        raise Exception(f"Variable '{name}' not declared.")

def analyze_semantics(ast):
    symbol_table = SymbolTable()
    visit_node(ast, symbol_table)

def visit_node(node, symbol_table):
    if node.type == "Program":
        for child in node.children:
            visit_node(child, symbol_table)

    elif node.type == "Assign":
        var_name = node.value
        expr = node.children[0]
        expr_type = visit_node(expr, symbol_table)  # Get type of RHS
        symbol_table.declare(var_name, expr_type)   # Store type of var

    elif node.type == "Identifier":
        return symbol_table.lookup(node.value)

    elif node.type == "Literal":
        value = node.value
        if isinstance(value, int):
            return "int"
        elif isinstance(value, str):
            return "string"
        # Add more types if needed

    elif node.type == "BinOp":
        left_type = visit_node(node.children[0], symbol_table)
        right_type = visit_node(node.children[1], symbol_table)
        op = node.value
        if left_type != right_type:
            raise Exception(f"Type mismatch in operation '{op}': {left_type} vs {right_type}")
        return left_type  # Assume result has same type

    elif node.type == "If":
        cond_type = visit_node(node.children[0], symbol_table)
        if cond_type != "int":
            raise Exception("Condition in 'if' statement must be of type int (treated as boolean).")

        symbol_table.enter_scope()
        visit_node(node.children[1], symbol_table)  # then
        symbol_table.exit_scope()

        symbol_table.enter_scope()
        visit_node(node.children[2], symbol_table)  # else
        symbol_table.exit_scope()

    elif node.type in ["Then", "Else"]:
        for stmt in node.children:
            visit_node(stmt, symbol_table)

    elif node.type == "Print":
        if not node.children:
            raise SemanticError("Missing expression in print statement", node)
        expr_type = visit_node(node.children[0], symbol_table)
        if expr_type not in ["int", "string"]:
            raise SemanticError(f"Cannot print value of type {expr_type}", node)

    elif node.type == "FunctionDecl":
        func_name = node.value
        if func_name in symbol_table.functions:
            raise Exception(f"Function '{func_name}' already defined.")
        symbol_table.functions[func_name] = node

        symbol_table.enter_scope()
        for stmt in node.children:
            visit_node(stmt, symbol_table)
        symbol_table.exit_scope()

class SemanticError(Exception):
    def __init__(self, message, node=None):
        self.message = message
        self.node = node
        super().__init__(self.format_message())

    def format_message(self):
        if self.node and hasattr(self.node, 'lineno'):
            return f"[Line {self.node.lineno}] Semantic Error: {self.message}"
        return f"Semantic Error: {self.message}"
