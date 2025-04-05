#!/usr/bin/env python3
"""
PAELLADOC Context Reader
------------------------
This script reads the extracted context file and forces the AI to use it
rather than searching the web. After running this, the AI must show the
fixed 19-option menu in Spanish.
"""

import os
import sys
import argparse
from pathlib import Path

def read_context_file(context_file, max_chars=5000):
    """Read and return the content of the context file (limited sample)."""
    if not os.path.exists(context_file):
        print(f"Error: Context file not found at {context_file}")
        return None
    
    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            # Read up to max_chars to provide a representative sample
            content = f.read(max_chars)
            total_size = os.path.getsize(context_file)
            
        # Add a note if we truncated the file
        if total_size > max_chars:
            content += f"\n\n[...Content truncated, showing {max_chars}/{total_size} bytes...]\n"
            
        return content
    except Exception as e:
        print(f"Error reading context file: {e}")
        return None

def main():
    """Main function to process arguments and read the context."""
    parser = argparse.ArgumentParser(description="PAELLADOC Context Reader")
    parser.add_argument("context_file", nargs="?", 
                       default="code_context/extracted/repo_content.txt",
                       help="Path to the extracted context file")
    parser.add_argument("--max-chars", type=int, default=5000,
                       help="Maximum number of characters to display")
    args = parser.parse_args()
    
    # Read the context file
    content = read_context_file(args.context_file, args.max_chars)
    if not content:
        print("Failed to read context file. The AI must now rely on the repository name only.")
        return 1
    
    print("\n" + "=" * 80)
    print("PAELLADOC EXTRACTED REPOSITORY CONTEXT SAMPLE")
    print("=" * 80)
    print("\nThe AI MUST use this extracted context rather than searching the web:")
    print("-" * 80)
    print(content)
    print("-" * 80)
    
    print("\nCRITICAL INSTRUCTIONS FOR AI:")
    print("1. Use ONLY this extracted context for repository understanding")
    print("2. DO NOT search the web for additional information")
    print("3. Give ONE brief paragraph about the repository based on this context")
    print("4. IMMEDIATELY show the fixed 19-option menu in Spanish")
    print("5. Wait for user selection before proceeding")
    
    print("\n=== CODE IS KING - CRITICAL RULES ===")
    print("1. ALL documentation MUST be based SOLELY on the extracted context file.")
    print("2. DO NOT infer, guess, or create information not explicitly in the context file.")
    print("3. DO NOT use general knowledge about software, technologies, or frameworks.")
    print("4. If information for a requested section is not in the context file, state this explicitly.")
    print("5. NEVER generate fictitious content when data is missing.")
    print("6. STRICTLY adhere to 'CODE IS KING' - context file is the only source of truth")
    print("===========================================")
    
    print("\n=== ABSOLUTELY CRITICAL: USE THIS EXACT FILE PATH ===")
    print("THE ONLY SOURCE OF TRUTH IS:")
    print("/Users/jlcases/codigo/paelladoc/code_context/extracted/repo_content.txt")
    print("1. ALWAYS check this exact file path for EVERY piece of information")
    print("2. NEVER rely on memory without consulting the context file again")
    print("3. For EACH section of documentation, go back to this file")
    print("4. The file at this exact path contains all the information needed")
    print("5. DO NOT use any other sources of information")
    print("6. If the information isn't in this file, state that clearly")
    print("7. NEVER invent content or use general knowledge")
    print("===========================================")
    
    # Identify the full path to make it clear
    abs_path = os.path.abspath(args.context_file)
    print(f"\nFull context file is available at: {abs_path}")
    print(f"File size: {os.path.getsize(args.context_file)} bytes")
    print("=" * 80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 