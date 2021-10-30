import ply.lex as lex

keywords = {
    keyword: keyword.upper()
    for keyword in [
        'if', 'else', 'for', 'while', 'break', 'continue',
        'return', 'eye', 'zeros', 'ones', 'print'
    ]
}

tokens = (
    *keywords.values(),
    'ASSIGN',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'FLOATNUMBER', 'NUMBER',
    'LPAREN', 'RPAREN', 'LPAREN_SQ', 'RPAREN_SQ', 'LPAREN_F', 'RPAREN_F',
    'PLUS_MATRIX', 'MINUS_MATRIX', "TIMES_MATRIX", 'DIVIDE_MATRIX', 'TRANSPOSE',
    'INCREMENT', 'DECREMENT', 'MULTIPLY_ASSIGN', 'DIVIDE_ASSIGN',
    'LESSER', 'GREATER', 'LESSER_EQUAL', 'GREATER_EQUAL', 'EQUALS', 'NOT_EQUAL',
    'RANGE', 'COMMA', 'SEMICOLON', 'ID'
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


def t_FLOATNUMBER(t):
    r"(?:\d+\.\d*|\.\d+)(?:[eE]-?\d+)?|\d+[eE]-?\d+"
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'ID')
    return t


# Ignored characters
t_ignore = " \t"

t_ignore_COMMENT = r'[#].*'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
class Scanner:
    def __init__(self):
        self.lexer = lex.lex()
