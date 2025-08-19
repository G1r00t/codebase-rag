# codebase-rag


### Create a .env and save it in the root directory 
.env structure
```
OPENAI_API_KEY=api key
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_CHAT_MODEL=gpt-4o
WATCHED_DIR=directory to run rag on
FAISS_INDEX_FILE=path to faiss index file
EMBEDDING_DIM=1536  # Modify if you're using a different embedding model
RAG_DISTANCE_METRIC=cosine
HYBRID_SEARCH_ALPHA=0.7
ENABLE_QUERY_EXPANSION=true
ENABLE_LLM_RERANKING=true
ENABLE_CODE_CHUNKING=false
```
