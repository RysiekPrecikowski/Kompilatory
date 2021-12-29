class Node(object):
    line = ""

class IntNum(Node):
    def __init__(self, line, value):
        self.value = value
        self.line = line


class FloatNum(Node):

    def __init__(self, line, value):
        self.value = value
        self.line = line


class Variable(Node):
    def __init__(self, line, name):
        self.name = name
        self.line = line


class String(Node):
    def __init__(self, line, value):
        self.value = value
        self.line = line


class BinExpr(Node):
    def __init__(self, line, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        self.line = line


class UnaryMinus(Node):
    def __init__(self, line, expr):
        self.expr = expr
        self.line = line


class ProgramBlock(Node):
    def __init__(self, line, stmt=None):
        if stmt is None:
            self.stmts = []
        else:
            self.stmts = [stmt]
        self.line = line


class Return(Node):
    def __init__(self, line, expr):
        self.expr = expr
        self.line = line


class While(Node):
    def __init__(self, line, cond, stmt):
        self.condition = cond
        self.stmt = stmt
        self.line = line


class For(Node):
    def __init__(self, line, _id, _range, _stmt):
        self.id = _id
        self.range = _range
        self.stmt = _stmt
        self.line = line


class Range(Node):
    def __init__(self, line, _min, _max):
        self.min = _min
        self.max = _max
        self.line = line


class If(Node):
    def __init__(self, line, cond, true, false=None):
        self.cond = cond
        self.true = true
        self.false = false
        self.line = line


class Break(Node):
    def __init__(self, line):
        self.line = line


class Continue(Node):
    def __init__(self, line):
        self.line = line


class FunctionCall(Node):
    def __init__(self, line, fun, args):
        self.fun = fun
        self.args = args
        self.line = line


class Assign(Node):
    def __init__(self, line, type, id, val):
        self.type = type
        self.id = id
        self.val = val
        self.line = line


class Transposition(Node):
    def __init__(self, line, val):
        self.val = val
        self.line = line


class MatrixOperation(Node):
    def __init__(self, line, type, identifier, index, value):
        self.type = type
        self.identifier = identifier
        self.index = index
        self.value = value
        self.line = line


class IDX(Node):
    def __init__(self, line, values=None):
        if values is None:
            values = []
        self.values = values
        self.line = line


class MatrixReference(Node):
    def __init__(self, line, target, idx):
        self.target = target
        self.idx = idx
        self.line = line


class Error(Node):
    def __init__(self, line):
        self.line = line

