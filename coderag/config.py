import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# === Environment Variables ===
# OpenAI API key and model settings (loaded from .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4")

# Embedding dimension (from .env or fallback)
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", 1536))

# Distance metric for retrieval
RAG_DISTANCE_METRIC = os.getenv("RAG_DISTANCE_METRIC", "cosine")

# Hybrid search settings
HYBRID_SEARCH_ALPHA = float(os.getenv("HYBRID_SEARCH_ALPHA", "0.7"))  # Semantic vs keyword weight
ENABLE_QUERY_EXPANSION = os.getenv("ENABLE_QUERY_EXPANSION", "true").lower() == "true"
ENABLE_LLM_RERANKING = os.getenv("ENABLE_LLM_RERANKING", "true").lower() == "true"
ENABLE_CODE_CHUNKING = os.getenv("ENABLE_CODE_CHUNKING", "false").lower() == "true"

# Project directory (from .env)
WATCHED_DIR = os.getenv("WATCHED_DIR", os.path.join(os.getcwd(), 'CodeRAG'))

FAISS_INDEX_FILE = os.getenv("FAISS_INDEX_FILE", os.path.join(WATCHED_DIR, 'coderag_index.faiss'))

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

IGNORE_PATHS = [
    os.path.join(WATCHED_DIR, ".venv"),
    os.path.join(WATCHED_DIR, "node_modules"),
    os.path.join(WATCHED_DIR, "__pycache__"),
    os.path.join(WATCHED_DIR, ".git"),
    os.path.join(WATCHED_DIR, "tests"),
]