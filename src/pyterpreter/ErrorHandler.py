import sys

from Token import *
from TokenType import *
from RuntimeError_ import *

#TODO: Probably refactor to have a single error function

class ErrorHandler:
    def __init__(self):
        self.hadError = False
        self.hadRuntimeError = False

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def errorOnToken(self, token: Token, message: str):
        if token.tokentype == TokenType.EOF:
            self.report(token.line, " at End", message)
        else:
            self.report(token.line, f" at {token.lexeme} ", message)

    def runtimeError(error: RuntimeError_):
        print(f"{error.message}\n[line {error.token.line}]")
        self.hadRuntimeError = True

    def report(self, line: int, where: str, message: str):
        print(f"[{line}] Error{where}: {message}", file=sys.stderr)
        self.hadError = True

