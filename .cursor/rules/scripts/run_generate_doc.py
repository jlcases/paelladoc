#!/usr/bin/env python3
"""
PAELLADOC Documentation Generator - Preparation Script
---------------------------------
This script ONLY prepares the repository context by:
1. Cloning the repository if it's a URL
2. Running extract_repo_content.py to extract the context
3. Then returning to allow the AI chat to handle the interactive documentation generation

Usage:
    python run_generate_doc.py repo_path language [options]
"""

import os
import sys
import subprocess
import argparse
import re
from pathlib import Path
import shutil

def ensure_directory_exists(directory):
    """Ensures the specified directory exists."""
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory

def is_git_url(path):
    """Check if the path looks like a git URL."""
    return path.startswith(('http://', 'https://', 'git@')) or path.endswith('.git')

def clone_repository(repo_url, clone_dir, force=False):
    """Clones the repository from the URL into the clone_dir."""
    clone_path = Path(clone_dir)
    if clone_path.exists():
        if force:
            print(f"Removing existing directory: {clone_path}")
            shutil.rmtree(clone_path)
        else:
            print(f"Directory already exists: {clone_path}. Using existing clone.")
            # Optionally add git pull logic here if needed
            return str(clone_path)

    ensure_directory_exists(os.path.dirname(clone_path))
    print(f"Cloning {repo_url} into {clone_path}...")
    try:
        subprocess.run(["git", "clone", repo_url, str(clone_path)], check=True, capture_output=True, text=True)
        print("Repository cloned successfully.")
        return str(clone_path)
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Error: 'git' command not found. Please ensure Git is installed and in your PATH.")
        return None

def run_context_extraction(local_repo_path, context_output_file):
    """Runs the extract_repo_content.py script."""
    script_path = Path(__file__).parent / "extract_repo_content.py"
    venv_path = Path(__file__).parent.parent.parent / ".venv" # Assuming venv is at project root

    if not script_path.exists():
        print(f"Error: Context extraction script not found at {script_path}")
        return False
        
    # Prepare arguments for extract_repo_content.py
    cmd = [
        sys.executable, 
        str(script_path), 
        local_repo_path, # Positional argument
        "--output", context_output_file, # Use the correct output path
        "--venv", str(venv_path) # Point to the venv used by the main project
        # Add other options like --line-numbers if needed, passed from main args
    ]
    
    print(f"\nRunning context extraction...")
    print(f"Command: {' '.join(cmd)}")
    try:
        # Ensure the output directory exists
        ensure_directory_exists(os.path.dirname(context_output_file))
        process = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Context extraction script finished.")
        print(f"Stdout:\n{process.stdout}")
        if process.stderr:
             print(f"Stderr:\n{process.stderr}")
        if not Path(context_output_file).exists():
             print(f"Warning: Context file {context_output_file} was not created by the script.")
             return False
        print(f"Context successfully extracted to: {context_output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running context extraction script: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Error: Python executable '{sys.executable}' or script '{script_path}' not found.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during context extraction: {e}")
        return False

def main():
    """Main function - ONLY handles repository preparation."""
    parser = argparse.ArgumentParser(description="PAELLADOC Context Preparation Script")
    # Arguments expected from the orchestrator/user
    parser.add_argument("repo_path", help="Path or URL to the repository")
    parser.add_argument("language", help="Output language for documentation (e.g., es, en)")
    parser.add_argument("--output", default="docs/generated", help="Output directory for generated documentation")
    parser.add_argument("--context-output-file", default="code_context/extracted/repo_content.txt", help="Path to save the extracted repository context")
    parser.add_argument("--clone-dir", default="temp_cloned_repos", help="Directory to clone remote repositories into")
    parser.add_argument("--template", default="standard", help="Documentation template to use")
    parser.add_argument("--force-context-regeneration", action="store_true", help="Force regeneration of context file")
    parser.add_argument("--force-clone", action="store_true", help="Force re-cloning by removing existing clone directory")
    
    args = parser.parse_args()

    actual_repo_path = args.repo_path
    clone_base_dir = args.clone_dir

    # --- Handle Git URL ---    
    if is_git_url(args.repo_path):
        repo_name = os.path.basename(args.repo_path)
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        repo_clone_path = os.path.join(clone_base_dir, repo_name)
        print(f"Detected Git URL. Attempting to clone into {repo_clone_path}")
        local_path = clone_repository(args.repo_path, repo_clone_path, args.force_clone)
        if not local_path:
            print("Failed to clone repository. Exiting.")
            sys.exit(1)
        actual_repo_path = local_path # Use the local path from now on
    elif not Path(actual_repo_path).is_dir():
         print(f"Error: Local repository path does not exist or is not a directory: {actual_repo_path}")
         sys.exit(1)
    # --- End Handle Git URL ---
    
    # --- Context Extraction --- 
    context_file = args.context_output_file
    context_exists = Path(context_file).exists()

    if not context_exists or args.force_context_regeneration:
        print(f"Regenerating context file: {context_file}")
        if not run_context_extraction(actual_repo_path, context_file):
            print("Failed to extract repository context. Exiting.")
            sys.exit(1)
    else:
        print(f"Using existing context file: {context_file}")
    # --- End Context Extraction ---
        
    # --- Returning to AI Chat for Interactive Documentation ---
    print(f"\nPAELLADOC run_generate_doc finished.")
    print(f"Context file prepared at: {context_file}")
    print(f"Local repository path: {actual_repo_path}")
    print(f"Documentation language: {args.language}")
    print(f"Documentation output directory: {args.output}")
    print(f"Documentation template: {args.template}")
    print("\nNow returning to AI chat for interactive documentation generation...")
    print("\n=== IMPORTANT MESSAGE FOR AI CHAT ===")
    print("1. ALWAYS ASK FOR LANGUAGE CONFIRMATION FIRST!")
    print("2. WAIT for explicit language confirmation from the user.")
    print("3. Only then proceed with repository analysis.")
    print("4. DO NOT SEARCH THE WEB for repository information!")
    print(f"5. PRESENT the DYNAMIC menu based on template files in the selected language ({args.language})!")
    print("6. ONE brief paragraph about repository then IMMEDIATELY show the dynamic menu")
    print("7. NO extensive analysis before showing the menu")
    print("8. WAIT for user selection before proceeding")
    print("9. The menu options are based on ACTUAL template files available in the system")
    print("10. When a user selects an option, USE THE EXISTING TEMPLATE file as the foundation")
    print("11. SAVE filled-in templates as MD files in the original template directories")
    print("12. DON'T just display documentation in the conversation, SAVE actual files")
    print("==========================================")
    
    print("\n=== CODE IS KING - CRITICAL INSTRUCTIONS ===")
    print("1. ALL documentation MUST be based SOLELY on the extracted context file.")
    print("2. The context file at code_context/extracted/repo_content.txt is the ONLY source of truth.")
    print("3. DO NOT infer, guess, or create information not explicitly in the context file.")
    print("4. If information requested is not in the context file, state this explicitly.")
    print("5. DO NOT use general knowledge about software, technologies, or frameworks.")
    print("6. NEVER generate fictitious content when data is missing.")
    print("7. STRICTLY adhere to 'CODE IS KING' - context file is the only source of truth")
    print("=====================================================")
    
    print("\n=== ABSOLUTELY CRITICAL: USE THIS EXACT FILE ===")
    print("THE ONLY SOURCE OF TRUTH IS:")
    print("/Users/jlcases/codigo/paelladoc/code_context/extracted/repo_content.txt")
    print("1. ALWAYS check this exact file path for EVERY piece of information")
    print("2. NEVER rely on memory without consulting the context file again")
    print("3. For EACH section of documentation, go back to this file")
    print("4. The file at this exact path contains all the information needed")
    print("5. DO NOT use any other sources of information")
    print("=====================================================")
    
    # Run the menu enforcer script to ensure the menu is displayed
    try:
        menu_enforcer_script = os.path.join(os.path.dirname(__file__), "enforce_fixed_menu.py")
        if os.path.exists(menu_enforcer_script):
            print("\nRunning menu enforcer to guarantee fixed menu presentation...")
            enforcer_process = subprocess.run(
                [sys.executable, menu_enforcer_script],
                check=True,
                text=True
            )
    except Exception as e:
        print(f"Warning: Could not run menu enforcer: {e}")

if __name__ == "__main__":
    main() 