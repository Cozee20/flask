import streamlit as st
import json
import faiss
from sentence_transformers import SentenceTransformer

from trie import Trie
from semantic_search import SearchEngine
from dependency_visualization import FunctionFinder
fgraph = r"C:\Users\Hp ProBook 640 G5\flask\.devcontainer\test\function_graph.json"

# -------------------- Load data --------------------
with open(fgraph, "r") as f:
    functions = json.load(f)

function_names = functions


# Build Trie
trie = Trie()
for name in function_names:
    trie.insert(name)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------- UI --------------------
st.title("🔍 Code Intelligence App")

query = st.text_input("Enter function name or description")

if query:
    # Autocomplete
    st.subheader("🔤 Autocomplete Suggestions")
    suggestions = trie.starts_with(query)
    st.write(suggestions[:10])

    # Dependencies
    st.subheader("🔗 Dependencies")
    deps = FunctionFinder(query)
    st.write(deps if deps else "No dependencies found")

    # Semantic Search
    st.subheader("🤖 Semantic Matches")
    results = SearchEngine(query)
    for r in results:
        st.write(f"**{r['name']}** — {r['docstring']}")
