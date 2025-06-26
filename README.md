# codebase-rag


### Create a .env and save it in the root directory 
.env structure
```
OPENAI_API_KEY=your-openai-api-key-here
FAISS_INDEX_PATH=faiss_index.bin
VECTOR_DIMENSION=1536
EMBEDDING_MODEL=text-embedding-ada-002
RAG_MODEL=gpt-3.5-turbo
RAG_TEMPERATURE=0.7
RAG_MAX_TOKENS=1000
RAG_TOP_K=5
RAG_TOP_P=0.9
DIRECTORY_TO_USE_RAG=/absolute/path/to/Rag-modules
```