from abc import ABC, abstractmethod
from Token import *

from Stmt import *
from Expr import *

class Visitor(ABC):
    @abstractmethod
    def visitBinaryExpr(self, expr: Binary):
        pass

    @abstractmethod
    def visitGroupingExpr(self, expr: Grouping):
        pass

    @abstractmethod
    def visitLiteralExpr(self, expr: Literal):
        pass

    @abstractmethod
    def visitUnaryExpr(self, expr: Unary):
        pass

    @abstractmethod
    def visitExpressionStmt(self, stmt: Expression):
        pass

    @abstractmethod
    def visitPrintStmt(self, stmt: Print):
        pass

