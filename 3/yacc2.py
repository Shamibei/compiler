import ply.yacc as yacc
from lex import tokens
from tree import ASTNode

# Precedence rules
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'GT', 'LT', 'GE', 'LE', 'NEQ'),
)

# Grammar rules and AST generation

def p_program(p):
    'program : statements'
    p[0] = ASTNode("Program", None, p[1])

def p_statements_multiple(p):
    'statements : statements statement'
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    'statements : statement'
    p[0] = [p[1]]

def p_statement_assign(p):
    'statement : LET IDENTIFIER EQUALS expression'
    p[0] = ASTNode("Assign", p[2], [p[4]])

def p_statement_print(p):
    'statement : PRINT STRING_LITERAL'
    string_node = ASTNode("Literal", value=p[2])
    p[0] = ASTNode("Print", children=[string_node])

def p_statement_function(p):
    'statement : FUNCTION IDENTIFIER statements'
    p[0] = ASTNode("FunctionDecl", p[2], p[3])

def p_statement_if(p):
    'statement : IF expression THEN statements ELSE statements'
    condition = p[2]
    then_block = ASTNode("Then", None, p[4])
    else_block = ASTNode("Else", None, p[6])
    p[0] = ASTNode("If", None, [condition, then_block, else_block])

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
    p[0] = ASTNode("BinOp", p[2], [p[1], p[3]])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_literal(p):
    'expression : INT_LITERAL'
    p[0] = ASTNode("Literal", p[1])

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = ASTNode("Identifier", p[1])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()
