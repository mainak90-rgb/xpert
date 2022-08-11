###########################################
# CONSTANTS
###########################################

DIGITS = '0123456789'
IGNORE = '; \t'

###########################################
# TOKENS
###########################################

# List of tokens

TT_INT      ='INT'
TT_FLOAT    ='FLOAT'
TT_PLUS     ='PLUS'
TT_MINUS    ='MINUS'
TT_MUL      ='MUL'
TT_DIV      ='DIV'
TT_INC      ='INC'  # ++
TT_DEC      ='DEC'  # --
TT_LPAREN   ='LPAREN'
TT_RAPREN   ='RAPREN'
TT_EOF      ='EOF'  # End of file

# Values of every tokens
TV_INT      ='int'
TV_FLOAT    ='float'
TV_PLUS     ='+'
TV_MINUS    ='-'
TV_MUL      ='*'
TV_DIV      ='/'
TV_LPAREN   ='('
TV_RAPREN   =')'


class Token:
    def __init__(self, type, value=None, pos_start = None, pos_end = None) -> None:
        self.type = type
        self.value = value
        
        if pos_start: 
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
            
        if pos_end:
            self.pos_end = pos_end.copy()
    
    def __repr__(self) -> str:
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'