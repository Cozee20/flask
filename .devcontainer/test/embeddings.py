import csv
from sentence_transformers import SentenceTransformer

CSV_PATH = r"C:\Users\Hp ProBook 640 G5\flask\results.csv"


def vectorize_from_csv(csv_path):
    
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        functions = list(reader)

    if not functions:
        raise ValueError("CSV file is empty or not read correctly")

  
    texts = [
    f"{f.get('name', '')} : {f.get('docstring', '')}"
    for f in functions
]
    
    model = SentenceTransformer("all-MiniLM-L6-v2")

  
    embeddings = model.encode(texts)

    return embeddings, functions


if __name__ == "__main__":
    embeddings, functions = vectorize_from_csv(CSV_PATH)

   
embedded_file = r"C:\Users\Hp ProBook 640 G5\flask\.devcontainer\test\Embedded.txt"
with open(embedded_file, "w", encoding="utf-8") as f:
    f.write("Vectorization successful\n")
    f.write(f"Number of functions: {len(functions)}\n")
    f.write(f"Embeddings shape: {embeddings.shape}\n")
    f.write("\nFirst function:\n")
    f.write("\nFirst embedding (All values):")
    f.write(str(embeddings[0][:]))