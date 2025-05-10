# This file contains the lexer in a format ready to use in a parser generator like PLY

import re
import sys

class Token:
    def __init__(self, type, value, lineno, lexpos):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.lexpos = lexpos

    def __repr__(self):
        return f"Token(type={self.type}, value={self.value}, lineno={self.lineno}, lexpos={self.lexpos})"

class Lexer:
    def __init__(self, token_specs):
        self.token_specs = token_specs

    def tokenize(self, text):
        position = 0
        lineno = 1
        while position < len(text):
            match = None
            for token_type, pattern in self.token_specs:
                regex = re.compile(pattern)
                match = regex.match(text, position)
                if match:
                    value = match.group(0)
                    if token_type == 'T_NEWLINE':
                        lineno += 1
                    if token_type != 'T_WHITESPACE':
                        yield Token(token_type, value, lineno, position)
                    position = match.end()
                    break
            if not match:
                raise SyntaxError(f"Illegal character at line {lineno}: {text[position]}")

if __name__ == "__main__":
    token_specs = [
        ('T_STRING_LITERAL', r'\"([^"\\]|\\.)*\"|\'([^\'\\]|\\.)*\''),  # String literals
        ('T_PRINT', r'\bonyesha\b'),  # print function
        ('T_LET', r'\bweka\b'),  # let statement
        ('T_INPUT', r'\bsoma\b'),  # input statement
        ('T_IF', r'\bikiwa\b'),  # if statement
        ('T_THEN', r'\bbasi\b'),  # then statement
        ('T_ELSE', r'\binginepo\b'),  # else statement
        ('T_FOR', r'\bkurudia\b'),  # for loop
        ('T_TO', r'\bhadi\b'),  # to keyword
        ('T_NEXT', r'\bendelea\b'),  # next keyword
        ('T_IDENTIFIER', r'[a-zA-Z_][a-zA-Z_0-9]*'),  # Identifiers
        ('T_INT_LITERAL', r'\b\d+\b'),  # Integer literals
        ('T_ADDITION', r'\+'),  # Addition operator
        ('T_SUBTRACTION', r'-'),  # Subtraction operator
        ('T_MULTIPLICATION', r'\*'),  # Multiplication operator
        ('T_DIVISION', r'/'),  # Division operator
        ('T_ASSIGNMENT', r'='),  # Assignment operator
        ('T_EQUAL', r'='),  # Equal operator
        ('T_NOT_EQUAL', r'<>|!='),  # Not equal operator
        ('T_GREATER_THAN', r'>'),  # Greater than operator
        ('T_LESS_THAN', r'<'),  # Less than operator
        ('T_GREATER_EQUAL', r'>='),  # Greater or equal operator
        ('T_LESS_EQUAL', r'<='),  # Less or equal operator
        ('T_COMMA', r','),  # Comma separator
        ('T_SEMICOLON', r';'),  # Semicolon separator
        ('T_LPAREN', r'\('),  # Left parenthesis
        ('T_RPAREN', r'\)'),  # Right parenthesis
        ('T_NEWLINE', r'\n'),  # Newline character
        ('T_WHITESPACE', r'[ \t]+'),  # Whitespace (ignored)
        ('T_UNKNOWN', r'.'),  # Any other character (catch-all for errors)
    ]

    lexer = Lexer(token_specs)

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                swahili_code = file.read()
            # Lex the code
            tokens = lexer.tokenize(swahili_code)
            for token in tokens:
                print(token)
        except FileNotFoundError:
            print(f"Error: File not found at '{filepath}'", file=sys.stderr)
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
