#!/bin/bash

# Script to update .gitignore with private projects
# Usage: ./update_gitignore.sh

# Set variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="../docs"
MEMORY_FILE="../.memory.json"
GITIGNORE_FILE="../.gitignore"

# Check if memory file exists
if [ ! -f "$MEMORY_FILE" ]; then
    echo "Error: Memory file not found at $MEMORY_FILE"
    exit 1
fi

# Check if gitignore file exists
if [ ! -f "$GITIGNORE_FILE" ]; then
    echo "Error: .gitignore file not found at $GITIGNORE_FILE"
    exit 1
fi

# Create a temporary file
TEMP_FILE=$(mktemp)

# Copy existing gitignore content up to private projects section
sed '/# Private projects/,$d' "$GITIGNORE_FILE" > "$TEMP_FILE" || {
    # If the section doesn't exist, copy the entire file
    cp "$GITIGNORE_FILE" "$TEMP_FILE"
    echo "" >> "$TEMP_FILE"
}

# Add private projects section header
cat >> "$TEMP_FILE" << EOF
# Private projects
# These are automatically generated based on .memory.json
/docs/*/private/
/pages/projects/*/private/

# Specific private projects - Auto-generated, do not edit manually
EOF

# Get list of private projects
if command -v jq >/dev/null 2>&1; then
    # Use jq to get private projects
    private_projects=$(jq -r '.projects | to_entries[] | select(.value.private == true) | .key' "$MEMORY_FILE")
else
    # Fallback if jq is not available
    private_projects=$(grep -o '"[^"]*".*"private".*true' "$MEMORY_FILE" | grep -o '"[^"]*"' | head -1 | tr -d '"')
fi

# Add each private project to gitignore
if [ -n "$private_projects" ]; then
    echo "$private_projects" | while read -r project; do
        if [ -n "$project" ]; then
            echo "/docs/$project/" >> "$TEMP_FILE"
            echo "/pages/projects/$project/" >> "$TEMP_FILE"
        fi
    done
else
    echo "# No private projects found" >> "$TEMP_FILE"
fi

# Update the original file
mv "$TEMP_FILE" "$GITIGNORE_FILE"

echo "Updated .gitignore with private projects" 