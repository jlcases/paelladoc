#!/bin/bash

# init_memory.sh - Memory initializer for external projects
# This script creates memory and context files without installing Git hooks
# Useful for projects in directories external to PAELLADOC

# Colors for messages
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# Function for messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get the path to the PAELLADOC directory
PAELLADOC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../../.." && pwd )"
log_info "PAELLADOC directory: $PAELLADOC_DIR"

# Get the path to the target directory (code project)
if [ -z "$1" ]; then
    # If no argument is provided, use the current directory
    PROJECT_PATH="$(pwd)"
else
    # Use the provided directory, converting to absolute path
    PROJECT_PATH="$(cd "$1" 2>/dev/null && pwd || echo "$1")"
    if [ ! -d "$PROJECT_PATH" ]; then
        log_error "The project directory '$1' does not exist or is not accessible."
        exit 1
    fi
fi

log_info "Code project at: $PROJECT_PATH"

# Get project name from directory
project_name=$(basename "$PROJECT_PATH")
log_info "Project name: $project_name"

# Documentation directory in PAELLADOC (not in the code repository)
DOCS_DIR="$PAELLADOC_DIR/docs/$project_name"
if [ ! -d "$DOCS_DIR" ]; then
    mkdir -p "$DOCS_DIR"
    log_info "Created documentation directory at $DOCS_DIR"
else
    log_info "Documentation directory already exists at $DOCS_DIR"
fi

# Get current date in ISO 8601 format
CURRENT_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TODAY=$(date +"%Y-%m-%d")

# Create memory file
MEMORY_FILE="$DOCS_DIR/.memory.json"
if [ ! -f "$MEMORY_FILE" ]; then
    # Use the memory template and replace variables
    TEMPLATE_FILE="$(dirname "$0")/memory_template.json"
    if [ ! -f "$TEMPLATE_FILE" ]; then
        log_error "Memory template file not found at $TEMPLATE_FILE"
        exit 1
    fi
    
    # Replace variables in template
    sed -e "s/PROJECT_NAME/$project_name/g" \
        -e "s|PROJECT_PATH|$PROJECT_PATH|g" \
        -e "s/CURRENT_DATE/$CURRENT_DATE/g" \
        -e "s/TODAY_DATE/$TODAY/g" \
        "$TEMPLATE_FILE" > "$MEMORY_FILE"
        
    log_info ".memory.json file created at $MEMORY_FILE using template"
else
    log_info ".memory.json file already exists at $MEMORY_FILE"
    
    # Check if it has AI support and project path
    if command -v jq &> /dev/null; then
        if ! jq -e '.ai_context' "$MEMORY_FILE" > /dev/null 2>&1; then
            log_warn "Memory file does not have AI support. It will be updated automatically."
            jq '. + {"ai_context": {"last_session": "'$CURRENT_DATE'", "conversation_summaries": [], "current_focus": "", "coding_preferences": {}, "next_tasks": []}}' "$MEMORY_FILE" > "$MEMORY_FILE.tmp" && mv "$MEMORY_FILE.tmp" "$MEMORY_FILE"
            log_info "Updated $MEMORY_FILE with AI support"
        fi
        
        # Update project path if it has changed
        current_path=$(jq -r '.project_path // ""' "$MEMORY_FILE")
        if [ "$current_path" != "$PROJECT_PATH" ]; then
            log_info "Updating project path in memory file"
            jq --arg path "$PROJECT_PATH" '.project_path = $path' "$MEMORY_FILE" > "$MEMORY_FILE.tmp" && mv "$MEMORY_FILE.tmp" "$MEMORY_FILE"
        fi
    else
        log_warn "jq is not installed. Cannot verify AI support."
    fi
fi

# Create context file
CONTEXT_FILE="$DOCS_DIR/project_context.json"
if [ ! -f "$CONTEXT_FILE" ]; then
    # Use the context template and replace variables
    TEMPLATE_FILE="$(dirname "$0")/context_template.json"
    if [ ! -f "$TEMPLATE_FILE" ]; then
        log_error "Context template file not found at $TEMPLATE_FILE"
        exit 1
    fi
    
    # Replace variables in template
    sed -e "s/PROJECT_NAME/$project_name/g" \
        -e "s|PROJECT_PATH|$PROJECT_PATH|g" \
        -e "s/CURRENT_DATE/$CURRENT_DATE/g" \
        -e "s/TODAY_DATE/$TODAY/g" \
        "$TEMPLATE_FILE" > "$CONTEXT_FILE"
        
    log_info "AI context file created at $CONTEXT_FILE using template"
else
    log_info "AI context file already exists at $CONTEXT_FILE"
    
    # Update project path if it has changed
    if command -v jq &> /dev/null; then
        current_path=$(jq -r '.project_path // ""' "$CONTEXT_FILE")
        if [ "$current_path" != "$PROJECT_PATH" ]; then
            log_info "Updating project path in context file"
            jq --arg path "$PROJECT_PATH" '.project_path = $path' "$CONTEXT_FILE" > "$CONTEXT_FILE.tmp" && mv "$CONTEXT_FILE.tmp" "$CONTEXT_FILE"
        fi
    fi
fi

# Clean up old files in the code project if they exist
PROJECT_DOCS_DIR="$PROJECT_PATH/docs/$project_name"
if [ -d "$PROJECT_DOCS_DIR" ]; then
    log_warn "Memory files found in the code repository."
    read -p "Do you want to remove them? (y/n): " clean_old_files
    if [[ "$clean_old_files" =~ ^[Yy]$ ]]; then
        if [ -f "$PROJECT_DOCS_DIR/.memory.json" ]; then
            rm "$PROJECT_DOCS_DIR/.memory.json"
            log_info "Removed .memory.json file from code repository"
        fi
        if [ -f "$PROJECT_DOCS_DIR/project_context.json" ]; then
            rm "$PROJECT_DOCS_DIR/project_context.json"
            log_info "Removed project_context.json file from code repository"
        fi
        # If the directory is empty, remove it too
        if [ -z "$(ls -A "$PROJECT_DOCS_DIR")" ]; then
            rmdir "$PROJECT_DOCS_DIR"
            log_info "Removed empty directory from code repository"
        fi
    fi
fi

# Suggest next step for hook installation
log_info "Memory successfully initialized at $DOCS_DIR"
log_info ""
log_info "To enable automatic memory updates with each commit, run:"
log_info "bash $(dirname "$0")/git_hook_installer.sh $PROJECT_PATH"
log_info ""
log_info "Or manually use PAELLADOC's CONTEXT, ACHIEVEMENT, ISSUE, and DECISION commands"

exit 0 