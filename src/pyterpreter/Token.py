from TokenType import TokenType

class Token(object):
    def __init__(self, tokentype: int, lexeme: str, literal: object, line: int):
        self.tokentype = tokentype
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def toString(self) -> str:
        return f"<Token> {self.tokentype:<25} | {self.lexeme:<10} | {str(self.literal):<10} | {self.line}"

    def __str__(self):
        return self.toString()

