from trie import Trie
from semantic_search import SearchEngine

def hybrid_search(query, trie, semantic_engine, top_k=5):
    trie_results = trie.starts_with(query)
    semantic_results = semantic_engine.semantic_search(query, top_k)

    scores = {}

    
    for rank, item in enumerate(trie_results):
        scores[item] = scores.get(item, 0) + 1.0 / (rank + 1)


    for rank, item in enumerate(semantic_results):
        scores[item] = scores.get(item, 0) + 0.7 / (rank + 1)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [item for item, _ in ranked[:top_k]]

