import timeit
import random 
import ast
from unittest import result
filepath = r"C:\Users\Hp ProBook 640 G5\flask\.devcontainer\test\repo.py"
def extract_names_from_file(filepath):
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
        self.is_end_of_word = True
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_end_of_word = False

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
        return curr.is_end_of_word




definitions = extract_names_from_file(filepath)

if not definitions:
    print("No definitions found. Exiting.")
    exit()

trie = Trie()
for name in definitions:
    trie.insert(name)

def brute_force_autocomplete(names, prefix):
    return [name for name in names if name.startswith(prefix)]

def trie_autocomplete(trie_obj, prefix):
    return trie_obj.starts_with(prefix)


prefixes = [
    name[: random.randint(1, min(4, len(name)))]
    for name in definitions
    if len(name) > 0
]

if not prefixes:
    print("Not enough data to generate prefixes.")
    queries = []
else:
    queries = random.choices(prefixes, k=5000)


def run_brute(names, qs):
    for q in qs:
        brute_force_autocomplete(names, q)

def run_trie(trie_obj, qs):
    for q in qs:
        trie_autocomplete(trie_obj, q)


if queries:
    print(f"Benchmarking with {len(definitions)} words and {len(queries)} queries...")

    brute_time = timeit.timeit(
        lambda: run_brute(definitions, queries),
        number=5
    )
    brute_avg = brute_time / (5 * len(queries))
    print(f"Brute-force avg query time: {brute_avg:.8f} seconds")

    trie_time = timeit.timeit(
        lambda: run_trie(trie, queries),
        number=5
    )
    trie_avg = trie_time / (5 * len(queries))
    print(f"Trie avg query time:        {trie_avg:.8f} seconds")
    
    if trie_avg < brute_avg:
        print(f"Trie is {brute_avg / trie_avg:.2f}x faster.")
else:
    print("Skipping benchmark due to lack of queries.")