# Instrucciones: Iniciar un Nuevo Proyecto de Documentación

Este documento explica paso a paso cómo iniciar un nuevo proyecto utilizando PAELLADOC.

## Requisitos Previos

- Asegúrate de tener instalado PAELLADOC en tu sistema
- Conocimiento básico del proyecto que quieres documentar

## Paso 1: Iniciar el Comando PAELLA

El comando principal para iniciar un nuevo proyecto es `PAELLA`. Puedes ejecutarlo de dos maneras:

### Método Simple (Conversacional)

Simplemente ejecuta:

```
PAELLA
```

Esto iniciará un flujo de conversación interactivo que te guiará a través del proceso.

### Método con Parámetros

Si ya tienes clara la información del proyecto, puedes proporcionarla directamente:

```
PAELLA project_name="MiProyecto" project_type="frontend" methodologies=["tdd"] git_workflow="github_flow"
```

## Paso 2: Proporcionar Información Básica del Proyecto

Durante el flujo de conversación, se te pedirá:

1. **Nombre del proyecto**: Un nombre único y descriptivo
2. **Descripción del proyecto**: Una breve descripción de su propósito
3. **Propósito principal**: El objetivo fundamental del proyecto
4. **Categoría del proyecto**: Web, Móvil, Escritorio, API, etc.

## Paso 3: Especificar Detalles Técnicos

Se te pedirá información técnica como:

1. **Entorno de desarrollo**: Sistemas operativos, runtime, versiones
2. **Frameworks y bibliotecas**: Tecnologías principales a utilizar
3. **Herramientas de build**: Configuración de compilación
4. **Base de datos**: Si aplica
5. **Estrategia de testeo**: Frameworks y enfoques de prueba

## Paso 4: Definir el Alcance de la Documentación

Especifica:

1. **Nivel de detalle**: Básico, Estándar, Detallado o Exhaustivo
2. **Audiencia principal**: Desarrolladores, Diseñadores, Stakeholders, etc.
3. **Áreas prioritarias**: Arquitectura técnica, APIs, Flujos de usuario, etc.
4. **Documentación existente**: Si hay que incorporar documentación previa

## Paso 5: Elegir Metodologías de Desarrollo

Selecciona:

1. **Metodologías**: TDD, BDD, Agile/Scrum, DevOps/CI, etc.
2. **Flujo de trabajo Git**: GitHub Flow, GitFlow, Trunk-based, etc.

## Paso 6: Confirmar Creación

Una vez proporcionada toda la información:

1. Confirma la creación de la estructura de documentación
2. PAELLADOC generará la estructura de carpetas y archivos iniciales
3. Se creará un archivo `.memory.json` para mantener el historial del proyecto

## Resultado

Después de completar estos pasos, tendrás:

1. Una estructura de carpetas en `docs/[nombre-proyecto]/`
2. Archivos de definición de proyecto iniciales
3. Un sistema de memoria para registrar decisiones y avances

## Próximos Pasos

- Usa `CONTINUE project_name="MiProyecto"` para retomar el trabajo en este proyecto
- Usa `MEMORY` para ver el registro del proyecto
- Usa `ACHIEVEMENT`, `ISSUE` o `DECISION` para registrar eventos importantes

## Ejemplo Completo

```
PAELLA project_name="WebShop" project_type="frontend" methodologies=["tdd"] git_workflow="github_flow"

> Bienvenido a PAELLADOC. Voy a ayudarte a documentar tu proyecto WebShop.
> Por favor, proporciona una breve descripción del proyecto:

Una tienda en línea para vender productos artesanales

> ¿Cuál es el propósito principal del proyecto?

Crear una plataforma para que artesanos locales puedan vender sus productos

> [... continúa el flujo de conversación ...]

> ¿Te gustaría que proceda a crear la estructura de documentación ahora?

Sí

> Estructura de documentación creada en docs/WebShop/ 