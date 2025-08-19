import numpy as np

def dot_product(a, b):
    """
    Compute dot product between two vectors.
    Returns a float; higher means more similar.
    """
    return float(np.dot(a, b))

def cosine_similarity(a, b):
    """
    Compute cosine similarity between two vectors.
    Returns a float in [-1, 1]; higher means more similar.
    """
    a = np.array(a)
    b = np.array(b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))

def euclidean_distance(a, b):
    """
    Compute negative Euclidean distance (so higher is more similar).
    """
    a = np.array(a)
    b = np.array(b)
    return -float(np.linalg.norm(a - b))
