import ply.lex as lex

# List of token names
tokens = (
    'LET', 'IDENTIFIER', 'EQUALS', 'INT_LITERAL', 'PRINT', 'STRING_LITERAL',
    'IF', 'THEN', 'ELSE', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
    'GT', 'LT', 'GE', 'LE', 'NEQ'
)

# Regular expression rules for simple tokens
t_LET = r'weka'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_EQUALS = r'='
t_INT_LITERAL = r'\d+'
t_PRINT = r'onyesha'
t_STRING_LITERAL = r'"[^"]*"'
t_IF = r'ikiwa'
t_THEN = r'basi'
t_ELSE = r'nginepo'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_NEQ = r'!='

# Skip whitespace
t_ignore = ' \t'

# Error handling for invalid characters
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
