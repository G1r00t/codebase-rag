import numpy as np
from index import load_index, get_metadata
from embeddings import generate_embeddings

def search_code(query, k=5):
    """Search the FAISS index using a text query."""
    index = load_index()  
    query_embedding = generate_embeddings(query) 

    if query_embedding is None:
        print("Failed to generate query embedding.")
        return []

    distances, indices = index.search(query_embedding, k)

    results = []
    for i, idx in enumerate(indices[0]): 
        if idx < len(get_metadata()): 
            file_data = get_metadata()[idx]
            results.append({
                "filename": file_data["filename"],
                "filepath": file_data["filepath"],
                "content": file_data["content"],
                "distance": distances[0][i] 
            })
        else:
            print(f"Warning: Index {idx} is out of bounds for metadata with length {len(get_metadata())}")
    return results
