# This file contains the directly coded lexer

import sys

class DirectLexer:
    def __init__(self):
        self.keywords = {
            'onyesha': 'T_PRINT',
            'weka': 'T_LET',
            'soma': 'T_INPUT',
            'ikiwa': 'T_IF',
            'basi': 'T_THEN',
            'inginepo': 'T_ELSE',
            'kurudia': 'T_FOR',
            'hadi': 'T_TO',
            'endelea': 'T_NEXT'
        }
        self.tokens = []

    def is_identifier(self, char):
        return char.isalpha() or char == '_'

    def is_digit(self, char):
        return char.isdigit()

    def lex(self, text):
        self.tokens = []
        i = 0
        while i < len(text):
            char = text[i]

            # Skip whitespace
            if char in ' \t':
                i += 1
                continue

            # Newline
            if char == '\n':
                self.tokens.append(('T_NEWLINE', '\n'))
                i += 1
                continue

            # Identifiers and keywords
            if self.is_identifier(char):
                start = i
                while i < len(text) and (self.is_identifier(text[i]) or self.is_digit(text[i])):
                    i += 1
                word = text[start:i]
                token_type = self.keywords.get(word, 'T_IDENTIFIER')
                self.tokens.append((token_type, word))
                continue

            # Numbers
            if self.is_digit(char):
                start = i
                while i < len(text) and self.is_digit(text[i]):
                    i += 1
                self.tokens.append(('T_INT_LITERAL', text[start:i]))
                continue

            # String literals
            if char in ('"', "'"):
                quote = char
                i += 1
                start = i
                while i < len(text) and text[i] != quote:
                    if text[i] == '\\' and i + 1 < len(text):
                        i += 2
                    else:
                        i += 1
                value = text[start:i]
                i += 1  # Skip closing quote
                self.tokens.append(('T_STRING_LITERAL', value))
                continue

            # Operators and punctuation
            if text[i:i+2] in ['<>', '!=']:
                self.tokens.append(('T_NOT_EQUAL', text[i:i+2]))
                i += 2
            elif text[i:i+2] == '>=':
                self.tokens.append(('T_GREATER_EQUAL', '>='))
                i += 2
            elif text[i:i+2] == '<=':
                self.tokens.append(('T_LESS_EQUAL', '<='))
                i += 2
            elif char == '+':
                self.tokens.append(('T_ADDITION', '+'))
                i += 1
            elif char == '-':
                self.tokens.append(('T_SUBTRACTION', '-'))
                i += 1
            elif char == '*':
                self.tokens.append(('T_MULTIPLICATION', '*'))
                i += 1
            elif char == '/':
                self.tokens.append(('T_DIVISION', '/'))
                i += 1
            elif char == '=':
                self.tokens.append(('T_EQUAL', '='))
                i += 1
            elif char == '>':
                self.tokens.append(('T_GREATER_THAN', '>'))
                i += 1
            elif char == '<':
                self.tokens.append(('T_LESS_THAN', '<'))
                i += 1
            elif char == ',':
                self.tokens.append(('T_COMMA', ','))
                i += 1
            elif char == ';':
                self.tokens.append(('T_SEMICOLON', ';'))
                i += 1
            elif char == '(':
                self.tokens.append(('T_LPAREN', '('))
                i += 1
            elif char == ')':
                self.tokens.append(('T_RPAREN', ')'))
                i += 1
            else:
                self.tokens.append(('T_UNKNOWN', char))
                i += 1

        return self.tokens


if __name__ == "__main__":
    lexer = DirectLexer()

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
