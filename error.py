from position import Position
from string_with_arrows import string_with_arrows

###########################################
# ERRORS
###########################################


class Error:
    def __init__(self, err_name:str, details:str, pos_start: Position, pos_end:Position) -> None:
        self.err_name = err_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end
    
    def as_string(self):
        result  = f'{self.err_name}: {self.details}\n'
        result += f'in File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

################Illegal Charecter Error#################

class IllegalCharecterError(Error):
    def __init__(self, details:str, pos_start:Position, pos_end:Position) -> None:
        super().__init__("Illegal Charecter", details, pos_start, pos_end)
        
        
################Invalid Syntax Error#################

class InvalidSyntaxError(Error):
    def __init__(self, details:str, pos_start:Position, pos_end:Position) -> None:
        super().__init__("Invalid Syntax", details, pos_start, pos_end)
