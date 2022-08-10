from tokens import *


###########################################
# NUMBER
###########################################

class Number:
    def __init__(self, value) -> None:
        self.value = value
        self.set_pos()
    
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        
    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
    
    def mul_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
        
    def div_by(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)
        
    def __repr__(self) -> str:
        return str(self.value)

###########################################
# INTERPRETER
###########################################

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        # print(method)
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    ##############################
    
    def visit_NumberNode(self, node):
        return Number(node.tok.value).set_pos(node.pos_start, node.pos_end)

    def visit_BinaryOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.tok.type == TT_PLUS:
            result = left.added_to(right)
        elif node.tok.type == TT_MINUS:
            result = left.subbed_by(right)
        elif node.tok.type == TT_MUL:
            result = left.mul_by(right)
        elif node.tok.type == TT_DIV:
            result = left.div_by(right)
        
        return result.set_pos(node.pos_start, node.pos_end)
        
    def visit_UnaryOpNode(self, node):
        number = self.visit(node.node)
        
        if node.tok.type == TT_MINUS:
            number = number.mul_by(Number(-1))
        
        return number.set_pos(node.pos_start, node.pos_end)