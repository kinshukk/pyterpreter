import sys
from typing import List

def defineType(outf, base_name: str, class_name: str, fields: str):
    outf.write(f"\nclass {class_name}({base_name}):\n")

    #TODO: set fields to None by default
    outf.write(f"   def __init__(self, {fields}):\n")

    field_list = fields.split(",")
    for field in field_list:
        field_name = field.split(":")[0].strip()
        outf.write(f"        self.{field_name} = {field_name}\n")

def defineAst(output_dir: str, base_name: str, types_: List[str]):
    path = f"{output_dir}/{base_name}.py"

    print(f"path: {path}")

    output_file = open(path, mode='w+', encoding="utf-8")

    output_file.write("from abc import ABC\n\n")
    
    output_file.write(f"class {base_name}(ABC):\n")
    
    output_file.write("    pass\n")
    
    for type_ in types_:
        class_name, fields = [v.strip() for v in type_.split("|")[:2]]

        defineType(output_file, base_name, class_name, fields)

def main():
    print(sys.argv)

    if len(sys.argv) != 2:
        print("Usage: python3 GenerateAst.py <output_directory>")
        sys.exit(1)

    output_dir = sys.argv[1]

    defineAst(output_dir, 
              "Expr",
              [
                "Binary | left: Expr, operator: Token, right: Expr",
                "Grouping | expression: Expr",
                "Literal | value",
                "Unary | operator: Token, right: Expr"
              ])

if __name__ == '__main__':
   main() 
