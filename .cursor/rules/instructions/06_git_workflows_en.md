# Instructions: Using Git Workflows

This document explains how to configure and use the Git workflows integrated into PAELLADOC to effectively manage the versioning of your projects.

## What are Git Workflows in PAELLADOC?

PAELLADOC provides predefined templates and configurations for different branching strategies and Git workflows, including:

- **GitFlow**: For projects with planned release cycles
- **GitHub Flow**: For continuous delivery and web projects
- **Trunk-Based Development**: For teams practicing continuous integration
- **GitLab Flow**: With environment-based branching
- **Simplified Flow**: For small projects or individual developers

Each workflow includes:
- Recommended branch structure
- Commit naming conventions
- Templates for Pull/Merge Requests
- Review and approval policies
- Automation scripts (hooks)

## Configure a Git Workflow

### During project initialization

When running the `PAELLA` command, you can select a Git workflow:

```
PAELLA project_name="MyProject"
...
> Select a Git workflow:
> 1. GitFlow
> 2. GitHub Flow
> 3. Trunk-Based Development
> 4. GitLab Flow
> 5. Simplified Flow
> 6. Custom
```

### For an existing project

Use the `GIT_WORKFLOW` command:

```
GIT_WORKFLOW project="MyProject" action="setup" workflow="github-flow"
```

Parameters:
- `project`: Project name (required)
- `action`: Action to perform (required)
  - Options: setup, update, info, help
- `workflow`: Workflow to configure (required for setup/update)
  - Options: gitflow, github-flow, trunk-based, gitlab-flow, simplified-flow

## View the Configuration of a Workflow

To view the details of the current configuration:

```
GIT_WORKFLOW project="MyProject" action="info"
```

This will display information such as:

```
> Configured Git workflow: GitHub Flow
> 
> Configuration:
> - Main branch: main
> - Commit conventions: Conventional Commits
> - Merge strategy: squash
> - Branch protection: enabled
> - CI verification required: enabled
> 
> Configured templates:
> - Pull Request (.github/PULL_REQUEST_TEMPLATE.md)
> - Commit (.gitmessage)
> 
> Configured hooks:
> - pre-commit: style validation
> - pre-push: test verification
```

## Customize a Workflow

### Create a custom workflow

```
GIT_WORKFLOW project="MyProject" action="create" workflow_name="My-Custom-Workflow"
```

PAELLADOC will start an interactive process:

```
> Creating new workflow: My-Custom-Workflow
> Answer the following questions to configure the workflow.
> 
> What will be the main branch of the repository? [main/master/trunk]: main
> 
> What commit convention would you like to use?
> 1. Conventional Commits (feat:, fix:, docs:, etc.)
> 2. Emoji-based (🚀 feat, 🐛 fix, 📝 docs, etc.)
> 3. Jira-ID first (ABC-123: feature description)
> 4. Custom
> Select an option: 1
> 
> What integration strategy do you prefer for Pull Requests?
> 1. Merge (preserves complete history)
> 2. Squash (one commit per PR)
> 3. Rebase (linear history)
> Select an option: 2
> 
> [Continues with more questions about branches, policies, etc.]
```

### Modify an existing workflow

```
GIT_WORKFLOW project="MyProject" action="update" workflow="github-flow"
```

This will show the current configuration and allow you to edit it:

```
> Editing workflow: GitHub Flow
> 
> Select the category to edit:
> 1. Branches and naming
> 2. Commit conventions
> 3. Integration strategies
> 4. Templates
> 5. Hooks and automation
> 
> Select an option: 2
> 
> [Shows options to modify commit conventions]
```

## Apply Workflow to an Existing Repository

To apply the configuration to an existing Git repository:

```
GIT_WORKFLOW project="MyProject" action="apply" target="./"
```

Parameters:
- `target`: Path to the Git repository (optional, default: "./")

This will apply:
- PR/MR templates if applicable
- Git configuration files like `.gitattributes` and `.gitignore`
- Git hooks in `.git/hooks/`
- Platform configuration file (GitHub/GitLab/etc.)

## Commands for Managing the Workflow

PAELLADOC provides commands to facilitate following the flow:

### Create a new branch according to the flow

```
GIT_BRANCH project="MyProject" type="feature" name="login-system"
```

This will create a branch with the correct format according to the selected flow.
For example, in GitFlow: `feature/login-system`

Parameters:
- `type`: Branch type (feature, bugfix, hotfix, release)
- `name`: Descriptive name

### Initiate a Pull/Merge Request

```
GIT_PR project="MyProject" branch="feature/login-system" target="develop" title="Login system implementation"
```

This will generate a template for the PR according to the configured flow.

### Generate a changelog for a version

```
GIT_CHANGELOG project="MyProject" version="v1.2.0" output="CHANGELOG.md"
```

## Common Use Cases

### Start a project with GitFlow

```
# Initialize the project
PAELLA project_name="EcommerceApp" 
...
> Select a Git workflow:
> 1. GitFlow

# Create branch for new functionality
GIT_BRANCH project="EcommerceApp" type="feature" name="shopping-cart"

# Create a release
GIT_BRANCH project="EcommerceApp" type="release" name="v1.0.0"
```

### Migrate a project to GitHub Flow

```
# Configure GitHub Flow
GIT_WORKFLOW project="MyProject" action="setup" workflow="github-flow"

# Apply configuration to the repository
GIT_WORKFLOW project="MyProject" action="apply"

# Create branch for new functionality
GIT_BRANCH project="MyProject" type="feature" name="user-profile"
```

### Customize the flow for large teams

```
# Create custom flow based on GitLab Flow
GIT_WORKFLOW project="EnterpriseApp" action="create" workflow_name="Enterprise-Flow"
...
> [Custom configuration]

# Add additional checks
GIT_WORKFLOW project="EnterpriseApp" action="update" workflow="Enterprise-Flow"
...
> Select the category to edit:
> 5. Hooks and automation
...
> [Add checks]
```

## Complete Development Cycle Example

```
# Start project with GitHub Flow
PAELLA project_name="WebShop" description="Online store"
...
> Select a Git workflow:
> 2. GitHub Flow

# Create repository (if it doesn't exist)
GIT_INIT project="WebShop"

# Start work on new functionality
GIT_BRANCH project="WebShop" type="feature" name="product-catalog"

# Development work...

# Prepare commit
GIT_COMMIT project="WebShop" message="feat(catalog): implement product listing component"

# Create Pull Request
GIT_PR project="WebShop" branch="product-catalog" target="main" title="Product catalog implementation"

# After approval and merge...

# Generate change documentation
GIT_CHANGELOG project="WebShop" version="v0.2.0" output="docs/CHANGELOG.md"
``` 