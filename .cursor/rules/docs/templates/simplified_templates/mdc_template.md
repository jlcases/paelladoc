description: "${PROJECT_NAME} - ${PROJECT_DESCRIPTION}"
globs: ["**/*"]
alwaysApply: true
instructions:
  global_architecture: |
    # Arquitectura Global de ${PROJECT_NAME}
    
    Consultar docs/${PROJECT_NAME}/00_index.md para la arquitectura completa del proyecto.

  code_standards: |
    # Estándares de Código
    
    Para información sobre estándares de código y mejores prácticas, consultar:
    docs/${PROJECT_NAME}/quick_task_documentation.md

patterns:
  - name: "Componentes Principales"
    pattern: "src/**/*"
    instructions: |
      # Componentes Principales
      
      Consultar docs/${PROJECT_NAME}/feature_documentation.md para detalles de implementación.

  - name: "Documentación de Bugs"
    pattern: "**/*.test.*"
    instructions: |
      # Pruebas y Errores
      
      Seguir el proceso de documentación de errores definido en:
      docs/${PROJECT_NAME}/bug_documentation.md

rules:
  - name: "${PROJECT_NAME}-rules"
    description: "Reglas de desarrollo para ${PROJECT_NAME}"
    patterns: ["**/*"]
    instructions:
      - "# ${PROJECT_NAME} - Reglas de Desarrollo"
      - ""
      - "## Documentación Completa"
      - "Toda la documentación está disponible en la carpeta docs/${PROJECT_NAME}/"
      - ""
      - "## Documentos Principales"
      - "- docs/${PROJECT_NAME}/00_index.md - Visión general del proyecto"
      - "- docs/${PROJECT_NAME}/feature_documentation.md - Especificaciones de funcionalidades"
      - "- docs/${PROJECT_NAME}/bug_documentation.md - Proceso de gestión de errores"
      - "- docs/${PROJECT_NAME}/quick_task_documentation.md - Tareas y configuración"

references:
  - "docs/${PROJECT_NAME}/00_index.md"
  - "docs/${PROJECT_NAME}/feature_documentation.md"
  - "docs/${PROJECT_NAME}/bug_documentation.md"
  - "docs/${PROJECT_NAME}/quick_task_documentation.md" 