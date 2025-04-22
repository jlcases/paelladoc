---
title: "Programming Style Selector Guide"
date: 2025-03-22
author: "PAELLADOC"
version: 1.0
status: "Active"
tags: ["programming", "style", "selection", "guidelines"]
---

# Programming Style Selection Guide

This document outlines how PAELLADOC selects and applies appropriate programming styles based on project characteristics and methodologies.

## Style Selection Criteria

### Project Type
PAELLADOC selects base programming styles according to the project type:

| Project Type | Primary Style | Secondary Styles |
|--------------|--------------|------------------|
| Frontend Web | frontend-react.md | tdd-methodology.md, github-workflow.md |
| Backend API | backend-node.md | tdd-methodology.md, github-workflow.md |
| Chrome Extension | chrome-extension.md | github-workflow.md |
| Full Stack | frontend-react.md, backend-node.md | tdd-methodology.md, github-workflow.md |
| Mobile App (React Native) | frontend-react.md | tdd-methodology.md, github-workflow.md |

### Development Methodologies
Additional styles are applied based on selected methodologies:

| Methodology | Style Template |
|-------------|---------------|
| Test-Driven Development | tdd-methodology.md |
| GitHub Workflow | github-workflow.md |

## Selection Process

1. During the `PAELLA` command initialization:
   - Project type is determined through user input
   - Development methodologies are selected

2. Style application:
   - Base styles are applied according to project type
   - Additional styles are layered based on methodologies
   - Conflicts are resolved with priority given to more specific rules

3. MDC Generation:
   - The `GENERATE_MDC` command incorporates selected styles
   - Style rules are referenced in the generated MDC file
   - Style documentation is included in the project documentation

## Style Customization

Project teams can customize the applied styles by:

1. Editing the style templates directly
2. Creating project-specific overrides in the project documentation
3. Adding custom style guides in the project's docs directory

## Style Application Examples

### Frontend React Project with TDD
```json
{
  "project_type": "frontend",
  "methodologies": ["tdd", "github_workflow"],
  "applied_styles": [
    "frontend-react.md",
    "tdd-methodology.md",
    "github-workflow.md"
  ]
}
```

### Backend Node.js API
```json
{
  "project_type": "backend",
  "methodologies": ["github_workflow"],
  "applied_styles": [
    "backend-node.md",
    "github-workflow.md"
  ]
}
```

### Chrome Extension
```json
{
  "project_type": "chrome_extension",
  "methodologies": [],
  "applied_styles": [
    "chrome-extension.md"
  ]
}
```

## Integration with Documentation

The programming style selection is documented in:
- The project overview document
- Technical architecture documentation
- Development guides

Each document references the applicable style guides and explains any project-specific adaptations or exceptions. 