# Instructions: Continuing an Existing Project

This document explains how to continue working on an existing documentation project using PAELLADOC.

## Prerequisites

- A project previously initiated with the `PAELLA` command
- Documentation structure in `docs/[project-name]/`

## Step 1: Use the CONTINUE Command

The main command to continue a project is `CONTINUE`. You must specify the project name:

```
CONTINUE project_name="MyProject"
```

This command:
- Loads the current state of the project from the memory system
- Retrieves all previously collected information
- Allows you to resume work from where you left off

## Step 2: Review Current Status

PAELLADOC will show you:

1. A project summary (name, type, description)
2. The current status of the documentation
3. Completed and pending sections

For example:
```
> Project: WebShop (frontend)
> Description: An online store selling handcrafted products
> Status: 3 sections completed, 2 sections pending
```

## Step 3: Select Work Area

You will be presented with options to continue:

1. **Complete pending sections**: Work on incomplete sections
2. **Update existing sections**: Modify already created documentation
3. **Add new documentation**: Create additional sections
4. **Manage project memory**: Record decisions, issues, or achievements

## Step 4: Complete Pending Sections

If you choose to complete pending sections:

1. The list of incomplete sections will be displayed
2. Select the section you want to complete
3. PAELLADOC will initiate a conversation flow to gather the necessary information

For example:
```
> Pending sections:
> 1. Technical architecture
> 2. Testing strategy
> Which section would you like to complete?

1

> Let's complete the technical architecture documentation...
```

## Step 5: Update Existing Sections

If you choose to update existing sections:

1. The list of already documented sections will be displayed
2. Select the section you want to modify
3. PAELLADOC will show the current information and guide you to update it

## Step 6: Add New Documentation

If you choose to add new documentation:

1. Available templates will be shown
2. Select the type of documentation you want to add
3. PAELLADOC will guide you to create the new section

## Step 7: Manage Project Memory

To record elements in the project memory:

1. **Achievements**: `ACHIEVEMENT description="Important achievement" category="development" impact_level="high"`
2. **Issues**: `ISSUE description="Critical issue" severity="high" area="technical"`
3. **Decisions**: `DECISION description="Architecture change" impact=["architecture"] rationale="Improve scalability"`

## Step 8: Save Changes

When finished, confirm the changes:

1. PAELLADOC will update the documentation files
2. The project memory system will be updated
3. Cursor rules will be generated or updated if enabled

## Common Use Cases

### Update Technical Details

```
CONTINUE project_name="WebShop"
> Select: Update existing sections
> Select: Technical specifications
```

### Add New Functionality

```
CONTINUE project_name="WebShop"
> Select: Add new documentation
> Select: Component specification
```

### Record an Important Decision

```
DECISION description="Migrate from MySQL to PostgreSQL" impact=["architecture", "development"] rationale="Better JSON data support and increased scalability"
```

## Complete Example

```
CONTINUE project_name="WebShop"

> Project: WebShop (frontend)
> Description: An online store selling handcrafted products
> Status: 3 sections completed, 2 sections pending
>
> What would you like to do?
> 1. Complete pending sections
> 2. Update existing sections
> 3. Add new documentation
> 4. Manage project memory

1

> Pending sections:
> 1. Technical architecture
> 2. Testing strategy
> Which section would you like to complete?

1

> Let's complete the technical architecture documentation...
> [... conversation flow continues ...]

> Technical architecture documentation completed.
> File updated: docs/WebShop/architecture/technical_architecture.md
``` 