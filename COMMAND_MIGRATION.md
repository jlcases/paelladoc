# Plan de Migración de Comandos a MCP

Esta tabla mapea los comandos legacy de PAELLADOC (.mdc) a las nuevas herramientas MCP y su sprint objetivo.

| Comando Legacy (.mdc) | Nombre Herramienta MCP | Sprint Objetivo | Notas                                    |
| :-------------------- | :--------------------- | :-------------- | :--------------------------------------- |
| PAELLA                | `paella.init`          | 1               | Flujo interactivo inicial                |
| CONTINUE              | `paella.continue`      | 1               | Reanudar proyecto existente              |
| VERIFY                | `docs.verify`          | 1               | Verificación de documentación            |
| HELP                  | `core.help`            | 1               | Ayuda contextual de comandos             |
| GENERATE_CODE         | `code.generate`        | 2               | Generación de código desde docs          |
| CODING_STYLE          | `style.apply`          | 2+              | Aplicar/gestionar estilos de código    |
| GIT_WORKFLOW          | `workflow.apply`       | 2+              | Aplicar/gestionar flujos de Git        |
| GENERATE_CONTEXT      | `context.extract`      | 2+              | Extraer contexto de repositorio        |
| GENERATE-DOC          | `docs.generate`        | 2+              | Generar documentación desde código       |
| ACHIEVEMENT           | `memory.add_achievement`| 2+              | Registrar logro en memoria             |
| ISSUE                 | `memory.add_issue`     | 2+              | Registrar incidencia en memoria          |
| DECISION              | `memory.add_decision`  | 2+              | Registrar decisión técnica en memoria    |
| MEMORY                | `memory.query`         | 2+              | Consultar memoria del proyecto           |

*Nota: Los sprints son estimaciones iniciales y pueden ajustarse.* 