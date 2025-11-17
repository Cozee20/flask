import os
import ast
import csv

file_full_pathh = r"C:\Users\Hp ProBook 640 G5\flask"
output_file = os.path.join(file_full_pathh, "results.csv")

def analyze_file(file_full_path): # Analyze a single Python file and extract classes, functions, docstrings, and function calls.
    with open(file_full_path, "r", encoding="utf-8", errors="ignore") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    results = []

    def get_func_name(node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return get_func_name(node.value) + "." + node.attr
        return ""

    for node in ast.walk(tree):

        # CLASS
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            class_doc = (ast.get_docstring(node) or "").replace("\n", " ").strip()

            results.append([
                file_full_path,
                "Class",
                class_name,
                class_doc,
                ""
            ])

        # FUNCTION
        elif isinstance(node, ast.FunctionDef):
            func_name = node.name
            func_doc = (ast.get_docstring(node) or "").replace("\n", " ").strip()

            calls = []
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    calls.append(get_func_name(child.func))

            results.append([
                file_full_path,
                "Function",
                func_name,
                func_doc,
                ", ".join(calls)
            ])

    return results


# WRITE RESULTS INTO CSV
with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["File", "Type", "Name", "Docstring", "Function Calls"])

    for root, _, files in os.walk(file_full_pathh):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rows = analyze_file(full_path)
                for row in rows:
                    writer.writerow(row)

print(f"Extraction complete! Results saved to: {output_file}")


    

