import ast
import re

def extract_code_elements(content, filepath):
    """Extract functions, classes, and important code blocks with context."""
    chunks = []
    
    try:
        # Parse Python AST
        tree = ast.parse(content)
        
        lines = content.split('\n')
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start_line = node.lineno - 1
                end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 10
                
                # Get the actual code block
                code_block = '\n'.join(lines[start_line:end_line])
                
                # Add context (docstring, imports above)
                context_start = max(0, start_line - 5)
                context_lines = lines[context_start:start_line]
                
                # Filter relevant context (imports, comments)
                context = '\n'.join([
                    line for line in context_lines 
                    if line.strip().startswith(('import', 'from', '#', '"""', "'''"))
                ])
                
                chunk_content = f"{context}\n\n{code_block}" if context else code_block
                
                chunks.append({
                    "content": chunk_content,
                    "type": "function" if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else "class",
                    "name": node.name,
                    "line_start": start_line + 1,
                    "line_end": end_line
                })
        
        # If no functions/classes found, chunk by logical blocks
        if not chunks:
            chunks = chunk_by_blocks(content, filepath)
            
    except SyntaxError:
        # Fallback for malformed Python files
        chunks = chunk_by_blocks(content, filepath)
    
    return chunks if chunks else [{"content": content, "type": "file", "name": "full_file"}]

def chunk_by_blocks(content, filepath, max_lines=50):
    """Fallback chunking by logical blocks."""
    lines = content.split('\n')
    chunks = []
    current_chunk = []
    current_lines = 0
    
    for line in lines:
        current_chunk.append(line)
        current_lines += 1
        
        # Split on class/function definitions or when chunk gets too large
        if (line.strip().startswith(('def ', 'class ', 'async def ')) and current_lines > 10) or current_lines >= max_lines:
            if len(current_chunk) > 1:  # Don't create tiny chunks
                chunks.append({
                    "content": '\n'.join(current_chunk[:-1]),
                    "type": "block",
                    "name": f"block_{len(chunks)}",
                    "line_start": len(chunks) * max_lines + 1
                })
                current_chunk = [line]
                current_lines = 1
    
    # Add remaining lines
    if current_chunk:
        chunks.append({
            "content": '\n'.join(current_chunk),
            "type": "block",
            "name": f"block_{len(chunks)}",
            "line_start": len(chunks) * max_lines + 1
        })
    
    return chunks