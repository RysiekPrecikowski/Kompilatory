import sys
import ply.yacc as yacc
from lab3 import Mparser
from lab3 import TreePrinter
from TypeChecker import TypeChecker
from lab1 import scanner

if __name__ == '__main__':
    files = [
        "control_transfer.m",
        "init.m",
        "opers.m"
    ]

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else files[2]
        # filename = file
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)


    parser = Mparser.parser
    text = file.read()
    ast = parser.parse(text, lexer=scanner.lexer)
    ast.printTree()
    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)
