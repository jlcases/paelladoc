#!/bin/bash

# PaellaDoc Management Script
# Usage: ./paelladoc.sh COMMAND [ARGS]

# Set variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="../docs"
MEMORY_FILE="../.memory.json"

# Display help message
show_help() {
    echo "PaellaDoc Management Script"
    echo "Usage: ./paelladoc.sh COMMAND [ARGS]"
    echo ""
    echo "Commands:"
    echo "  SYNC                   Synchronize projects from docs to pages"
    echo "  DELETE <project>       Delete a project from docs and pages"
    echo "  PRIVATE <project>      Mark a project as private"
    echo "  PUBLIC <project>       Mark a project as public"
    echo "  LIST                   List all projects and their status"
    echo "  SERVE                  Start Jekyll server"
    echo "  UPDATE-GITIGNORE       Update .gitignore with private projects"
    echo "  HELP                   Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./paelladoc.sh SYNC"
    echo "  ./paelladoc.sh DELETE myproject"
    echo "  ./paelladoc.sh PRIVATE secretproject"
    echo "  ./paelladoc.sh PUBLIC publicproject"
    echo "  ./paelladoc.sh LIST"
    echo "  ./paelladoc.sh SERVE"
    echo "  ./paelladoc.sh UPDATE-GITIGNORE"
}

# List all projects and their status
list_projects() {
    echo "Listing all projects:"
    echo "---------------------"
    
    # Check if docs directory exists
    if [ ! -d "$DOCS_DIR" ]; then
        echo "Error: Docs directory not found at $DOCS_DIR"
        return 1
    fi
    
    # Get list of projects in docs
    for project_dir in "$DOCS_DIR"/*; do
        if [ -d "$project_dir" ]; then
            project=$(basename "$project_dir")
            
            # Check if project is private
            is_private="false"
            if [ -f "$MEMORY_FILE" ] && command -v jq >/dev/null 2>&1; then
                is_private=$(jq -r ".projects.\"$project\".private // false" "$MEMORY_FILE")
            elif [ -f "$MEMORY_FILE" ]; then
                if grep -q "\"$project\".*\"private\".*true" "$MEMORY_FILE"; then
                    is_private="true"
                fi
            fi
            
            # Check if project exists in pages
            in_pages="No"
            if [ -d "$SCRIPT_DIR/projects/$project" ]; then
                in_pages="Yes"
            fi
            
            # Display project info
            if [ "$is_private" = "true" ]; then
                echo "🔒 $project (Private, In Pages: $in_pages)"
            else
                echo "🌐 $project (Public, In Pages: $in_pages)"
            fi
        fi
    done
}

# Update gitignore and run sync after privacy changes
update_after_privacy_change() {
    # Update gitignore
    "$SCRIPT_DIR/update_gitignore.sh"
    
    # Run sync to update pages
    "$SCRIPT_DIR/sync_projects.sh"
}

# Main script logic
case "${1^^}" in
    "SYNC")
        echo "Synchronizing projects from docs to pages..."
        "$SCRIPT_DIR/sync_projects.sh"
        ;;
    "DELETE")
        if [ -z "$2" ]; then
            echo "Error: Project name is required for DELETE command."
            echo "Usage: ./paelladoc.sh DELETE <project>"
            exit 1
        fi
        echo "Deleting project: $2"
        "$SCRIPT_DIR/delete_project.sh" "$2"
        
        # Update gitignore after deletion
        "$SCRIPT_DIR/update_gitignore.sh"
        ;;
    "PRIVATE")
        if [ -z "$2" ]; then
            echo "Error: Project name is required for PRIVATE command."
            echo "Usage: ./paelladoc.sh PRIVATE <project>"
            exit 1
        fi
        echo "Marking project as private: $2"
        "$SCRIPT_DIR/set_private.sh" "$2" "true"
        
        # Update gitignore and sync
        update_after_privacy_change
        ;;
    "PUBLIC")
        if [ -z "$2" ]; then
            echo "Error: Project name is required for PUBLIC command."
            echo "Usage: ./paelladoc.sh PUBLIC <project>"
            exit 1
        fi
        echo "Marking project as public: $2"
        "$SCRIPT_DIR/set_private.sh" "$2" "false"
        
        # Update gitignore and sync
        update_after_privacy_change
        ;;
    "LIST")
        list_projects
        ;;
    "SERVE")
        echo "Starting Jekyll server..."
        cd "$SCRIPT_DIR" && bundle exec jekyll serve --livereload
        ;;
    "UPDATE-GITIGNORE")
        echo "Updating .gitignore with private projects..."
        "$SCRIPT_DIR/update_gitignore.sh"
        ;;
    "HELP"|"")
        show_help
        ;;
    *)
        echo "Error: Unknown command '$1'"
        show_help
        exit 1
        ;;
esac

exit 0 