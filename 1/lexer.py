# This file contains the original, regex based lexer (we are not likely to use this)

import re
import sys

class Lexer:
    def __init__(self, token_specs):
        self.token_specs = token_specs
        self.tokens = []

    def lex(self, text):
        self.tokens = []
        position = 0
        while position < len(text):
            match = None
            for token_type, pattern in self.token_specs:
                regex = re.compile(pattern)
                match = regex.match(text, position)
                if match:
                    value = match.group(0)
                    if token_type != ('T_WHITESPACE'):  # Ignore whitespace
                        self.tokens.append((token_type, value))
                    position = match.end()
                    break
        return self.tokens

if __name__ == "__main__":
    token_specs = [
        ('T_STRING_LITERAL', r'\"([^"\\]|\\.)*\"|\'([^\'\\]|\\.)*\''),
        ('T_PRINT', r'\bonyesha\b'),
        ('T_LET', r'\bweka\b'),
        ('T_INPUT', r'\bsoma\b'),
        ('T_IF', r'\bikiwa\b'),
        ('T_THEN', r'\bbasi\b'),
        ('T_ELSE', r'\binginepo\b'),
        ('T_FOR', r'\bkurudia\b'),
        ('T_TO', r'\bhadi\b'),
        ('T_NEXT', r'\bendelea\b'),
        ('T_IDENTIFIER', r'[a-zA-Z_][a-zA-Z_0-9]*'),
        ('T_INT_LITERAL', r'\b\d+\b'),
        ('T_ADDITION', r'\+'),
        ('T_SUBTRACTION', r'-'),
        ('T_MULTIPLICATION', r'\*'),
        ('T_DIVISION', r'/'),
        ('T_ASSIGNMENT', r'='),
        ('T_EQUAL', r'='),
        ('T_NOT_EQUAL', r'<>|!='),
        ('T_GREATER_THAN', r'>'),
        ('T_LESS_THAN', r'<'),
        ('T_GREATER_EQUAL', r'>='),
        ('T_LESS_EQUAL', r'<='),
        ('T_COMMA', r','),
        ('T_SEMICOLON', r';'),
        ('T_LPAREN', r'\('),
        ('T_RPAREN', r'\)'),
        ('T_NEWLINE', r'\n'),
        ('T_WHITESPACE', r'[ \t]+'),
        ('T_UNKNOWN', r'.'),
    ]

    lexer = Lexer(token_specs)

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                swahili_code = file.read()
            tokens = lexer.lex(swahili_code)
            for token in tokens:
                print(token)
        except FileNotFoundError:
            print(f"Error: File not found at '{filepath}'", file=sys.stderr)
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
    