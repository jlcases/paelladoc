# PAELLADOC Templates

This directory contains all templates used by the PAELLADOC system, organized following MECE principles (Mutually Exclusive, Collectively Exhaustive).

## Directory Structure

All templates follow a consistent organization pattern:

| Directory | Purpose | Types of Templates |
|-----------|---------|-------------------|
| `Product/` | Main product documentation templates | Project definition, market research, etc. |
| `simplified_templates/` | Simplified documentation | Quick tasks, bug reports, etc. |
| `conversation_flows/` | Conversation flow definitions | JSON files defining conversation structures |
| `coding_styles/` | Coding style guidelines | Frontend, backend, etc. |
| `github-workflows/` | Git workflow guidelines | GitHub Flow, GitFlow, etc. |
| `code_generation/` | Code generation templates | Component templates, etc. |
| `methodologies/` | Development methodologies | TDD, BDD, etc. |
| `product_management/` | Product management templates | User stories, etc. |
| `scripts/` | Template-related scripts | Utility scripts |

## Naming Conventions

1. Directory names: lowercase with hyphens for multi-word names
2. Template files: descriptive snake_case with appropriate extension
3. Supporting files: follow the convention of their respective type

## Usage Guidelines

1. **Template References**: When referencing templates in code or JSON files, use relative paths from the workspace root.
2. **Template Updates**: When updating templates, ensure that all dependent systems are also updated.
3. **New Templates**: New templates should be added to the appropriate directory, not at the root.
4. **Template Documentation**: Each template should have a header comment explaining its purpose and usage.

## Moving Templates

Templates that don't fit the current structure should be moved to the appropriate directory:

- `workflow_selector.md` and `programming_style_selector.md` should be moved to their respective directories
- Stand-alone documentation templates should be moved to `simplified_templates/`

## Integration with Features

Templates are integrated with PAELLADOC features as defined in the `.cursor/rules/feature_map.md` document. Each template should clearly relate to at least one feature definition.

## Maintenance

Regular template maintenance should include:

1. **Validation**: Ensuring templates are valid and up-to-date
2. **Consolidation**: Merging similar templates to reduce redundancy
3. **Documentation**: Keeping template headers and this README up-to-date
4. **Clean-up**: Removing obsolete templates

Always reference the feature map when making changes to ensure system-wide consistency. 