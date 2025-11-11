import time
import statistics
import os   
import ast
from unittest import result
filepath = r"C:\Users\Hp ProBook 640 G5\flask\.devcontainer\test\repo.py"
def extract_names_from_file(filepath):
    """Extract all function and class names from a Python file."""
    names = []
    with open(filepath, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=filepath)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.append(node.name)
        elif isinstance(node, ast.ClassDef):
            names.append(node.name)
    return names


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_end_of_word = True

    def search(self, word: str) -> bool:
        curr = self.root
        for c in word:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return curr.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return True
def benchmark_trie_operations(trie: Trie, words: list[str], iterations: int = 1000) -> dict[str, float]:
    insert_times = []
    search_times = []
    prefix_times = []

    for _ in range(iterations):
        word = words[_ % len(words)]

        start = time.perf_counter()
        trie.insert(word)
        end = time.perf_counter()
        insert_times.append(end - start)

        start = time.perf_counter()
        trie.search(word)
        end = time.perf_counter()
        search_times.append(end - start)

        prefix = word[:len(word)//2]
        start = time.perf_counter()
        trie.starts_with(prefix)
        end = time.perf_counter()
        prefix_times.append(end - start)

    return {
        "insert_avg": statistics.mean(insert_times),
        "search_avg": statistics.mean(search_times),
        "prefix_avg": statistics.mean(prefix_times),
    }
if __name__ == "__main__":
    names = extract_names_from_file(filepath)
    trie = Trie()
    # provide fallback words if the file contained no functions/classes
    if not names:
        names = ["test", "example", "sample"]
    # run the benchmark to obtain the result dictionary
    result = benchmark_trie_operations(trie, names, iterations=1000)

    trie_benchmark_results = r"C:\Users\Hp ProBook 640 G5\flask\.devcontainer\test\results_autocomplete.md"
    with open(trie_benchmark_results, "w", encoding="utf-8") as f:
        f.write("# Trie Benchmark Results\n\n")
        f.write("| Operation | Average Time (seconds) |\n")
        f.write(f"| Insert    | {result['insert_avg']:.10f}      |\n")
        f.write(f"| Search    | {result['search_avg']:.10f}      |\n")
        f.write(f"| Starts With | {result['prefix_avg']:.10f}    |\n")


  