import sys
from typing import List

'''
    Generates the file src/pyterpreter/Expr.py

    We can add new Expr types by adding lines to the list passed to defineAst() inside main()
'''

def defineImports(outf):
    outf.write("from abc import ABC, abstractmethod\n")
    outf.write("from Token import *\n")
    #outf.write("from TokenType import *")
    outf.write("\n")


def defineType(outf, base_name: str, class_name: str, fields: str):
    outf.write(f"\nclass {class_name}({base_name}):\n")

    #TODO: set fields to None by default
    outf.write(f"    def __init__(self, {fields}):\n")

    field_list = fields.split(",")
    for field in field_list:
        #field_name = field.split(":")[0].strip()
        outf.write(f"        self.{field} = {field}\n")

    outf.write("\n")
    outf.write(f"    def accept(self, visitor):\n")
    outf.write(f"        return visitor.visit{class_name}{base_name}(self)\n")

def addVisitorLines(base_name: str, types_: List[str], visitorLines: List[str]):
    #outf.write("\nclass Visitor(ABC):\n")
    
    #add import at the beginning of visitorLines
    visitorLines.insert(0, f"from {base_name} import *\n")

    for type_ in types_:
        type_name = type_.split("|")[0].strip()

        visitorLines.append(f"    @abstractmethod\n")
        visitorLines.append(f"    def visit{type_name}{base_name}(self, {base_name.lower()}: {type_name}):\n")
        visitorLines.append(f"        pass\n\n")

def defineBaseClass(outf, base_name: str):
    outf.write(f"class {base_name}:\n")
    
    outf.write("    pass\n")
    

def defineExprClasses(outf, base_name: str, types_: List[str]):
    outf.write("\n")

    for type_ in types_:
        class_name, fields = [v.strip() for v in type_.split("|")[:2]]

        defineType(outf, base_name, class_name, fields)
    

def defineAst(output_dir: str, base_name: str, types_: List[str], visitorLines: List[str]):
    path = f"{output_dir}/{base_name}.py"

    print(f"path: {path}")

    output_file = open(path, mode='w+', encoding="utf-8")
    
    defineImports(output_file)

    defineBaseClass(output_file, base_name)

    defineExprClasses(output_file, base_name, types_)

    addVisitorLines(base_name, types_, visitorLines)

def visitorImports(outf):
    defineImports(outf)

def defineVisitor(output_dir: str, visitorLines: List[str]):
    outf = open(f"{output_dir}/Visitor.py", mode="w+", encoding="utf-8")

    visitorImports(outf)

    for line in visitorLines:
        outf.write(line)

    outf.close()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 GenerateAst.py <output_directory>")
        sys.exit(1)

    output_dir = sys.argv[1]
    visitorLines = ["\nclass Visitor(ABC):\n"]

    defineAst(output_dir, 
              "Expr",
              [
                "Binary | left, operator, right",
                "Grouping | expression",
                "Literal | value",
                "Unary | operator, right"
              ],
              visitorLines)
    
    defineAst(output_dir,
              "Stmt",
              [
                  "Expression | expression",
                  "Print | expression"
              ],
              visitorLines)

    defineVisitor(output_dir, visitorLines)

if __name__ == '__main__':
   main() 
