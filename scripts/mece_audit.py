import os
import json
from pathlib import Path
from datetime import datetime, timezone
import fnmatch # For wildcard matching

# --- Configuration ---
# Assuming the script is run from the project root
PROJECT_ROOT = Path(".")
TAXONOMY_FILE = PROJECT_ROOT / "taxonomy.json"
AUDIT_REPORT_FILE = PROJECT_ROOT / "mece_audit_report.json"

# Base directory for the original rules and templates
RULES_BASE_DIR = PROJECT_ROOT / ".cursor/rules"

# File extensions/patterns to consider within the rules directory
# We include .py in case there were scripts inside .cursor/rules/scripts
RELEVANT_FILE_PATTERNS = ["*.mdc", "*.md", "*.json", "*.sh", "*.js", "*.py"]

# Exclude specific files or patterns within .cursor/rules if necessary
EXCLUDE_FILES = ["__init__.py", "README.md"] # Keep this general, add more if needed
EXCLUDE_DIRS = [".venv", ".git", "__pycache__", ".pytest_cache", "node_modules"] # General excludes

# --- Helper Functions ---

def load_taxonomy(file_path: Path) -> dict:
    """Loads the taxonomy data from the JSON file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Taxonomy file not found at: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_taxonomy(file_path: Path, data: dict):
    """Saves the updated taxonomy data back to the JSON file."""
    data["audit_timestamp"] = datetime.now(timezone.utc).isoformat()
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def find_relevant_files(base_dir: Path, file_patterns: list[str], exclude_files: list[str], exclude_dirs: list[str]) -> set[Path]:
    """Finds all relevant files within the specified base directory, respecting excludes."""
    relevant_files = set()
    absolute_exclude_dirs = { (base_dir.parent / d).resolve() for d in exclude_dirs } # Excludes relative to project root
    
    print(f"Scanning directory tree starting from: {base_dir.resolve()}")
    if not base_dir.is_dir():
        print(f"Error: Rules base directory not found: {base_dir}")
        return set()

    for root, dirs, files in os.walk(base_dir, topdown=True):
        current_root_path = Path(root).resolve()
        
        # Filter excluded directories (check against resolved paths)
        dirs[:] = [d for d in dirs 
                   if (current_root_path / d).resolve() not in absolute_exclude_dirs and 
                      d not in exclude_dirs] # Also check by name just in case

        for file in files:
            if file in exclude_files:
                continue
                
            file_path = Path(root) / file
            # Check if the file matches any of the relevant patterns
            if any(fnmatch.fnmatch(file, pattern) for pattern in file_patterns):
                 # Store path relative to the RULES_BASE_DIR for matching taxonomy patterns
                try:
                    relative_path = file_path.relative_to(base_dir)
                    relevant_files.add(relative_path)
                except ValueError:
                    print(f"Warning: Could not make path relative: {file_path} to {base_dir}")
                    # Decide how to handle - skip or store absolute?
                    # Storing relative to project root might be useful fallback
                    try:
                         relevant_files.add(file_path.relative_to(PROJECT_ROOT))
                    except ValueError:
                         relevant_files.add(file_path) # Keep absolute if all else fails

    print(f"Found {len(relevant_files)} relevant files for audit within {base_dir}.")
    return relevant_files

def audit_files(taxonomy_data: dict, files_in_repo: set[Path]) -> tuple[list[Path], dict[Path, list[str]]]:
    """Audits files against the taxonomy patterns."""
    patterns_to_category = {}
    all_patterns = set()

    # Use the 'patterns' key which now covers rules and templates
    pattern_key = "patterns"
    if pattern_key not in taxonomy_data:
         print(f"Error: Key '{pattern_key}' not found in taxonomy data.")
         # Attempt to fallback to legacy keys if needed, though 'patterns' should exist now
         # ... (fallback logic could be added here if necessary) ...
         return list(files_in_repo), {}

    # Build map of pattern -> category
    for category, patterns in taxonomy_data.get(pattern_key, {}).items():
        if not isinstance(patterns, list):
            print(f"Warning: Patterns for category '{category}' are not a list, skipping.")
            continue
        for pattern in patterns:
            patterns_to_category[pattern] = category
            all_patterns.add(pattern)

    uncategorized = []
    duplicates = {} # file -> list of categories
    categorized_count = 0

    print(f"Auditing {len(files_in_repo)} files against {len(all_patterns)} patterns...")
    for file_path in files_in_repo:
        matched_categories = set()
        # Match against the string representation of the path relative to RULES_BASE_DIR
        file_path_str = str(file_path) 

        for pattern in all_patterns:
            if fnmatch.fnmatch(file_path_str, pattern):
                matched_categories.add(patterns_to_category[pattern])
        
        if matched_categories:
             categorized_count += 1
        if not matched_categories:
            uncategorized.append(file_path)
        elif len(matched_categories) > 1:
            duplicates[file_path] = sorted(list(matched_categories))

    print(f"Audit complete. Categorized: {categorized_count}, Uncategorized: {len(uncategorized)}, Duplicates: {len(duplicates)}")
    return sorted(uncategorized), duplicates

# --- Main Execution ---

def main():
    """Main function to run the MECE audit.""" 
    print("Starting MECE Audit...")
    try:
        taxonomy = load_taxonomy(TAXONOMY_FILE)
        print(f"Loaded taxonomy from: {TAXONOMY_FILE}")

        actual_files = find_relevant_files(
            RULES_BASE_DIR, # Scan inside .cursor/rules/
            RELEVANT_FILE_PATTERNS,
            EXCLUDE_FILES,
            EXCLUDE_DIRS
        )

        uncategorized_files, duplicate_files = audit_files(taxonomy, actual_files)

        print("\n--- MECE Audit Results ---")

        if uncategorized_files:
            print(f"\n[!] {len(uncategorized_files)} Uncategorized Files Found (relative to {RULES_BASE_DIR}):")
            # Sort for readability
            uncategorized_files.sort(key=lambda p: str(p))
            for f in uncategorized_files:
                print(f"  - {f}")
        else:
            print(f"\n[✓] No uncategorized files found within {RULES_BASE_DIR}.")

        if duplicate_files:
            print(f"\n[!] {len(duplicate_files)} Files in Multiple Categories Found:")
            # Sort for readability
            sorted_duplicates = sorted(duplicate_files.items(), key=lambda item: str(item[0]))
            for f, cats in sorted_duplicates:
                print(f"  - {f} -> {cats}")
        else:
            print(f"\n[✓] No files found in multiple categories.")

        # Save updated taxonomy with timestamp
        save_taxonomy(TAXONOMY_FILE, taxonomy)
        print(f"\nUpdated taxonomy saved to: {TAXONOMY_FILE}")

        # Save audit report 
        report_data = {
            "audit_timestamp": taxonomy["audit_timestamp"],
            "scan_base_directory": str(RULES_BASE_DIR),
            "uncategorized_files": [str(f) for f in uncategorized_files],
            "duplicate_files": {str(f): cats for f, cats in duplicate_files.items()}
        }
        with open(AUDIT_REPORT_FILE, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
        print(f"Audit summary saved to: {AUDIT_REPORT_FILE}")

        print("\nMECE Audit Finished.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 