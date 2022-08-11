from error import IllegalCharecterError
import position
from tokens import *


###########################################
# LEXER
###########################################

class Lexer:
    def __init__(self, fn: str, text: str) -> None:
        self.text = text
        self.pos = position.Position(0, -1, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self) -> None:
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char:
            if self.current_char in IGNORE:
                self.advance()

            elif self.current_char == TV_PLUS:
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                # tp = Token(TT_PLUS, pos_start=self.pos)
                pos = self.pos.copy()
                self.advance()
                # if self.current_char == TV_PLUS:
                #     tokens.append(Token(TT_INC, pos_start=pos, pos_end=self.pos))
                #     self.advance()
                # else: tokens.append(tp)

            elif self.current_char == TV_MINUS:
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                # tm = Token(TT_MINUS, pos_start=self.pos)
                # pos = self.pos.copy()
                self.advance()
                # if self.current_char == TV_MINUS:
                #     tokens.append(Token(TT_DEC, pos_start=pos, pos_end=self.pos))
                #     self.advance()
                # else: tokens.append(tm)

            elif self.current_char == TV_MUL:
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()

            elif self.current_char == TV_DIV:
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()

            elif self.current_char == TV_LPAREN:
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()

            elif self.current_char == TV_RAPREN:
                tokens.append(Token(TT_RAPREN, pos_start=self.pos))
                self.advance()

            elif self.current_char in DIGITS:
                tokens.append(self.make_number())

            else:
                char = self.current_char
                pos_start = self.pos.copy()
                self.advance
                return [], IllegalCharecterError("'" + char + "'", pos_start, self.pos)

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self) -> Token:
        num_str = ''
        dot_count = 0
        pos = self.pos.copy()

        while self.current_char and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos, self.pos)
