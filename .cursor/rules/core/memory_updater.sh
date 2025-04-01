#!/bin/bash

# memory_updater.sh - Automatic update of .memory.json files for any PAELLADOC project
# Installed as part of the Git hooks system
# Version 2.0 with AI integration to maintain context between sessions

# Determine the project root directory
PROJECT_ROOT=$(git rev-parse --show-toplevel)

# Find .memory.json files in the project
find_memory_files() {
    find "$PROJECT_ROOT" -name ".memory.json" -type f
}

# Function to get current date in ISO format
get_iso_date() {
    date -u '+%Y-%m-%dT%H:%M:%SZ'
}

# Get project name from directory
get_project_name() {
    basename "$PROJECT_ROOT"
}

# Save current conversation context
update_ai_context() {
    local memory_file="$1"
    local current_date=$(get_iso_date)
    local ymd_date=$(date '+%Y-%m-%d')
    
    # Check jq dependency
    if ! command -v jq &> /dev/null; then
        echo "WARNING: jq is not installed. Cannot update AI context."
        return 1
    fi
    
    # Read current memory file
    if [ ! -f "$memory_file" ]; then
        echo "ERROR: Memory file not found: $memory_file"
        return 1
    fi
    
    # Update last session date
    jq --arg date "$current_date" '
    # Create ai_context structure if it doesn't exist
    if .ai_context == null then 
        .ai_context = {
            "last_session": $date,
            "conversation_summaries": [],
            "current_focus": "",
            "coding_preferences": {},
            "next_tasks": []
        }
    else 
        .ai_context.last_session = $date
    end
    ' "$memory_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
    
    # Look for Cursor files to extract context if they exist
    cursor_context_file="$PROJECT_ROOT/.cursor/project_context.json"
    
    # Also look in the project documentation folder if it exists
    project_name=$(basename "$PROJECT_ROOT")
    docs_context_file="$PROJECT_ROOT/docs/$project_name/project_context.json"
    
    if [ -f "$cursor_context_file" ]; then
        echo "Found Cursor context file: $cursor_context_file"
        # Try to integrate Cursor context
        jq -s '.[0].ai_context.cursor_data = .[1] | .[0]' "$memory_file" "$cursor_context_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
    elif [ -f "$docs_context_file" ]; then
        echo "Found project context file: $docs_context_file"
        # Try to integrate project context
        jq -s '.[0].ai_context.cursor_data = .[1] | .[0]' "$memory_file" "$docs_context_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
    fi
    
    echo "AI context updated in $memory_file"
    return 0
}

# Extract relevant information from commit messages
extract_decisions_from_commits() {
    local memory_file="$1"
    local commit_msg="$2"
    local ymd_date=$(date '+%Y-%m-%d')
    
    # Check message format that might contain decisions
    if echo "$commit_msg" | grep -q -E '(decision|decidido|implemented|refactor|DECISION|REFACTOR)'; then
        # Create a decision entry based on commit message
        decision=$(echo "$commit_msg" | sed -E 's/^(feat|fix|docs|style|refactor|perf|test|chore)(\([^)]+\))?:\s*//i')
        
        # Extract rationale if present (after "because", "due to", etc.)
        rationale=""
        if echo "$commit_msg" | grep -q -E '(due to|since|as)'; then
            rationale=$(echo "$commit_msg" | sed -E 's/^.*?(due to|since|as)\s+//i')
        fi
        
        # Add decision to memory file
        if [ -n "$decision" ]; then
            jq --arg date "$ymd_date" \
               --arg decision "$decision" \
               --arg rationale "$rationale" \
            '
            # Ensure key_decisions exists
            if .key_decisions == null then .key_decisions = [] else . end |
            # Add decision
            .key_decisions += [{
                "date": $date,
                "decision": $decision,
                "rationale": $rationale,
                "ai_extracted": true,
                "source": "commit_message"
            }]
            ' "$memory_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
            
            echo "Decision extracted from commit message: $decision"
        fi
    fi
}

# Analyze modified files to detect technical debt patterns
analyze_files_for_tech_debt() {
    local memory_file="$1"
    local modified_files="$2"
    local current_date=$(get_iso_date)
    local ymd_date=$(date '+%Y-%m-%d')
    
    # Only proceed if we have jq
    if ! command -v jq &> /dev/null; then
        return 1
    fi
    
    # Patterns that might indicate technical debt
    # TODO, FIXME, HACK, WORKAROUND, XXX
    for file in $modified_files; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            # Analyze code files
            if [[ $file == *.js || $file == *.ts || $file == *.jsx || $file == *.tsx || $file == *.py || $file == *.rb || $file == *.java || $file == *.c || $file == *.cpp || $file == *.h || $file == *.hpp || $file == *.cs ]]; then
                # Look for technical debt comments
                tech_debt=$(grep -n -E '(TODO|FIXME|HACK|WORKAROUND|XXX|tech[- ]?debt):?' "$PROJECT_ROOT/$file" | head -5)
                
                if [ -n "$tech_debt" ]; then
                    while IFS=: read -r line_num comment; do
                        # Remove common comment prefixes
                        clean_comment=$(echo "$comment" | sed -E 's/^[[:space:]]*\/\/[[:space:]]*//;s/^[[:space:]]*#[[:space:]]*//;s/^[[:space:]]*\/\*[[:space:]]*//;s/^[[:space:]]*\*[[:space:]]*//')
                        
                        # Determine priority based on keywords
                        priority="medium"
                        if echo "$clean_comment" | grep -q -E '(urgent|critical|high|priority|blocker|ASAP)'; then
                            priority="high"
                        elif echo "$clean_comment" | grep -q -E '(eventually|someday|nice to have|low)'; then
                            priority="low"
                        fi
                        
                        # Add technical debt entry
                        jq --arg desc "[$file:$line_num] $clean_comment" \
                           --arg priority "$priority" \
                           --arg date "$current_date" \
                           --arg file "$file" \
                           --arg line "$line_num" \
                        '
                        # Ensure technical_debt exists
                        if .technical_debt == null then .technical_debt = [] else . end |
                        # Add technical debt
                        .technical_debt += [{
                            "description": $desc,
                            "priority": $priority,
                            "estimated_effort": "unknown",
                            "ai_identified": true,
                            "detected_at": $date,
                            "file": $file,
                            "line": $line
                        }]
                        ' "$memory_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
                        
                        echo "Technical debt detected in $file:$line_num"
                    done <<< "$tech_debt"
                fi
            fi
        fi
    done
}

# Update quality metrics from coverage files
update_quality_metrics() {
    local memory_file="$1"
    local modified_files="$2"
    
    # Check if there are changes in tests
    if echo "$modified_files" | grep -q "test\|spec"; then
        echo "Changes detected in tests, updating metrics..."
        
        # Look for coverage files in common locations
        coverage_files=(
            "$PROJECT_ROOT/coverage/coverage-summary.json"
            "$PROJECT_ROOT/coverage/lcov-report/coverage-summary.json"
            "$PROJECT_ROOT/jest-coverage/coverage-summary.json"
        )
        
        for cov_file in "${coverage_files[@]}"; do
            if [ -f "$cov_file" ]; then
                if command -v jq &> /dev/null; then
                    # Extract detailed coverage metrics
                    LINES_PCT=$(jq -r '.total.lines.pct' "$cov_file" 2>/dev/null || echo "")
                    STATEMENTS_PCT=$(jq -r '.total.statements.pct' "$cov_file" 2>/dev/null || echo "")
                    FUNCTIONS_PCT=$(jq -r '.total.functions.pct' "$cov_file" 2>/dev/null || echo "")
                    BRANCHES_PCT=$(jq -r '.total.branches.pct' "$cov_file" 2>/dev/null || echo "")
                    
                    if [ -n "$LINES_PCT" ]; then
                        # Update quality metrics
                        jq --argjson lines "$LINES_PCT" \
                           --argjson statements "$STATEMENTS_PCT" \
                           --argjson functions "$FUNCTIONS_PCT" \
                           --argjson branches "$BRANCHES_PCT" \
                        '
                        # Create quality_metrics structure if it doesn't exist
                        if .quality_metrics == null then 
                            .quality_metrics = {}
                        else . end |
                        # Update metrics
                        .quality_metrics.test_coverage = $lines |
                        .quality_metrics.coverage_details = {
                            "lines": $lines,
                            "statements": $statements,
                            "functions": $functions,
                            "branches": $branches,
                            "last_updated": "'$(get_iso_date)'"
                        }
                        ' "$memory_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
                        
                        echo "Coverage metrics updated from $cov_file"
                        break
                    fi
                else
                    echo "WARNING: jq is not installed. Cannot update detailed metrics."
                fi
            fi
        done
    fi
}

# Function to update a specific memory file
update_memory_file() {
    local memory_file="$1"
    local rel_path="${memory_file#$PROJECT_ROOT/}"
    
    echo "Updating memory file: $rel_path"
    
    # Get required data
    ISO_DATE=$(get_iso_date)
    YMD_DATE=$(date '+%Y-%m-%d')
    PROJECT_NAME=$(get_project_name)
    MODIFIED_FILES=$(git diff --name-only --staged)
    COMMIT_MSG=$(git log -1 --pretty=%B 2>/dev/null || echo "WIP")
    COMMIT_TYPE=$(echo "$COMMIT_MSG" | grep -oE '^(feat|fix|docs|style|refactor|perf|test|chore)' || echo "update")
    
    # Check jq dependency
    if command -v jq &> /dev/null; then
        # Create modifications structure
        local modules_json="[]"
        for file in $MODIFIED_FILES; do
            # Extract file type and module
            if [[ $file == *.ts || $file == *.js || $file == *.tsx || $file == *.jsx || $file == *.scss || $file == *.css || $file == *.html || $file == *.md ]]; then
                dir=$(dirname "$file")
                basename=$(basename "$file" .ts)
                basename=${basename%.js}
                basename=${basename%.tsx}
                basename=${basename%.jsx}
                basename=${basename%.scss}
                basename=${basename%.css}
                basename=${basename%.html}
                basename=${basename%.md}
                modules_json=$(echo "$modules_json" | jq --arg file "$file" --arg dir "$dir" --arg basename "$basename" '. += [{"file": $file, "dir": $dir, "module": $basename}]')
            fi
        done
        
        # Update .memory.json file
        jq --arg date "$ISO_DATE" \
           --arg ymd "$YMD_DATE" \
           --arg commit_type "$COMMIT_TYPE" \
           --arg commit_msg "$COMMIT_MSG" \
           --arg project "$PROJECT_NAME" \
           --argjson modules "$modules_json" \
           '
           # Ensure project_name exists
           if .project_name == null then .project_name = $project else . end |
           
           # Update date
           .last_updated = $date |
           
           # Create or update git activity
           if (.git_activity | not) then .git_activity = [] else . end |
           .git_activity += [{
               "date": $ymd,
               "type": $commit_type,
               "message": $commit_msg,
               "files_count": ($modules | length),
               "files": $modules
           }] |
           
           # Limit git history to last 20 entries
           .git_activity = (.git_activity | sort_by(.date) | reverse | .[0:20])
           ' \
           "$memory_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
        
        # Extract decisions from commit message
        extract_decisions_from_commits "$memory_file" "$COMMIT_MSG"
        
        # Analyze files for technical debt
        analyze_files_for_tech_debt "$memory_file" "$MODIFIED_FILES"
        
        # Update metrics
        update_quality_metrics "$memory_file" "$MODIFIED_FILES"
        
        # Update AI context
        update_ai_context "$memory_file"
        
        # Add updated file to commit
        git add "$memory_file"
        
    else
        # Basic fallback without jq
        echo "WARNING: jq is not installed. Updating only date in $rel_path"
        if [ -f "$memory_file" ]; then
            sed -i.bak "s/\"last_updated\":[[:space:]]*\"[^\"]*\"/\"last_updated\": \"$ISO_DATE\"/" "$memory_file" && rm -f "$memory_file.bak"
            git add "$memory_file"
        fi
    fi
}

# Main function
main() {
    # Find all memory files
    memory_files=$(find_memory_files)
    
    if [ -z "$memory_files" ]; then
        echo "No .memory.json files found in the project."
        return 0
    fi
    
    # Update each memory file
    for memory_file in $memory_files; do
        update_memory_file "$memory_file"
    done
    
    echo "Memory files update completed."
}

# Run the main function
main

exit 0 