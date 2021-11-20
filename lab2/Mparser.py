
from lab1 import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ("left", "ASSIGN",  'INCREMENT', 'DECREMENT', 'MULTIPLY_ASSIGN', 'DIVIDE_ASSIGN'),
    ("left", "LESSER", 'GREATER', 'LESSER_EQUAL', 'GREATER_EQUAL', 'EQUALS', 'NOT_EQUAL'),
    ("left", "PLUS", 'MINUS', 'PLUS_MATRIX', 'MINUS_MATRIX'),
    ("left", "TIMES", 'DIVIDE', "TIMES_MATRIX", 'DIVIDE_MATRIX'),
    ('right', "ONES", "ZEROS", "EYE"),
    ("left", "TRANSPOSE"),
    ("right", "RANGE"),
    ("left", "UMINUS"),
    ("nonassoc", "IFX"),
    ("nonassoc", "ELSE"),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, ' {2} ')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """
    program : stmt
            | program stmt
    """

def p_stmt(p):
    """
    stmt : expr SEMICOLON
         | print_stmt
         | if_stmt
         | while_stmt
         | for_stmt
         | BREAK SEMICOLON
         | CONTINUE SEMICOLON
         | RETURN expr SEMICOLON
         | SEMICOLON
         | LPAREN_F RPAREN_F
         | LPAREN_F stmt_list RPAREN_F
    stmt_list : stmt
              | stmt_list stmt
    """

def p_epxr(p):
    """
    expr : ID
         | NUMBER
         | FLOATNUMBER
         | STRING
         | ID ASSIGN expr
         | ID INCREMENT expr
         | ID DECREMENT expr
         | ID MULTIPLY_ASSIGN expr
         | ID DIVIDE_ASSIGN expr
         | expr LPAREN_SQ list RPAREN_SQ ASSIGN expr
         | expr LPAREN_SQ list RPAREN_SQ INCREMENT expr
         | expr LPAREN_SQ list RPAREN_SQ DECREMENT expr
         | expr LPAREN_SQ list RPAREN_SQ MULTIPLY_ASSIGN expr
         | expr LPAREN_SQ list RPAREN_SQ DIVIDE_ASSIGN expr
         | expr PLUS expr
         | expr MINUS expr
         | MINUS expr %prec UMINUS
         | expr TIMES expr
         | expr DIVIDE expr
         | expr PLUS_MATRIX expr
         | expr MINUS_MATRIX expr
         | expr TIMES_MATRIX expr
         | expr DIVIDE_MATRIX expr
         | expr GREATER expr
         | expr LESSER expr
         | expr GREATER_EQUAL expr
         | expr LESSER_EQUAL expr
         | expr EQUALS expr
         | expr NOT_EQUAL expr
         | EYE LPAREN expr RPAREN
         | ONES LPAREN expr RPAREN
         | ZEROS LPAREN expr RPAREN
         | LPAREN_SQ RPAREN_SQ
         | LPAREN_SQ list RPAREN_SQ
         | expr TRANSPOSE
    list : expr
         | list COMMA expr
    """

def p_if_stmt(p):
    """
    if_stmt : IF LPAREN expr RPAREN stmt %prec IFX
            | IF LPAREN expr RPAREN stmt ELSE stmt
    """

def p_loop_stmt(p):
    """
    while_stmt : WHILE LPAREN expr RPAREN stmt
    range : expr RANGE expr
    for_stmt : FOR ID ASSIGN range stmt
    """


def p_print(p):
    """
    print_stmt : PRINT list SEMICOLON
    """


parser = yacc.yacc()
