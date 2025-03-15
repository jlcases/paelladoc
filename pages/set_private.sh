#!/bin/bash

# Script to mark a project as private in memory file
# Usage: ./set_private.sh PROJECT_NAME [true|false]

# Check if project name is provided
if [ -z "$1" ]; then
    echo "Error: Project name is required."
    echo "Usage: ./set_private.sh PROJECT_NAME [true|false]"
    exit 1
fi

# Set variables
PROJECT_NAME="$1"
PRIVATE_STATUS="${2:-true}"  # Default to true if not specified
MEMORY_FILE="../.memory.json"
DOCS_DIR="../docs"
PROJECTS_DIR="projects"

# Validate private status
if [ "$PRIVATE_STATUS" != "true" ] && [ "$PRIVATE_STATUS" != "false" ]; then
    echo "Error: Private status must be 'true' or 'false'."
    echo "Usage: ./set_private.sh PROJECT_NAME [true|false]"
    exit 1
fi

# Check if project exists in docs
if [ ! -d "$DOCS_DIR/$PROJECT_NAME" ]; then
    echo "Warning: Project '$PROJECT_NAME' not found in docs directory."
    echo "Will still update memory file, but project may not exist."
fi

# Update memory file
if [ -f "$MEMORY_FILE" ]; then
    # Check if jq is available
    if command -v jq >/dev/null 2>&1; then
        # Create a temporary file
        TEMP_FILE=$(mktemp)
        
        # Check if projects key exists
        if ! jq -e '.projects' "$MEMORY_FILE" > /dev/null 2>&1; then
            # Create projects object if it doesn't exist
            jq '. + {"projects":{}}' "$MEMORY_FILE" > "$TEMP_FILE"
            mv "$TEMP_FILE" "$MEMORY_FILE"
        fi
        
        # Check if project exists in memory
        if ! jq -e ".projects.\"$PROJECT_NAME\"" "$MEMORY_FILE" > /dev/null 2>&1; then
            # Create project object if it doesn't exist
            jq ".projects += {\"$PROJECT_NAME\":{\"private\":$PRIVATE_STATUS}}" "$MEMORY_FILE" > "$TEMP_FILE"
        else
            # Update existing project
            jq ".projects.\"$PROJECT_NAME\".private = $PRIVATE_STATUS" "$MEMORY_FILE" > "$TEMP_FILE"
        fi
        
        # Update the original file
        mv "$TEMP_FILE" "$MEMORY_FILE"
        
        echo "Updated memory file: Set project '$PROJECT_NAME' private status to $PRIVATE_STATUS"
    else
        echo "Error: jq not found. Cannot update memory file."
        echo "Please install jq or manually update $MEMORY_FILE"
        exit 1
    fi
else
    echo "Error: Memory file not found at $MEMORY_FILE"
    echo "Creating a new memory file with project settings"
    
    # Check if jq is available
    if command -v jq >/dev/null 2>&1; then
        # Create a new memory file with project settings
        echo "{\"projects\":{\"$PROJECT_NAME\":{\"private\":$PRIVATE_STATUS}}}" | jq '.' > "$MEMORY_FILE"
        echo "Created new memory file with project '$PROJECT_NAME' private status set to $PRIVATE_STATUS"
    else
        # Create a basic JSON file without jq
        echo "{\"projects\":{\"$PROJECT_NAME\":{\"private\":$PRIVATE_STATUS}}}" > "$MEMORY_FILE"
        echo "Created new memory file with project '$PROJECT_NAME' private status set to $PRIVATE_STATUS"
    fi
fi

# If project is now private, remove it from pages
if [ "$PRIVATE_STATUS" = "true" ] && [ -d "$PROJECTS_DIR/$PROJECT_NAME" ]; then
    echo "Removing private project from pages: $PROJECT_NAME"
    rm -rf "$PROJECTS_DIR/$PROJECT_NAME"
fi

# If project is now public, sync it to pages
if [ "$PRIVATE_STATUS" = "false" ] && [ -d "$DOCS_DIR/$PROJECT_NAME" ]; then
    echo "Project is now public. Run ./sync_projects.sh to update pages."
fi

echo "Private status update completed!" 