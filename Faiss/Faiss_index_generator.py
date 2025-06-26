import faiss
import numpy as np
embedding_dim = 1536
num_vectors = 1000  # Number of vectors to generate
embeddings = np.random.random((num_vectors, embedding_dim)).astype('float32')
index = faiss.IndexFlatL2(embedding_dim)
index.add(embeddings)
# Save the index to a file
faiss.write_index(index, "/home/gr00t/placement-projects/rag-codebase/Faiss/CodeRAG-masterfaiss_index.bin")

print(f"FAISS index saved to /home/gr00t/placement-projects/rag-codebase/Faiss/CodeRAG-masterfaiss_index.bin")
