# PAELLADOC Feature Map

This document provides a comprehensive mapping between feature definitions (MDC files) and their implementations across the PAELLADOC system, following MECE principles (Mutually Exclusive, Collectively Exhaustive).

## Core Features

| Feature | Definition (MDC) | Implementation | Description |
|---------|------------------|----------------|-------------|
| Commands | `.cursor/rules/core/commands.mdc` | `paelladoc.mdc` command definitions | Defines the main PAELLADOC commands |
| Help System | `.cursor/rules/core/help.mdc` | HELP command in `paelladoc.mdc` | Implements the help system for commands |
| Verification | `.cursor/rules/core/verification.mdc` | VERIFY command in `paelladoc.mdc` | Implements verification processes |

## Project Features

| Feature | Definition (MDC) | Implementation | Description |
|---------|------------------|----------------|-------------|
| Coding Styles | `.cursor/rules/features/coding_styles.mdc` | `.cursor/rules/templates/coding_styles/` | Manages programming styles |
| Conversation Workflow | `.cursor/rules/features/conversation_workflow.mdc` | `.cursor/rules/templates/conversation_flows/*.json` and `paelladoc_conversation_config.json` | Manages conversation flows |
| Git Workflows | `.cursor/rules/features/git_workflows.mdc` | `.cursor/rules/templates/github-workflows/` | Manages Git workflows |
| Product Management | `.cursor/rules/features/product_management.mdc` | `.cursor/rules/templates/product_management/` | Manages product features |
| Project Memory | `.cursor/rules/features/project_memory.mdc` | `.cursor/rules/templates/Product/memory_template.json` | Manages project memory system |
| Templates | `.cursor/rules/features/templates.mdc` | `.cursor/rules/templates/` | Manages documentation templates |
| Code Generation | `.cursor/rules/features/code_generation.mdc` | `.cursor/rules/templates/code_generation/` | Manages code generation |
| Interfaces | `.cursor/rules/features/interfaces.mdc` | Various UI-related templates | Manages user interfaces |

## Documentation and Templates

| Template Category | Directory | Purpose | Related Feature |
|------------------|-----------|---------|----------------|
| Product | `.cursor/rules/templates/Product/` | Main product documentation templates | Templates, Product Management |
| Simplified | `.cursor/rules/templates/simplified_templates/` | Simplified documentation templates | Templates |
| Conversation Flows | `.cursor/rules/templates/conversation_flows/` | JSON-based conversation flow definitions | Conversation Workflow |
| Coding Styles | `.cursor/rules/templates/coding_styles/` | Coding style guidelines | Coding Styles |
| GitHub Workflows | `.cursor/rules/templates/github-workflows/` | Git workflow guidelines | Git Workflows |
| Code Generation | `.cursor/rules/templates/code_generation/` | Code generation templates | Code Generation |
| Methodologies | `.cursor/rules/templates/methodologies/` | Development methodology guidelines | Multiple |

## Scripts and Automation

| Script | Location | Purpose | Related Feature |
|--------|----------|---------|----------------|
| generate_mdc.js | `.cursor/rules/scripts/` | Generates MDC files | Multiple |
| mdc_cleanup.js | `.cursor/rules/scripts/` | Cleans MDC files | Multiple |
| mdc_generation.js | `.cursor/rules/scripts/` | Core MDC generation logic | Multiple |

## Configuration Files

| File | Location | Purpose | Related Feature |
|------|----------|---------|----------------|
| paelladoc_conversation_config.json | `.cursor/rules/` | Configures conversation flows | Conversation Workflow |
| paelladoc.mdc | `.cursor/rules/` | Main PAELLADOC rule definitions | Multiple |
| imports.mdc | `.cursor/rules/` | Manages imports | Multiple |

## Maintenance Guidelines

1. **Adding New Features**: 
   - Create an MDC file in `.cursor/rules/features/`
   - Implement the feature in appropriate template directories
   - Update this feature map
   - Reference the feature in `paelladoc.mdc` imports

2. **Modifying Existing Features**:
   - Update both the MDC file and the implementation
   - Update this feature map if implementation locations change
   - Test for consistency between definition and implementation

3. **Removing Features**:
   - Remove references in `paelladoc.mdc` imports
   - Remove the MDC file
   - Remove implementation files
   - Update this feature map 