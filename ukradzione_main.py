import sys
import ukradzione as scanner

def tokens(input):
    lexer = scanner.lexer
    lexer.input(text)
    while token := lexer.token():
        yield token


if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else 'example.txt'

    text = """
    A = zeros(5);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
I = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere
D1 = A.+B' ; # add element-wise A with transpose of B
D2 -= A.-B' ; # substract element-wise A with transpose of B
D3 *= A.*B' ; # multiply element-wise A with transpose of B
D4 /= A./B' ; # divide element-wise A with transpose of B


    """

    # try:
    #     with open(filename) as file:
    #         text = file.read()
    # except IOError:
    #     print("Cannot open {0} file".format(filename))
    #     sys.exit(0)

    for tok in tokens(text):
        print("(%d): %s(%s)" % (tok.lineno, tok.type, tok.value))