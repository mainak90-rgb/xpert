from error import InvalidSyntaxError
from tokens import *

###########################################
# NODES
###########################################


# Number node class

class NumberNode:
    def __init__(self, token):
        self.tok = token

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self) -> str:
        return f'{self.tok}'


# Binary operator node class

class BinaryOpNode:
    def __init__(self, token, right, left) -> None:
        self.tok = token
        self.right = right
        self.left = left

        self.pos_start = self.left.pos_start
        self.pos_end = self.right.pos_end

    def __repr__(self) -> str:
        return f'({self.left}, {self.tok}, {self.right})'

# Unary operator node class


class UnaryOpNode:
    def __init__(self, token, node) -> None:
        self.tok = token
        self.node = node

        self.pos_start = self.tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self) -> str:
        return f'({self.tok}, {self.node})'


###########################################
# PARSER
###########################################

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.idx = -1
        self.advance()

    def advance(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.current_tok = self.tokens[self.idx]
        return self.current_tok

    #################################

    # Parse func
    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                "Expected '+', '-', '*','/','^' or '%'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))
        return res

    # Expression func
    def expr(self):
        return self.binaryOp(self.term, self.term, (TT_PLUS, TT_MINUS))

    # Term func
    def term(self):
        return self.binaryOp(self.factor, self.factor, (TT_MUL, TT_DIV, TT_MOD))

    #Factor func
    def factor(self):
        result = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            result.register(self.advance())
            factor = result.register(self.factor())
            if result.error:
                return result
            return result.success(UnaryOpNode(tok, factor))

        return self.power()

    # Power func
    def power(self):
        return self.binaryOp(self.block, self.factor, (TT_POW,))

    # Block func
    def block(self):
        result = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            result.register(self.advance())
            return result.success(NumberNode(tok))

        elif tok.type == TT_LPAREN:
            result.register(self.advance())
            expr = result.register(self.expr())
            if result.error:
                return result
            if self.current_tok.type == TT_RAPREN:
                result.register(self.advance())
                return result.success(expr)
            else:
                return result.failure(InvalidSyntaxError("Expected ')'", self.current_tok.pos_start, self.current_tok.pos_end))

        return result.failure(InvalidSyntaxError("Expected int or float or '('", tok.pos_start, tok.pos_end))

    ####################################

    # Binary operation func
    def binaryOp(self, func1, func2, tokens: tuple):
        result = ParseResult()
        left = result.register(func1())
        if result.error:
            return result

        while self.current_tok.type in tokens:
            tok = self.current_tok
            result.register(self.advance())
            right = result.register(func2())
            if result.error:
                return result
            left = BinaryOpNode(tok, right, left)

        return result.success(left)


###########################################
# PARSE_RESULT
###########################################

class ParseResult:
    def __init__(self) -> None:
        self.node = None
        self.error = None

    ######################

    def register(self, result):
        if isinstance(result, ParseResult):
            if result.error:
                self.error = result.error
            return result.node

        return result

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self
