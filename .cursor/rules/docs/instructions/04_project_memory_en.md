# Instructions: Using the Project Memory System

This document explains how to use PAELLADOC's memory system to record and query the evolution of a project.

## What is the Memory System?

PAELLADOC's memory system is a structured record that stores:
- Important achievements (ACHIEVEMENTS)
- Issues encountered (ISSUES)
- Technical decisions (DECISIONS)

This memory facilitates:
- Tracking project evolution
- Documenting key decisions
- Knowledge transfer
- Justification for architectural changes

## Recording Elements in Memory

### Recording an Achievement

Use the `ACHIEVEMENT` command:

```
ACHIEVEMENT description="Successful implementation of OAuth authentication" category="security" impact_level="high"
```

Parameters:
- `description`: Detailed description of the achievement (required)
- `category`: Achievement category (required)
  - Options: architecture, development, documentation, testing, security, performance, product, design, research
- `impact_level`: Impact level (optional, default: "medium")
  - Options: high, medium, low

### Recording an Issue

Use the `ISSUE` command:

```
ISSUE description="SQL injection vulnerability in search form" severity="critical" area="security"
```

Parameters:
- `description`: Detailed description of the issue (required)
- `severity`: Severity level (required)
  - Options: critical, high, medium, low
- `area`: Affected area (required)
  - Options: product, technical, process, security, performance

### Recording a Technical Decision

Use the `DECISION` command:

```
DECISION description="Change from MySQL to PostgreSQL for data storage" impact=["architecture", "development"] rationale="Better support for JSON data and greater scalability"
```

Parameters:
- `description`: Description of the decision (required)
- `impact`: Impacted areas (required, array)
  - Options: architecture, development, documentation, testing, security, performance, product, design, process
- `rationale`: Justification for the decision (required)

## Querying the Project Memory

Use the `MEMORY` command to view the record:

```
MEMORY filter="all" format="detailed"
```

Parameters:
- `filter`: Filter by category (optional, default: "all")
  - Options: all, achievements, issues, decisions, product, technical
- `format`: Output format (optional, default: "detailed")
  - Options: detailed, summary, timeline

### Filtering Examples

Show only decisions:
```
MEMORY filter="decisions"
```

Show only technical issues:
```
MEMORY filter="issues" format="summary"
```

View the complete timeline:
```
MEMORY filter="all" format="timeline"
```

## Common Use Cases

### Architectural Change

When making an important architectural change:

1. Document the decision:
```
DECISION description="Migrate from monolithic to microservices architecture" impact=["architecture", "development", "operations"] rationale="Improve scalability and allow independent deployment of components"
```

2. Record achievements during implementation:
```
ACHIEVEMENT description="First microservice deployed (Authentication)" category="architecture" impact_level="high"
```

3. Document issues encountered:
```
ISSUE description="Increased latency in inter-service communications" severity="medium" area="performance"
```

### Security Traceability

To document security improvements:

1. Record the issue:
```
ISSUE description="JWT tokens without expiration time" severity="high" area="security"
```

2. Record the decision:
```
DECISION description="Implement JWT tokens with expiration and rotation" impact=["security", "development"] rationale="Mitigate risks of compromised tokens"
```

3. Record the achievement:
```
ACHIEVEMENT description="Enhanced authentication system with secure tokens" category="security" impact_level="high"
```

### Changes in Testing Strategy

To document testing changes:

1. Record the decision:
```
DECISION description="Adopt Testing Library instead of Enzyme" impact=["testing", "development"] rationale="Better practices for user-centered testing"
```

2. Record achievements:
```
ACHIEVEMENT description="100% of tests migrated to Testing Library" category="testing" impact_level="medium"
```

## Complete Example

```
# Record an important decision
DECISION description="Migrate the database to a cloud managed service" impact=["architecture", "operations", "security"] rationale="Reduce maintenance burden and improve availability"

> Decision recorded in the project memory.

# Record an achievement after implementing the decision
ACHIEVEMENT description="Complete migration to Azure managed database" category="operations" impact_level="high"

> Achievement recorded in the project memory.

# View the complete memory
MEMORY

> === WEBSHOP PROJECT MEMORY ===
> 
> DECISIONS:
> [2023-07-15] Migrate the database to a cloud managed service
>   Impact: architecture, operations, security
>   Rationale: Reduce maintenance burden and improve availability
>
> ACHIEVEMENTS:
> [2023-08-01] Complete migration to Azure managed database
>   Category: operations
>   Impact: high
>
> ISSUES:
> No issues recorded. 