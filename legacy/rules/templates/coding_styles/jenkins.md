---
title: "Jenkins Pipeline Coding Style Guide"
date: 2025-03-22
author: "PAELLADOC"
version: 1.0
status: "Active"
tags: ["Jenkins", "CI/CD", "pipeline", "automation", "DevOps"]
---

# Jenkins Pipeline Coding Style Guide

## Pipeline Structure
- Use declarative pipelines over scripted pipelines for readability and maintainability
- Organize pipeline into logical stages that represent the build process
- Keep stage names concise and descriptive of their purpose
- Use consistent stage ordering across all pipelines in the organization
- Implement clear section comments for complex pipeline sections
- Break out complex logic into shared libraries when possible
- Limit pipeline length for maintainability (consider refactoring if over 300 lines)

## Naming Conventions
- Use camelCase for variable names (`buildVersion`, `deployTarget`)
- Use UPPERCASE for constants (`MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`)
- Use descriptive names for stages (`Build`, `Test`, `Deploy`, `Verify`)
- Prefix environment variables with context (`APP_VERSION`, `DEPLOY_TARGET`)
- Use clear naming for parameters (`version`, `environment`, `debugMode`)
- Name Jenkinsfiles consistently (e.g., `Jenkinsfile` for primary pipeline, `Jenkinsfile.deploy` for specialized pipelines)

## Groovy Syntax
- Use Groovy's concise syntax for readability
- Leverage Groovy's built-in methods for string manipulation and collections
- Prefer explicit typing for method parameters and return values
- Use string interpolation (`"Building version ${version}"`) over concatenation
- Apply consistent indentation (2 or 4 spaces, standardized across all pipelines)
- Avoid unnecessary semicolons (follow Groovy conventions)
- Use proper parentheses for clarity in complex expressions

## Pipeline Parameters
- Define all pipeline parameters at the top of the file
- Provide meaningful default values for all parameters
- Include description for each parameter
- Group related parameters together with comments
- Use appropriate parameter types (string, boolean, choice)
- Implement parameter validation early in the pipeline
- Document any dependencies between parameters

## Shared Libraries
- Abstract common functionality into shared libraries
- Implement proper versioning for shared libraries
- Document library function parameters and return values
- Create unit tests for shared library code
- Use semantic versioning for library releases
- Include usage examples in library documentation
- Keep libraries focused on specific functionality domains

## Environment Variables
- Define all environment variables in the `environment` block when possible
- Use credential binding for sensitive values
- Document the purpose of each environment variable
- Keep environment-specific values in appropriate configuration files
- Use consistent naming across different pipelines
- Avoid hardcoding values that may change between environments
- Consider using a centralized configuration source

## Error Handling
- Implement proper try/catch blocks for error-prone operations
- Define clear error messages that facilitate troubleshooting
- Set appropriate timeouts for long-running processes
- Implement retry logic for unstable operations
- Log relevant context information when errors occur
- Clean up resources in `finally` blocks or `post` sections
- Consider automatic notification on pipeline failures

## Security Practices
- Use Jenkins Credentials for all secrets
- Avoid printing sensitive information in logs
- Implement appropriate access controls to pipelines
- Scan artifacts for vulnerabilities before deployment
- Validate inputs, especially those from external sources
- Use secure agent communication (HTTPS/SSH)
- Audit pipeline changes through source control

## Testing and Validation
- Validate Jenkinsfile syntax before committing (`jenkins-cli validate`)
- Implement pipeline unit testing for complex logic
- Test pipeline changes in a staging Jenkins instance first
- Include pipeline syntax validation in CI/CD for Jenkinsfiles
- Use the replay feature carefully and document changes
- Test parameterized builds with different input combinations
- Validate infrastructure-as-code resources before deployment

## Notifications
- Implement consistent notification strategy across pipelines
- Configure notifications based on build status (success, failure, unstable)
- Include relevant build information in notifications
- Use different notification channels based on severity
- Avoid notification fatigue by being selective about notification triggers
- Include troubleshooting links in failure notifications
- Consider audience-specific notifications (developers vs. management)

## Documentation
- Include a header comment explaining the pipeline's purpose
- Document non-obvious parameters or environment requirements
- Add inline comments for complex logic sections
- Maintain up-to-date documentation for shared libraries
- Document any manual steps or prerequisites
- Include links to related resources (build documentation, application docs)
- Document expected outputs and artifacts

## Pipeline Performance
- Use parallel stages for independent tasks
- Implement appropriate caching strategies
- Utilize agent labels to target appropriate build nodes
- Clean up workspace to avoid disk space issues
- Optimize resource usage (specify container resources when appropriate)
- Monitor and analyze pipeline execution times
- Archive only necessary artifacts to save space and time

## Artifact Management
- Define a consistent artifact naming convention
- Include relevant metadata with artifacts (build number, git commit, etc.)
- Implement artifact cleanup policies
- Use appropriate repository tools (Artifactory, Nexus) rather than storing in Jenkins
- Document artifact retention policies
- Implement versioning strategy for artifacts
- Validate artifact integrity before deployment

## Deployment Practices
- Implement environment promotion strategy (dev → test → staging → production)
- Use infrastructure-as-code for deployment environments
- Implement deployment approval gates when appropriate
- Include deployment verification steps
- Implement rollback capability for failed deployments
- Document deployment prerequisites
- Consider canary or blue-green deployment strategies for critical applications

## Code Quality and Maintenance
- Review and refactor pipelines regularly
- Apply the DRY (Don't Repeat Yourself) principle
- Implement code quality checks for application code and pipeline code
- Maintain a consistent style across all pipelines
- Regularly update shared libraries and dependencies
- Implement pipeline tests to verify functionality
- Document technical debt and address it systematically 