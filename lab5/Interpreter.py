
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
from collections import defaultdict
import numpy as np

sys.setrecursionlimit(10000)

operations = {}

operations['+'] = lambda a, b: a + b
operations['-'] = lambda a, b: a - b
operations['*'] = lambda a, b: a * b
operations['/'] = lambda a, b: a / b

operations['<'] = lambda a, b: a < b
operations['>'] = lambda a, b: a > b
operations['=='] = lambda a, b: a == b
operations['!='] = lambda a, b: a != b
operations['<='] = lambda a, b: a <= b
operations['>='] = lambda a, b: a >= b



class Interpreter(object):

    def __init__(self):
        self.memory = Memory()
        self.stack = MemoryStack()


    @on('node')
    def visit(self, node):
        pass

    @when(AST.Node)
    def visit(self, node: AST.Node):
        pass

    @when(AST.IntNum)
    def visit(self, node: AST.IntNum):
        self.stack.push(node.value)

    @when(AST.FloatNum)
    def visit(self, node: AST.FloatNum):
        node.value = float(node.value)
        self.stack.push(node.value)

    @when(AST.Variable)
    def visit(self, node: AST.Variable):
        self.stack.push(self.memory.get(node.name))

    @when(AST.String)
    def visit(self, node: AST.String):
        self.stack.push(node.value)
        
    @when(AST.BinExpr)
    def visit(self, node: AST.BinExpr):
        self.visit(node.left)
        self.visit(node.right)

        r = self.stack.pop()
        l = self.stack.pop()

        op = node.op if node.op[0] != '.' else node.op[1:]

        self.stack.push(operations[op](l, r))

    @when(AST.UnaryMinus)
    def visit(self, node: AST.UnaryMinus):
        self.visit(node.expr)
        self.stack.push(-self.stack.pop())

    @when(AST.ProgramBlock)
    def visit(self, node: AST.ProgramBlock):
        for stmt in node.stmts:
            self.visit(stmt)

    @when(AST.While)
    def visit(self, node: AST.While):
        self.visit(node.condition)
        cond = self.stack.pop()
        
        self.memory = Memory(self.memory)
        try:
            while cond:
                try:
                    self.visit(node.stmt)
                except ContinueException:
                    pass
                self.visit(node.condition)
                cond = self.stack.pop()
        except BreakException:
            pass
        finally:
            self.memory = self.memory.parent

    @when(AST.For)
    def visit(self, node: AST.For):
        for_id = node.id.name
        self.visit(node.range)
        for_range = self.stack.pop()
        
        self.memory = Memory(self.memory)
        try:
            for v in for_range:
                self.memory.put(for_id, v)
                try:
                    self.visit(node.stmt)
                except ContinueException:
                    pass
        except BreakException:
            pass
        finally:
            self.memory = Memory(self.memory)

    @when(AST.Range)
    def visit(self, node: AST.Range):
        self.visit(node.min)
        self.visit(node.max)
        max_value = self.stack.pop()
        min_value = self.stack.pop()
        self.stack.push(range(min_value, max_value + 1))

    @when(AST.If)
    def visit(self, node: AST.If):
        self.visit(node.cond)
        cond = self.stack.pop()
        if cond:
            self.visit(node.true)
        else:
            self.visit(node.false)

    @when(AST.Break)
    def visit(self, node: AST.Break):
        raise BreakException

    @when(AST.Continue)
    def visit(self, node: AST.Continue):
        raise ContinueException

    @when(AST.FunctionCall)
    def visit(self, node: AST.FunctionCall):
        for arg in node.args:
            self.visit(arg) 


        if len(node.args) == 1:
            arg = self.stack.pop()
            args = (arg, arg)
        else:
            args = tuple([self.stack.pop() for _ in range(len(node.args))])

        if node.fun == 'zeros':
            self.stack.push(np.zeros(args))
        elif node.fun == 'ones':
            self.stack.push(np.ones(args))        
        elif node.fun == 'eye':
            self.stack.push(np.eye(*args))
        elif node.fun == 'print':
            for arg in node.args:
                self.visit(arg)
            for arg in reversed([self.stack.pop() for _ in range(len(node.args))]):
                print(arg, end = " ")
            print()
 

    @when(AST.Assign)
    def visit(self, node: AST.Assign):
        if node.type == '=':
            if isinstance(node.id, AST.MatrixReference):
                self.visit(node.id.target)
                target = self.stack.pop()

                self.visit(node.val)
                value = self.stack.pop()

                for idx in node.id.idx.values:
                    self.visit(idx)
                
                indices = [None for _ in range(len(node.id.idx.values))]

                for i, idx in enumerate(reversed([self.stack.pop() for _ in node.id.idx.values])):
                    if isinstance(idx, range):
                        indices[i] = slice(idx.start, idx.stop)
                    else:
                        indices[i] = idx


                target[tuple(indices)] = value

            else:
                self.visit(node.val)
                self.memory.put(node.id.name, self.stack.pop())
        else:
            self.visit(AST.BinExpr(node.line, node.type[:-1], node.id, node.val))
            self.memory.put(node.id.name, self.stack.pop())

    @when(AST.Transposition)
    def visit(self, node: AST.Transposition):
        self.visit(node.val)
        M = self.stack.pop()
        self.stack.push(M.T)

    @when(AST.IDX)
    def visit(self, node: AST.IDX):
        for value in node.values:
            self.visit(value)

        values = [self.stack.pop() for _ in range(len(node.values))]
        values.reverse()
        self.stack.push(np.array(values))

    @when(AST.MatrixReference)
    def visit(self, node: AST.MatrixReference):
        self.visit(node.target)
        target = self.stack.pop()

        for idx in node.idx.values:
            self.visit(idx)

        indices = [None for _ in range(len(node.idx.values))]

        for i, idx in enumerate(reversed([self.stack.pop() for _ in node.idx.values])):
            if isinstance(idx, range):
                indices[i] = slice(idx.start, idx.stop)
            else:
                indices[i] = idx

        self.stack.push(target[tuple(indices)])

    @when(AST.Error)
    def visit(self, node: AST.Error):
        pass

