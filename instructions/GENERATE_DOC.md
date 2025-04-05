# GENERATE_DOC Command Reference

## Overview

`GENERATE_DOC` is a powerful command in PAELLADOC that generates comprehensive documentation from code repositories. The command can analyze both local repositories and remote GitHub URLs, extracting key information to create structured documentation based on available templates.

## New in v0.2.0

- **Dynamic Template Menu**: Now displays all available templates organized by category
- **Complete Multilingual Support**: Full support for both English and Spanish
- **Direct GitHub URL Support**: Ability to analyze repositories directly from GitHub URLs
- **Enhanced Output Control**: Better file organization in the output directory

## Syntax

```
GENERATE_DOC repo_path=<path_or_url> language=<en|es> [options]
```

## Required Parameters

| Parameter | Description |
|-----------|-------------|
| `repo_path` | Path to local repository or GitHub URL to analyze |
| `language` | Language for documentation output ("en" for English, "es" for Spanish) |

## Optional Parameters

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `output` | Output directory for generated documentation | `docs/generated` |
| `context_output_file` | Path for the extracted context file | `code_context/extracted/repo_content.txt` |
| `clone_dir` | Directory for cloning remote repositories | `temp_cloned_repos` |
| `template` | Specific documentation template to use | `standard` |
| `force_context_regeneration` | Force regeneration of context even if it exists | `false` |
| `force_clone` | Force re-cloning of remote repository | `false` |

## Examples

### Basic Usage with Local Repository

```
GENERATE_DOC repo_path=/path/to/local/repo language=en
```

### Documentation from GitHub URL

```
GENERATE_DOC repo_path=https://github.com/username/repository language=es
```

### Custom Output Directory

```
GENERATE_DOC repo_path=/path/to/repo language=en output=/custom/docs/path
```

### Force Context Regeneration

```
GENERATE_DOC repo_path=/path/to/repo language=en force_context_regeneration=true
```

## Process Flow

1. **Language Confirmation**: The system will confirm your preferred language (English or Spanish).
2. **Repository Analysis**: 
   - For local repositories, the system analyzes the files directly
   - For GitHub URLs, the system clones the repository and then analyzes it
3. **Context Extraction**: Code is converted to a text format for analysis
4. **Menu Presentation**: A dynamic menu of documentation options is presented based on available templates
5. **Documentation Generation**: Based on your selection, the system generates documentation
6. **File Output**: Documentation is saved to the specified output directory

## Dynamic Template Menu

The menu is dynamically generated based on templates available in the system. These templates are organized into categories such as:

- Product Documentation
- Coding Styles
- Methodologies
- Git Workflows
- Product Management

Each category contains multiple template options that you can select to generate specific documentation.

## Output Files

All generated documentation is saved to the output directory (default: `docs/generated/`) as markdown files. The naming follows a consistent pattern based on the selected template.

## Use Cases

### Legacy Codebase Documentation

Ideal for generating documentation for existing codebases with poor or no documentation. Simply point to your repository and generate comprehensive documentation in minutes.

```
GENERATE_DOC repo_path=/path/to/legacy/codebase language=en
```

### Open Source Project Analysis

Quickly understand an open source project's architecture and components by generating documentation directly from its GitHub URL.

```
GENERATE_DOC repo_path=https://github.com/organization/open-source-project language=en
```

### Multilingual Documentation

Generate documentation in both English and Spanish to support international teams or projects.

```
# English documentation
GENERATE_DOC repo_path=/path/to/repo language=en

# Spanish documentation
GENERATE_DOC repo_path=/path/to/repo language=es
```

## Tips

- For best results, ensure your repository follows standard conventions for its language/framework
- The command works best with repositories that have clear structure and organization
- For larger repositories, the analysis may take longer but will provide more comprehensive results
- Use the generated documentation as a starting point and enhance it as needed

## Troubleshooting

- If the command fails to clone a GitHub repository, ensure the URL is correct and the repository is accessible
- If documentation is incomplete, try using `force_context_regeneration=true` to refresh the analysis
- For repositories with unusual structures, you may need to specify a custom template

## Related Commands

- `GENERATE_CONTEXT`: Manually extract repository context
- `PAELLA`: Initialize a new documentation project
- `CONTINUE`: Continue working on existing documentation 