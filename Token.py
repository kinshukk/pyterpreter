from TokenType import TokenType

class Token(object):
    def __init__(self, tokentype: int, lexeme: str, literal: object, line: int):
        self.tokentype = tokentype
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def toString(self) -> str:
        return f"{self.tokentype} {self.lexeme}\t{self.line}"

    def __str__(self):
        return "<Token> {}".format(self.toString())

