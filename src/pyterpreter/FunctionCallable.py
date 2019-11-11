from Callable import Callable
from Environment import Environment

class FunctionCallable(Callable):
    def __init__(self, declaration):
        self.declaration = declaration

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(enclosing=interpreter.globals)

        #bind parameter names to passed arguments
        for param_token, arg in zip(self.declaration.params, arguments):
            environment.define(param_token.lexeme, arg)

        interpreter.executeBlock(self.declaration.body, environment)
        return None

    def __str__(self):
        return f"<Function '{self.declaration.name.lexeme}'>"
