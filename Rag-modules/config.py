import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index.bin")
VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", 1536)) 
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")  
RAG_MODEL = os.getenv("RAG_MODEL", "gpt-3.5-turbo")  
RAG_TEMPERATURE = float(os.getenv("RAG_TEMPERATURE", 0.7))  
RAG_MAX_TOKENS = int(os.getenv("RAG_MAX_TOKENS", 1000)) 
RAG_TOP_K = int(os.getenv("RAG_TOP_K", 5))  
RAG_TOP_P = float(os.getenv("RAG_TOP_P", 0.9))  
DIRECTORY_TO_USE_RAG = os.getenv("DIRECTORY_TO_USE_RAG", os.path.join(os.getcwd(),'Rag-modules'))  
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

IGNORE_PATHS = [
    os.path.join(DIRECTORY_TO_USE_RAG, ".venv"),
    os.path.join(DIRECTORY_TO_USE_RAG, "node_modules"),
    os.path.join(DIRECTORY_TO_USE_RAG, "__pycache__"),
    os.path.join(DIRECTORY_TO_USE_RAG, ".git"),
    os.path.join(DIRECTORY_TO_USE_RAG, "tests"),
]
