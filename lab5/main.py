import sys
import ply.yacc as yacc
import scanner
import Mparser
import TreePrinter
from TypeChecker import TypeChecker
from Interpreter import Interpreter

if __name__ == '__main__':

    examples = ['fibonacci.m', 'pi.m', 'primes.m', 'sqrt.m', 'triangle.m', 'matrix.m']

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else 'lab5/examples/' + examples[5]
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()

    ast = parser.parse(text, lexer=scanner.lexer)

    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)

    # ast.accept(Interpreter())
    Interpreter().visit(ast)

    # in future
    # ast.accept(OptimizationPass1())
    # ast.accept(OptimizationPass2())
    # ast.accept(CodeGenerator())
