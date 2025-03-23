# Instructions: Customizing and Using Coding Styles

This document explains how to customize and apply coding styles in PAELLADOC to maintain consistency in your projects.

## What are Coding Styles in PAELLADOC?

Coding styles in PAELLADOC are sets of rules and conventions that define:
- Code formatting standards
- Recommended patterns
- Naming practices
- Preferred architectures
- Linting rules

PAELLADOC includes default templates for:
- Frontend with React
- Backend with Node.js
- Chrome Extensions
- Mobile applications (React Native)
- Desktop applications (Electron)

## Selecting a Coding Style

### During project initialization

When running the `PAELLA` command, you'll have the option to select coding styles:

```
PAELLA project_name="MyProject"
...
> Select coding styles:
> 1. Frontend - React
> 2. Backend - Node.js
> 3. Chrome Extension
> 4. React Native
> 5. Electron
> 6. Custom
```

### For an existing project

Use the `CODING_STYLE` command:

```
CODING_STYLE project="MyProject" action="add" style="frontend-react"
```

Parameters:
- `project`: Project name (required)
- `action`: Action to perform (required)
  - Options: add, remove, update, list
- `style`: Style to apply (required for add/update)
  - Predefined values: frontend-react, backend-node, chrome-extension, react-native, electron

## View Rules of a Coding Style

To view the rules defined in a coding style:

```
CODING_STYLE project="MyProject" action="view" style="frontend-react"
```

## Customize a Coding Style

### Create a custom style

```
CODING_STYLE project="MyProject" action="create" style_name="My-Custom-Style"
```

PAELLADOC will start an interactive process to define the rules:

```
> Creating new coding style: My-Custom-Style
> Answer the following questions to configure the style.
> 
> What language is your style based on? [JavaScript/TypeScript/Python/PHP/Other]: TypeScript
> 
> What naming conventions would you like to use?
> 1. camelCase for variables, PascalCase for classes
> 2. snake_case for all identifiers
> 3. kebab-case for files, camelCase for variables
> 4. Custom
> Select an option: 1
> 
> What indentation style do you prefer?
> 1. Spaces (2)
> 2. Spaces (4)
> 3. Tabs
> Select an option: 1
> 
> [Continues with more questions about patterns, architecture, etc.]
```

### Modify an existing style

```
CODING_STYLE project="MyProject" action="update" style="frontend-react"
```

This will show the current rules and allow you to edit them:

```
> Editing style: frontend-react
> 
> Select the category to edit:
> 1. Naming conventions
> 2. Code formatting
> 3. Recommended patterns
> 4. Linting tools
> 5. Architecture
> 
> Select an option: 2
> 
> [Shows options to modify code formatting]
```

## Apply Coding Style to a File or Set of Files

To apply a style to existing files:

```
CODING_STYLE project="MyProject" action="apply" style="frontend-react" target="src/components/*.jsx"
```

Parameters:
- `target`: Path or glob pattern of files to apply the style to (required)

## Verify Style Compliance

To check if a set of files complies with a defined style:

```
CODING_STYLE project="MyProject" action="verify" style="frontend-react" target="src"
```

This will analyze the files and show a compliance report:

```
> Verifying 'frontend-react' style in 'src' directory
> 
> Files analyzed: 47
> Compliant files: 42
> Files with issues: 5
> 
> Issues found:
> - src/components/Header.jsx: Naming convention violation (line 12)
> - src/utils/helpers.js: Incorrect indentation (lines 24-30)
> ...
```

## Common Use Cases

### Start a project with multiple styles

```
PAELLA project_name="EcommerceApp" 
...
> Select coding styles:
> 1. Frontend - React
> 2. Backend - Node.js
```

This will configure the project with both styles, applying:
- React style for `src/client`, `src/components`, etc. directories
- Node.js style for `src/server`, `src/api`, etc. directories

### Migrate existing code to a defined style

```
# First check current compliance
CODING_STYLE project="MyProject" action="verify" style="frontend-react" target="src"

# Automatically apply possible corrections
CODING_STYLE project="MyProject" action="apply" style="frontend-react" target="src" auto_fix="true"

# Verify new compliance
CODING_STYLE project="MyProject" action="verify" style="frontend-react" target="src"
```

### Share a custom style between projects

```
# Export custom style
CODING_STYLE project="ProjectA" action="export" style="My-Custom-Style" output="~/paelladoc-styles/my-style.json"

# Import style in another project
CODING_STYLE project="ProjectB" action="import" source="~/paelladoc-styles/my-style.json" style_name="My-Custom-Style"
```

## Complete Workflow Example

```
# Start a new project with frontend-react style
PAELLA project_name="Dashboard" description="Administration panel"
...
> Select coding styles:
> 1. Frontend - React

# Customize the style for specific needs
CODING_STYLE project="Dashboard" action="update" style="frontend-react"
...
> Editing style: frontend-react
> [Make modifications]

# Generate code using the custom style
GENERATE_CODE project="Dashboard" output="./dashboard-code"

# Verify that the generated code complies with the style
CODING_STYLE project="Dashboard" action="verify" style="frontend-react" target="./dashboard-code"
``` 