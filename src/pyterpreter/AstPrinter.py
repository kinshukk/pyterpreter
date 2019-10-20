from Expr import *
from Token import *
from TokenType import *

#TODO: But how does ABC work?

class AstPrinter(Visitor):
    def __init__(self):
        pass

    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def parenthesize(self, name: str, *args) -> str:
        res = f"({name}"

        for expr in args:
            res += f" {expr.accept(self)}"

        res += ")"

        return res

    def visitBinaryExpr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: Literal) -> str:
        if expr.value == None:
            return "nil"

        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

if __name__ == "__main__":
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, '-', None, 1),
            Literal(42)
        ),
        Token(TokenType.SLASH, "*", None, 1),
        Grouping(
            Literal(3.14159)
        )
    )

    printer = AstPrinter()

    print(printer.print(expression))
