import re
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_CHAT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def expand_query(query):
    """Expand user query with programming synonyms and context."""
    expansions = {
        # Common programming terms
        'function': ['def', 'method', 'procedure', 'routine'],
        'variable': ['var', 'parameter', 'argument', 'param'],
        'error': ['exception', 'bug', 'issue', 'problem'],
        'loop': ['for', 'while', 'iterate', 'iteration'],
        'class': ['object', 'type', 'struct'],
        'import': ['from', 'include', 'require', 'load'],
        'return': ['output', 'result', 'yield'],
        'print': ['log', 'output', 'display', 'show'],
    }
    
    words = re.findall(r'\w+', query.lower())
    expanded_terms = set(words)
    
    for word in words:
        if word in expansions:
            expanded_terms.update(expansions[word])
    
    return ' '.join(expanded_terms)

def rerank_by_relevance(query, results, top_k=None):
    """Rerank results using LLM for better relevance."""
    if not results or len(results) <= 3:
        return results
    
    # Create compact summaries for reranking
    summaries = []
    for i, result in enumerate(results[:10]):  # Limit for token efficiency
        content_preview = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
        summaries.append(f"{i}: {result['filename']} - {content_preview}")
    
    prompt = f"""Query: "{query}"

Rank these code snippets by relevance to the query (most relevant first).
Return only numbers separated by commas (e.g., "2,0,4,1,3"):

{chr(10).join(summaries)}

Rankings:"""

    try:
        response = client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=100
        )
        
        rankings = response.choices[0].message.content.strip()
        indices = [int(x.strip()) for x in rankings.split(',') if x.strip().isdigit()]
        
        # Reorder results based on LLM ranking
        reranked = []
        for idx in indices:
            if 0 <= idx < len(results):
                reranked.append(results[idx])
        
        # Add any missed results at the end
        used_indices = set(indices)
        for i, result in enumerate(results):
            if i not in used_indices:
                reranked.append(result)
        
        return reranked[:top_k] if top_k else reranked
        
    except Exception as e:
        print(f"Reranking failed: {e}")
        return results  # Return original order on failure

def extract_intent(query):
    """Extract intent from query for better search strategy."""
    patterns = {
        'debug': r'\b(error|bug|fix|issue|problem|exception|traceback)\b',
        'implement': r'\b(how to|create|make|implement|build|write|code)\b',
        'understand': r'\b(what|why|how does|explain|understand|meaning)\b',
        'find': r'\b(find|search|locate|where|show me)\b',
        'optimize': r'\b(optimize|improve|better|faster|efficient)\b'
    }
    
    query_lower = query.lower()
    for intent, pattern in patterns.items():
        if re.search(pattern, query_lower):
            return intent
    
    return 'general'