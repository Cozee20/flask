import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

def load_function_names(csv_path=r"C:\Users\Hp ProBook 640 G5\flask\results.csv"):
    if not os.path.exists(csv_path):
        return [
           "Error: CSV file not found."
        ]

    try:
        data = pd.read_csv(csv_path)
        if "name" not in data.columns:
            print("Warning: 'name' column not found in CSV. Using empty list.")
            return []

        calls = data["name"].dropna().astype(str)
        unique = set()
        for row in calls:
            for fn in row.split(","):
                fn = fn.strip()
                if fn:
                    unique.add(fn)
        return list(unique)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []

class SearchEngine:
    def __init__(self, function_names):
        self.function_names = function_names
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        
        vectors = self.encoder.encode(function_names, normalize_embeddings=True)
        vectors = np.array(vectors).astype("float32")

        dim = vectors.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        
        self.index.add(vectors)

        print(f"Indexed {len(function_names)} functions")

    def semanticsearch(self, query, top_k=5):
        if not self.function_names:
            return []

       
        query_vec = self.encoder.encode([query], normalize_embeddings=True).astype("float32")
        
      
        k = min(top_k, len(self.function_names))
        
     
        distances, indices = self.index.search(query_vec, k)

        results = []
       
        for score, idx in zip(distances[0], indices[0]):
           
            if idx != -1 and 0 <= idx < len(self.function_names):
                results.append({
                    "name": self.function_names[idx],
                    "similarity": float(score),
                    "distance": 1.0 - float(score)
                })
        return results

if __name__ == "__main__":
    functions = load_function_names()
    
    if not functions:
        print("No functions to index. Exiting.")
    else:
        engine = SearchEngine(functions)

        while True:
            query = input("\nSearch (q to quit): ").strip()
            if query.lower() == "q":
                break

            results = engine.semanticsearch(query)
            if not results:
                print("No matches found")
                continue

            for i, r in enumerate(results, 1):
                print(f"{i}. {r['name']} | similarity: {r['similarity']:.3f} | distance: {r['distance']:.3f}")