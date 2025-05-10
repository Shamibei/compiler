# === parser.py ===
import ply.yacc as yacc
from lex import tokens

start = 'program'


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'GT', 'LT', 'GE', 'LE', 'NEQ'),
)

def p_program(p):
    'program : statements'
    print("Program parsed successfully.")

def p_statements_multiple(p):
    'statements : statements statement'
    pass

def p_statements_single(p):
    'statements : statement'
    pass

def p_statement_assign(p):
    'statement : LET IDENTIFIER EQUALS expression'
    print(f"Assign: {p[2]} = {p[4]}")

def p_statement_print(p):
    'statement : PRINT STRING_LITERAL'
    print(f"Print: {p[2]}")

def p_statement_if(p):
    'statement : IF expression THEN statements ELSE statements'
    print(f"If condition: {p[2]}")
    print(f"Then block executed.")
    print(f"Else block executed.")

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression
                  | expression NEQ expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_literal(p):
    'expression : INT_LITERAL'
    p[0] = p[1]

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()