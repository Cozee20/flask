import faiss
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
funcs = extract_functions("math_utils.py")

merged = []
for name, doc in docs.items():
    if name in funcs:
        merged.append({
            "id": name,
            "docstring": doc,
            "file": funcs[name]["file"],
            "line": funcs[name]["line"]
        })
documents = [m["docstring"] for m in merged]
embeddings = model.encode(documents)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

print("Index built with", index.ntotal, "items")
