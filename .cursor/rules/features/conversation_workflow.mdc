---
description: When a PAELLADOC command is invoked with missing parameters, guide the user through the appropriate interactive conversation workflow to gather the necessary information
globs: 
alwaysApply: false
---

# Conversational Workflow for Commands

## Overview

When invoked with minimal parameters or without required parameters, PAELLADOC commands should initiate an interactive conversational workflow to collect the necessary information from the user. This approach creates a more natural, human-friendly experience compared to requiring users to remember specific parameter formats.

## Implementation Structure

The conversation flows are implemented using JSON configuration files located in `.cursor/rules/templates/conversation_flows/`. These files define the exact structure, questions, and flow logic for each conversation.

The main JSON files are:
- `main_conversation_flow.json`: Primary conversation flow for PAELLA and CONTINUE commands
- `technical_specifications_flow.json`: Technical specifications gathering workflow

A central configuration file `.cursor/rules/paelladoc_conversation_config.json` manages these flows, defining which conversations are required for each command.

## General Conversation Flow Principles

1. **Progressive Disclosure**: Present information gradually, starting with essential questions and progressively moving to more detailed ones.
2. **Context Awareness**: Use existing information from the project memory to avoid asking redundant questions.
3. **Explanatory Guidance**: Provide brief explanations of options when presenting choices.
4. **Confirmatory Feedback**: Summarize collected information at key points to confirm user intent.
5. **Adaptability**: Adjust the flow based on user responses to previous questions.

## Command-Specific Conversation Flows

### PAELLA Command Flow

1. **Initial Greeting and Purpose Explanation**:
   - Introduction as PAELLADOC system
   - Explanation of the documentation process
   - Overview of what information will be gathered

2. **Project Basics Conversation**:
   - Ask for project name if not provided
   - Ask for project type (frontend, backend, etc.)
   - Ask for project purpose and brief description
   - Ask about target users and stakeholders

3. **Development Methodology Conversation**:
   - Ask about preferred development methodologies
   - Ask about Git workflow preferences
   - Ask about coding style preferences
   - Ask about testing approach

4. **Documentation Scope Conversation**:
   - Ask about documentation depth needed
   - Ask about documentation priorities
   - Ask about existing documentation to incorporate
   - Ask about confidentiality requirements

5. **Next Steps Guidance**:
   - Explain how to continue the documentation process
   - Explain how to use the CONTINUE command
   - Explain how to use other PAELLADOC commands
   - Offer to start setting up the documentation structure

The implementation of this flow is in `main_conversation_flow.json`.

### GENERATE_CODE Command Flow

When the GENERATE_CODE command is invoked without all required parameters, the following conversation flow MUST be followed:

1. **Project Information Verification**:
   - Verify project name and type from memory or ask
   - Confirm or ask for output path
   - Example: "I see you want to generate code for the project 'paellaseo'. Is that correct? Where would you like the generated code to be stored?"

2. **Development Methodology Selection**:
   - Ask which development methodology the user wants to apply
   - Explain the implications of each methodology for code generation
   - Collect multiple methodologies if applicable
   - Example: "Which development methodologies would you like to apply to this project? Options include:"
     - **TDD (Test-Driven Development)**: Write tests before implementing features
     - **BDD (Behavior-Driven Development)**: Focus on business behavior with scenarios
     - **Scrum**: Iterative approach with sprints and regular meetings
     - **CI (Continuous Integration)**: Automated testing and integration
     - **Pair Programming**: Collaborative development approach

3. **Git Workflow Selection**:
   - Ask which Git workflow the user prefers
   - Explain the benefits of each workflow option
   - Configure the appropriate Git structure based on selection
   - Example: "Which Git workflow would you like to use for this project? Options include:"
     - **GitHub Flow**: Simple branch-based workflow with feature branches
     - **GitFlow**: Structured workflow with develop and release branches
     - **Trunk-Based**: Direct commits to main branch with feature flags
     - **No Workflow**: Simple Git usage without formal workflow

4. **Language & Technology Stack**:
   - Confirm or ask for primary programming language
   - Ask about specific frameworks or libraries to include
   - Determine testing frameworks based on methodology
   - Example: "The project is set to use TypeScript. Is this correct? Are there any specific frameworks or libraries you'd like to include?"

5. **Testing Strategy**:
   - Confirm if tests should be included (based on methodology)
   - Ask about test coverage requirements
   - Determine types of tests needed (unit, integration, e2e)
   - Example: "Based on TDD methodology, tests will be included. What level of test coverage would you like to aim for? What types of tests would you like to include?"

6. **Repository Management**:
   - Ask if a new repository should be created
   - Determine repository type and visibility
   - Configure CI/CD based on Git workflow selection
   - Example: "Would you like me to create a new repository for this code? If yes, what type of repository and what visibility setting would you prefer?"

This conversation flow MUST be followed completely, and code generation MUST NOT begin until all required parameters have been gathered. The implementation of this flow uses both `main_conversation_flow.json` and `technical_specifications_flow.json`.

## Implementation Guidelines

1. **Parameter Storage**: Store collected parameters in the project memory for future reference
2. **Progressive Refinement**: Allow for refinement of parameters in follow-up conversations
3. **Persistent Context**: Maintain context across multiple interactions
4. **Default Suggestions**: Offer intelligent defaults based on project type and previous choices
5. **Cancellation Support**: Allow users to cancel the flow at any point without side effects
6. **Resumability**: Support resuming an interrupted conversation flow

## Conversation Flow Definition

In command definitions, use the `conversation_flow` object to specify the required flow:

```yaml
conversation_flow:
  enabled: true
  required: true
  steps:
    - step: "step_id"
      required_params: ["param1", "param2"]
      message: "Step description message"
    # Additional steps...
```

## Configuration Structure

The JSON configuration in `.cursor/rules/paelladoc_conversation_config.json` manages the relationship between commands and conversation flows. This central configuration ensures consistent conversation handling across the system. 