import ply.yacc as yacc

from lab1 import scanner
# from lab3 import AST
# from lab3 import TreePrinter
import AST

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
    program : stmt
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
    stmt : print_stmt
         | if_stmt
         | while_stmt
         | for_stmt
    """
    p[0] = p[1]

def p_program_block(p):
    """
    stmt : LPAREN_F stmt_list RPAREN_F
    """
    p[0] = p[2]


def p_stmt_list_start(p):
    """
    stmt_list : stmt
    """
    p[0] = AST.ProgramBlock(p[1])

def p_stmt_list_add(p):
    """
    stmt_list : stmt_list stmt
    """
    p[0] = p[1]
    p[0].stmts.append(p[2])

def p_empty_stmt(p):
    """
    stmt : SEMICOLON
         | LPAREN_F RPAREN_F
    """

    p[0] = AST.ProgramBlock()
    # print("p_empyt_stmt", p[0])


def p_break(p):
    """
    stmt : BREAK SEMICOLON
    """

    p[0] = AST.Break()
    # print("break", p[0])


def p_continue(p):
    """
    stmt : CONTINUE SEMICOLON
    """
    p[0] = AST.Continue()
    # print("continue", p[0])


def p_stmt_semicolon(p):
    """
    stmt : expr SEMICOLON
    """
    p[0] = p[1]
    # print("stmt semicolon", p[0])



def p_return(p):
    """
    stmt : RETURN expr SEMICOLON
    """
    p[0] = AST.Return(p[2])


def p_comparison(p):
    """
    comparison : expr GREATER expr
               | expr LESSER expr
               | expr GREATER_EQUAL expr
               | expr LESSER_EQUAL expr
               | expr EQUALS expr
               | expr NOT_EQUAL expr
    """
    p[0] = AST.BinExpr(p[2], p[1], p[3])


def p_operator(p):
    """
    operator : expr PLUS expr
             | expr MINUS expr
             | expr TIMES expr
             | expr DIVIDE expr
    """
    p[0] = AST.BinExpr(p[2], p[1], p[3])

def p_uminus(p):
    """
    operator : MINUS expr %prec UMINUS
    """
    p[0] = AST.UnaryMinus(p[2])

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
    p[0] = AST.Assign(p[2], AST.Variable(p[1]), p[3], )




def p_expression_operation(p):
    """
    expression_operation : expr PLUS_MATRIX expr
                         | expr MINUS_MATRIX expr
                         | expr TIMES_MATRIX expr
                         | expr DIVIDE_MATRIX expr
    """
    p[0] = AST.BinExpr(p[2], p[1], p[3])


def p_matrix_element_operation(p):
    """
    matrix_element_operation : lvalue ASSIGN expr
                             | lvalue INCREMENT expr
                             | lvalue DECREMENT expr
                             | lvalue MULTIPLY_ASSIGN expr
                             | lvalue DIVIDE_ASSIGN expr
    """
    p[0] = AST.Assign(p[2], p[1], p[3])


def p_matrix_reference(p):
    """
    lvalue : expr idx
    """
    p[0] = AST.MatrixReference(p[1], p[2])



def p_idx(p):
    """
    idx : LPAREN_SQ list RPAREN_SQ
    """
    p[0] = AST.IDX(p[2])

def p_list(p):
    """
    list : expr
    """
    p[0] = [p[1]]

def p_list_add(p):
    """
    list : list COMMA expr
    """
    p[0] = p[1]
    p[0].append(p[3])

def p_empty(p):
    """
    empty : LPAREN_SQ RPAREN_SQ
    """
    p[0] = AST.IDX()


def p_special_matrix(p):
    """
    special_matrix : EYE LPAREN expr RPAREN
                   | ONES LPAREN expr RPAREN
                   | ZEROS LPAREN expr RPAREN
    """
    p[0] = AST.FunctionCall(p[1], [p[3]])


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
    """
    p[0] = p[1]

def p_transpose(p):
    """
     expr : expr TRANSPOSE
    """
    p[0] = AST.Transposition(p[1])


def p_if_stmt(p):
    """
    if_stmt : IF LPAREN expr RPAREN stmt %prec IFX
    """
    # pierwsza produckcja (%prec IFX) - gdy nie wiemy do ktorego ifa ma byc else
    p[0] = AST.If(p[3], p[5])


def p_if_else_stmt(p):
    """
    if_stmt : IF LPAREN expr RPAREN stmt ELSE stmt
    """
    p[0] = AST.If(p[3], p[5], p[7])


def p_while_stmt(p):
    """
    while_stmt : WHILE LPAREN expr RPAREN stmt
    """
    p[0] = AST.While(p[3], p[5])


def p_for_stmt(p):
    """
    for_stmt : FOR ID ASSIGN range stmt
    """

    p[0] = AST.For(AST.Variable(p[2]), p[4], p[5])


def p_range(p):
    """
    range : expr RANGE expr
    """
    p[0] = AST.Range(p[1], p[3])


def p_print(p):
    """
    print_stmt : PRINT list SEMICOLON
    """
    p[0] = AST.FunctionCall(p[1], p[2])


parser = yacc.yacc()
