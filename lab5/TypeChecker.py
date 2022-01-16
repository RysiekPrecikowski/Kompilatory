from collections import defaultdict

import AST
from SymbolTable import SymbolTable


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if not node:
            return #TODO
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class ArrayT:
    def __init__(self, dims, eltype, size):
        self.dims = dims
        self.eltype = eltype
        self.size = size

    def __hash__(self):
        return hash((self.dims, self.eltype, self.size))

    def __eq__(self, other):
        if not isinstance(other, ArrayT):
            return False
        if self.dims != other.dims:
            return False
        if self.eltype != other.eltype:
            return False

        for s1, s2 in zip(self.size, other.size):
            if s1 != s2:
                return False
        return True

    def __repr__(self):
        return f"Array (d: {self.dims} s: {self.size} eltype: {self.eltype})"


AnyT = 'any'
IntT = 'int'
FloatT = 'float'
StringT = 'string'
RangeT = 'range'
BoolT = 'bool'

type_table = defaultdict(
    lambda: defaultdict(
        lambda: defaultdict(
            lambda: AnyT
        ))
)

for operator in '+-*/':
    type_table[operator][IntT][IntT] = IntT
    type_table[operator][IntT][FloatT] = FloatT
    type_table[operator][FloatT][IntT] = FloatT
    type_table[operator][FloatT][FloatT] = FloatT

type_table['*'][StringT][IntT] = StringT

for operator in ['<', '<=', '>', '>=', '!=', '==']:
    type_table[operator][IntT][IntT] = BoolT
    type_table[operator][IntT][FloatT] = BoolT
    type_table[operator][FloatT][FloatT] = BoolT
    type_table[operator][FloatT][FloatT] = BoolT

for operator in ['==', '!=']:
    type_table[operator][StringT][StringT] = BoolT


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.loop_count = 0

    def visit_FloatNum(self, node):
        return FloatT

    def visit_IntNum(self, node):
        return IntT

    def visit_Variable(self, node: AST.Variable):
        type1 = self.symbol_table.get(node.name)
        # print(type1, node.name)
        if type1 is None:
            print(f'Line {node.line}: Cannot find variable: {node.name}')
            return AnyT
        return type1

    def visit_String(self, node):
        return StringT

    def visit_BinExpr(self, node: AST.BinExpr):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        operator = node.op

        # print(type_left, node.right)

        if operator[0] == '.':
            op = operator[1:]
            type1 = type_left.eltype if isinstance(type_left, ArrayT) else type_left
            type2 = type_right.eltype if isinstance(type_right, ArrayT) else type_right

            # print(type_left, type_right)

            if isinstance(type_left, ArrayT) or isinstance(type_right, ArrayT):
                type3 = type_table[op][type1][type2]
                if type3 == AnyT:
                    print(
                        f'Line {node.line}: Can not apply {op} for {type1} and {type2}, expression will result in any type')

                return ArrayT(type_right.dims, type3, type_right.size)

            print(f'Line {node.line}: Cannnot apply {op} for {type1} and {type2}, at least one argument must be array')
            return AnyT

        result_type = type_table[operator][type_left][type_right]

        if result_type == AnyT:
            print(
                f'Line {node.line}: Cannot use {operator} with {type_left} , {type_right}')
        return result_type

    def visit_UnaryMinus(self, node: AST.UnaryMinus):
        expr_type = self.visit(node.expr)

        if expr_type not in [FloatT, IntT]:
            print(f'Line {node.line}: cannot use unary minus with {expr_type}')
        return expr_type

    def visit_ProgramBlock(self, node: AST.ProgramBlock):
        self.symbol_table.pushScope()
        self.visit(node.stmts)

    def visit_Return(self, node: AST.Return):
        self.visit(node.expr)
        print(f"Line {node.line}: return outside function")
        return None

    def visit_While(self, node: AST.While):
        self.loop_count += 1

        condt = self.visit(node.condition)
        if condt != BoolT:
            print(f'Line {node.line}: While condition is not boolean')

        self.symbol_table.pushScope()
        self.visit(node.stmt)
        self.symbol_table.popScope()

        self.loop_count -= 1

    def visit_For(self, node: AST.For):
        self.loop_count += 1
        type1 = self.visit(node.range)
        if type1 != 'range':
            print(f'Line {node.line}: For loop error')

        # self.symbol_table.pushScope()
        # self.symbol_table.current_scope.put(node.id, IntT)
        self.symbol_table.put(node.id.name, IntT)

        self.visit(node.stmt)

        self.symbol_table.popScope()
        self.loop_count -= 1

    def visit_Range(self, node):
        if not self.visit(node.min) == self.visit(node.max) == IntT:
            print(f"Line {node.line}: Range extremes must be integers")
        return RangeT

    def visit_If(self, node: AST.If):
        condt = self.visit(node.cond)
        if condt != BoolT:
            print(f'Line {node.line}: If condition is not boolean')

        self.symbol_table.pushScope()
        self.visit(node.true)
        self.symbol_table.popScope()

        self.symbol_table.pushScope()
        self.visit(node.false)
        self.symbol_table.popScope()

    def visit_Break(self, node: AST.Break):
        if self.loop_count == 0:
            print(f"Line {node.line}: Using break outside of loop")

    def visit_Continue(self, node: AST.Continue):
        if self.loop_count == 0:
            print(f"Line {node.line}: Using continue outside of loop")

    def visit_FunctionCall(self, node: AST.FunctionCall):
        self.visit(node.args)

        if node.fun == 'print':
            self.visit(node.args)
            return

        if node.fun in ['zeros', 'eye', 'ones']:
            if len(node.args) == 1:
                return ArrayT(2, IntT, (node.args[0].value, node.args[0].value))

            return ArrayT(len(node.args), IntT, tuple(arg.value for arg in node.args))
        return AnyT

    def visit_Assign(self, node: AST.Assign):
        type1 = self.visit(node.val)
        if isinstance(node.id, AST.MatrixReference):
            type2 = self.symbol_table.get(node.id.target.name)
            if type1 != type2.eltype:
                print(f"Line {node.line}: Wrong types {type2.eltype}, {type1}")
            return type1
        else:
            self.symbol_table.put(node.id.name, type1)
        # print(f"doddaje {node.id.name, type1}")
        return type1

    def visit_Transposition(self, node: AST.Transposition):
        type1 = self.symbol_table.get(node.val.name)
        if not isinstance(type1, ArrayT):
            print(f"Line {node.line}: Cannot transpose {type1}")
            return ArrayT(2, AnyT, (None, None))
        if type1.dims != 2:
            print(f"Line {node.line}: Cannot transpose {type1}")
            return ArrayT(2, type1.eltype, (None, None))
        m, n = type1.size
        return ArrayT(2, type1.eltype, (n, m))

    def visit_IDX(self, node: AST.IDX):
        types = list(map(self.visit, node.values))
        eltype = types[0]
        if any(eltype != t for t in types):
            if isinstance(eltype, ArrayT):
                print(f"Line {node.line}: Inconsistant vector lengths")
                return ArrayT(eltype.dims + 1, eltype.eltype, (len(types),) + eltype.size)

            print(f'Line {node.line}: Inconsistant vector value types')
            return ArrayT(1, AnyT, (len(types),))

        # if isinstance(eltype, ArrayT):
        #     return ArrayT(eltype.dims + 1, eltype.eltype, (len(types),) + eltype.size)
        return ArrayT(1, eltype, (len(types),))

    def visit_MatrixReference(self, node: AST.MatrixReference):
        targett = self.symbol_table.get(node.target.name) if isinstance(node.target, AST.Variable) else self.visit(
            node.target)

        if targett == StringT and len(node.idx.values) != 1:
            print(f"Line {node.line}: Indexing string with {len(node.idx.values)} dimensions")
            return IntT
        if isinstance(targett, ArrayT):
            if len(node.idx.values) != targett.dims:
                print(f"Line {node.line}: Indexing {targett.dims}d array with {len(node.idx.values)} dimensions")

            indices = [i.value for i in node.idx.values]

            for i, m in zip(indices, targett.size):
                if not 1 <= i <= m:
                    print(f"Line {node.line}: Index out of range")
                    break

            return targett.eltype
        print(f"Line {node.line}: {targett} is not indexable")
        return AnyT

    def visit_Error(self, node: AST.Error):
        pass
