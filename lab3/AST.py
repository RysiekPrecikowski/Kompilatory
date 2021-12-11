
class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):

    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class String(Node):
    def __init__(self, value):
        self.value = value


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryMinus(Node):
    def __init__(self, expr):
        self.expr = expr

class ProgramBlock(Node):
    def __init__(self, stmt=None):
        if stmt is None:
            self.stmts = []
        else:
            self.stmts = [stmt]


class Return(Node):
    def __init__(self, expr):
        self.expr = expr


class While(Node):
    def __init__(self, cond, stmt):
        self.condition = cond
        self.stmt = stmt


class For(Node):
    def __init__(self, _id, _range, _stmt):
        self.id = _id
        self.range = _range
        self.stmt = _stmt


class Range(Node):
    def __init__(self, _min, _max):
        self.min = _min
        self.max = _max


class If(Node):
    def __init__(self, cond, true, false=None):
        self.cond = cond
        self.true = true
        self.false = false


class Break(Node):
    pass


class Continue(Node):
    pass


class FunctionCall(Node):
    def __init__(self, fun, args):
        self.fun = fun
        self.args = args


class Assign(Node):
    def __init__(self, type, id, val):
        self.type = type
        self.id = id
        self.val = val


class Transposition(Node):
    def __init__(self, val):
        self.val = val


class MatrixOperation(Node):
    def __init__(self, type, identifier, index, value):
        self.type = type
        self.identifier = identifier
        self.index = index
        self.value = value


class IDX(Node):
    def __init__(self, values=None):
        if values is None:
            values = []
        self.values = values


class MatrixReference(Node):
    def __init__(self, target, idx):
        self.target = target
        self.idx = idx

class Error(Node):
    def __init__(self):
        pass
