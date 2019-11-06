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
            Return True if current token is of type type_, without advancing
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
            assignment -> IDENTIFIER '=' assignment | logic_or
        '''
        expr = self.logic_or()

        if self.match([TokenType.EQUAL]):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                return Assign(expr.name, value)

            self.error(equals, "Invalid target for assignment")

        return expr

    def logic_or(self) -> Expr:
        '''
            logic_or -> logic_and ( 'or' logic_and )*
        '''
        left = self.logic_and()

        while self.match([TokenType.OR]):
            operator = self.previous()
            right = self.logic_and()
            left = Logical(left, operator, right)

        return left

    def logic_and(self) -> Expr:
        '''
            logic_and -> equality ( 'and' equality )*
        '''
        left = self.equality()

        while self.match([TokenType.AND]):
            operator = self.previous()
            right = self.equality()
            left = Logical(left, operator, right)
        
        return left

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
            statement -> expressionStatement | printStatement | block | ifStatement | whileStatement | forStatement
        '''
        if self.match([TokenType.PRINT]):
            return self.printStatement()

        elif self.match([TokenType.LEFT_BRACE]):
            return Block(self.block())

        elif self.match([TokenType.IF]):
            return self.ifStatement()

        elif self.match([TokenType.WHILE]):
            return self.whileStatement()

        elif self.match([TokenType.FOR]):
            return self.forStatement()

        else:
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

    def block(self) -> List[Stmt]:
        '''
            block -> '{' declaration* '}'
        '''
        declarations = []

        while (not self.check(TokenType.RIGHT_BRACE)) and not self.isAtEnd():
            declarations.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after block")
        return declarations

    def ifStatement(self) -> If:
        '''
            ifStatement -> 'if' '(' expression ')' statement ( 'else' statement )?

            dangling 'else' is coupled with the innermost 'if'
        '''
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'if'")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after if condition")

        #statement, not declaration, since statement covers nested if, blocks, print, expressions,
        #but doesn't permit a variable declared without use inside the thenBranch
        thenBranch = self.statement()
        
        elseBranch = None
        if(self.match([TokenType.ELSE])):
            elseBranch = self.statement()

        return If(condition, thenBranch, elseBranch)

    def whileStatement(self) -> While:
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'while'")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after condition to match '('")

        body = self.statement()

        return While(condition, body)

    def forStatement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after for")

        #parse initializer
        if self.match([TokenType.SEMICOLON]):
            initializer = None
        elif self.match([TokenType.VAR]):
            initializer = self.varDeclaration()
        else:
            initializer = self.expressionStatement()

        #condition
        if not self.check(TokenType.SEMICOLON):
            #If condition is not empty
            condition = self.expression()
        else:
            condition = None

        self.consume(TokenType.SEMICOLON, "Expected ';' after loop condition")

        #increment expression
        if not self.check(TokenType.RIGHT_PAREN):
            #incrementing expression not empty
            increment = self.expression()
        else:
            increment = None

        self.consume(TokenType.RIGHT_PAREN, "Expected closing ')' after for clauses")

        body = self.statement()


        #make an equivalent while loop, with initializer before the loop, 
        #and increment at the end of loop body

        if increment is not None:
            body = Block([
                body,
                increment
            ])

        if condition is not None:
            body = While(condition, body)

        if initializer is not None:
            body = Block([
                initializer,
                body
            ])

        return body
