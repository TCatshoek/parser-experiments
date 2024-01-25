from typing import List


class ParseError(Exception):
    def __init__(self, position, char):
        self.position = position
        self.char = char

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"Parse error at position: {self.position}, char: {self.char}"


def tokenize(input_string: str):
    tokens = []
    position = 0

    while position < len(input_string):
        char = input_string[position]

        if char.isspace():
            position += 1

        elif char.isnumeric():
            scan_pos = position
            while scan_pos < len(input_string) and input_string[scan_pos].isnumeric():
                scan_pos += 1
            tokens.append(("NUMBER", int(input_string[position:scan_pos])))
            position = scan_pos

        elif char == "+":
            tokens.append(("ADD", char))
            position += 1

        elif char == "-":
            tokens.append(("SUB", char))
            position += 1

        elif char == "*":
            tokens.append(("MUL", char))
            position += 1

        elif char == "/":
            tokens.append(("DIV", char))
            position += 1

        elif char == "(":
            tokens.append(("LPAREN", char))
            position += 1

        elif char == ")":
            tokens.append(("RPAREN", char))
            position += 1

        else:
            raise ParseError(position, char)

    return tokens

"""
Recursive Descent Parser for the following grammar:

expression     ::= term { ("+" | "-") term }
term           ::= factor { ("*" | "/") factor }
factor         ::= number | "(" expression ")"
number         ::= [0-9]+

"""

class BinOp:
    __match_args__ = ("op", "left", "right")

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"

class Num:
    __match_args__ = ("n",)

    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return str(self.n)


class TokenStream:
    def __init__(self, tokens: List):
        self._tokens = tokens
        self._pos = 0

    def __next__(self):
        if self._pos < len(self._tokens):
            item = self._tokens[self._pos]
            self._pos += 1
            return item
        else:
            raise StopIteration

    def peek(self, n=0):
        if self._pos + n >= len(self._tokens):
            return None
        return self._tokens[self._pos + n]



def parse(tokens):
    return parse_expression(TokenStream(tokens))

def parse_expression(tokens):
    left = parse_term(tokens)

    while next_token := tokens.peek():
        match next_token:
            case ("ADD" | "SUB", op):
                next(tokens)
                right = parse_term(tokens)
                left = BinOp(op, left, right)
            case _:
                break

    return left

def parse_term(tokens):
    left = parse_factor(tokens)

    while next_token := tokens.peek():
        match next_token:
            case ("MUL" | "DIV", op):
                next(tokens)
                right = parse_factor(tokens)
                left = BinOp(op, left, right)
            case _:
                break

    return left

def parse_factor(tokens):
    token = next(tokens, None)
    match token:

        case ("NUMBER", n):
            return Num(n)

        case ("LPAREN", _):
            expr = parse_expression(tokens)

            if next(tokens, None) != ("RPAREN", ")"):
                raise ParseError(tokens._pos, "Expected closing bracket")

            return expr

def evaluate(expression):
    match expression:
        case Num(n):
            return n
        case BinOp(op, left, right):
            match op:
                case "+":
                    return evaluate(left) + evaluate(right)
                case "-":
                    return evaluate(left) - evaluate(right)
                case "/":
                    return evaluate(left) / evaluate(right)
                case "*":
                    return evaluate(left) * evaluate(right)

if __name__ == "__main__":
    input_string = "100 / 2 + 1"
    tokens = tokenize(input_string)
    ast = parse(tokens)
    answer = evaluate(ast)
    print(answer)
