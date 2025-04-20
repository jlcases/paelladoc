#!/usr/bin/env python3
"""
extract_repo_content.py - Convert code repositories to text format using repopack

This script processes a code repository and converts it to a text file 
that can be easily consumed by AI systems for documentation generation.

Usage:
    python extract_repo_content.py repo_path [options]

Options:
    --output FILE           Output file name (default: repopack_output.txt)
    --line-numbers          Show line numbers in the output
    --style FORMAT          Output style: plain or xml (default: plain)
    --ignore PATTERNS       Additional patterns to ignore (comma-separated)
    --venv PATH             Path to virtual environment (default: .venv)
"""

import os
import sys
import subprocess
import argparse
import venv


def setup_virtual_env(venv_path):
    """Create and setup virtual environment if it doesn't exist."""
    if not os.path.exists(venv_path):
        print(f"Creating virtual environment at {venv_path}...")
        venv.create(venv_path, with_pip=True)
    
    # Determine the pip path based on the platform
    if sys.platform == "win32":
        pip_path = os.path.join(venv_path, "Scripts", "pip")
    else:
        pip_path = os.path.join(venv_path, "bin", "pip")
    
    # Install repopack
    print("Installing repopack...")
    subprocess.check_call([pip_path, "install", "repopack"])
    
    return venv_path


def run_repopack(repo_path, output_file, venv_path, line_numbers=False, style="plain", ignore=None):
    """Run repopack on the repository."""
    if not os.path.exists(repo_path):
        print(f"Error: Repository path {repo_path} does not exist")
        sys.exit(1)
    
    # Determine the repopack executable path
    if sys.platform == "win32":
        repopack_path = os.path.join(venv_path, "Scripts", "repopack")
    else:
        repopack_path = os.path.join(venv_path, "bin", "repopack")
    
    # Build command
    cmd = [repopack_path, repo_path, "-o", output_file]
    
    if line_numbers:
        cmd.append("--output-show-line-numbers")
    
    if style:
        cmd.append("--output-style")
        cmd.append(style)
    
    if ignore:
        cmd.append("--ignore")
        cmd.append(ignore)
    
    # Execute repopack
    print(f"Processing repository: {repo_path}")
    print(f"Command: {' '.join(cmd)}")
    subprocess.check_call(cmd)
    
    print(f"Repository content has been extracted to: {output_file}")


def main():
    """Main function to process arguments and run the script."""
    parser = argparse.ArgumentParser(description="Convert code repositories to text format")
    parser.add_argument("repo_path", help="Path to the repository")
    parser.add_argument("--output", default="repopack_output.txt", help="Output file name")
    parser.add_argument("--line-numbers", action="store_true", help="Show line numbers in output")
    parser.add_argument("--style", choices=["plain", "xml"], default="plain", help="Output style")
    parser.add_argument("--ignore", help="Additional patterns to ignore (comma-separated)")
    parser.add_argument("--venv", default=".venv", help="Path to virtual environment")
    
    args = parser.parse_args()
    
    # Setup virtual environment
    venv_path = setup_virtual_env(args.venv)
    
    # Run repopack
    run_repopack(
        args.repo_path,
        args.output,
        venv_path,
        line_numbers=args.line_numbers,
        style=args.style,
        ignore=args.ignore
    )


if __name__ == "__main__":
    main() 