from scanner import lexer
import sys

def tokens(input):
    lexer.input(input)
    while token := lexer.token():
        yield token

def main():
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer.input(text)  # Give the lexer some input

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print("%d: %s ( %s )" % (tok.lineno, tok.type, tok.value))

if __name__ == '__main__':
    main()
