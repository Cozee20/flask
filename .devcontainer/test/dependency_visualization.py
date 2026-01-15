import os
import json
import ast
import builtins
import networkx as nx
import matplotlib.pyplot as plt

FOLDER_PATH = r"C:\Users\Hp ProBook 640 G5\flask\.devcontainer\test"
GRAPH_JSON = "function_graph.json"
GRAPH_IMAGE = "graph.png"

py_paths = []

def analyze_repo(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                py_paths.append(os.path.join(root, file))

analyze_repo(FOLDER_PATH)


built_ins = set(dir(builtins))

class FunctionFinder(ast.NodeVisitor):
    def __init__(self):
        self.function_stack = []
        self.calls = {}

    def visit_FunctionDef(self, node):
        self.function_stack.append(node.name)
        self.calls.setdefault(node.name, [])
        self.generic_visit(node)
        self.function_stack.pop()

    def visit_Call(self, node):
        if self.function_stack and isinstance(node.func, ast.Name):
            caller = self.function_stack[-1]
            callee = node.func.id

            if callee not in built_ins:
                self.calls[caller].append(callee)

        self.generic_visit(node)

graph = {}

for path in py_paths:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            continue

    finder = FunctionFinder()
    finder.visit(tree)

    for func, calls in finder.calls.items():
        graph.setdefault(func, []).extend(calls)


with open(GRAPH_JSON, "w") as f:
    json.dump(graph, f, indent=4)


def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

    return visited


def has_cycle(graph):
    visited = set()
    stack = set()

    def visit(node):
        if node in stack:
            return True
        if node in visited:
            return False

        visited.add(node)
        stack.add(node)

        for neighbor in graph.get(node, []):
            if visit(neighbor):
                return True

        stack.remove(node)
        return False

    return any(visit(node) for node in graph)


G = nx.DiGraph()

for func, calls in graph.items():
    for callee in calls:
        G.add_edge(func, callee)

plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=3000,
    font_size=9,
    arrowsize=20
)

plt.title("Function Dependency Graph")
plt.savefig(GRAPH_IMAGE)
plt.close()


print("function_graph.json created")
print("graph.png created")
print("Cycle detected:", has_cycle(graph))
