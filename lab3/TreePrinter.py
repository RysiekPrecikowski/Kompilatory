from lab3 import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.value))

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.name))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.value))

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.UnaryMinus)
    def printTree(self, indent=0):
        print("|  " * indent + "UNARYMINUS")
        self.expr.printTree(indent + 1)

    @addToClass(AST.ProgramBlock)
    def printTree(self, indent=0):
        for stmt in self.stmts:
            stmt.printTree(indent)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print("|  " * indent + "RETURN")
        self.expr.printTree(indent + 1)


    @addToClass(AST.While)
    def printTree(self, indent=0):
        print("|  " * indent + "WHILE")
        self.condition.printTree(indent + 1)
        self.stmt.printTree(indent + 1)


    @addToClass(AST.For)
    def printTree(self, indent=0):
        print("|  " * indent + "FOR")
        self.id.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.stmt.printTree(indent + 1)


    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print("|  " * indent + "RANGE")
        self.min.printTree(indent + 1)
        self.max.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print("|  " * indent + "IF")
        self.cond.printTree(indent + 1)
        print("|  " * indent + "THEN")
        self.true.printTree(indent + 1)
        if self.false:
            print("|  " * indent + "ELSE")
            self.false.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print("|  " * indent + "BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print("|  " * indent + "CONTINUE")

    @addToClass(AST.FunctionCall)
    def printTree(self, indent=0):
        print("|  " * indent + self.fun)
        for arg in self.args:
            arg.printTree(indent+1)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        print("|  " * indent + self.type)
        self.id.printTree(indent + 1)
        self.val.printTree(indent + 1)

    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        print("|  " * indent + "TRANSPOSE")
        self.val.printTree(indent+1)

    @addToClass(AST.MatrixOperation)
    def printTree(self, indent=0):
        print("|  " * indent + self.type)
        self.identifier.printTree(indent+1)
        self.index.printTree(indent + 1)
        self.value.printTree(indent + 1)

    @addToClass(AST.IDX)
    def printTree(self, indent=0):
        print("|  " * indent + "IDX")
        for v in self.values:
            v.printTree(indent + 1)

    @addToClass(AST.MatrixReference)
    def printTree(self, indent=0):
        print("| " * indent + "REF")
        self.target.printTree(indent+1)
        self.idx.printTree(indent+1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        print("| " * indent + "ERROR !!!")
