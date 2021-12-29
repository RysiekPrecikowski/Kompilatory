import sys
import ply.yacc as yacc
from lab3 import Mparser
from lab3 import TreePrinter
from TypeChecker import TypeChecker
from lab1 import scanner

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "control_transfer.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    # Mparser = Mparser()
    # parser = yacc.yacc(module=Mparser)
    # text = file.read()
    #
    # ast = parser.parse(text, lexer=Mparser.scanner)

    parser = Mparser.parser
    text = file.read()
    ast = parser.parse(text, lexer=scanner.lexer)

    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)
