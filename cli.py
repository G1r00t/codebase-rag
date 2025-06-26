#!/usr/bin/env python3
"""
Simple CLI for CodeRAG - Query only (no indexing)
"""

import argparse
import sys
from openai import OpenAI
from Rag_modules.config import OPENAI_KEY
from prompt_flow import execute_rag_flow

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_KEY)


def interactive_mode():
    """Interactive chat mode"""
    print("CodeRAG CLI - Interactive Mode")
    print("Type 'quit', 'exit', or 'q' to exit")
    print("-" * 40)
    
    while True:
        try:
            query = input("\n🤖 Ask your coding question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not query:
                continue
                
            print("\n🔍 Searching...")
            response = execute_rag_flow(query)
            print(f"\n📝 Response:\n{response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


def single_query(query):
    """Execute a single query"""
    try:
        print(f"Query: {query}")
        print("-" * 40)
        response = execute_rag_flow(query)
        print(f"Response:\n{response}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="CodeRAG CLI - Your Coding Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Interactive mode
  %(prog)s -q "How to prevent SQL injection?"  # Single query
  %(prog)s --query "Best practices for authentication"
        """
    )
    
    parser.add_argument(
        '-q', '--query',
        help='Single query to execute (non-interactive mode)'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Force interactive mode (default if no query provided)'
    )
    
    args = parser.parse_args()
    
    # If query is provided, run single query mode
    if args.query:
        single_query(args.query)
    else:
        # Default to interactive mode
        interactive_mode()


if __name__ == '__main__':
    main()