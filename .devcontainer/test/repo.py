import os
import ast
import csv

repo_path = r"C:\Users\Hp ProBook 640 G5\flask"


output_file = os.path.join(repo_path, "results.csv")


with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["File", "Type", "Name", "Docstring"])  

    
    for root, _, files in os.walk(repo_path):  
        for name in files:
            if not name.endswith(".py"):
                continue

            file_full_path = os.path.join(root, name)
            try:
             with open(file_full_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    tree = ast.parse(content, filename=file_full_path)

                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            doc = ast.get_docstring(node)
                            writer.writerow([file_full_path, "Function", node.name, doc or ""])
                        elif isinstance(node, ast.ClassDef):
                            doc = ast.get_docstring(node)
                            writer.writerow([file_full_path, "Class", node.name, doc or ""])

            except (SyntaxError, UnicodeDecodeError) as e:
                print(f"Skipping file due to error: {file_full_path} {e}")

print(f"""Extraction complete! Results saved to: {output_file}""")
