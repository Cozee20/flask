import json
import faiss
import numpy as np
import os
import sys
from sentence_transformers import SentenceTransformer

# -----------------------------
# 1. FIXED PATH CONFIGURATION
# -----------------------------
# We use os.path.dirname to automatically find where THIS script is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Assuming your metadata is in the same folder as this script, or one level up
# Adjust this line if your json file is in a different specific folder
DATA_FILE = r"C:\Users\Hp ProBook 640 G5\flask\.devcontainer\test\function_graph.json"
INDEX_FILE = r"C:\Users\Hp ProBook 640 G5\flask\functions.index"

# -----------------------------
# 2. ROBUST RESOURCE LOADING
# -----------------------------
def load_resources():
    print("Loading resources...")

    # Check Metadata
    if not os.path.exists(DATA_FILE):
        print(f"❌ CRITICAL ERROR: Metadata file not found at: {DATA_FILE}")
        print("   -> Did you run the indexing script? Is the path correct?")
        sys.exit(1) # Stop script immediately

    # Check Index
    if not os.path.exists(INDEX_FILE):
        print(f"❌ CRITICAL ERROR: FAISS Index not found at: {INDEX_FILE}")
        sys.exit(1)

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            functions = json.load(f)
            
        index = faiss.read_index(INDEX_FILE)
        model = SentenceTransformer("all-MiniLM-L6-v2")
        
        print("✅ Resources loaded successfully.")
        return index, functions, model
        
    except Exception as e:
        print(f"❌ Error during loading: {e}")
        sys.exit(1)

# Load immediately
index, functions, model = load_resources()

# -----------------------------
# 3. SEARCH FUNCTION
# -----------------------------
def search_ai(query, top_k=5):
    # Encode
    query_emb = model.encode([query], convert_to_numpy=True).astype('float32')
    faiss.normalize_L2(query_emb)

    # Search
    distances, indices = index.search(query_emb, top_k)

    results = []
    for score, idx in zip(distances[0], indices[0]):
        if idx == -1 or idx >= len(functions): 
            continue 

        func = functions[idx]
        results.append({
            "id": func.get("name", "Unknown"),
            "file": func.get("file", "Unknown File"),
            "line": func.get("line", 0),
            "docstring": func.get("docstring", "")[:100], 
            "score": float(score)
        })

    return results

# -----------------------------
# 4. TEST RUN
# -----------------------------
if __name__ == "__main__":
    test_query = "database connection"
    print(f"\nTesting Query: '{test_query}'")
    print("-" * 50)
    
    hits = search_ai(test_query)
    
    if not hits:
        print("No results found.")
    
    for h in hits:
        # Check keys exist before printing to avoid KeyError
        print(f"[{h['score']:.4f}] {h['id']}")
        print(f"   File: {h['file']}:{h['line']}")
        print(f"   Desc: {h['docstring']}...")
        print()