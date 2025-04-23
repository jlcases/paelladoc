description: "${PROJECT_NAME} - ${PROJECT_DESCRIPTION}"
globs: ["**/*"]
alwaysApply: true
instructions:
  global_architecture: |
    # Global Architecture of ${PROJECT_NAME}
    
    Consult docs/${PROJECT_NAME}/00_index.md for the complete project architecture.

  code_standards: |
    # Code Standards
    
    For information on code standards and best practices, consult:
    docs/${PROJECT_NAME}/quick_task_documentation.md

patterns:
  - name: "Main Components"
    pattern: "src/**/*"
    instructions: |
      # Main Components
      
      Consult docs/${PROJECT_NAME}/feature_documentation.md for implementation details.

  - name: "Bug Documentation"
    pattern: "**/*.test.*"
    instructions: |
      # Tests and Errors
      
      Follow the error documentation process defined in:
      docs/${PROJECT_NAME}/bug_documentation.md

rules:
  - name: "${PROJECT_NAME}-rules"
    description: "Development rules for ${PROJECT_NAME}"
    patterns: ["**/*"]
    instructions:
      - "# ${PROJECT_NAME} - Development Rules"
      - ""
      - "## Complete Documentation"
      - "All documentation is available in the docs/${PROJECT_NAME}/ folder"
      - ""
      - "## Main Documents"
      - "- docs/${PROJECT_NAME}/00_index.md - Project overview"
      - "- docs/${PROJECT_NAME}/feature_documentation.md - Feature specifications"
      - "- docs/${PROJECT_NAME}/bug_documentation.md - Error management process"
      - "- docs/${PROJECT_NAME}/quick_task_documentation.md - Tasks and configuration"

references:
  - "docs/${PROJECT_NAME}/00_index.md"
  - "docs/${PROJECT_NAME}/feature_documentation.md"
  - "docs/${PROJECT_NAME}/bug_documentation.md"
  - "docs/${PROJECT_NAME}/quick_task_documentation.md" 