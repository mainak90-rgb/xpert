class Position:
    def __init__(self, ln: int, col: int, idx: int, fname: str, ftxt: str) -> None:
        self.ln = ln
        self.col = col
        self.idx = idx
        self.fn = fname
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0
        # return self

    def copy(self):
        return Position(self.ln, self.col, self.idx, self.fn, self.ftxt)
