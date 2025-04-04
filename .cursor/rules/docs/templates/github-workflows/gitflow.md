---
title: "Gitflow Workflow Methodology Guide"
date: 2025-03-22
author: "PAELLADOC"
version: 1.0
status: "Active"
tags: ["github", "git", "workflow", "collaboration", "version control", "gitflow"]
---

# Gitflow Workflow Methodology

## Branching Strategy
- Uses two permanent main branches: `main` (production) and `develop` (development)
- Creates `feature/` branches from `develop` for new functionality
- Uses `release/` branches to prepare new production versions
- Implements `hotfix/` branches directly from `main` to fix critical issues
- All branches eventually merge into both `develop` and `main`
- Uses tags to mark versions in `main`

## Branch Management
- `main` branch: contains stable production code
- `develop` branch: contains the latest development changes
- `feature/feature-name` branches: for new functionalities
- `release/x.y.z` branches: for preparing new version releases
- `hotfix/x.y.z` branches: for urgent fixes in production
- Delete feature, release, and hotfix branches after merging

## Development Process
- All development starts from `develop`
- Create a feature branch with `git flow feature start feature-name`
- Develop the functionality with regular commits
- Finish with `git flow feature finish feature-name` to merge with `develop`
- Group multiple features into a release
- Start a release with `git flow release start x.y.z`
- Final fixes are made in the release branch
- Finish with `git flow release finish x.y.z` to merge with `main` and `develop`

## Version Control
- Follow Semantic Versioning (SemVer)
- Format: MAJOR.MINOR.PATCH (example: 2.3.1)
- Increment MAJOR for backward-incompatible changes
- Increment MINOR for backward-compatible new features
- Increment PATCH for backward-compatible bug fixes
- Use tags for each version released to production

## Commit Guidelines
- Follow commit conventions similar to GitHub Flow
- Use format: `type(scope): message` (e.g., `feat(auth): add login form`)
- Common types: feat, fix, docs, style, refactor, test, chore
- Mention related issue number when appropriate
- Keep commits focused on single logical changes

## Pull Requests
- Create PRs to integrate features into develop
- Use PRs to review changes before merging
- Keep PRs focused on a single functionality
- Require reviews before approving merges
- Resolve all review comments before merging

## Releases
- Create release branches when develop has enough features
- Minor fixes are made directly in the release branch
- Version and tag in `main` when finishing a release
- Merge release changes to both `main` and `develop`
- Document changes in CHANGELOG.md

## Hotfixes
- Create hotfixes from `main` for critical errors in production
- Merge hotfixes to both `main` and `develop`
- Increment the PATCH version for each hotfix
- Tag hotfix versions in `main`
- Prioritize hotfixes over other ongoing development

## Recommended Tools
- Git Flow extension: facilitates workflow management
- Sourcetree: graphical interface with Git Flow support
- GitHub/GitLab: for code hosting and review
- Husky: for pre-commit hooks and validation
- Semantic Release: for automated version management

## CI/CD Integration
- Run tests on all branches
- Build and verify quality on feature branches
- Implement test environments for release branches
- Automatically deploy from `main` to production
- Ensure each merge to `main` is deployable 