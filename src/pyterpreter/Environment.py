from RuntimeError_ import *
from Token import Token

class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: str, value: object):
        '''
            define a new variable

            if variable exists, redefine it
        '''
        self.values[name] = value

    def get(self, name: Token):
        '''
            get the value bound to a variable name

            we're checking for the variable's existence at runtime
        '''
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        raise RuntimeError_(name, f"Undefined variable {name.lexeme}")

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        raise RuntimeError_(name, f"Undefined variable {name.lexeme}")
