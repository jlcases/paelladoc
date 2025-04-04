# Instructions: Starting a New Documentation Project

This document explains step by step how to start a new project using PAELLADOC.

## Prerequisites

- Make sure you have PAELLADOC installed on your system
- Basic knowledge of the project you want to document

## Step 1: Start the PAELLA Command

The main command to start a new project is `PAELLA`. You can run it in two ways:

### Simple Method (Conversational)

Simply run:

```
PAELLA
```

This will start an interactive conversation flow that will guide you through the process.

### Method with Parameters

If you already have clear information about the project, you can provide it directly:

```
PAELLA project_name="MyProject" project_type="frontend" methodologies=["tdd"] git_workflow="github_flow"
```

## Step 2: Provide Basic Project Information

During the conversation flow, you will be asked for:

1. **Project name**: A unique and descriptive name
2. **Project description**: A brief description of its purpose
3. **Main purpose**: The fundamental objective of the project
4. **Project category**: Web, Mobile, Desktop, API, etc.

## Step 3: Specify Technical Details

You will be asked for technical information such as:

1. **Development environment**: Operating systems, runtime, versions
2. **Frameworks and libraries**: Main technologies to use
3. **Build tools**: Build configuration
4. **Database**: If applicable
5. **Testing strategy**: Testing frameworks and approaches

## Step 4: Define Documentation Scope

Specify:

1. **Level of detail**: Basic, Standard, Detailed, or Exhaustive
2. **Main audience**: Developers, Designers, Stakeholders, etc.
3. **Priority areas**: Technical architecture, APIs, User flows, etc.
4. **Existing documentation**: Whether to incorporate previous documentation

## Step 5: Choose Development Methodologies

Select:

1. **Methodologies**: TDD, BDD, Agile/Scrum, DevOps/CI, etc.
2. **Git workflow**: GitHub Flow, GitFlow, Trunk-based, etc.

## Step 6: Confirm Creation

Once all the information has been provided:

1. Confirm the creation of the documentation structure
2. PAELLADOC will generate the initial folder and file structure
3. A `.memory.json` file will be created to maintain the project history

## Result

After completing these steps, you will have:

1. A folder structure in `docs/[project-name]/`
2. Initial project definition files
3. A memory system to record decisions and progress

## Next Steps

- Use `CONTINUE project_name="MyProject"` to resume work on this project
- Use `MEMORY` to view the project log
- Use `ACHIEVEMENT`, `ISSUE`, or `DECISION` to record important events

## Complete Example

```
PAELLA project_name="WebShop" project_type="frontend" methodologies=["tdd"] git_workflow="github_flow"

> Welcome to PAELLADOC. I will help you document your WebShop project.
> Please provide a brief description of the project:

An online store to sell handcrafted products

> What is the main purpose of the project?

Create a platform for local artisans to sell their products

> [... conversation flow continues ...]

> Would you like me to proceed with creating the documentation structure now?

Yes

> Documentation structure created in docs/WebShop/
``` 