# PAELLADOC Directory Structure

This document defines the standardized directory structure for the PAELLADOC system, following MECE principles (Mutually Exclusive, Collectively Exhaustive).

## Overview

The PAELLADOC system is organized into these main sections:

```
.cursor/rules/
├── core/                  # Core functionality definitions
├── features/              # Feature-specific definitions
├── scripts/               # Utility scripts
├── templates/             # Documentation and code templates
│   ├── coding_styles/     # Coding style guidelines
│   ├── code_generation/   # Code generation templates
│   ├── conversation_flows/ # Conversation flow configurations
│   ├── github-workflows/  # Git workflow guidelines
│   ├── methodologies/     # Development methodology guidelines
│   ├── Product/           # Main product documentation templates
│   ├── product_management/ # Product management templates
│   ├── scripts/           # Template-specific scripts
│   ├── selectors/         # Selection guide templates
│   └── simplified_templates/ # Simple documentation templates
├── DIRECTORY_STRUCTURE.md # This document
├── feature_map.md         # Mapping between features and implementations
├── imports.mdc            # Import definitions
├── paelladoc_conversation_config.json # Conversation configuration
└── paelladoc.mdc          # Main PAELLADOC definition
```

## Directory Purposes

### Core Directory (`core/`)

Contains core functionality definitions in MDC format:
- `commands.mdc`: Command definitions
- `help.mdc`: Help system implementation
- `verification.mdc`: Verification process implementation

### Features Directory (`features/`)

Contains feature-specific definitions in MDC format:
- `coding_styles.mdc`: Programming style guides
- `code_generation.mdc`: Code generation system
- `conversation_workflow.mdc`: Conversation workflow system
- `git_workflows.mdc`: Git workflow methodologies
- `interfaces.mdc`: User interface definitions
- `product_management.mdc`: Product management features
- `project_memory.mdc`: Project memory system
- `templates.mdc`: Template management system

### Scripts Directory (`scripts/`)

Contains utility scripts for the PAELLADOC system:
- `generate_mdc.js`: MDC generation script
- `mdc_cleanup.js`: MDC cleanup script
- `mdc_generation.js`: Core MDC generation logic
- `README.md`: Script documentation

### Templates Directory (`templates/`)

Contains all templates used by PAELLADOC, organized by purpose.
See the `.cursor/rules/templates/README.md` file for detailed information about template organization.

## Root Directory Files

- `DIRECTORY_STRUCTURE.md`: This document, explaining the directory structure
- `feature_map.md`: Maps feature definitions to their implementations
- `imports.mdc`: Defines imports for the PAELLADOC system
- `paelladoc_conversation_config.json`: Configuration for conversation flows
- `paelladoc.mdc`: Main PAELLADOC rule definitions

## Naming Conventions

1. **Directories**: lowercase with hyphens for multi-word names
2. **MDC Files**: descriptive names with `.mdc` extension
3. **JSON Files**: descriptive names with `.json` extension
4. **Documentation**: uppercase with underscores for multi-word names
5. **Scripts**: descriptive names with `.js` extension

## Organizational Principles

1. **Separation of Concerns**: Each file has a single, well-defined purpose
2. **MECE Structure**: Directories are organized to be mutually exclusive and collectively exhaustive
3. **Consistent Naming**: Files follow consistent naming conventions
4. **Clear Hierarchies**: Directory structure clearly represents functional hierarchies
5. **Documentation**: Each directory includes appropriate documentation

## Maintenance Guidelines

When maintaining the PAELLADOC system:

1. **Adding Components**: Place in the appropriate directory based on function
2. **Removing Components**: Update references in `paelladoc.mdc` and `feature_map.md`
3. **Directory Structure Changes**: Update this document and any affected references
4. **New Directories**: Include a README.md explaining the directory's purpose 