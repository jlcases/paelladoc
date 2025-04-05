#!/usr/bin/env python3
"""
PAELLADOC Test Script for GENERATE_DOC
--------------------------------------
This script tests the hybrid approach for the GENERATE_DOC command.
It verifies:
1. Repository cloning works (if it's a URL)
2. Content extraction happens correctly
3. The script returns to let AI chat handle the menu presentation

Usage:
    python test_generate_doc.py [repo_path] [language]
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Test the GENERATE_DOC command's hybrid approach")
    parser.add_argument("repo_path", help="Path or URL to the repository", nargs="?", default="https://github.com/mdn/content")
    parser.add_argument("language", help="Language for documentation", nargs="?", default="en")
    parser.add_argument("--output", default="docs/test_generated", help="Output directory")
    parser.add_argument("--context-file", default="code_context/extracted/test_repo_content.txt", help="Context output file")
    parser.add_argument("--force-clone", action="store_true", help="Force re-cloning of remote repo")
    parser.add_argument("--force-context", action="store_true", help="Force context regeneration")
    
    args = parser.parse_args()
    
    # The actual script we want to test
    generate_doc_script = os.path.join(os.path.dirname(__file__), "run_generate_doc.py")
    
    # Build the command
    cmd = [
        sys.executable,
        generate_doc_script,
        args.repo_path,
        args.language,
        "--output", args.output,
        "--context-output-file", args.context_file
    ]
    
    if args.force_clone:
        cmd.append("--force-clone")
    
    if args.force_context:
        cmd.append("--force-context-regeneration")
    
    # Print what we're about to run
    print(f"Running test with command:")
    print(" ".join(cmd))
    print("\n" + "=" * 50)
    
    # Run the command
    try:
        process = subprocess.run(cmd, check=True, text=True)
        print("\n" + "=" * 50)
        print("Test completed successfully!")
        
        # Verify expected outputs
        context_file_exists = os.path.isfile(args.context_file)
        context_file_size = os.path.getsize(args.context_file) if context_file_exists else 0
        
        print("\nVerification:")
        print(f"Context file exists: {context_file_exists}")
        print(f"Context file size: {context_file_size} bytes")
        
        if context_file_exists and context_file_size > 0:
            print("✅ Test PASSED: Script correctly prepared repository context")
            print("\nNow the AI chat should take over and present the interactive documentation menu.")
        else:
            print("❌ Test FAILED: Script did not generate the expected context file")
            
    except subprocess.CalledProcessError as e:
        print(f"Test failed with error code {e.returncode}")
        print(f"Error message: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 