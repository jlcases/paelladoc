# Referencia de Comandos PAELLADOC

Este documento proporciona una referencia completa de todos los comandos disponibles en PAELLADOC, su sintaxis, parámetros y ejemplos de uso.

## Comandos Principales

### PAELLA

Inicia un nuevo proyecto de documentación con PAELLADOC.

```
PAELLA project_name="MiProyecto" [description="Descripción del proyecto"] [category="Web"]
```

Parámetros:
- `project_name`: Nombre del proyecto (obligatorio)
- `description`: Breve descripción del proyecto (opcional)
- `category`: Categoría del proyecto (opcional)
  - Valores: Web, Mobile, Desktop, API, Library, Other
- `output_dir`: Directorio de salida (opcional, predeterminado: "./docs/{project_name}")

Ejemplo:
```
PAELLA project_name="WebShop" description="Tienda online de productos electrónicos" category="Web"
```

### CONTINUE

Continúa trabajando con un proyecto de documentación existente.

```
CONTINUE project_name="MiProyecto" [section="arquitectura"]
```

Parámetros:
- `project_name`: Nombre del proyecto (obligatorio)
- `section`: Sección específica a continuar (opcional)
  - Si no se especifica, muestra un menú con las secciones disponibles

Ejemplo:
```
CONTINUE project_name="WebShop" section="requisitos"
```

### GENERATE_CODE

Genera código basado en la documentación del proyecto.

```
GENERATE_CODE project_name="MiProyecto" [output="./src"] [type="frontend"]
```

Parámetros:
- `project_name`: Nombre del proyecto (obligatorio)
- `output`: Directorio donde se generará el código (opcional, predeterminado: "./src")
- `type`: Tipo de código a generar (opcional)
  - Valores: frontend, backend, full-stack, mobile, etc.
- `language`: Lenguaje principal para la generación (opcional)
  - Si no se especifica, se utilizará el definido en las especificaciones técnicas

Ejemplo:
```
GENERATE_CODE project_name="WebShop" output="./web-shop-code" type="frontend" language="typescript"
```

## Comandos de Gestión de Memoria

### ACHIEVEMENT

Registra un logro importante en la memoria del proyecto.

```
ACHIEVEMENT description="Descripción del logro" category="categoría" [impact_level="high"]
```

Parámetros:
- `description`: Descripción detallada del logro (obligatorio)
- `category`: Categoría del logro (obligatorio)
  - Opciones: architecture, development, documentation, testing, security, performance, product, design, research
- `impact_level`: Nivel de impacto (opcional, predeterminado: "medium")
  - Opciones: high, medium, low

Ejemplo:
```
ACHIEVEMENT description="Implementación del sistema de autenticación con OAuth" category="security" impact_level="high"
```

### ISSUE

Registra un problema o desafío en la memoria del proyecto.

```
ISSUE description="Descripción del problema" severity="nivel" area="área"
```

Parámetros:
- `description`: Descripción detallada del problema (obligatorio)
- `severity`: Nivel de severidad (obligatorio)
  - Opciones: critical, high, medium, low
- `area`: Área afectada (obligatorio)
  - Opciones: product, technical, process, security, performance

Ejemplo:
```
ISSUE description="Problema de rendimiento en la carga de imágenes" severity="high" area="performance"
```

### DECISION

Registra una decisión técnica o de producto en la memoria del proyecto.

```
DECISION description="Descripción de la decisión" impact=["área1", "área2"] rationale="Justificación"
```

Parámetros:
- `description`: Descripción de la decisión (obligatorio)
- `impact`: Áreas impactadas (obligatorio, array)
  - Opciones: architecture, development, documentation, testing, security, performance, product, design, process
- `rationale`: Justificación de la decisión (obligatorio)

Ejemplo:
```
DECISION description="Migrar de MySQL a PostgreSQL" impact=["architecture", "development"] rationale="Mejor soporte para datos JSON y mayor escalabilidad"
```

### MEMORY

Consulta la memoria del proyecto.

```
MEMORY [filter="tipo"] [format="formato"]
```

Parámetros:
- `filter`: Filtrar por categoría (opcional, predeterminado: "all")
  - Opciones: all, achievements, issues, decisions, product, technical
- `format`: Formato de salida (opcional, predeterminado: "detailed")
  - Opciones: detailed, summary, timeline

Ejemplo:
```
MEMORY filter="decisions" format="summary"
```

## Comandos de Estilos de Codificación

### CODING_STYLE

Gestiona los estilos de codificación del proyecto.

```
CODING_STYLE project="MiProyecto" action="acción" [style="estilo"] [target="ruta"]
```

Parámetros:
- `project`: Nombre del proyecto (obligatorio)
- `action`: Acción a realizar (obligatorio)
  - Opciones: add, remove, update, list, view, create, apply, verify, export, import
- `style`: Estilo a aplicar (obligatorio para add/update/view)
  - Valores predefinidos: frontend-react, backend-node, chrome-extension, react-native, electron
- `target`: Ruta o patrón glob de archivos (obligatorio para apply/verify)
- `style_name`: Nombre del nuevo estilo (obligatorio para create)
- `auto_fix`: Corregir automáticamente problemas (opcional para apply)
  - Valores: true, false
- `output`: Ruta de salida para export (obligatorio para export)
- `source`: Ruta del archivo a importar (obligatorio para import)

Ejemplos:
```
# Añadir un estilo
CODING_STYLE project="WebShop" action="add" style="frontend-react"

# Verificar código 
CODING_STYLE project="WebShop" action="verify" style="frontend-react" target="src"

# Crear estilo personalizado
CODING_STYLE project="WebShop" action="create" style_name="WebShop-Style"
```

## Comandos de Flujos de Trabajo Git

### GIT_WORKFLOW

Gestiona los flujos de trabajo Git del proyecto.

```
GIT_WORKFLOW project="MiProyecto" action="acción" [workflow="flujo"] [target="ruta"]
```

Parámetros:
- `project`: Nombre del proyecto (obligatorio)
- `action`: Acción a realizar (obligatorio)
  - Opciones: setup, update, info, help, create, apply
- `workflow`: Flujo de trabajo a configurar (obligatorio para setup/update)
  - Opciones: gitflow, github-flow, trunk-based, gitlab-flow, simplified-flow
- `workflow_name`: Nombre del nuevo flujo (obligatorio para create)
- `target`: Ruta al repositorio Git (opcional para apply, predeterminado: "./")

Ejemplos:
```
# Configurar GitFlow
GIT_WORKFLOW project="WebShop" action="setup" workflow="gitflow"

# Ver configuración actual
GIT_WORKFLOW project="WebShop" action="info"
```

### GIT_BRANCH

Crea una nueva rama según el flujo de trabajo configurado.

```
GIT_BRANCH project="MiProyecto" type="tipo" name="nombre"
```

Parámetros:
- `project`: Nombre del proyecto (obligatorio)
- `type`: Tipo de rama (obligatorio)
  - Opciones: feature, bugfix, hotfix, release
- `name`: Nombre descriptivo (obligatorio)

Ejemplo:
```
GIT_BRANCH project="WebShop" type="feature" name="carrito-compra"
```

### GIT_PR

Inicia un Pull/Merge Request según el flujo configurado.

```
GIT_PR project="MiProyecto" branch="rama" target="destino" title="título" [description="descripción"]
```

Parámetros:
- `project`: Nombre del proyecto (obligatorio)
- `branch`: Rama origen (obligatorio)
- `target`: Rama destino (obligatorio)
- `title`: Título del PR (obligatorio)
- `description`: Descripción detallada (opcional)

Ejemplo:
```
GIT_PR project="WebShop" branch="feature/carrito-compra" target="develop" title="Implementación del carrito de compra"
```

### GIT_CHANGELOG

Genera documentación de cambios.

```
GIT_CHANGELOG project="MiProyecto" version="versión" [output="ruta"]
```

Parámetros:
- `project`: Nombre del proyecto (obligatorio)
- `version`: Versión para la que generar el changelog (obligatorio)
- `output`: Archivo de salida (opcional, predeterminado: "CHANGELOG.md")

Ejemplo:
```
GIT_CHANGELOG project="WebShop" version="v1.0.0" output="docs/CHANGELOG.md"
```

## Comandos de Verificación

### VERIFY

Verifica la completitud y consistencia de la documentación.

```
VERIFY project="MiProyecto" [section="sección"] [level="nivel"]
```

Parámetros:
- `project`: Nombre del proyecto (obligatorio)
- `section`: Sección específica a verificar (opcional)
  - Si no se especifica, verifica todo el proyecto
- `level`: Nivel de verificación (opcional, predeterminado: "standard")
  - Opciones: basic, standard, strict

Ejemplo:
```
VERIFY project="WebShop" section="arquitectura" level="strict"
```

### CHECK_LINKS

Verifica los enlaces internos y externos en la documentación.

```
CHECK_LINKS project="MiProyecto" [fix="auto"]
```

Parámetros:
- `project`: Nombre del proyecto (obligatorio)
- `fix`: Modo de corrección (opcional)
  - Opciones: none, prompt, auto

Ejemplo:
```
CHECK_LINKS project="WebShop" fix="prompt"
```

## Comandos de Asistencia

### HELP

Muestra ayuda sobre comandos específicos o PAELLADOC en general.

```
HELP [comando]
```

Parámetros:
- `comando`: Comando específico sobre el que obtener ayuda (opcional)
  - Si no se especifica, muestra la ayuda general

Ejemplo:
```
HELP PAELLA
```

### TEMPLATE

Gestiona las plantillas de documentación.

```
TEMPLATE action="acción" [template="plantilla"] [output="ruta"]
```

Parámetros:
- `action`: Acción a realizar (obligatorio)
  - Opciones: list, view, apply, create, edit, export
- `template`: Nombre de la plantilla (obligatorio excepto para list)
  - Plantillas disponibles: architecture, api-docs, requirements, user-stories, etc.
- `output`: Ruta de salida (obligatorio para apply/export)

Ejemplo:
```
TEMPLATE action="apply" template="architecture" output="docs/WebShop/architecture.md"
``` 