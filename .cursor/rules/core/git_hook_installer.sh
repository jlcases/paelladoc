#!/bin/bash

# git_hook_installer.sh - Git hooks installer for PAELLADOC projects
# This script installs the necessary hooks for the memory system to work
# Version 2.0 with support for AI integration

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

# Determine project root directory
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$PROJECT_ROOT" ]; then
    log_error "Git repository not found. Run this script from a Git repository."
    exit 1
fi

# Path to Git hooks directory
GIT_HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
if [ ! -d "$GIT_HOOKS_DIR" ]; then
    log_error "Git hooks directory not found at $GIT_HOOKS_DIR"
    exit 1
fi

# Path to scripts directory in PAELLADOC
PAELLADOC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
MEMORY_UPDATER="$PAELLADOC_DIR/core/memory_updater.sh"

if [ ! -f "$MEMORY_UPDATER" ]; then
    log_error "memory_updater.sh script not found at $MEMORY_UPDATER"
    exit 1
fi

# Path for Cursor directory
CURSOR_DIR="$PROJECT_ROOT/.cursor"

# Install or update pre-commit hook
install_pre_commit_hook() {
    local pre_commit_hook="$GIT_HOOKS_DIR/pre-commit"
    local temp_hook="$pre_commit_hook.temp"
    
    # Create hook calling the memory_updater.sh script
    cat > "$temp_hook" << EOF
#!/bin/bash

# Pre-commit hook for PAELLADOC projects
# Automatically installed by git_hook_installer.sh

# Execute memory updater
MEMORY_UPDATER="$MEMORY_UPDATER"
if [ -f "\$MEMORY_UPDATER" ]; then
    bash "\$MEMORY_UPDATER"
else
    echo "ERROR: memory_updater.sh script not found at \$MEMORY_UPDATER"
    exit 1
fi

# Continue with normal pre-commit hook flow
EOF

    # If a pre-commit hook already exists, add its content to the new one
    if [ -f "$pre_commit_hook" ]; then
        log_info "Updating existing pre-commit hook..."
        echo -e "\n# Original pre-commit hook\n" >> "$temp_hook"
        cat "$pre_commit_hook" | grep -v "memory_updater.sh" >> "$temp_hook"
    else
        log_info "Creating new pre-commit hook..."
    fi
    
    # Make executable and install
    chmod +x "$temp_hook"
    mv "$temp_hook" "$pre_commit_hook"
    
    log_info "Pre-commit hook successfully installed at $pre_commit_hook"
}

# Set up structure for AI context
setup_cursor_ai_context() {
    # Get project name
    project_name=$(basename "$PROJECT_ROOT")
    
    # Create project documentation directory if it doesn't exist
    PROJECT_DOCS_DIR="$PROJECT_ROOT/docs/$project_name"
    if [ ! -d "$PROJECT_DOCS_DIR" ]; then
        mkdir -p "$PROJECT_DOCS_DIR"
        log_info "Created documentation directory at $PROJECT_DOCS_DIR"
    fi
    
    # Create Cursor directory if it doesn't exist
    if [ ! -d "$CURSOR_DIR" ]; then
        mkdir -p "$CURSOR_DIR"
        log_info "Created Cursor directory at $CURSOR_DIR"
    fi
    
    # Define locations for context file
    local cursor_context_file="$CURSOR_DIR/project_context.json"
    local project_context_file="$PROJECT_DOCS_DIR/project_context.json"
    
    # Decide which location to use for context
    # Prioritize the specific project directory
    local context_file="$project_context_file"
    local context_path_for_gitignore=".cursor/project_context.json docs/$project_name/project_context.json"
    
    # Create initial context file if it doesn't exist
    if [ ! -f "$context_file" ]; then
        cat > "$context_file" << EOF
{
  "project_name": "$project_name",
  "initialized_at": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "last_updated": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "conversation_summaries": [],
  "key_insights": [],
  "current_focus": "",
  "development_context": {
    "methodology": "",
    "current_phase": "",
    "active_tasks": []
  }
}
EOF
        log_info "Created AI context file at $context_file"
        
        # If it exists in another location, migrate the data
        if [ -f "$cursor_context_file" ] && [ "$context_file" != "$cursor_context_file" ]; then
            log_info "Found existing context at $cursor_context_file, migrating data..."
            if command -v jq &> /dev/null; then
                # Combine data from both contexts
                jq -s '.[0] * .[1]' "$context_file" "$cursor_context_file" > "$context_file.tmp" && mv "$context_file.tmp" "$context_file"
                log_info "Context data successfully migrated"
            else
                log_warn "Could not migrate context data (jq not installed)"
                cp "$cursor_context_file" "$context_file"
            fi
        fi
        
        # Add context files to .gitignore if not already there
        if [ -f "$PROJECT_ROOT/.gitignore" ]; then
            context_files_ignored=true
            for path in $context_path_for_gitignore; do
                if ! grep -q "^$path" "$PROJECT_ROOT/.gitignore"; then
                    context_files_ignored=false
                    break
                fi
            done
            
            if [ "$context_files_ignored" = false ]; then
                echo -e "\n# AI context files\n$context_path_for_gitignore" >> "$PROJECT_ROOT/.gitignore"
                log_info "Added context files to .gitignore"
            fi
        else
            echo -e "# AI context files\n$context_path_for_gitignore" > "$PROJECT_ROOT/.gitignore"
            log_info "Created .gitignore with context files exclusion"
        fi
    else
        log_info "AI context file already exists at $context_file"
    fi
}

# Check requirements
check_requirements() {
    # Check for jq (recommended but not mandatory)
    if ! command -v jq &> /dev/null; then
        log_warn "jq is not installed. Recommended for full functionality."
        log_warn "Install jq with: brew install jq (macOS) or apt-get install jq (Linux)"
    else
        log_info "jq is correctly installed."
    fi
    
    # Check for memory files
    memory_files=$(find "$PROJECT_ROOT" -name ".memory.json" -type f)
    if [ -z "$memory_files" ]; then
        log_warn "No .memory.json files found in the project."
        
        # Ask if a memory file should be created
        read -p "Do you want to create a .memory.json file in docs/PROJECT/.memory.json? (y/n): " create_memory
        if [[ "$create_memory" =~ ^[Yy]$ ]]; then
            # Get project name
            project_name=$(basename "$PROJECT_ROOT")
            
            # Create directory if it doesn't exist
            mkdir -p "$PROJECT_ROOT/docs/$project_name"
            
            # Create initial memory with AI integration support
            cat > "$PROJECT_ROOT/docs/$project_name/.memory.json" << EOF
{
  "project_name": "$project_name",
  "project_type": "",
  "language": "",
  "created_at": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "last_updated": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "methodology": "",
  "git_workflow": "",
  "progress": {
    "current_phase": "initialization",
    "completed_percentage": 0,
    "completed_stories": [],
    "in_progress_stories": [],
    "pending_stories": []
  },
  "code_structure": {
    "source_directory": "",
    "test_directory": "",
    "main_modules": []
  },
  "git_activity": [],
  "key_decisions": [],
  "technical_debt": [],
  "quality_metrics": {
    "test_coverage": 0,
    "code_duplication": 0
  },
  "ai_context": {
    "last_session": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
    "conversation_summaries": [],
    "current_focus": "",
    "coding_preferences": {},
    "next_tasks": []
  },
  "dependencies": {
    "production": [],
    "development": []
  },
  "next_steps": []
}
EOF
            log_info ".memory.json file created at docs/$project_name/.memory.json"
        fi
    else
        log_info "Found $(echo "$memory_files" | wc -l | tr -d ' ') .memory.json files:"
        echo "$memory_files" | sed 's|'"$PROJECT_ROOT"'/||g' | sed 's|^|  - |g'
        
        # Check if they have AI support
        for memory_file in $memory_files; do
            if command -v jq &> /dev/null; then
                if ! jq -e '.ai_context' "$memory_file" > /dev/null 2>&1; then
                    log_warn "File $memory_file does not have AI support. It will be automatically updated."
                    jq '. + {"ai_context": {"last_session": "'$(date -u '+%Y-%m-%dT%H:%M:%SZ')'", "conversation_summaries": [], "current_focus": "", "coding_preferences": {}, "next_tasks": []}}' "$memory_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
                    log_info "Updated $memory_file with AI support"
                fi
            fi
        done
    fi
}

# Main function
main() {
    log_info "Installing Git hooks and AI system for PAELLADOC project..."
    
    # Check requirements
    check_requirements
    
    # Install pre-commit hook
    install_pre_commit_hook
    
    # Set up structure for AI
    setup_cursor_ai_context
    
    log_info "Installation completed. The AI and memory system will update automatically with each commit."
    log_info "To activate full AI integration in Cursor, use the CONTEXT command in your chats."
}

# Run the main function
main

exit 0 