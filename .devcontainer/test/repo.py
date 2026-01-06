import os
import ast
import csv

file_full_pathh = r"C:\Users\Hp ProBook 640 G5\flask"
output_file = os.path.join(file_full_pathh, "results.csv")

class DefinitionExtractor(ast.NodeVisitor):

    def __init__(self):
        self.functions = []
        self.classes = []

    def visit_FunctionDef(self, node):
        self.functions.append({
            "name": node.name, 
            "line": node.lineno
        })
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append({
            "name": node.name,
            "line": node.lineno
        })
        self.generic_visit(node)

class DocstringReader(ast.NodeVisitor):

    def visit_FunctionDef(self, node):
       
        docstring = ast.get_docstring(node)
        
        if docstring:
            print(f"Function '{node.name}' has docstring: {docstring}")
        else:
            print(f"Function '{node.name}' has NO docstring.")

       
        self.generic_visit(node)

  

class NameFinder(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(f"DEFINED function: '{node.name}'")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            print(f"CALLED function:  '{node.func.id}'")
        self.generic_visit(node)




with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["type", "name", "line"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for root, _, files in os.walk(file_full_pathh):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=file_path)
                    extractor = DefinitionExtractor() 
                    extractor.visit(tree) 

                    for func in extractor.functions:
                        writer.writerow({
                            "type": "function",
                            "name": func["name"],
                            "line": func["line"]
                        })

                    for cls in extractor.classes:
                        writer.writerow({
                            "type": "class",
                            "name": cls["name"],
                            "line": cls["line"]
                        })


    

