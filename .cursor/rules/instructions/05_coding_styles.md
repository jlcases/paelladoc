# Instrucciones: Personalizar y Utilizar Estilos de Codificación

Este documento explica cómo personalizar y aplicar estilos de codificación en PAELLADOC para mantener consistencia en tus proyectos.

## ¿Qué son los Estilos de Codificación en PAELLADOC?

Los estilos de codificación en PAELLADOC son conjuntos de reglas y convenciones que definen:
- Estándares de formato del código
- Patrones recomendados
- Prácticas de nombramiento
- Arquitecturas preferidas
- Reglas de linting

PAELLADOC incluye plantillas predeterminadas para:
- Frontend con React
- Backend con Node.js
- Extensiones de Chrome
- Aplicaciones móviles (React Native)
- Aplicaciones de escritorio (Electron)

## Seleccionar un Estilo de Codificación

### Durante la inicialización de un proyecto

Al ejecutar el comando `PAELLA`, tendrás la opción de seleccionar estilos de codificación:

```
PAELLA project_name="MiProyecto"
...
> Selecciona los estilos de codificación:
> 1. Frontend - React
> 2. Backend - Node.js
> 3. Chrome Extension
> 4. React Native
> 5. Electron
> 6. Personalizado
```

### Para un proyecto existente

Utiliza el comando `CODING_STYLE`:

```
CODING_STYLE project="MiProyecto" action="add" style="frontend-react"
```

Parámetros:
- `project`: Nombre del proyecto (obligatorio)
- `action`: Acción a realizar (obligatorio)
  - Opciones: add, remove, update, list
- `style`: Estilo a aplicar (obligatorio para add/update)
  - Valores predefinidos: frontend-react, backend-node, chrome-extension, react-native, electron

## Ver Reglas de un Estilo de Codificación

Para consultar las reglas definidas en un estilo de codificación:

```
CODING_STYLE project="MiProyecto" action="view" style="frontend-react"
```

## Personalizar un Estilo de Codificación

### Crear un estilo personalizado

```
CODING_STYLE project="MiProyecto" action="create" style_name="Mi-Estilo-Custom"
```

PAELLADOC iniciará un proceso interactivo para definir las reglas:

```
> Creando nuevo estilo de codificación: Mi-Estilo-Custom
> Responde a las siguientes preguntas para configurar el estilo.
> 
> ¿En qué lenguaje está basado tu estilo? [JavaScript/TypeScript/Python/PHP/Other]: TypeScript
> 
> ¿Qué convenciones de nombrado deseas usar?
> 1. camelCase para variables, PascalCase para clases
> 2. snake_case para todos los identificadores
> 3. kebab-case para archivos, camelCase para variables
> 4. Personalizado
> Selecciona una opción: 1
> 
> ¿Qué estilo de indentación prefieres?
> 1. Espacios (2)
> 2. Espacios (4)
> 3. Tabs
> Selecciona una opción: 1
> 
> [Continúa con más preguntas sobre patrones, arquitectura, etc.]
```

### Modificar un estilo existente

```
CODING_STYLE project="MiProyecto" action="update" style="frontend-react"
```

Esto mostrará las reglas actuales y permitirá editarlas:

```
> Editando estilo: frontend-react
> 
> Selecciona la categoría a editar:
> 1. Convenciones de nombrado
> 2. Formato de código
> 3. Patrones recomendados
> 4. Herramientas de linting
> 5. Arquitectura
> 
> Selecciona una opción: 2
> 
> [Muestra opciones para modificar el formato de código]
```

## Aplicar Estilo de Codificación a un Archivo o Conjunto de Archivos

Para aplicar un estilo a archivos existentes:

```
CODING_STYLE project="MiProyecto" action="apply" style="frontend-react" target="src/components/*.jsx"
```

Parámetros:
- `target`: Ruta o patrón glob de los archivos a los que aplicar el estilo (obligatorio)

## Verificar el Cumplimiento del Estilo

Para verificar si un conjunto de archivos cumple con un estilo definido:

```
CODING_STYLE project="MiProyecto" action="verify" style="frontend-react" target="src"
```

Esto analizará los archivos y mostrará un informe de cumplimiento:

```
> Verificando estilo 'frontend-react' en el directorio 'src'
> 
> Archivos analizados: 47
> Archivos que cumplen: 42
> Archivos con problemas: 5
> 
> Problemas encontrados:
> - src/components/Header.jsx: Violación de convención de nombrado (línea 12)
> - src/utils/helpers.js: Indentación incorrecta (líneas 24-30)
> ...
```

## Casos de Uso Comunes

### Iniciar un proyecto con múltiples estilos

```
PAELLA project_name="EcommerceApp" 
...
> Selecciona los estilos de codificación:
> 1. Frontend - React
> 2. Backend - Node.js
```

Esto configurará el proyecto con ambos estilos, aplicando:
- Estilo React para directorios `src/client`, `src/components`, etc.
- Estilo Node.js para directorios `src/server`, `src/api`, etc.

### Migrar código existente a un estilo definido

```
# Verificar primero el cumplimiento actual
CODING_STYLE project="MiProyecto" action="verify" style="frontend-react" target="src"

# Aplicar automáticamente las correcciones posibles
CODING_STYLE project="MiProyecto" action="apply" style="frontend-react" target="src" auto_fix="true"

# Verificar el nuevo cumplimiento
CODING_STYLE project="MiProyecto" action="verify" style="frontend-react" target="src"
```

### Compartir un estilo personalizado entre proyectos

```
# Exportar estilo personalizado
CODING_STYLE project="ProyectoA" action="export" style="Mi-Estilo-Custom" output="~/paelladoc-styles/mi-estilo.json"

# Importar estilo en otro proyecto
CODING_STYLE project="ProyectoB" action="import" source="~/paelladoc-styles/mi-estilo.json" style_name="Mi-Estilo-Custom"
```

## Ejemplo Completo de Flujo de Trabajo

```
# Iniciar un nuevo proyecto con estilo frontend-react
PAELLA project_name="Dashboard" description="Panel de administración"
...
> Selecciona los estilos de codificación:
> 1. Frontend - React

# Personalizar el estilo para necesidades específicas
CODING_STYLE project="Dashboard" action="update" style="frontend-react"
...
> Editando estilo: frontend-react
> [Realizas modificaciones]

# Generar código usando el estilo personalizado
GENERATE_CODE project="Dashboard" output="./dashboard-code"

# Verificar que el código generado cumpla con el estilo
CODING_STYLE project="Dashboard" action="verify" style="frontend-react" target="./dashboard-code"
``` 