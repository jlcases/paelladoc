#!/usr/bin/env python3
"""
PAELLADOC Continue Command - Project Scanner Script
---------------------------------
This script scans the docs directory for existing projects, reads their memory.json files,
and prepares a list of projects for the user to continue working on.

Usage:
    python run_continue.py [options]
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime

def ensure_directory_exists(directory):
    """Ensures the specified directory exists."""
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory

def find_project_root():
    """Find the project root by locating the .cursor directory."""
    current_dir = Path(os.getcwd())
    # Try to find the project root by looking for .cursor directory
    while current_dir != current_dir.parent:
        if (current_dir / '.cursor').exists():
            return current_dir
        current_dir = current_dir.parent
    
    # If not found, use current directory as fallback
    return Path(os.getcwd())

def scan_projects_directory(docs_path):
    """
    Recursively scans docs directory and its subdirectories for projects with memory.json files
    Returns a list of projects with their details
    """
    projects = []
    docs_dir = Path(docs_path)
    
    if not docs_dir.exists() or not docs_dir.is_dir():
        print(f"Docs directory not found: {docs_path}")
        return []
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(docs_dir):
        root_path = Path(root)
        
        # Check if memory.json exists in this directory
        memory_file = root_path / 'memory.json'
        if memory_file.exists() and memory_file.is_file():
            try:
                with open(memory_file, 'r') as f:
                    memory_data = json.load(f)
                
                # Extract key information
                project_info = {
                    "name": memory_data.get("project_name", root_path.name),
                    "type": memory_data.get("project_type", "Unknown"),
                    "language": memory_data.get("language", "Unknown"),
                    "last_updated": memory_data.get("last_updated", "Unknown"),
                    "methodologies": memory_data.get("methodologies", []),
                    "git_workflow": memory_data.get("git_workflow", "Unknown"),
                    "path": str(root_path)
                }
                projects.append(project_info)
                
            except json.JSONDecodeError:
                print(f"Error decoding memory.json for project in {root_path}")
            except Exception as e:
                print(f"Error reading project in {root_path}: {e}")
    
    # Sort projects by last_updated timestamp (most recent first)
    try:
        projects.sort(key=lambda x: datetime.fromisoformat(x["last_updated"]) if x["last_updated"] != "Unknown" else datetime.min, reverse=True)
    except (ValueError, TypeError):
        # Fall back to sorting by name if datetime parsing fails
        projects.sort(key=lambda x: x["name"])
        
    return projects

def main():
    """Main function - handles project directory scanning."""
    # Find project root and default docs path
    project_root = find_project_root()
    default_docs_path = project_root / "docs"
    
    parser = argparse.ArgumentParser(description="PAELLADOC CONTINUE Command - Project Scanner")
    parser.add_argument("--docs-path", default=str(default_docs_path), 
                        help="Path to the docs directory containing projects")
    
    args = parser.parse_args()
    
    # Scan for projects
    print(f"Scanning for projects in {args.docs_path} and its subdirectories...")
    projects = scan_projects_directory(args.docs_path)
    
    # Display results
    if not projects:
        print("\n=== NO PROJECTS FOUND ===")
        print("No projects found to continue. Use the PAELLA command to create a new project.")
        print("=============================================")
        return
    
    print("\n=== AVAILABLE PROJECTS ===")
    for i, project in enumerate(projects, 1):
        last_updated = project["last_updated"] if project["last_updated"] != "Unknown" else "No date available"
        print(f"{i}. {project['name']} - {project['type']} - Last updated: {last_updated}")
        print(f"   Path: {project['path']}")
    
    # Print additional information for the AI chat to use
    print("\n=== PROJECT DETAILS FOR AI CHAT ===")
    print(json.dumps(projects))
    print("====================================")
    
    print("\n=== CONTINUE COMMAND WORKFLOW ===")
    print("1. ALWAYS list the available projects first")
    print("2. WAIT for the user to select a project by number or name")
    print("3. LOAD the selected project's memory.json file")
    print("4. ASK about updating Cursor rules and template synchronization")
    print("5. ONE QUESTION AT A TIME - WAIT for user response before proceeding")
    print("6. DO NOT combine multiple questions into a single message")
    print("7. FOLLOW the exact sequence in the rules file")
    print("=============================================")

if __name__ == "__main__":
    main() 