import json
function_graph = "C:\\Users\\Hp ProBook 640 G5\\flask\\.devcontainer\\test\\function_graph.json"
with open(function_graph) as f:
    graph = json.load(f)

def get_dependencies(function_name):
    for f in graph:
        if isinstance(f, dict) and f.get("name") == function_name:
            return f.get("deps", [])
    return []