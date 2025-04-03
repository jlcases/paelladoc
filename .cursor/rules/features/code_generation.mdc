---
description: When user asks about code generation, uses the GENERATE_CODE or CREATE_REPO commands, or discusses generating code from documentation, guide them through the process and explain requirements
globs: 
alwaysApply: false
---

# Code Generation

## Commands

### GENERATE_CODE
Generates code based on completed documentation

#### Arguments:
- `project_name` (string, required): Name of the project to generate code for
- `output_path` (string, required): Path where generated code will be stored (can be a different repository)
- `code_type` (string): Type of code to generate. Options: "frontend", "backend", "full_stack", "extension", "library". Default: "full_stack"
- `language` (string): Primary language to use. Options: "javascript", "typescript", "python", "java", "ruby", "go", "php". Default: "typescript"
- `style_guide` (string): Style guide to follow for code generation. Default: based on project type
- `include_tests` (boolean): Whether to generate tests for the code. Default: true
- `github_repo` (string): Optional GitHub repository to create/push to
- `methodologies` (comma-separated): Development methodologies to apply. Options: "tdd", "bdd", "scrum", "ci", "pair". Required.
- `git_workflow` (string): Git workflow to use. Options: "github_flow", "gitflow", "trunk_based", "no_workflow". Required.

#### Behavior with Existing Documentation:
When the GENERATE_CODE command is invoked without parameters, the system MUST:

1.  **Check Project Memory**: Extract project details from existing documentation. If none, suggest PAELLA command.
2.  **Auto-Populate Parameters**: Use values from documentation, prompt only for missing ones.
3.  **Summarize Documentation Analysis**: Confirm extracted components, APIs, data models. Highlight missing info.
4.  **Review and Confirmation**: Present parameters for confirmation, allow overrides, confirm critical decisions (output path, repo).

#### Required Conversation Flow:
If parameters are missing, initiate a conversation to gather:

1.  **Project Info**: Verify name, type; ask for output path.
2.  **Methodologies**: Ask for TDD, BDD, etc., explain implications.
3.  **Git Workflow**: Ask for preferred workflow (GitHub Flow, GitFlow, etc.), explain benefits.
4.  **Language/Stack**: Confirm language, ask for frameworks/libraries.
5.  **Testing Strategy**: Confirm test inclusion, ask for coverage goals, test types.
6.  **Repo Management**: Ask about creating a new repo, type, visibility, CI/CD setup.

Code generation starts ONLY after all required parameters are gathered.

### CREATE_REPO
Creates a new repository for generated code

#### Arguments:
- `repo_name` (string, required): Name of the repository to create
- `repo_type` (string): Type of repository. Options: "github", "gitlab", "local". Default: "github"
- `visibility` (string): Repository visibility. Options: "public", "private". Default: "private"
- `include_ci` (boolean): Whether to include CI/CD configuration. Default: true
- `license` (string): License to use. Options: "MIT", "Apache-2.0", "GPL-3.0", etc. Default: "MIT"

## Code Generation Architecture & Process

1.  **Documentation Analysis**: Extract requirements, architecture, components, APIs.
2.  **Scaffolding**: Generate project structure.
3.  **Component Generation**: Create individual components.
4.  **Integration**: Connect components.
5.  **Testing**: Generate tests.
6.  **Deployment/Repo**: Configure CI/CD, manage repository.

## Documentation Sources Used

- Architecture Documents
- API Specifications
- Component Specifications
- Data Models
- User Stories

## Code Quality Assurance

Generated code undergoes linting, testing (unit, integration, E2E), security scanning, and documentation generation. 