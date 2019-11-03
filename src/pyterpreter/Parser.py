from typing import List

from Token import *
from TokenType import *
from Expr import *
from Stmt import *
from ErrorHandler import *

class Parser:
    class ParseError(RuntimeError):
        def __init__(self, message):
            super().__init__(message)

    def __init__(self, tokens: List[Token], error_handler: ErrorHandler, logging: bool=False):
        self.logging = logging
        self.tokens = tokens
        self.current = 0
        self.error_handler = error_handler

    def peek(self) -> TokenType:
        return self.tokens[self.current]

    def isAtEnd(self) -> bool:
        return self.peek().tokentype == TokenType.EOF

    def previous(self) -> TokenType:
        return self.tokens[self.current - 1]

    def advance(self) -> TokenType:
        if not self.isAtEnd():
            self.current += 1

        return self.previous()

    def error(self, token: Token, message: str) -> ParseError:
        self.error_handler.errorOnToken(token, message)
        #Empty string for now
        return Parser.ParseError("")

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
                
                if self.logging:
                    print(f"Matched {self.previous()}")

                return True

        return False
        

    #TODO: Implement this
    def ternary(self) -> Expr:
        '''
            TODO: Make this better
            ternary -> ternary "?" ternary ":" ternary | expression
        '''
        pass

    def expression(self) -> Expr:
        '''
            expression -> commaSeparated
        '''
        return self.commaSeparated()
    
    def commaSeparated(self) -> Expr:
        '''
            commaSeparated -> assignment ( "," assignment )*
        '''
        left = self.assignment()

        while self.match([TokenType.COMMA]):
            operator = self.previous()
            right = self.assignment()
            left = Binary(left, operator, right)

        return left

    def assignment(self) -> Expr:
        '''
            assignment -> IDENTIFIER '=' assignment | equality
        '''
        expr = self.equality()

        if self.match([TokenType.EQUAL]):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                return Assign(expr.name, value)

            self.error(equals, "Invalid target for assignment")

        return expr

    def equality(self) -> Expr:
        '''
            equality -> comparison ( ('!=' | '==') comparison )* 
        '''
        #consume left comparison
        left = self.comparison()

        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            left = Binary(left, operator, right)

        return left

    def comparison(self) -> Expr:
        '''
            comparison -> addition ( ('<' | '>' | '<=' | '>=') addition )*
        '''

        left = self.addition()

        while self.match([TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL]):
            operator = self.previous()
            right = self.addition()
            left = Binary(left, operator, right)

        return left

    def addition(self) -> Expr:
        '''
            addition -> multiplication ( ( '+' | '-' ) multiplication )*
        '''
        left = self.multiplication()

        while self.match([TokenType.PLUS, TokenType.MINUS]):
            operator = self.previous()
            right = self.multiplication()
            left = Binary(left, operator, right)

        return left

    def multiplication(self) -> Expr:
        '''
            multiplication -> unary ( ( '/' | '-' ) unary )*
        '''
        left = self.unary()

        while self.match([TokenType.SLASH, TokenType.STAR]):
            operator = self.previous()
            right = self.unary()
            left = Binary(left, operator, right)

        return left
        

    def unary(self) -> Expr:
        '''
            unary -> ( '!' | '-' ) unary | primary
        '''
        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        else:
            return self.primary()

    def consume(self, type_: TokenType, message: str) -> Token:
        '''
            Used when we expect a given token type "type_". Raises error when not found
        '''
        if self.check(type_):
            if self.logging:
                result = self.advance()
                print(f"Consumed {result}")
                return result

            return self.advance()

        raise self.error(self.peek(), message)
        

    def primary(self) -> Expr:
        '''
            primary -> NUMBER
                     | STRING 
                     | "false" 
                     | "true" 
                     | "nil" 
                     | "(" commaSeparated ")" 
                     | IDENTIFIER
        '''
        if self.match([TokenType.FALSE]):
            return Literal(False)
        if self.match([TokenType.TRUE]):
            return Literal(True)
        if self.match([TokenType.NIL]):
            return Literal(None)

        if self.match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(self.previous().literal)

        if self.match([TokenType.LEFT_PAREN]):
            expr = self.commaSeparated()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return Grouping(expr)

        if self.match([TokenType.IDENTIFIER]):
            return Variable(self.previous())

        raise self.error(self.peek(), "Expected expression")

    def synchronize(self):
        self.advance()
        new_block_tokens = [
            TokenType.CLASS,
            TokenType.FUN,
            TokenType.VAR,
            TokenType.FOR,
            TokenType.IF,
            TokenType.WHILE,
            TokenType.PRINT,
            TokenType.RETURN
        ]
        
        #Find a statement boundary
        while not self.isAtEnd():
            if self.previous().tokentype == TokenType.SEMICOLON:
                return

            if self.peek().tokentype in new_block_tokens:
                return
            
            self.advance()

    #TODO: BUG: parser fails for assignment like 1 = 2
    #AstPrinter only prints 1, even though scanner can scan the tokens
    def parse(self):
        '''
            Convert list of tokens to a list of valid statements
        
            program -> declaration* EOF
        '''
        statements = []

        while not self.isAtEnd():
            statements.append(self.declaration())

        return statements

    def declaration(self) -> Stmt:
        '''
            declaration -> variableDeclaration | statement;
        '''
        try:
            if self.match([TokenType.VAR]):
                return self.varDeclaration()
            else:
                return self.statement()
        except Parser.ParseError as e:
            self.synchronize()
            return None

    def varDeclaration(self) -> Stmt:
        '''
            variableDeclaration -> 'var' IDENTIFIER ('=' expression)? ';'

            'var' assumed to have been consumed already by caller
        '''
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name")

        initializer = None
        if self.match([TokenType.EQUAL]):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")

        return Var(name, initializer)

    def statement(self) -> Stmt:
        '''
            statement -> expressionStatement | printStatement
        '''
        if self.match([TokenType.PRINT]):
            return self.printStatement()

        return self.expressionStatement()

    def printStatement(self) -> Stmt:
        '''
            printStatement -> 'print' expression ';'
        '''
        #Already consumed the 'print' token, so no need to do that here
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after print value")
        return Print(value)

    def expressionStatement(self) -> Stmt:
        '''
            expressionStatement -> expression ';'
        '''
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after expression")
        return Expression(expr)
