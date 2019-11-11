from abc import ABC, abstractmethod
from Token import *

from Stmt import *
from Expr import *

class Visitor(ABC):
    @abstractmethod
    def visitAssignExpr(self, expr: Assign):
        pass

    @abstractmethod
    def visitBinaryExpr(self, expr: Binary):
        pass

    @abstractmethod
    def visitCallFunctionExpr(self, expr: CallFunction):
        pass

    @abstractmethod
    def visitGroupingExpr(self, expr: Grouping):
        pass

    @abstractmethod
    def visitLiteralExpr(self, expr: Literal):
        pass

    @abstractmethod
    def visitLogicalExpr(self, expr: Logical):
        pass

    @abstractmethod
    def visitUnaryExpr(self, expr: Unary):
        pass

    @abstractmethod
    def visitVariableExpr(self, expr: Variable):
        pass

    @abstractmethod
    def visitBlockStmt(self, stmt: Block):
        pass

    @abstractmethod
    def visitExpressionStmt(self, stmt: Expression):
        pass

    @abstractmethod
    def visitFunctionStmt(self, stmt: Function):
        pass

    @abstractmethod
    def visitIfStmt(self, stmt: If):
        pass

    @abstractmethod
    def visitPrintStmt(self, stmt: Print):
        pass

    @abstractmethod
    def visitVarStmt(self, stmt: Var):
        pass

    @abstractmethod
    def visitWhileStmt(self, stmt: While):
        pass

