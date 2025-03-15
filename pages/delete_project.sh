#!/bin/bash

# Script to delete a project from both docs and pages
# Usage: ./delete_project.sh PROJECT_NAME

# Check if project name is provided
if [ -z "$1" ]; then
    echo "Error: Project name is required."
    echo "Usage: ./delete_project.sh PROJECT_NAME"
    exit 1
fi

# Set variables
PROJECT_NAME="$1"
DOCS_DIR="../docs"
PROJECTS_DIR="projects"
MEMORY_FILE="../.memory.json"

# Check if project exists in docs
if [ ! -d "$DOCS_DIR/$PROJECT_NAME" ]; then
    echo "Warning: Project '$PROJECT_NAME' not found in docs directory."
else
    # Delete project from docs
    echo "Deleting project from docs: $PROJECT_NAME"
    rm -rf "$DOCS_DIR/$PROJECT_NAME"
fi

# Check if project exists in pages
if [ ! -d "$PROJECTS_DIR/$PROJECT_NAME" ]; then
    echo "Warning: Project '$PROJECT_NAME' not found in pages directory."
else
    # Delete project from pages
    echo "Deleting project from pages: $PROJECT_NAME"
    rm -rf "$PROJECTS_DIR/$PROJECT_NAME"
fi

# Update memory file if it exists
if [ -f "$MEMORY_FILE" ]; then
    # Check if jq is available
    if command -v jq >/dev/null 2>&1; then
        # Create a temporary file
        TEMP_FILE=$(mktemp)
        
        # Remove project from memory file using jq
        jq "del(.projects.\"$PROJECT_NAME\")" "$MEMORY_FILE" > "$TEMP_FILE"
        
        # Update the original file
        mv "$TEMP_FILE" "$MEMORY_FILE"
        
        echo "Updated memory file: Removed project '$PROJECT_NAME'"
    else
        echo "Warning: jq not found. Cannot update memory file automatically."
        echo "Please manually remove the project from $MEMORY_FILE"
    fi
else
    echo "Warning: Memory file not found at $MEMORY_FILE"
fi

echo "Project deletion completed!" 