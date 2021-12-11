from lab1 import scanner
import ply.yacc as yacc

from lab3 import AST

tokens = scanner.tokens

precedence = (
    ("left", "ASSIGN", 'INCREMENT', 'DECREMENT', 'MULTIPLY_ASSIGN', 'DIVIDE_ASSIGN'),
    ("left", "LESSER", 'GREATER', 'LESSER_EQUAL', 'GREATER_EQUAL', 'EQUALS', 'NOT_EQUAL'),
    ("left", "PLUS", 'MINUS', 'PLUS_MATRIX', 'MINUS_MATRIX'),
    ("left", "TIMES", 'DIVIDE', "TIMES_MATRIX", 'DIVIDE_MATRIX'),
    ('right', "ONES", "ZEROS", "EYE"),
    ("left", "TRANSPOSE"),
    ("right", "RANGE"),
    ("right", "UMINUS"),
    ("nonassoc", "IFX"),
    ("nonassoc", "ELSE"),
)


def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}: LexToken({p.type}, ' {p.value} ')")
    else:
        print("Unexpected end of input")



def p_program_simple(p):
    """
    program: stmt
    """
    p[0] = AST.ProgramBlock(p[1])

def p_program_add(p):
    """
    program : program stmt
    """
    program_block = p[1]
    program_block.stmts.append(p[2])
    p[0] = program_block


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

def p_stmt_semicolon(p):
    pass

def p_comparison(p):
    """
    comparison : expr GREATER expr
               | expr LESSER expr
               | expr GREATER_EQUAL expr
               | expr LESSER_EQUAL expr
               | expr EQUALS expr
               | expr NOT_EQUAL expr
    """


def p_operator(p):
    """
    operator : expr PLUS expr
             | expr MINUS expr
             | MINUS expr %prec UMINUS
             | expr TIMES expr
             | expr DIVIDE expr
    """


# def p_type_recognition(p):
#     """
#     type_recognition : Variable
#                      | intNum
#                      | floatNum
#                      | string
#     """

def p_Variable(p):
    """
    type_recognition : ID
    """
    p[0] = AST.Variable(p[1])

def p_intNum(p):
    """
    type_recognition : NUMBER
    """
    p[0] = AST.IntNum(p[1])

def p_floatNum(p):
    """
    type_recognition : FLOATNUMBER
    """
    p[0] = AST.FloatNum(p[1])

def p_string(p):
    """
    type_recognition : STRING
    """
    p[0] = AST.String(p[1])

def p_single_operation(p):
    """
    single_operation : ID ASSIGN expr
                     | ID INCREMENT expr
                     | ID DECREMENT expr
                     | ID MULTIPLY_ASSIGN expr
                     | ID DIVIDE_ASSIGN expr
    """


def p_expression_operation(p):
    """
    expression_operation : expr PLUS_MATRIX expr
                         | expr MINUS_MATRIX expr
                         | expr TIMES_MATRIX expr
                         | expr DIVIDE_MATRIX expr
    """


def p_matrix_element_operation(p):
    """
    matrix_element_operation : expr idx ASSIGN expr
                             | expr idx INCREMENT expr
                             | expr idx DECREMENT expr
                             | expr idx MULTIPLY_ASSIGN expr
                             | expr idx DIVIDE_ASSIGN expr
    """


def p_idx(p):
    """
    idx : LPAREN_SQ list RPAREN_SQ
    """


def p_list(p):
    """
    list : expr
         | list COMMA expr
    """


def p_empty(p):
    """
    empty : LPAREN_SQ RPAREN_SQ
    """
    # p[0]

def p_special_matrix(p):
    """
    special_matrix : EYE LPAREN expr RPAREN
                   | ONES LPAREN expr RPAREN
                   | ZEROS LPAREN expr RPAREN
    """


def p_epxr(p):
    """
    expr : type_recognition
         | single_operation
         | matrix_element_operation
         | expression_operation
         | comparison
         | operator
         | special_matrix
         | empty
         | idx
         | expr TRANSPOSE
    """


def p_if_stmt(p):
    """
    if_stmt : IF LPAREN expr RPAREN stmt %prec IFX
            | IF LPAREN expr RPAREN stmt ELSE stmt
    """
    # pierwsza produckcja (%prec IFX) - gdy nie wiemy do ktorego ifa ma byc else

def p_while_stmt(p):
    """
    while_stmt : WHILE LPAREN expr RPAREN stmt
    """


def p_for_stmt(p):
    """
    for_stmt : FOR ID ASSIGN range stmt
    range : expr RANGE expr
    """


def p_print(p):
    """
    print_stmt : PRINT list SEMICOLON
    """


parser = yacc.yacc()
