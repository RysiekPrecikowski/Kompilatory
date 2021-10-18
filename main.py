# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------
keywords = {
    keyword: keyword.upper()
    for keyword in [
        'if', 'else', 'for', 'while', 'break', 'continue',
        'return', 'eye', 'zeros', 'ones', 'print'
    ]
}

tokens = (
    'NAME', 'ASSIGN', 'FLOAT_NUMBER', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'PLUS_MATRIX', 'MINUS_MATRIX', "TIMES_MATRIX", 'DIVIDE_MATRIX', 'INCREMENT',
    'DECREMENT', 'MULTIPLY_ASSIGN', 'DIVIDE_ASSIGN', 'LESSER', 'GREATER', 'LESSER_EQUAL', 'GREATER_EQUAL', 'EQUALS',
    'NOT_EQUAL', 'LPAREN_SQ', 'RPAREN_SQ', 'LPAREN_F', 'RPAREN_F', 'TRANSPOSE', 'RANGE', 'COMMA', 'SEMICOLON',

*keywords.values(),
)

# Tokens

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

t_PLUS_MATRIX = r'\.+'
t_MINUS_MATRIX = r'\.-'
t_TIMES_MATRIX = r'\.\*'
t_DIVIDE_MATRIX = r'\./'

t_ASSIGN = r'='

t_INCREMENT = r'\+='
t_DECREMENT = r'-='
t_MULTIPLY_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='

t_LESSER = r'<'
t_GREATER = r'>'
t_LESSER_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_NOT_EQUAL = r'!='
t_EQUALS = r'=='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LPAREN_SQ = r'\['
t_RPAREN_SQ = r']'
t_LPAREN_F = r'}'
t_RPAREN_F = r'}'

t_TRANSPOSE = r'\''

t_RANGE = r':'

t_COMMA = r','
t_SEMICOLON = r';'


t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
# t_STRING = r'"[a-zA-Z_][a-zA-Z0-9_]*"'

#todo float :)
# t_FLOAT_NUMBER = r'(\d*\.\d+)|(\d+\.\d*)'
t_FLOAT_NUMBER = r"[-+]?\d*\.\d+|\d+"
# def t_FLOAT_NUMBER(t):
#     r'(\d*\.\d+)|(\d+\.\d*)'
#     # '[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
#
#     try:
#         t.value = float(t.value)
#     except ValueError:
#         print("Integer value too large %d", t.value)
#         t.value = 0
#     return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"



def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lexer = lex.lex()

text = """
    A = zeros(5);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
I = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere
D1 = A.+B' ; # add element-wise A with transpose of B
D2 -= A.-B' ; # substract element-wise A with transpose of B
D3 *= A.*B' ; # multiply element-wise A with transpose of B
D4 /= A./B' ; # divide element-wise A with transpose of B

"""
def tokens(input):
    lexer.input(text)
    while token := lexer.token():
        yield token


for tok in tokens(text):
    print("(%d): %s(%s)" % (tok.lineno, tok.type, tok.value))