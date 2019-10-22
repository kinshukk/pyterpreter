import sys

from ErrorHandler import *
from scanner import *
from Parser import *
from AstPrinter import *

#error codes are used according to 
#   https://www.freebsd.org/cgi/man.cgi?query=sysexits&apropos=0&sektion=0&manpath=FreeBSD+4.3-RELEASE&format=html

class Preter:
    def __init__(self):
        self.error_handler = ErrorHandler()

    def run(self, program):
        #print("Running: \n{}".format(program))

        scanner = Scanner(program, self.error_handler)

        tokens = scanner.scanTokens()

        parser = Parser(tokens, self.error_handler)
        expression = parser.parse()

        if self.error_handler.hadError:
            return

        print(AstPrinter().print(expression))

    def runFile(self, filename):
        with open(filename, mode='r', encoding='utf-8') as f:
            self.run("".join(f.readlines()))
            
            if self.error_handler.hadError:
                sys.exit(65)

    def runPrompt(self):
        try:
            while True:
                print(">>>", end="")
                self.run(input())

                #error shouldn't kill the interactive prompt
                self.error_handler.hadError = False
        
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
