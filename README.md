# Codebase RAG

A powerful Retrieval-Augmented Generation (RAG) system designed for intelligent codebase analysis and querying. This tool leverages OpenAI's language models and FAISS vector search to enable natural language interactions with your code repositories.

## Features

- **Intelligent Code Search**: Semantic search across your entire codebase using vector embeddings
- **Hybrid Search**: Combines vector similarity with traditional keyword matching (configurable via `HYBRID_SEARCH_ALPHA`)
- **Query Expansion**: Automatically expands queries for better retrieval results
- **LLM Reranking**: Optionally reranks results using language model understanding
- **Code Chunking**: Smart code splitting for better context preservation
- **Multiple Interfaces**: 
  - CLI for terminal-based interactions
  - Web interface via Streamlit/Flask
  - Programmatic API
- **Real-time Monitoring**: Watch directory for code changes and auto-update indexes
- **Flexible Configuration**: Extensive environment-based configuration

## Architecture

The system consists of several key components:

- **FAISS.py**: Vector index management and similarity search
- **app.py**: Web application interface
- **cli.py**: Command-line interface
- **main.py**: Core orchestration logic
- **prompt_flow.py**: LLM prompt management and query processing
- **coderag/**: Core module with RAG functionality

## Installation

1. Clone the repository:
```bash
git clone https://github.com/G1r00t/codebase-rag.git
cd codebase-rag
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables (see Configuration section below)

## Configuration

Create a `.env` file in the root directory with the following structure:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_CHAT_MODEL=gpt-4o

# Directory Configuration
WATCHED_DIR=/path/to/your/codebase
FAISS_INDEX_FILE=/path/to/faiss_index.bin

# Embedding Configuration
EMBEDDING_DIM=1536  # Modify if using a different embedding model

# RAG Configuration
RAG_DISTANCE_METRIC=cosine
HYBRID_SEARCH_ALPHA=0.7  # Balance between vector (1.0) and keyword (0.0) search

# Feature Flags
ENABLE_QUERY_EXPANSION=true
ENABLE_LLM_RERANKING=true
ENABLE_CODE_CHUNKING=false
```

### Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_EMBEDDING_MODEL` | Model for generating embeddings | `text-embedding-ada-002` |
| `OPENAI_CHAT_MODEL` | Model for chat completions | `gpt-4o` |
| `WATCHED_DIR` | Directory to index and monitor | Required |
| `FAISS_INDEX_FILE` | Path to store/load FAISS index | Required |
| `EMBEDDING_DIM` | Dimension of embedding vectors | `1536` |
| `RAG_DISTANCE_METRIC` | Distance metric for similarity | `cosine` |
| `HYBRID_SEARCH_ALPHA` | Weight for hybrid search (0-1) | `0.7` |
| `ENABLE_QUERY_EXPANSION` | Expand queries for better results | `true` |
| `ENABLE_LLM_RERANKING` | Rerank results using LLM | `true` |
| `ENABLE_CODE_CHUNKING` | Enable smart code chunking | `false` |

## Usage

### Command Line Interface

Run interactive CLI:
```bash
python cli.py
```

### Web Interface

Launch the web application:
```bash
python app.py
```

### Programmatic Usage

```python
from coderag import CodebaseRAG

# Initialize the RAG system
rag = CodebaseRAG(
    watched_dir="/path/to/codebase",
    index_file="faiss_index.bin"
)

# Query your codebase
result = rag.query("How does authentication work?")
print(result)
```

### Main Script

Run the main orchestration:
```bash
python main.py
```

## How It Works

1. **Indexing**: The system scans your specified directory, processes code files, and generates embeddings using OpenAI's embedding model
2. **Vector Storage**: Embeddings are stored in a FAISS index for efficient similarity search
3. **Query Processing**: User queries are embedded and compared against the index
4. **Hybrid Search**: Results combine vector similarity with optional keyword matching
5. **Reranking**: LLM optionally reranks results for better relevance
6. **Response Generation**: Retrieved context is fed to the language model to generate natural language responses

## Advanced Features

### Query Expansion
When enabled, the system automatically expands your queries to include related terms and concepts, improving retrieval accuracy.

### LLM Reranking
The system can use a language model to rerank retrieved results based on semantic relevance to your query, not just vector similarity.

### Hybrid Search
Adjust the `HYBRID_SEARCH_ALPHA` parameter to balance between:
- Pure vector search (α = 1.0)
- Pure keyword search (α = 0.0)
- Balanced hybrid (α = 0.5-0.7)

## Project Structure

```
codebase-rag/
├── coderag/           # Core RAG module
├── FAISS.py          # Vector index operations
├── app.py            # Web interface
├── cli.py            # Command-line interface
├── main.py           # Main orchestration
├── prompt_flow.py    # Prompt management
├── requirements.txt  # Python dependencies
├── .env             # Environment configuration
└── .gitignore       # Git ignore rules
```

## Requirements

- Python 3.8+
- OpenAI API key
- Sufficient disk space for FAISS index
- Dependencies listed in `requirements.txt`

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

[Specify your license here]

## Author

Created by [G1r00t](https://github.com/G1r00t)

## Acknowledgments

- Built with [FAISS](https://github.com/facebookresearch/faiss) for efficient similarity search
- Powered by [OpenAI](https://openai.com/) language models
- Inspired by modern RAG architectures for code understanding

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/G1r00t/codebase-rag).
