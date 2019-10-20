import sys

class ErrorHandler:
    def __init__(self):
        self.hadError = False
    
    def error(self, line: int, message: str):
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        print(f"[{line}] Error{where}: {message}", file=sys.stderr)
        self.hadError = True

