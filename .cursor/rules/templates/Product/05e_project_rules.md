# Project Rules Template

## General Information

- **Project Name**: [Name]
- **Creation Date**: [Date]
- **Responsible**: [Name of the responsible person]
- **Version**: [Version number]

## Purpose

This template documents the rules and conventions to follow during project development. It serves as a reference for the development team to ensure consistency, quality, and compliance with standards across all code and documentation.

## Testing Rules (MECE)

### Test Structure

- **Folder Organization**:
  - `tests/domain/`: Tests for the domain layer (business rules)
    - `models/`: Domain model tests
    - `services/`: Domain service tests
    - `ports/`: Interface contract tests
    - `repositories/`: Repository interface tests
    - `requests/`: Request model tests
  - `tests/application/`: Tests for the application layer (orchestration)
  - `tests/infrastructure/`: Tests for the infrastructure layer (external integration)
  - `tests/interfaces/`: Tests for the user interface layer

### Naming Conventions

- **Test Files**: `test_[module_name].py`
- **Test Classes**: `Test[ClassName]`
- **Test Methods**: `test_[functionality_to_test]_[condition]_[expected_result]`

### Allowed Dependencies

- **Domain Tests**:
  - Allowed dependencies:
    - Pydantic v2 (for model validation)
    - Typing (for type hints)
    - Datetime (for temporal logic)
    - Domain port modules
  - Focus: Business rules and validation

- **Application Tests**:
  - Can use mocks for both domain and external services
  - Focus: Coordination between domain and infrastructure

- **Infrastructure Tests**:
  - Real integration or sophisticated mocks
  - Focus: Interactions with databases and external services

### Coverage and Quality

- **Minimum Coverage**:
  - Domain Layer: [X%]
  - Application Layer: [X%]
  - Infrastructure Layer: [X%]
  - Interface Layer: [X%]

- **Quality Validations**:
  - All tests must be independent of each other
  - No production code without associated tests
  - Avoid tests that depend on execution order

## Task Management Rules (MECE)

### Task Structure

- **ID Format**: [Prefix]-[Number] (Ex: TASK-001)
- **Allowed States**:
  - Pending
  - In Progress
  - In Review
  - Completed
  - Blocked

### Prioritization

- **Priority Levels**:
  - **Mandatory**: Must be completed without exception
  - **High**: Critical for business/project
  - **Medium**: Important but not critical
  - **Low**: Can be postponed if necessary

### Assignment and Tracking

- **Assignment Rules**:
  - Each task must have a clear responsible person
  - Don't work on more than [X] tasks simultaneously
  - Update status daily

- **Tracking Metrics**:
  - Team velocity (story points per sprint)
  - Completion rate (% of completed vs planned tasks)
  - Lead time (time from creation to completion)

## Terminal Command Rules (MECE)

### General Conventions

- **Command Structure**: [Describe the standard structure for commands]
- **Script Location**: [Directory for scripts]
- **Documentation**: All commands must have help accessible with `---help`

### Prohibited Commands

- **List of Prohibited Commands**:

### Recommended Commands

- **Environment Management**:
  - [Command]: [Description and usage]
- **Build and Deploy**:
  - [Command]: [Description and usage]
- **Testing**:
  - [Command]: [Description and usage]

## Pre-commit Protection Rules (MECE)

### Mandatory Verifications

- **Linting**: All files must pass linter checks
- **Formatting**: All files must be formatted according to conventions
- **Tests**: [Set of tests that must pass]
- **Commit Size**: [Rules about maximum commit size]

### Exceptions

- **Excluded Files**: [List of excluded files or patterns]
- **Bypass Conditions**: [Conditions under which verifications can be skipped]

## Language and Style Rules (MECE)

### General Conventions

- **Language**: [Standard language for code, comments, documentation]
- **Indentation**: [Spaces/Tabs and amount]
- **Maximum Line Length**: [Number of characters]

### By Language

- **Python**:
  - **Style**: [PEP 8, etc.]
  - **Docstrings**: [Format: Google, NumPy, etc.]
  - **Imports**: [Order and grouping]

- **JavaScript/TypeScript**:
  - **Style**: [Airbnb, Standard, etc.]
  - **Documentation Format**: [JSDoc, etc.]
  - **Modules**: [ES Modules vs CommonJS]

### Naming

- **Variables**: [Convention: camelCase, snake_case, etc.]
- **Functions**: [Convention]
- **Classes**: [Convention]
- **Constants**: [Convention]
- **Files**: [Convention]

## Operational Rules (MECE)

### Environments

- **Development**:
  - **URL**: [Environment URL]
  - **Access**: [How to access]
  - **Limitations**: [Specific restrictions]

- **Staging**:
  - **URL**: [Environment URL]
  - **Access**: [How to access]
  - **Limitations**: [Specific restrictions]

- **Production**:
  - **URL**: [Environment URL]
  - **Access**: [How to access]
  - **Limitations**: [Specific restrictions]

### Deployment

- **Frequency**: [Deployment policy: continuous, scheduled, etc.]
- **Maintenance Windows**: [When deployments can be performed]
- **Rollback**: [Rollback procedure]

## Commit Rules (MECE)

### Granularity

- **Recommended Size**: Small and focused commits
- **Frequency**: Make frequent commits during development
- **Atomicity**: Each commit should represent a single logical change

### Commit Messages

- **Format**:

  ```plaintext
  [type]: [short message]
  
  [detailed description (optional)]
  
  [issue references (optional)]
  ```

- **Commit Types**:
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation changes
  - `style`: Formatting changes (non-functional)
  - `refactor`: Code refactoring
  - `test`: Adding or fixing tests
  - `chore`: Changes to build process, tools, etc.

- **Recommendations**:
  - Use present tense in messages
  - First line maximum 50 characters
  - Message body maximum 72 characters per line
  - Explain the "what" and "why" instead of the "how"

## DeepThinker Rules (MECE)

### Methodology

- **Thinking Process**:
  - Break down complex problems into manageable subproblems
  - Consider multiple perspectives
  - Evaluate pros and cons of each approach
  - Reflect on decisions made

### Phases

- **Problem Analysis**:
  - Define the problem clearly
  - Identify constraints and requirements
  - Determine success criteria

- **Solution Exploration**:
  - Generate multiple approaches
  - Research literature and best practices
  - Consider creative solutions

- **Evaluation and Decision**:
  - Analyze advantages and disadvantages
  - Evaluate feasibility and complexity
  - Select optimal approach

- **Implementation and Reflection**:
  - Implement chosen solution
  - Verify results against criteria
  - Document lessons learned

### Documentation

- **Format**: [Documentation format details]
- **Location**: [Where documentation is stored]
- **Update Frequency**: [When to update]

## Project Priorities (MECE)

### Prioritization Criteria

- **User Value**: [High/Medium/Low] - [Description]
- **Technical Complexity**: [High/Medium/Low] - [Description]
- **Risk**: [High/Medium/Low] - [Description]
- **Dependencies**: [High/Medium/Low] - [Description]

### Project Directives

- **Project Name**: [Name]
- **AI-First Approach**: [Yes/No] - [Implications]
- **Timestamp Format**: [Standard format]

## Appendices

- **Recommended Tools**: [List of tools with links]
- **References**: [Links to relevant external documentation]
- **Examples**: [Links to best practice examples]

---

This template follows MECE principles by dividing project rules into mutually exclusive categories (testing, task management, commands, etc.) and collectively exhaustive (covering all aspects necessary to completely define the project rules).
