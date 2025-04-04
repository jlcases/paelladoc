# Instrucciones: Utilizar los Flujos de Trabajo Git

Este documento explica cómo configurar y utilizar los flujos de trabajo Git integrados en PAELLADOC para gestionar eficazmente el versionado de tus proyectos.

## ¿Qué son los Flujos de Trabajo Git en PAELLADOC?

PAELLADOC proporciona plantillas y configuraciones predefinidas para diferentes estrategias de ramificación y flujos de trabajo Git, incluyendo:

- **GitFlow**: Para proyectos con ciclos de release planificados
- **GitHub Flow**: Para entrega continua y proyectos web
- **Trunk-Based Development**: Para equipos que practican integración continua
- **GitLab Flow**: Con ramificaciones por entorno de despliegue
- **Simplified Flow**: Para proyectos pequeños o desarrolladores individuales

Cada flujo de trabajo incluye:
- Estructura de ramas recomendada
- Convenciones de nomenclatura para commits
- Plantillas para Pull/Merge Requests
- Políticas de revisión y aprobación
- Scripts de automatización (hooks)

## Configurar un Flujo de Trabajo Git

### Durante la inicialización de un proyecto

Al ejecutar el comando `PAELLA`, puedes seleccionar un flujo de trabajo Git:

```
PAELLA project_name="MiProyecto"
...
> Selecciona un flujo de trabajo Git:
> 1. GitFlow
> 2. GitHub Flow
> 3. Trunk-Based Development
> 4. GitLab Flow
> 5. Simplified Flow
> 6. Personalizado
```

### Para un proyecto existente

Utiliza el comando `GIT_WORKFLOW`:

```
GIT_WORKFLOW project="MiProyecto" action="setup" workflow="github-flow"
```

Parámetros:
- `project`: Nombre del proyecto (obligatorio)
- `action`: Acción a realizar (obligatorio)
  - Opciones: setup, update, info, help
- `workflow`: Flujo de trabajo a configurar (obligatorio para setup/update)
  - Opciones: gitflow, github-flow, trunk-based, gitlab-flow, simplified-flow

## Ver la Configuración de un Flujo de Trabajo

Para ver los detalles de la configuración actual:

```
GIT_WORKFLOW project="MiProyecto" action="info"
```

Esto mostrará información como:

```
> Flujo de trabajo Git configurado: GitHub Flow
> 
> Configuración:
> - Rama principal: main
> - Convenciones de commit: Conventional Commits
> - Estrategia de merge: squash
> - Protección de rama: activada
> - Verificación CI requerida: activada
> 
> Plantillas configuradas:
> - Pull Request (.github/PULL_REQUEST_TEMPLATE.md)
> - Commit (.gitmessage)
> 
> Hooks configurados:
> - pre-commit: validación de estilo
> - pre-push: verificación de tests
```

## Personalizar un Flujo de Trabajo

### Crear un flujo personalizado

```
GIT_WORKFLOW project="MiProyecto" action="create" workflow_name="Mi-Workflow-Custom"
```

PAELLADOC iniciará un proceso interactivo:

```
> Creando nuevo flujo de trabajo: Mi-Workflow-Custom
> Responde a las siguientes preguntas para configurar el flujo.
> 
> ¿Cuál será la rama principal del repositorio? [main/master/trunk]: main
> 
> ¿Qué convención de commits deseas usar?
> 1. Conventional Commits (feat:, fix:, docs:, etc.)
> 2. Emoji-based (🚀 feat, 🐛 fix, 📝 docs, etc.)
> 3. Jira-ID first (ABC-123: feature description)
> 4. Personalizado
> Selecciona una opción: 1
> 
> ¿Qué estrategia de integración prefieres para Pull Requests?
> 1. Merge (preserva historia completa)
> 2. Squash (un commit por PR)
> 3. Rebase (historia lineal)
> Selecciona una opción: 2
> 
> [Continúa con más preguntas sobre ramas, políticas, etc.]
```

### Modificar un flujo existente

```
GIT_WORKFLOW project="MiProyecto" action="update" workflow="github-flow"
```

Esto mostrará la configuración actual y permitirá editarla:

```
> Editando flujo de trabajo: GitHub Flow
> 
> Selecciona la categoría a editar:
> 1. Ramas y nombrado
> 2. Convenciones de commit
> 3. Estrategias de integración
> 4. Plantillas
> 5. Hooks y automatización
> 
> Selecciona una opción: 2
> 
> [Muestra opciones para modificar las convenciones de commit]
```

## Aplicar Flujo de Trabajo a un Repositorio Existente

Para aplicar la configuración a un repositorio Git existente:

```
GIT_WORKFLOW project="MiProyecto" action="apply" target="./"
```

Parámetros:
- `target`: Ruta al repositorio Git (opcional, predeterminado: "./")

Esto aplicará:
- Plantillas de PR/MR si corresponde
- Archivos de configuración Git como `.gitattributes` y `.gitignore`
- Hooks de Git en `.git/hooks/`
- Archivo de configuración para la plataforma (GitHub/GitLab/etc.)

## Comandos para Gestionar el Flujo de Trabajo

PAELLADOC proporciona comandos para facilitar el seguimiento del flujo:

### Crear una nueva rama según el flujo

```
GIT_BRANCH project="MiProyecto" type="feature" name="login-system"
```

Esto creará una rama con el formato correcto según el flujo seleccionado.
Por ejemplo, en GitFlow: `feature/login-system`

Parámetros:
- `type`: Tipo de rama (feature, bugfix, hotfix, release)
- `name`: Nombre descriptivo

### Iniciar un Pull/Merge Request

```
GIT_PR project="MiProyecto" branch="feature/login-system" target="develop" title="Implementación del sistema de login"
```

Esto generará una plantilla para el PR según el flujo configurado.

### Generar un changelog para una versión

```
GIT_CHANGELOG project="MiProyecto" version="v1.2.0" output="CHANGELOG.md"
```

## Casos de Uso Comunes

### Iniciar un proyecto con GitFlow

```
# Inicializar el proyecto
PAELLA project_name="EcommerceApp" 
...
> Selecciona un flujo de trabajo Git:
> 1. GitFlow

# Crear rama para nueva funcionalidad
GIT_BRANCH project="EcommerceApp" type="feature" name="carrito-compra"

# Crear una release
GIT_BRANCH project="EcommerceApp" type="release" name="v1.0.0"
```

### Migrar un proyecto a GitHub Flow

```
# Configurar GitHub Flow
GIT_WORKFLOW project="MiProyecto" action="setup" workflow="github-flow"

# Aplicar configuración al repositorio
GIT_WORKFLOW project="MiProyecto" action="apply"

# Crear rama para nueva funcionalidad
GIT_BRANCH project="MiProyecto" type="feature" name="user-profile"
```

### Personalizar el flujo para equipos grandes

```
# Crear flujo personalizado basado en GitLab Flow
GIT_WORKFLOW project="EnterpriseApp" action="create" workflow_name="Enterprise-Flow"
...
> [Configuración personalizada]

# Añadir verificaciones adicionales
GIT_WORKFLOW project="EnterpriseApp" action="update" workflow="Enterprise-Flow"
...
> Selecciona la categoría a editar:
> 5. Hooks y automatización
...
> [Añadir verificaciones]
```

## Ejemplo Completo de Ciclo de Desarrollo

```
# Iniciar proyecto con GitHub Flow
PAELLA project_name="WebShop" description="Tienda online"
...
> Selecciona un flujo de trabajo Git:
> 2. GitHub Flow

# Crear repositorio (si no existe)
GIT_INIT project="WebShop"

# Iniciar trabajo en nueva funcionalidad
GIT_BRANCH project="WebShop" type="feature" name="product-catalog"

# Trabajo de desarrollo...

# Preparar commit
GIT_COMMIT project="WebShop" message="feat(catalog): implement product listing component"

# Crear Pull Request
GIT_PR project="WebShop" branch="product-catalog" target="main" title="Implementación de catálogo de productos"

# Después de la aprobación y merge...

# Generar documentación de cambios
GIT_CHANGELOG project="WebShop" version="v0.2.0" output="docs/CHANGELOG.md"
``` 