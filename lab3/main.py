
import sys
import ply.yacc as yacc
from lab2 import Mparser
from lab1 import scanner

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    # Mparser = Mparser()
    # parser = yacc.yacc(module=Mparser)
    parser = Mparser.parser

    text = file.read()
    ast = parser.parse(text, lexer=scanner.lexer)
    print(ast)
    ast.printTree()