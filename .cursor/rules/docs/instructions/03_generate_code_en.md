# Instructions: Generating Code from Documentation

This document explains how to use PAELLADOC to generate code based on project documentation.

## Prerequisites

- A fully documented project with PAELLADOC
- Complete technical specifications
- Finalized architecture documentation

## Step 1: Start the GENERATE_CODE Command

The main command for generating code is `GENERATE_CODE`. You can run it in two ways:

### Simple Method (Conversational)

Simply run:

```
GENERATE_CODE project_name="MyProject"
```

This will start an interactive conversation flow that will guide you through the process.

### Method with Complete Parameters

If you already have all the details clear, you can provide them directly:

```
GENERATE_CODE project_name="MyProject" output_path="../generated_code" code_type="frontend" language="typescript" include_tests=true github_repo="username/repo" methodologies=["tdd"] git_workflow="github_flow"
```

## Step 2: Verify Project Information

PAELLADOC will verify that all necessary information is complete:

1. **Basic project information**: Name, description, purpose
2. **Technical specifications**: Tech stack, frameworks, dependencies
3. **Technical architecture**: Components, modules, structure
4. **Data models**: Entities, relationships, schemas

If any critical information is missing, PAELLADOC will guide you to complete it before proceeding.

## Step 3: Select Development Methodologies

You will be asked to confirm or select:

1. **Development methodologies**: TDD, BDD, Agile/Scrum, etc.
2. **Git workflow**: GitHub Flow, GitFlow, Trunk-based, etc.
3. **Testing strategy**: Test types, coverage, frameworks

## Step 4: Configure the Output Environment

Specify where and how the code will be generated:

1. **Output path**: Directory where the code will be generated
2. **Code type**: Frontend, backend, fullstack, etc.
3. **Main language**: JavaScript, TypeScript, Python, etc.
4. **GitHub integration**: Repository for the code (optional)

## Step 5: Review the Configuration

Before proceeding, PAELLADOC will display a complete summary of the configuration:

```
> Code generation configuration:
> Project: WebShop
> Type: Frontend (React)
> Language: TypeScript
> Testing: Jest + Testing Library
> Methodologies: TDD
> Git Flow: GitHub Flow
> Output: ../generated_code/webshop
> Repository: username/webshop
```

## Step 6: Start Generation

Once the configuration is confirmed:

1. PAELLADOC will analyze all available documentation
2. Extract components, models, routes, etc.
3. Generate the project structure
4. Create code files according to specifications
5. Configure testing and CI/CD tools based on selected methodologies

During this process, PAELLADOC will show the progress:

```
> Analyzing documentation...
> Project structure created
> Generating components (12/24)
> Generating tests (18/36)
> Configuring CI/CD tools
```

## Step 7: Repository Management (Optional)

If you specified a GitHub repository:

1. PAELLADOC will create the repository if it doesn't exist
2. Configure branch structure according to the selected Git flow
3. Initialize the repository with the generated code
4. Configure GitHub Actions or workflows according to methodologies

## Step 8: Review the Generated Code

Once generation is complete:

1. PAELLADOC will provide a summary of generated files
2. Tell you where to find the code
3. Explain how to run and test the project

```
> Code generation completed
> Code generated in: ../generated_code/webshop
> Repository created: https://github.com/username/webshop
> 
> To run the project:
> cd ../generated_code/webshop
> npm install
> npm start
```

## Common Use Cases

### Generate a React Frontend

```
GENERATE_CODE project_name="Dashboard" code_type="frontend" language="typescript" include_tests=true methodologies=["tdd"]
```

### Generate an Express Backend API

```
GENERATE_CODE project_name="API" code_type="backend" language="javascript" include_tests=true methodologies=["tdd", "ci"]
```

### Generate a Chrome Extension

```
GENERATE_CODE project_name="Extension" code_type="extension" language="javascript" include_tests=true
```

## Complete Example

```
GENERATE_CODE project_name="WebShop"

> Verifying WebShop project information...
> Complete technical specifications found.
>
> Where would you like the code to be generated?

../generated_code/webshop

> The identified methodologies are: TDD
> Would you like to keep these methodologies or modify them?

Keep

> Would you like to create a GitHub repository for this code?

Yes

> What is the repository name? (username/repo)

myusername/webshop

> Code generation configuration:
> Project: WebShop
> Type: Frontend (React)
> Language: TypeScript
> Testing: Jest + Testing Library
> Methodologies: TDD
> Git Flow: GitHub Flow
> Output: ../generated_code/webshop
> Repository: myusername/webshop
>
> Do you confirm this configuration?

Yes

> Starting code generation...
> [... generation progress ...]
> Generation completed.
> Code generated in: ../generated_code/webshop
> Repository created: https://github.com/myusername/webshop
``` 