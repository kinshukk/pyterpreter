from Expr import *
from TokenType import *
from ErrorHandler import *
from RuntimeError_ import *

class Interpreter(Visitor):
    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler

    def visitBinaryExpr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        typ_ = expr.operator.tokentype

        if typ_ == TokenType.MINUS:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) - float(right)
        
        elif typ_ == TokenType.PLUS:
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            
            elif isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            
            else:
                raise RuntimeError_(expr.operator, "Operands must be both numbers or both strings")
        
        elif typ_ == TokenType.SLASH:
            #TODO: Check Values? IEEE 754 rules?
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) / float(right)

        elif typ_ == TokenType.STAR:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) * float(right)
        
        elif typ_ == TokenType.GREATER:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) > float(right)

        elif typ_ == TokenType.GREATER_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) >= float(right)
        
        elif typ_ == TokenType.LESS:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) < float(right)
        
        elif typ_ == TokenType.LESS_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) <= float(right)

        elif typ_ == TokenType.BANG_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return not (left == right)

        elif typ_ == TokenType.EQUAL_EQUAL:
            return left == right


    def visitGroupingExpr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visitLiteralExpr(self, expr: Literal):
        return expr.value

    def visitUnaryExpr(self, expr: Unary):
        right = self.evaluate(expr.right)

        if expr.operator == TokenType.MINUS:
            self.checkNumberOperand(expr.operator, right)
            return -float(right)

        if expr.operator == TokenType.BANG:
            #TODO: type checks for this?
            return not self.truthyness(right)

        #Something's wrong/Unreachable
        return None

    def checkNumberOperands(self, operator: TokenType, *args):
        for arg in args:
            if not isinstance(arg, float):
                raise RuntimeError_(operator, "Operands must be a number")

    def truthyness(self, thing) -> bool:
        '''
            false and nil evaluate to false, everything else is truthy
        '''
        if thing is None:
            return False
        if isinstance(thing, bool):
            #why cast to bool if it's already instance of bool?
            return bool(thing)

        return True

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def interpret(self, expression: Expr):
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except RuntimeError_ as e:
            self.error_handler.runtimeError(e)
    
    def stringify(self, thing):
        if thing is None:
            return "nil"
        else:
            return str(thing)
