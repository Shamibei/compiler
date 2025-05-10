from lex2 import lexer
from yacc2 import parser
from tree import print_ast

def main():
    try:
        with open("test.sw", "r", encoding="utf-8") as file:
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

if __name__ == "__main__":
    main()
