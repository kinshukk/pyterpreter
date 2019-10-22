import sys

from Token import *
from TokenType import *

#TODO: Probably refactor to have a single error function

class ErrorHandler:
    def __init__(self):
        self.hadError = False
    
    def error(self, line: int, message: str):
        self.report(line, "", message)

    def errorOnToken(self, token: Token, message: str):
        if token.tokentype == TokenType.EOF:
            self.report(token.line, " at End", message)
        else:
            self.report(token.line, f" at {token.lexeme} ", message)

    def report(self, line: int, where: str, message: str):
        print(f"[{line}] Error{where}: {message}", file=sys.stderr)
        self.hadError = True

