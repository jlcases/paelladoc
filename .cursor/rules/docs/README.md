# PAELLADOC - MECE Documentation System

## Directory Structure

The PAELLADOC system follows a MECE (Mutually Exclusive, Collectively Exhaustive) architecture to ensure clear separation of concerns and complete coverage of functionality. This document serves as the primary guide to understanding the organization of the `.cursor/rules/` directory.

```
/Users/jlcases/codigo/paelladoc/.cursor/rules/
├── orchestrator/                # Central orchestrator definition
│   └── paelladoc.mdc            # Defines all commands, args, and delegates to modules
├── commands/                    # Command definitions & basic logic, categorized
│   ├── core/                    # -> Core system commands (help, verification)
│   ├── memory/                  # -> Project memory interaction commands
│   ├── code/                    # -> Code analysis, generation, and context commands
│   ├── styles/                  # -> Coding style and Git workflow commands
│   ├── product/                 # -> Product/Project management commands
│   └── templates/               # -> Documentation template management commands
├── modules/                     # Core functional implementations
│   ├── code_analysis/          # -> Logic for code analysis and doc generation
│   ├── memory_management/      # -> Logic for handling project memory
│   └── conversation/           # -> Logic for managing interactive conversation flows
├── scripts/                    # Utility and executable scripts
│   └── extract_repo_content.py  # -> Script to extract text from repositories
├── config/                     # System-wide configuration files
│   ├── imports.mdc             # -> Defines rule import relationships
│   └── ...                     # -> Other config files (e.g., conversation settings)
└── docs/                       # Documentation, guides, and historical references
    ├── README.md               # -> This file: System structure and principles
    └── ...                     # -> Other docs (e.g., old structures, command guides)
```

## Key Components and Their Roles

### Orchestrator (`orchestrator/`)
- **Purpose**: The single entry point and central coordinator of the system.
- **Key File**: `paelladoc.mdc`
  - Defines *all* user-facing commands (like `PAELLA`, `GENERATE_DOC`, `MEMORY`, etc.).
  - Specifies arguments, validation rules, and expected behavior for each command.
  - Delegates the actual execution logic to the appropriate `.mdc` files within the `commands/` or `modules/` directories via the `module:` directive.
  - Imports necessary configurations and rules using the `imports:` section.

### Commands (`commands/`)
- **Purpose**: Defines the interface and primary handling logic for specific commands or groups of related commands, categorized by function. These rules often contain the `description` used by the AI agent to find the right command based on user intent.
- **Subdirectories**:
  - `core/`: Fundamental system commands (e.g., `help.mdc`, `verification.mdc`).
  - `memory/`: Commands for interacting with project memory (e.g., `project_memory.mdc` handling `ACHIEVEMENT`, `ISSUE`, `DECISION`).
  - `code/`: Commands related to code processing (e.g., `generate_context.mdc`, `generate_doc.mdc`, `code_generation.mdc`).
  - `styles/`: Commands for managing coding standards and workflows (e.g., `coding_styles.mdc`, `git_workflows.mdc`).
  - `product/`: Commands related to project/product management tasks (e.g., `product_management.mdc` handling `STORY`, `SPRINT`).
  - `templates/`: Commands for managing documentation templates (e.g., `template.mdc` handling `TEMPLATE`).

### Modules (`modules/`)
- **Purpose**: Contains the core implementation logic for complex functionalities that might be used by one or more commands. Separating logic into modules promotes reusability and keeps command definitions cleaner.
- **Subdirectories**:
  - `code_analysis/`: Implements the detailed logic for analyzing code and generating documentation content (used by `GENERATE_DOC`).
  - `memory_management/`: Handles the storage, retrieval, and updating of project memory (used by `MEMORY`, `ACHIEVEMENT`, etc., and potentially `CONTINUE`).
  - `conversation/`: Defines specific interactive conversation flows used by commands that require user input gathering (e.g., `documentation_generation` flow).

### Scripts (`scripts/`)
- **Purpose**: Holds standalone executable scripts used by the system, often invoked by a command's behavior definition (e.g., `run_script: true`).
- **Key File Example**: `extract_repo_content.py` is called by the `GENERATE_CONTEXT` command to process a repository.

### Config (`config/`)
- **Purpose**: Stores configuration files that define system-wide settings or relationships.
- **Key Files**:
  - `imports.mdc`: Specifies which `.mdc` rules should be imported and considered by the orchestrator.
  - `paelladoc_conversation_config.json` (Example): Could define parameters or prompts for conversation flows.

### Docs (`docs/`)
- **Purpose**: Contains all documentation related to the PAELLADOC system itself, including architectural guides, command references, and potentially archived or historical information.
- **Key File**: `README.md` (this file) provides the primary overview of the `.cursor/rules` structure.

## Architecture Principles

The PAELLADOC system adheres to these principles:

1.  **MECE Organization**: Ensures clear responsibilities and full functional coverage.
2.  **Command-Module Separation**: Command files define *what* a command does (interface, intent), while module files define *how* complex operations are performed.
3.  **Central Orchestration**: `orchestrator/paelladoc.mdc` is the definitive source for all available commands, ensuring consistency.
4.  **Intent-Based Discovery**: Rule `description` fields are written to reflect user goals, aiding AI agent in selecting the correct rule.

This structure aims for clarity, maintainability, and scalability as the PAELLADOC system evolves.

## MECE Command Organization

The commands are organized into categories that are:
1. Mutually exclusive (no overlap in purpose)
2. Collectively exhaustive (covering all required functionality)

- **Core Commands**: Basic system operations (HELP, VERIFY)
- **Memory Commands**: Project memory management (ACHIEVEMENT, ISSUE, DECISION, MEMORY)
- **Code Commands**: Code analysis and generation (GENERATE_CONTEXT, GENERATE-DOC, GENERATE_CODE)
- **Style Commands**: Programming style and workflows (CODING_STYLE, WORKFLOW)
- **Product Commands**: Product management (STORY, SPRINT, MEETING, RESEARCH)
- **Template Commands**: Template management (TEMPLATE, GENERATE_RULES) 