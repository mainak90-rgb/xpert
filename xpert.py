from interpreter import Interpreter, Context
from lexer import Lexer
from parser import Parser


def run(text: str, fn: str) -> str:
    # Generate Tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    # Check lexing error
    if error:
        return error.as_string()

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()

    # Check parsing error
    if ast.error:
        return ast.error.as_string()

    # Return the output
    interpreter = Interpreter()
    context = Context("<_main>")
    result = interpreter.visit(ast.node, context)
    if result.error:
        return result.error.as_string()
    return result.value
