from scanner import Scanner

def tokens(input):
    scanner = Scanner()
    scanner.lexer.input(input)
    while token := scanner.lexer.token():
        yield token

def main():
    text = """A = zeros(5);  # create 5x5 matrix filled with zeros
        B = ones(7);   # create 7x7 matrix filled with ones
        I = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere
        D1 = A.+B' ; # add element-wise A with transpose of B
        D2 -= A.-B' ; # substract element-wise A with transpose of B
        D3 *= A.*B' ; # multiply element-wise A with transpose of B
        D4 /= A./B' ; # divide element-wise A with transpose of B
        """

    for tok in tokens(text):
        print("(%d): %s (%s)" % (tok.lineno, tok.type, tok.value))

if __name__ == '__main__':
    main()
