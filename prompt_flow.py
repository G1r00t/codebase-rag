from openai import OpenAI
from Rag_modules.config import OPENAI_KEY, RAG_MODEL
from Rag_modules.search import search_code

client = OpenAI(api_key=OPENAI_KEY)

SYSTEM_PROMPT = """
You are an expert coding assistant. Your task is to help users with their question. Use the retrieved code context to inform your responses, but feel free to suggest better solutions if appropriate.
"""

PRE_PROMPT = """
Based on the user's query and the following code context, provide a helpful response. If improvements can be made, suggest them with explanations.

User Query: {query}

Retrieved Code Context:
{code_context}

Your response:
"""

def execute_rag_flow(user_query):
    try:
        # Perform code search
        search_results = search_code(user_query)
        
        if not search_results:
            return "No relevant code found for your query."
        
        # Prepare code context
        code_context = "\n\n".join([
            f"File: {result['filename']}\n{result['content']}"
            for result in search_results[:3]  # Limit to top 3 results
        ])
        
        # Construct the full prompt
        full_prompt = PRE_PROMPT.format(query=user_query, code_context=code_context)
        
        # Generate response using OpenAI
        response = client.chat.completions.create(
            model=RAG_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error in RAG flow execution: {e}"