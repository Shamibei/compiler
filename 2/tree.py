class ASTNode:
    def __init__(self, type_, value=None, children=None):
        self.type = type_
        self.value = value
        self.children = children if children else []

    def __repr__(self):
        return f"{self.type}({self.value})"

# Function to print the AST in a readable tree format
def print_ast(node, indent="", is_last=True):
    if not isinstance(node, ASTNode):
        print(indent + ("└── " if is_last else "├── ") + str(node))
        return

    branch = "└── " if is_last else "├── "
    print(indent + branch + f"{node.type}({node.value})")

    indent += "    " if is_last else "│   "
    for i, child in enumerate(node.children):
        print_ast(child, indent, i == len(node.children) - 1)

# Example usage for generating and printing a simple AST
if __name__ == "__main__":
    # Sample AST creation (for demonstration)
    ast_root = ASTNode("Program", None, [
        ASTNode("Assign", "x", [ASTNode("Literal", 10)]),
        ASTNode("Assign", "y", [ASTNode("Literal", 20)]),
        ASTNode("BinOp", "+", [
            ASTNode("Identifier", "x"),
            ASTNode("Identifier", "y")
        ]),
    ])

    # Printing the AST
    print("Abstract Syntax Tree:")
    print_ast(ast_root)
