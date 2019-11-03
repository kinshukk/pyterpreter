import sys

from ErrorHandler import *
from scanner import *
from Parser import *
from AstPrinter import *
from Interpreter import *

#error codes are used according to 
#   https://www.freebsd.org/cgi/man.cgi?query=sysexits&apropos=0&sektion=0&manpath=FreeBSD+4.3-RELEASE&format=html

class Preter:
    def __init__(self):
        self.error_handler = ErrorHandler()
        self.interpreter = Interpreter(self.error_handler)

    def printTokens(self, tokens):
        print(f"{'Type':<33} | {'lexeme':<10} | {'literal':<10} | line")
        for token in tokens:
            print(token)
        print("\n")

    def run(self, program, debug=False):
        #print("Running: \n{}".format(program))

        scanner = Scanner(program, self.error_handler)

        tokens = scanner.scanTokens()

        if debug:
            print("Tokens:")
            for token in tokens:
                print(token)

        #self.printTokens(tokens)

        parser = Parser(tokens, self.error_handler)
        statements = parser.parse()

        if self.error_handler.hadError or self.error_handler.hadRuntimeError:
            return

        #print("AstPrinter expression:")
        #print(AstPrinter().print(expression))

        self.interpreter.interpret(statements)

    def runFile(self, filename):
        with open(filename, mode='r', encoding='utf-8') as f:
            self.run("".join(f.readlines()))
            
            if self.error_handler.hadError:
                sys.exit(65)
            if self.error_handler.hadRuntimeError:
                sys.exit(70)

    def runPrompt(self, debug=False):
        try:
            while True:
                print(">>>", end="")
                self.run(input(), debug=debug)

                #error shouldn't kill the interactive prompt
                self.error_handler.hadError = False
                self.error_handler.hadRuntimeError = False

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")

    def main(self):
        if len(sys.argv[1:]) > 1:
            print("Usage: preter [script]")
        elif len(sys.argv[1:]) == 1:
            self.runFile(sys.argv[1])
        else:
            self.runPrompt()

if __name__ == '__main__':
    interpreter = Preter()
    interpreter.main()
