from typing import List

from Token import *
from TokenType import *
from Expr import *

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def peek(self) -> TokenType:
        return self.tokens[self.current]

    def isAtEnd(self) -> bool:
        return self.peek().type == EOF

    def previous(self) -> TokenType:
        return self.tokens[self.current - 1]

    def advance(self) -> TokenType:
        if not self.isAtEnd():
            self.current += 1

        return self.previous()

    def check(self, type_: TokenType) -> bool:
        '''
            Return True if current token is of type type_
        '''
        if self.isAtEnd():
            return False

        return self.peek().tokentype == type_

    def match(self, types: List[TokenType]) -> bool:
        '''
            Check if current token is of any type in types. 
            If yes, consume it and return True, else False
        '''
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True

        return False

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        '''
            equality -> comparison ( ('!' | '-') comparison )* 
        '''
        #consume left comparison
        left = self.comparison()

        while self.match([BANG_EQUAL, EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            left = Binary(left, operator, right)

        return left

    def comparison(self) -> Expr:
        '''
            comparison -> addition ( ('<' | '>' | '<=' | '>=') addition )*
        '''

        left = self.addition()

        while self.match([LESS, GREATER, LESS_EQUAL, GREATER_EQUAL]):
            operator = self.previous()
            right = self.addition()
            left = Binary(left, operator, right)

        return left

    def addition(self) -> Expr:
        '''
            addition -> multiplication ( ( '+' | '-' ) multiplication )*
        '''
        left = self.multiplication()

        while self.match([PLUS, MINUS]):
            operator = self.previous()
            right = self.multiplication()
            left = Binary(left, operator, right)

        return left

    def multiplication(self) -> Expr:
        '''
            multiplication -> unary ( ( '/' | '-' ) unary )*
        '''
        left = self.unry()

        while self.match([SLASH, STAR]):
            operator = self.previous()
            right = self.unary()
            left = Binary(left, operator, right)

        return left
        

    def unary(self) -> Expr:
        '''
            unary -> ( '!' | '-' ) unary | primary
        '''
        if self.match([BANG, MINUS]):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        else:
            return self.primary()

    def primary(self) -> Expr:
        '''
            primary -> NUMBER | STRING | "false" | "true" | "nil" | "(" expression ")"
        '''
        if self.match([FALSE]):
            return Literal(False)
        if self.match([TRUE]):
            return Literal(True)
        if self.match([NIL]):
            return Literal(None)

        if self.match([NUMBER, STRING]):
            return Literal(self.previous().literal)

        if self.match([LEFT_PAREN]):
            expr = self.expression()
            self.consume(RIGHT_PAREN, "Expected ')' after expression")
            return Grouping(expr)
