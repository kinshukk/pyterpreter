from TokenType import TokenType

class Token(object):
    def __init__(self, tokentype: int, lexeme: str, literal: object, line: int):
        self.tokentype = tokentype
        self.lexeme = lexeme
        this.literal = literal
        this.line = line

    def toString(self) -> str:
        return "{} {} {}".format(this.type, this.lexeme, this.literal)

    def __str__(self):
        return "<Token> {}".format(this.toString())

