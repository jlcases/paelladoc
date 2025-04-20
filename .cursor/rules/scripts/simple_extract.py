#!/usr/bin/env python3
"""
Simple Repository Extractor
--------------------------
A minimal script that clones a repository and extracts basic information
to create a context file.
"""

import os
import sys
import subprocess
import argparse
import glob
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

def extract_basic_info(repo_path, context_file):
    """Extract basic info from repository into a text file."""
    if not os.path.exists(repo_path):
        print(f"Error: Repository path does not exist: {repo_path}")
        return False
    
    # Create output directory if needed
    ensure_directory_exists(os.path.dirname(context_file))
    
    # Start with basic repository info
    with open(context_file, 'w', encoding='utf-8') as f:
        f.write(f"Repository path: {repo_path}\n")
        f.write(f"Extraction date: {subprocess.check_output(['date']).decode('utf-8')}\n\n")
        
        # Get repository structure
        f.write("=== REPOSITORY STRUCTURE ===\n")
        
        # Get list of directories
        try:
            dirs = [d for d in os.listdir(repo_path) if os.path.isdir(os.path.join(repo_path, d)) and not d.startswith('.')]
            f.write(f"Directories: {', '.join(dirs)}\n\n")
        except Exception as e:
            f.write(f"Error listing directories: {e}\n\n")
        
        # Extract README if exists
        readme_files = glob.glob(os.path.join(repo_path, "README*"))
        if readme_files:
            f.write("=== README CONTENT ===\n")
            try:
                with open(readme_files[0], 'r', encoding='utf-8') as readme:
                    f.write(readme.read())
                f.write("\n\n")
            except Exception as e:
                f.write(f"Error reading README: {e}\n\n")
        
        # Look for package.json or similar files to determine dependencies
        package_files = glob.glob(os.path.join(repo_path, "package.json"))
        if package_files:
            f.write("=== DEPENDENCIES ===\n")
            try:
                with open(package_files[0], 'r', encoding='utf-8') as pkg:
                    f.write(pkg.read())
                f.write("\n\n")
            except Exception as e:
                f.write(f"Error reading package.json: {e}\n\n")
        
        # Sample some code files
        f.write("=== CODE SAMPLES ===\n")
        extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.java', '.c', '.cpp']
        found_files = []
        
        for ext in extensions:
            files = glob.glob(os.path.join(repo_path, f"**/*{ext}"), recursive=True)
            found_files.extend(files[:3])  # Take up to 3 files of each type
            
        for code_file in found_files[:10]:  # Limit to 10 files total
            f.write(f"\n--- {os.path.relpath(code_file, repo_path)} ---\n")
            try:
                with open(code_file, 'r', encoding='utf-8') as code:
                    content = code.read()
                    # Limit to first 500 chars if file is large
                    if len(content) > 500:
                        f.write(content[:500] + "\n...(truncated)...\n")
                    else:
                        f.write(content)
            except Exception as e:
                f.write(f"Error reading file: {e}\n")
    
    print(f"Repository information extracted to: {context_file}")
    return True

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Simple Repository Extractor")
    parser.add_argument("repo_path", help="Path or URL to the repository")
    parser.add_argument("--output", default="code_context/extracted/repo_content.txt", 
                       help="Output file for extracted context")
    parser.add_argument("--clone-dir", default="temp_cloned_repos", 
                       help="Directory to clone remote repositories into")
    parser.add_argument("--force-clone", action="store_true", 
                       help="Force re-cloning by removing existing clone directory")
    
    args = parser.parse_args()
    
    actual_repo_path = args.repo_path
    clone_base_dir = args.clone_dir
    
    # Handle Git URL
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
        
        actual_repo_path = local_path
    elif not os.path.isdir(actual_repo_path):
        print(f"Error: Local repository path does not exist or is not a directory: {actual_repo_path}")
        sys.exit(1)
    
    # Extract repository information
    if not extract_basic_info(actual_repo_path, args.output):
        print("Failed to extract repository information. Exiting.")
        sys.exit(1)
    
    print("\nRepository preparation completed successfully.")
    print(f"Context file: {args.output}")
    print(f"Local repository path: {actual_repo_path}")
    
    print("\n=== IMPORTANT MESSAGE FOR AI CHAT ===")
    print("1. READ the extracted context file. DO NOT search the web!")
    print("2. Give ONE brief paragraph about the repository")
    print("3. IMMEDIATELY show the fixed 19-option menu in Spanish")
    print("4. Wait for user selection before proceeding")
    print("==========================================")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 