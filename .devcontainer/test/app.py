import streamlit as st
import json
import faiss
from sentence_transformers import SentenceTransformer

from trie import Trie
from semantic_search import SearchEngine
from graph import get_dependencies
function_graph_path = "C:\\Users\\Hp ProBook 640 G5\\flask\\.devcontainer\\test\\function_graph.json"

with open(function_graph_path, "r") as f:
    functions = json.load(f)

function_names = list(functions.keys())
trie = Trie()
for name in function_names:
    trie.insert(name)


model = SentenceTransformer("all-MiniLM-L6-v2")


st.title("Code Intelligence App")

query = st.text_input("Enter function name or description")

if query:
    # Autocomplete
    st.subheader("Autocomplete Suggestions")
    suggestions = trie.autocomplete(query)
    st.write(suggestions[:10])

    # Dependencies
    st.subheader("Dependencies")
    deps = get_dependencies(query)
    st.write(deps if deps else "No dependencies found")

    # Semantic Search
    st.subheader("Semantic Matches")

    engine = SearchEngine(function_names)
    results = engine.semanticsearch(query, top_k=5)

    for r in results:
        st.write(r)