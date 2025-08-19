from openai import OpenAI
from coderag.config import OPENAI_API_KEY, OPENAI_CHAT_MODEL, RAG_DISTANCE_METRIC
from coderag.search import search_code
from coderag.query_enhancement import expand_query, rerank_by_relevance, extract_intent

client = OpenAI(api_key=OPENAI_API_KEY)

def get_intent_prompt(intent):
    """Get specialized system prompt based on query intent."""
    prompts = {
        'debug': "You're a debugging expert. Focus on identifying issues, explaining errors, and providing fixes.",
        'implement': "You're a coding mentor. Provide step-by-step implementation guidance with examples.",
        'understand': "You're a code explainer. Break down complex concepts into clear, understandable explanations.",
        'find': "You're a code navigator. Help locate and explain relevant code sections.",
        'optimize': "You're a performance expert. Suggest optimizations and best practices."
    }
    return prompts.get(intent, "You're an expert coding assistant providing comprehensive help.")

def format_code_context(results, max_chars=8000):
    """Format search results with token management."""
    context_parts = []
    total_chars = 0
    
    for i, result in enumerate(results, 1):
        score_info = ""
        if 'semantic_score' in result and 'keyword_score' in result:
            score_info = f" (sem:{result['semantic_score']:.2f}, kw:{result['keyword_score']:.2f})"
        elif 'score' in result:
            score_info = f" (score:{result['score']:.3f})"
            
        content = result['content']
        if total_chars + len(content) > max_chars:
            content = content[:max_chars - total_chars - 100] + "...[truncated]"
        
        part = f"=== File {i}: {result['filename']}{score_info} ===\nPath: {result['filepath']}\nContent:\n{content}\n"
        context_parts.append(part)
        total_chars += len(part)
        
        if total_chars >= max_chars:
            break
    
    return "\n".join(context_parts)

def execute_rag_flow(user_query, k=5):
    try:
        # Extract intent and expand query
        intent = extract_intent(user_query)
        expanded_query = expand_query(user_query)
        
        # Search with both original and expanded query
        search_results = search_code(user_query, k=k*2)  # Get more candidates
        
        if not search_results:
            return "No relevant code found for your query."
        
        # Rerank results using LLM
        reranked_results = rerank_by_relevance(user_query, search_results, top_k=k)
        
        # Format context efficiently
        code_context = format_code_context(reranked_results)
        
        # Use intent-specific system prompt
        system_prompt = get_intent_prompt(intent)
        
        prompt = f"""User Query: {user_query}
Query Intent: {intent}

Retrieved Code Context:
{code_context}

Provide a focused, actionable response based on the code context above."""

        response = client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1500
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error in RAG flow execution: {e}"