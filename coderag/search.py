import numpy as np
import re
from collections import Counter
from .index import load_index, get_metadata, get_embeddings
from .embeddings import generate_embeddings
from .distances import cosine_similarity
from .config import RAG_DISTANCE_METRIC

def keyword_search(query, metadata, k=10):
    """Simple keyword matching with TF-IDF-like scoring."""
    query_terms = set(re.findall(r'\w+', query.lower()))
    
    scores = []
    for i, data in enumerate(metadata):
        content = data['content'].lower()
        # Count term frequencies
        content_terms = re.findall(r'\w+', content)
        term_freq = Counter(content_terms)
        
        score = 0
        for term in query_terms:
            if term in term_freq:
                # Simple TF scoring with bonus for exact matches
                tf = term_freq[term] / len(content_terms)
                score += tf * 10 if term in content else tf
        
        scores.append((i, score))
    
    # Sort by score and return top k indices
    scores.sort(key=lambda x: x[1], reverse=True)
    return [idx for idx, score in scores[:k] if score > 0]

def search_code(query, k=5, alpha=0.7):
    """
    Hybrid search combining semantic and keyword matching.
    alpha: weight for semantic search (1-alpha for keyword search)
    """
    index = load_index()
    query_embedding = generate_embeddings(query)
    metadata = get_metadata()
    stored_embeddings = get_embeddings()

    if query_embedding is None:
        print("Failed to generate query embedding.")
        return []

    # Semantic search
    search_k = min(k * 3, index.ntotal)  # Get more candidates
    distances, indices = index.search(query_embedding, search_k)
    
    # Keyword search
    keyword_indices = keyword_search(query, metadata, k * 3)
    
    # Combine results with scores
    results = {}
    
    # Add semantic results
    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):
            if RAG_DISTANCE_METRIC == "cosine" and stored_embeddings:
                sem_score = cosine_similarity(query_embedding.flatten(), stored_embeddings[idx])
            else:
                sem_score = 1.0 / (1.0 + distances[0][i])
            
            results[idx] = {
                "data": metadata[idx],
                "semantic_score": sem_score,
                "keyword_score": 0
            }
    
    # Add/update keyword results
    for idx in keyword_indices:
        if idx < len(metadata):
            # Recalculate keyword score for normalization
            content = metadata[idx]['content'].lower()
            query_terms = set(re.findall(r'\w+', query.lower()))
            content_terms = Counter(re.findall(r'\w+', content))
            
            kw_score = sum(content_terms.get(term, 0) for term in query_terms) / len(content_terms)
            
            if idx in results:
                results[idx]["keyword_score"] = kw_score
            else:
                results[idx] = {
                    "data": metadata[idx],
                    "semantic_score": 0,
                    "keyword_score": kw_score
                }
    
    # Calculate final scores and format results
    final_results = []
    for idx, data in results.items():
        final_score = alpha * data["semantic_score"] + (1 - alpha) * data["keyword_score"]
        
        final_results.append({
            "filename": data["data"]["filename"],
            "filepath": data["data"]["filepath"],
            "content": data["data"]["content"],
            "score": final_score,
            "semantic_score": data["semantic_score"],
            "keyword_score": data["keyword_score"]
        })
    
    # Sort by final score and return top k
    final_results.sort(key=lambda x: x["score"], reverse=True)
    return final_results[:k]