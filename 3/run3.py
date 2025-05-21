from lex2 import lexer 
from yacc2 import parser
from tree import ASTNode, print_ast
from semantic import analyze_semantics
from semantic import SemanticError
from ir_gen import generate_ir, ir_code
from codegen import generate_assembly


def main():
    try:
        with open("test3.sw", "r", encoding="utf-8") as file:
            data = file.read()
    except FileNotFoundError:
        print("Error: 'testsw' file not found.")
        return

    # Tokenize the input using lexer
    lexer.input(data)

    # Print tokens (optional, for debugging)
    print("TOKENS:")
    for tok in lexer:
        print(tok)

    # Parse the input and generate AST
    print("\nPARSING...")
    ast = parser.parse(data)

    if ast is None:
        print("\nNo AST generated. Likely a syntax error in input.")
        return

    # Print the AST
    print("\nABSTRACT SYNTAX TREE:")
    print_ast(ast)

    print("\nPerforming Semantic Analysis...")
    try:
        analyze_semantics(ast)
    except SemanticError as e:
        print(e)
        return
    print("Semantic analysis completed.")
    print("AST and semantic analysis completed successfully.")

    generate_ir(ast)
    print("\nGenerating IR code...")
    print("IR code:")
    for line in ir_code:
        print(line)
    print("\nIR code generation completed successfully.")

    print("\nGenerating Assembly code...")
    generate_assembly(ir_code)
    print("Assembly code:")
    print("\nAssembly code generation completed successfully.")


if __name__ == "__main__":
    main()
