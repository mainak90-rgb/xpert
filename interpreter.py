from tokens import *
from error import RTError


#######################################
# RUNTIME RESULT
#######################################

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self


###########################################
# NUMBER
###########################################

class Number:
    def __init__(self, value) -> None:
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def mul_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def div_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    'Division by zero',
                    other.pos_start, other.pos_end, self.context
                )
            return Number(self.value / other.value).set_context(self.context), None

    def __repr__(self) -> str:
        return str(self.value)

#######################################
# CONTEXT
#######################################


class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos


###########################################
# INTERPRETER
###########################################


class Interpreter:
    def visit(self, node,context:Context):
        method_name = f'visit_{type(node).__name__}'
        # print(method)
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context:Context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ##############################

    def visit_NumberNode(self, node, context:Context):
        return RTResult().success(Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_BinaryOpNode(self, node, context:Context):
        res = RTResult()
        left = res.register(self.visit(node.left, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right, context))
        if res.error:
            return res

        if node.tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.tok.type == TT_MUL:
            result, error = left.mul_by(right)
        elif node.tok.type == TT_DIV:
            result, error = left.div_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context:Context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        error = None

        if node.tok.type == TT_MINUS:
            number, error = number.mul_by(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
