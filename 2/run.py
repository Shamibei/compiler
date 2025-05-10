from yacc import parser
from lex import lexer

def main():
    try:
        # Attempt to read the 'testree.sw' file
        with open("test.sw", "r", encoding="utf-8") as file:
            data = file.read()
    except FileNotFoundError:
        print("Error: 'testree.sw' file not found.")
        return

    # Lexical analysis (tokenize the input data)
    lexer.input(data)
    print("TOKENS:")
    for tok in lexer:
        print(tok)

    print("\nPARSING...")
    ast = parser.parse(data)  # Parse the tokenized data into an AST

if __name__ == "__main__":
    main()
