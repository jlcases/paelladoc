#!/bin/bash

# Script to sync project documentation from docs/ to Jekyll site structure
# Usage: ./sync_projects.sh

# Set variables
DOCS_DIR="../docs"
PROJECTS_DIR="projects"
MEMORY_FILE="../.memory.json"
CURRENT_DATE=$(date +"%Y-%m-%d")

# Create projects directory if it doesn't exist
mkdir -p "$PROJECTS_DIR"

# Function to check if a project is private
is_project_private() {
    local project="$1"
    
    # Check if memory file exists
    if [ -f "$MEMORY_FILE" ]; then
        # Use jq to check if project is marked as private
        if command -v jq >/dev/null 2>&1; then
            local is_private=$(jq -r ".projects.\"$project\".private // false" "$MEMORY_FILE")
            if [ "$is_private" = "true" ]; then
                return 0  # True, project is private
            fi
        else
            # Fallback if jq is not available
            if grep -q "\"$project\".*\"private\".*true" "$MEMORY_FILE"; then
                return 0  # True, project is private
            fi
        fi
    fi
    
    return 1  # False, project is not private
}

# Function to add Jekyll front matter to markdown files
add_front_matter() {
    local file="$1"
    local project="$2"
    local title=$(grep -m 1 "^# " "$file" | sed 's/^# //')
    
    # If no title found, use filename
    if [ -z "$title" ]; then
        title=$(basename "$file" .md | sed 's/_/ /g' | sed 's/^[0-9]*-//' | sed 's/^[0-9]*_//')
        title="$(tr '[:lower:]' '[:upper:]' <<< ${title:0:1})${title:1}"
    fi
    
    # Extract description if available (first paragraph after title)
    local description=$(awk '/^# /{flag=1;next} /^$/{if(flag==1)flag=2} /^[^#]/{if(flag==2){print;flag=3}}' "$file" | head -1)
    
    # If no description found, create a generic one
    if [ -z "$description" ]; then
        description="Documentation for the $title section of the $project project."
    fi
    
    # Get the order number from filename if available
    local order=50
    if [[ $(basename "$file") =~ ^[0-9]+ ]]; then
        order=$(basename "$file" | grep -o "^[0-9]*")
        # If order is empty, set default
        if [ -z "$order" ]; then
            order=50
        fi
    fi
    
    # Create temporary file with front matter
    local temp_file=$(mktemp)
    cat > "$temp_file" << EOF
---
layout: project-layout
title: "$title"
description: "$description"
project: "$project"
date: $CURRENT_DATE
order: $order
---

EOF
    
    # Append original content without the title
    sed '1,/^# /d' "$file" >> "$temp_file"
    
    # Replace original file
    mv "$temp_file" "$file"
}

# Function to create index file for a project
create_project_index() {
    local project_dir="$1"
    local project=$(basename "$project_dir")
    local index_file="$project_dir/index.md"
    
    # Check if 00_index.md exists and use it as a base
    if [ -f "$project_dir/00_index.md" ]; then
        cp "$project_dir/00_index.md" "$index_file"
    else
        # Create a basic index file
        cat > "$index_file" << EOF
# $project Documentation

This is the documentation for the $project project.

## Available Documents

EOF
        
        # List all documents in the project
        for doc in "$project_dir"/*.md; do
            if [ "$(basename "$doc")" != "index.md" ]; then
                local doc_title=$(grep -m 1 "^# " "$doc" | sed 's/^# //')
                if [ -z "$doc_title" ]; then
                    doc_title=$(basename "$doc" .md | sed 's/_/ /g' | sed 's/^[0-9]*-//' | sed 's/^[0-9]*_//')
                    doc_title="$(tr '[:lower:]' '[:upper:]' <<< ${doc_title:0:1})${doc_title:1}"
                fi
                echo "- [$doc_title]($(basename "$doc"))" >> "$index_file"
            fi
        done
    fi
    
    # Add front matter to index
    add_front_matter "$index_file" "$project"
}

# Function to clean up projects that no longer exist in docs
cleanup_removed_projects() {
    # Get list of projects in Jekyll site
    for project_dir in "$PROJECTS_DIR"/*; do
        if [ -d "$project_dir" ]; then
            local project=$(basename "$project_dir")
            
            # Check if project still exists in docs or is now private
            if [ ! -d "$DOCS_DIR/$project" ] || is_project_private "$project"; then
                echo "Removing project from Jekyll site: $project (deleted or now private)"
                rm -rf "$project_dir"
            fi
        fi
    done
}

# Process each project in the docs directory
echo "Starting documentation sync..."

# First, clean up removed projects
cleanup_removed_projects

# Then process each project in docs
for project_dir in "$DOCS_DIR"/*; do
    if [ -d "$project_dir" ]; then
        project=$(basename "$project_dir")
        
        # Skip private projects
        if is_project_private "$project"; then
            echo "Skipping private project: $project"
            continue
        fi
        
        echo "Processing project: $project"
        
        # Create project directory in Jekyll site
        mkdir -p "$PROJECTS_DIR/$project"
        
        # Copy all markdown files
        find "$project_dir" -name "*.md" -exec cp {} "$PROJECTS_DIR/$project/" \;
        
        # Process each markdown file to add front matter
        for md_file in "$PROJECTS_DIR/$project"/*.md; do
            echo "  Adding front matter to: $(basename "$md_file")"
            add_front_matter "$md_file" "$project"
        done
        
        # Create or update index file
        echo "  Creating index for: $project"
        create_project_index "$PROJECTS_DIR/$project"
        
        # Copy any assets
        if [ -d "$project_dir/assets" ]; then
            echo "  Copying assets for: $project"
            mkdir -p "$PROJECTS_DIR/$project/assets"
            cp -r "$project_dir/assets"/* "$PROJECTS_DIR/$project/assets/"
        fi
    fi
done

echo "Documentation sync completed!" 