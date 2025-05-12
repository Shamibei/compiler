# === lexer.py ===
import ply.lex as lex

# List of token names
tokens = [
    'IDENTIFIER', 'INT_LITERAL', 'STRING_LITERAL',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', 'GT', 'LT', 'GE', 'LE', 'NEQ'
]

# Reserved keywords
reserved = {
    'weka': 'LET',
    'onyesha': 'PRINT',
    'ikiwa': 'IF',
    'basi': 'THEN',
    'nginepo': 'ELSE',
    'function': 'FUNCTION'
}

tokens += list(reserved.values())

# Token regex definitions
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_GT      = r'>'
t_LT      = r'<'
t_GE      = r'>='
t_LE      = r'<='
t_NEQ     = r'!='

def t_STRING_LITERAL(t):
    r'\"([^"\\]|\\.)*\"'
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()