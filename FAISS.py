import faiss
import numpy as np

# Example: Let's assume you have an array of embeddings
# You need to create an array of shape (num_vectors, embedding_dim)
embedding_dim = 1536
num_vectors = 1000  # Example number of vectors

# Random embeddings for the example
embeddings = np.random.random((num_vectors, embedding_dim)).astype('float32')

# Create a FAISS index
index = faiss.IndexFlatL2(embedding_dim)  # L2 distance is used here
index.add(embeddings)  # Add your embeddings to the index

# Save the FAISS index to a file
faiss.write_index(index, "/home/gr00t/my-pro/codebase-rag-main/faiss_index.bin")

print(f"FAISS index saved to /home/gr00t/my-pro/codebase-rag-main/faiss_index.bin")
