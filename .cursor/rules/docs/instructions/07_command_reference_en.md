# PAELLADOC Command Reference

This document provides a comprehensive reference of all available commands in PAELLADOC, including syntax, parameters, and usage examples.

## Basic Commands

### PAELLA

Initializes a new documentation project.

**Syntax:**
```
PAELLA [project_name="ProjectName"] [description="Project description"] [tech_stack="Stack1,Stack2"] [templates="Template1,Template2"]
```

**Parameters:**
- `project_name`: Name of the project (required)
- `description`: Brief description of the project (optional)
- `tech_stack`: Technologies used in the project (optional)
- `templates`: Documentation templates to include (optional)

**Example:**
```
PAELLA project_name="EcommerceApp" description="Online shopping platform" tech_stack="React,Node.js,MongoDB" templates="API,Frontend,Database"
```

### CONTINUE

Continues working on an existing documentation project.

**Syntax:**
```
CONTINUE project_name="ProjectName" [section="Section name"]
```

**Parameters:**
- `project_name`: Name of the project to continue (required)
- `section`: Specific section to work on (optional)

**Example:**
```
CONTINUE project_name="EcommerceApp" section="API Documentation"
```

### GENERATE_CODE

Generates code based on existing project documentation.

**Syntax:**
```
GENERATE_CODE project="ProjectName" output_path="./path" [language="Language"] [framework="Framework"] [github_repo="username/repo"]
```

**Parameters:**
- `project`: Project name to generate code from (required)
- `output_path`: Path where to save generated code (required)
- `language`: Main programming language (optional)
- `framework`: Framework to use (optional)
- `github_repo`: GitHub repository to push code to (optional)

**Example:**
```
GENERATE_CODE project="EcommerceApp" output_path="./code" language="JavaScript" framework="React" github_repo="myusername/ecommerce-frontend"
```

### HELP

Displays help information for PAELLADOC commands.

**Syntax:**
```
HELP [command="Command name"]
```

**Parameters:**
- `command`: Command to get help for (optional - if omitted, lists all commands)

**Example:**
```
HELP command="GENERATE_CODE"
```

## Documentation Management Commands

### ADD_SECTION

Adds a new section to an existing project's documentation.

**Syntax:**
```
ADD_SECTION project="ProjectName" section_type="Type" section_name="Name" [template="Template name"]
```

**Parameters:**
- `project`: Project name (required)
- `section_type`: Type of section (API, UI, Database, etc.) (required)
- `section_name`: Name of the new section (required)
- `template`: Template to use for the section (optional)

**Example:**
```
ADD_SECTION project="EcommerceApp" section_type="API" section_name="User Authentication" template="RESTful_API"
```

### UPDATE_SECTION

Updates an existing documentation section.

**Syntax:**
```
UPDATE_SECTION project="ProjectName" section="SectionName" [content="New content or instructions"]
```

**Parameters:**
- `project`: Project name (required)
- `section`: Section to update (required)
- `content`: New content or instructions for updating (optional)

**Example:**
```
UPDATE_SECTION project="EcommerceApp" section="Database Schema" content="Update product table with new fields"
```

### VERIFY

Verifies documentation for completeness and consistency.

**Syntax:**
```
VERIFY project="ProjectName" [section="SectionName"] [standard="StandardName"]
```

**Parameters:**
- `project`: Project name (required)
- `section`: Specific section to verify (optional)
- `standard`: Documentation standard to verify against (optional)

**Example:**
```
VERIFY project="EcommerceApp" standard="OpenAPI_3.0"
```

## Project Memory Commands

### ACHIEVEMENT

Records a project achievement in the memory system.

**Syntax:**
```
ACHIEVEMENT project="ProjectName" title="Achievement title" description="Detailed description" [date="YYYY-MM-DD"] [importance="level"]
```

**Parameters:**
- `project`: Project name (required)
- `title`: Title of the achievement (required)
- `description`: Detailed description (required)
- `date`: Date of achievement (optional, defaults to current date)
- `importance`: Importance level (low, medium, high) (optional)

**Example:**
```
ACHIEVEMENT project="EcommerceApp" title="Complete Shopping Cart" description="Implemented the shopping cart functionality with all required features" importance="high"
```

### ISSUE

Records a project issue in the memory system.

**Syntax:**
```
ISSUE project="ProjectName" title="Issue title" description="Detailed description" [status="Status"] [resolution="Resolution strategy"]
```

**Parameters:**
- `project`: Project name (required)
- `title`: Title of the issue (required)
- `description`: Detailed description (required)
- `status`: Current status (open, in-progress, resolved) (optional)
- `resolution`: Resolution strategy or solution (optional)

**Example:**
```
ISSUE project="EcommerceApp" title="Payment Gateway Integration Issue" description="The Stripe integration is failing with timeout errors" status="in-progress" resolution="Contacting Stripe support for assistance"
```

### DECISION

Records a technical decision in the memory system.

**Syntax:**
```
DECISION project="ProjectName" title="Decision title" description="Detailed description" [alternatives="Alternative options"] [reasoning="Decision reasoning"]
```

**Parameters:**
- `project`: Project name (required)
- `title`: Title of the decision (required)
- `description`: Detailed description (required)
- `alternatives`: Alternative options considered (optional)
- `reasoning`: Reasoning behind the decision (optional)

**Example:**
```
DECISION project="EcommerceApp" title="Database Selection" description="Selected MongoDB for product data storage" alternatives="PostgreSQL, MySQL, DynamoDB" reasoning="Need for flexible schema and document-based storage for product attributes"
```

### MEMORY

Queries the project memory system.

**Syntax:**
```
MEMORY project="ProjectName" [type="Type"] [query="Search term"] [format="output format"]
```

**Parameters:**
- `project`: Project name (required)
- `type`: Type of memory items to query (achievement, issue, decision, all) (optional)
- `query`: Search term to filter results (optional)
- `format`: Output format (text, markdown, json) (optional)

**Example:**
```
MEMORY project="EcommerceApp" type="decision" query="database" format="markdown"
```

## Coding Style Commands

### CODING_STYLE

Manages coding styles for a project.

**Syntax:**
```
CODING_STYLE project="ProjectName" action="Action" [style_name="StyleName"] [target="FilePath"]
```

**Parameters:**
- `project`: Project name (required)
- `action`: Action to perform (view, apply, customize, verify) (required)
- `style_name`: Name of the coding style (required for some actions)
- `target`: Target file or directory (required for apply/verify)

**Example:**
```
CODING_STYLE project="EcommerceApp" action="apply" style_name="React_Best_Practices" target="./src/components"
```

## Git Workflow Commands

### GIT_WORKFLOW

Manages Git workflows for a project.

**Syntax:**
```
GIT_WORKFLOW project="ProjectName" action="Action" [workflow="WorkflowName"] [target="Repository path"]
```

**Parameters:**
- `project`: Project name (required)
- `action`: Action to perform (setup, update, info, apply, create) (required)
- `workflow`: Name of the workflow (required for some actions)
- `target`: Target repository path (required for apply)

**Example:**
```
GIT_WORKFLOW project="EcommerceApp" action="setup" workflow="github-flow"
```

### GIT_BRANCH

Creates a new Git branch following the configured workflow.

**Syntax:**
```
GIT_BRANCH project="ProjectName" type="BranchType" name="BranchName"
```

**Parameters:**
- `project`: Project name (required)
- `type`: Branch type (feature, bugfix, hotfix, release) (required)
- `name`: Descriptive name (required)

**Example:**
```
GIT_BRANCH project="EcommerceApp" type="feature" name="user-profile"
```

### GIT_PR

Initiates a Pull/Merge Request following the configured workflow.

**Syntax:**
```
GIT_PR project="ProjectName" branch="BranchName" target="TargetBranch" title="PR Title"
```

**Parameters:**
- `project`: Project name (required)
- `branch`: Source branch (required)
- `target`: Target branch (required)
- `title`: Title of the PR (required)

**Example:**
```
GIT_PR project="EcommerceApp" branch="feature/user-profile" target="develop" title="User profile implementation"
```

### GIT_CHANGELOG

Generates a changelog for a version.

**Syntax:**
```
GIT_CHANGELOG project="ProjectName" version="VersionNumber" [output="OutputPath"]
```

**Parameters:**
- `project`: Project name (required)
- `version`: Version number (required)
- `output`: Output path for the changelog (optional)

**Example:**
```
GIT_CHANGELOG project="EcommerceApp" version="v1.2.0" output="docs/CHANGELOG.md"
```

## System Commands

### EXPORT

Exports documentation in various formats.

**Syntax:**
```
EXPORT project="ProjectName" [section="SectionName"] format="Format" output="OutputPath"
```

**Parameters:**
- `project`: Project name (required)
- `section`: Section to export (optional - if omitted, exports all)
- `format`: Output format (pdf, html, markdown, docx) (required)
- `output`: Output path (required)

**Example:**
```
EXPORT project="EcommerceApp" format="pdf" output="./documentation.pdf"
```

### IMPORT

Imports external documentation into a PAELLADOC project.

**Syntax:**
```
IMPORT project="ProjectName" source="SourcePath" [type="DocumentationType"] [target_section="SectionName"]
```

**Parameters:**
- `project`: Project name (required)
- `source`: Path or URL to the source documentation (required)
- `type`: Type of documentation being imported (optional)
- `target_section`: Section to import into (optional)

**Example:**
```
IMPORT project="EcommerceApp" source="./legacy-docs/api-specs.yaml" type="OpenAPI" target_section="API Documentation"
```

### VERSION

Displays PAELLADOC version information.

**Syntax:**
```
VERSION
```

**Example:**
```
VERSION
``` 