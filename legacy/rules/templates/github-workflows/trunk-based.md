---
title: "Trunk-Based Development Workflow Guide"
date: 2025-03-22
author: "PAELLADOC"
version: 1.0
status: "Active"
tags: ["github", "git", "workflow", "trunk-based", "version control", "continuous delivery"]
---

# Trunk-Based Development Workflow

## Core Principles
- Development centered on a single main branch (`main` or `trunk`)
- Small and frequent commits directly to the main branch
- Use of feature flags to hide features under development
- Continuous integration with the trunk several times a day
- Small and frequent deployments to production

## Branching Strategy
- Exclusively use the `main` branch (trunk) for production code
- Create short-lived branches for development (typically less than 1-2 days)
- Continuously integrate changes via pull requests or merge requests
- Avoid long-lived or divergent branches
- No specific branches for releases or development

## Development Process
- Update your local code frequently (`git pull`)
- Create a branch for each feature or fix: `git checkout -b small-feature`
- Keep changes small and atomic (< 400 lines of code)
- Merge to `main` as soon as possible, ideally multiple times a day
- Use feature flags for incomplete or experimental features

## Feature Flags
- Implement flags for all features under development
- Enable/disable features at runtime
- Allow deploying inactive code to production
- Separate deployment from release
- Remove flags once the feature is complete and stable

## Automated Testing
- Maintain a comprehensive test suite that runs on each commit
- Emphasize fast unit tests for immediate feedback
- Include integration tests to verify component interactions
- Implement end-to-end tests for critical scenarios
- Ensure tests are deterministic and reliable

## Continuous Integration
- Every commit to `main` must pass all tests
- Configure automatic test execution for each pull request
- Prioritize immediate fixes for failing tests in `main`
- Maintain high test coverage (>80%)
- Run static code analysis on each commit

## Continuous Deployment
- Automate deployments from `main` to production
- Implement progressive deployments or canary releases
- Include automatic rollback in case of issues
- Actively monitor each deployment
- Keep each deployment small for easier debugging

## Pull Requests
- Use PRs for code review, not for feature approval
- Keep PRs small and focused on a single task
- Establish mandatory but quick reviews (less than 24 hours)
- Automate basic validations (linting, tests, builds)
- Favor early communication about changes under development

## Versioning
- Generate versions automatically based on commits
- Use semantic or calendar versioning
- Each commit to `main` is potentially a production version
- Tag releases periodically for reference
- Maintain an automated CHANGELOG based on commit messages

## Recommended Tools
- Toggle or LaunchDarkly for feature flags
- GitHub Actions, CircleCI, or GitLab CI for continuous integration
- ArgoCD or FluxCD for continuous deployment
- Jest, pytest, or JUnit for automated testing
- SonarQube for static code analysis

## Team Practices
- Foster collective code ownership
- Pair programming for complex changes
- Constant communication about changes in progress
- Rotation of roles and responsibilities
- Regular retrospectives to improve the process 