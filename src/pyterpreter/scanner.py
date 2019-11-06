from typing import List
from collections import namedtuple

from TokenType import *
from Token import *
from ErrorHandler import ErrorHandler

DoubleToken = namedtuple("DoubleSingle", "single, double")

'''
    Tokenizes the program string
'''

class Scanner:
    
    def __init__(self, source: str, error_handler: ErrorHandler):
        self.source = source
        self.error_handler = error_handler

        self.tokens = []

        self._start = 0
        self._current = 0
        self._line = 1

        self.single_tokens = {
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_BRACE,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            '-': TokenType.MINUS,
            '+': TokenType.PLUS,
            ';': TokenType.SEMICOLON,
            '*': TokenType.STAR,
        }

        self.double_tokens = {
            '!': DoubleToken(TokenType.BANG, TokenType.BANG_EQUAL),
            '=': DoubleToken(TokenType.EQUAL, TokenType.EQUAL_EQUAL),
            '<': DoubleToken(TokenType.LESS, TokenType.LESS_EQUAL),
            '>': DoubleToken(TokenType.GREATER, TokenType.GREATER_EQUAL),
        }

        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }

    def _isAtEnd(self) -> bool:
        return self._current >= len(self.source)

    def scanTokens(self) -> List[Token]:
        while not self._isAtEnd():
            self._start = self._current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self._line))

        return self.tokens

    def advance(self) -> chr:
        #TODO: Won't this cause an error at the end of source?
        self._current += 1
        return self.source[self._current - 1]

    def match(self, expected) -> bool:
        '''Conditional advance. Consume only if it's what we expected'''
        if self._isAtEnd():
            return False

        if self.source[self._current] != expected:
            return False

        self._current += 1
        return True

    def addToken(self, tokentype: TokenType, literal=None):
        text = self.source[self._start: self._current]
        self.tokens.append(Token(tokentype, text, literal, self._line))

    def peek(self):
        '''what character is at the current position?'''
        if self._isAtEnd():
            return "\0"

        return self.source[self._current]

    def _string(self):
        #find nearest ending doublequote
        while self.peek() != '"' and not self._isAtEnd():
            if self.peek() == '\n':
                self._line += 1

            self.advance()

        if self._isAtEnd():
            self.error_handler.error(self._line, "Unterminated string")
            return

        #consume the closing doublequote
        self.advance()

        self.addToken(TokenType.STRING, self.source[self._start + 1: self._current - 1])

        #TODO: escape sequences

    def peekNext(self):
        if self._current + 1 >= len(self.source):
            return '\0'
        return self.source[self._current + 1]

    def number(self):
        '''
        Consume numbers without trailing decimal points
            Fine: 123, 1234.5678
            Not fine: 456.
        '''
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peekNext().isdigit():
            self.advance()

        while self.peek().isdigit():
            self.advance()

        self.addToken(TokenType.NUMBER, float(self.source[self._start: self._current]))

    def identifier(self):
        while self.peek().isalnum():
            self.advance()

        text = self.source[self._start: self._current]
        tokentype = None

        if text in self.keywords.keys():
            tokentype = self.keywords[text]
        else:
            tokentype = TokenType.IDENTIFIER

        self.addToken(tokentype)

    def multilineComment(self):
        while self.peek() != '\0' and self.peekNext() != '\0':
            if self.match('\n'):
                self._line += 1
            elif self.peek() == '*' and self.peekNext() == '/':
                #get out only if comment ends
                self.advance()
                self.advance()
                return
            else:
                self.advance()
        
        self.error_handler.error(self._line, "Unexpected EOF: Multiline comment didn't end")

    def scanToken(self):
        c = self.advance()
        
        if c in self.single_tokens.keys():
            self.addToken(self.single_tokens[c])
        
        elif c in self.double_tokens.keys():
            #check for double tokens with '='
            if self.match("="):
                self.addToken(self.double_tokens[c].double)
            else:
                self.addToken(self.double_tokens[c].single)
        
        elif c == '/':
            #comment, consume till end of line or file, whichever's first
            if self.match('/'):
                while self.peek() != "\n" and not self._isAtEnd():
                    self.advance()

            elif self.match("*"):
                self.multilineComment()

            else:
                self.addToken(TokenType.SLASH)

        elif c == ' ' or c == '\r' or c == '\t':
            #skip whitespace
            pass
        
        elif c == '\n':
            #increment line number
            self._line += 1

        elif c == '"':
            #strings
            self._string()

        else:
            if c.isdigit():
                self.number()

            elif c.isalpha():
                self.identifier()

            else:
                self.error_handler.error(self._line, f"Unexpected character {c}")

