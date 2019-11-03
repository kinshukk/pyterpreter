from RuntimeError_ import *
from Token import Token

class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing


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

        #look in higher up scopes
        elif self.enclosing is not None:
            return self.enclosing.get(name)
        
        else:
            raise RuntimeError_(name, f"Undefined variable {name.lexeme}")

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value

        elif self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        
        else:
            raise RuntimeError_(name, f"Undefined variable {name.lexeme}")
