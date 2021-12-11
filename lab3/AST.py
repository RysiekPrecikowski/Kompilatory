
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


class ProgramBlock(Node):
    def __init__(self, stmt):
        self.stmts = [stmt]
# ...
# fill out missing classes
# ...

class Error(Node):
    def __init__(self):
        pass
