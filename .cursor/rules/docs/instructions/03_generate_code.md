# Instrucciones: Generar Código desde la Documentación

Este documento explica cómo utilizar PAELLADOC para generar código a partir de la documentación de un proyecto.

## Requisitos Previos

- Un proyecto completamente documentado con PAELLADOC
- Especificaciones técnicas completas
- Documentación de arquitectura finalizada

## Paso 1: Iniciar el Comando GENERATE_CODE

El comando principal para generar código es `GENERATE_CODE`. Puedes ejecutarlo de dos maneras:

### Método Simple (Conversacional)

Simplemente ejecuta:

```
GENERATE_CODE project_name="MiProyecto"
```

Esto iniciará un flujo de conversación interactivo que te guiará a través del proceso.

### Método con Parámetros Completos

Si ya tienes claros todos los detalles, puedes proporcionarlos directamente:

```
GENERATE_CODE project_name="MiProyecto" output_path="../generated_code" code_type="frontend" language="typescript" include_tests=true github_repo="usuario/repo" methodologies=["tdd"] git_workflow="github_flow"
```

## Paso 2: Verificar Información del Proyecto

PAELLADOC verificará que toda la información necesaria esté completa:

1. **Información básica del proyecto**: Nombre, descripción, propósito
2. **Especificaciones técnicas**: Stack tecnológico, frameworks, dependencias
3. **Arquitectura técnica**: Componentes, módulos, estructura
4. **Modelos de datos**: Entidades, relaciones, esquemas

Si alguna información crítica falta, PAELLADOC te guiará para completarla antes de proceder.

## Paso 3: Seleccionar Metodologías de Desarrollo

Se te pedirá confirmar o seleccionar:

1. **Metodologías de desarrollo**: TDD, BDD, Agile/Scrum, etc.
2. **Flujo de trabajo Git**: GitHub Flow, GitFlow, Trunk-based, etc.
3. **Estrategia de testing**: Tipos de pruebas, cobertura, frameworks

## Paso 4: Configurar el Entorno de Salida

Especifica dónde y cómo se generará el código:

1. **Ruta de salida**: Directorio donde se generará el código
2. **Tipo de código**: Frontend, backend, fullstack, etc.
3. **Lenguaje principal**: JavaScript, TypeScript, Python, etc.
4. **Integración con GitHub**: Repositorio para el código (opcional)

## Paso 5: Revisar la Configuración

Antes de proceder, PAELLADOC mostrará un resumen completo de la configuración:

```
> Configuración de generación de código:
> Proyecto: WebShop
> Tipo: Frontend (React)
> Lenguaje: TypeScript
> Testing: Jest + Testing Library
> Metodologías: TDD
> Flujo Git: GitHub Flow
> Salida: ../generated_code/webshop
> Repositorio: usuario/webshop
```

## Paso 6: Iniciar la Generación

Una vez confirmada la configuración:

1. PAELLADOC analizará toda la documentación disponible
2. Extraerá componentes, modelos, rutas, etc.
3. Generará la estructura del proyecto
4. Creará los archivos de código según las especificaciones
5. Configurará herramientas de testing y CI/CD según las metodologías seleccionadas

Durante este proceso, PAELLADOC mostrará el progreso:

```
> Analizando documentación...
> Estructura del proyecto creada
> Generando componentes (12/24)
> Generando tests (18/36)
> Configurando herramientas de CI/CD
```

## Paso 7: Gestión del Repositorio (Opcional)

Si especificaste un repositorio GitHub:

1. PAELLADOC creará el repositorio si no existe
2. Configurará la estructura de ramas según el flujo Git seleccionado
3. Inicializará el repositorio con el código generado
4. Configurará GitHub Actions o workflows según las metodologías

## Paso 8: Revisar el Código Generado

Una vez completada la generación:

1. PAELLADOC proporcionará un resumen de los archivos generados
2. Te indicará dónde encontrar el código
3. Te explicará cómo ejecutar y probar el proyecto

```
> Generación de código completada
> Código generado en: ../generated_code/webshop
> Repositorio creado: https://github.com/usuario/webshop
> 
> Para ejecutar el proyecto:
> cd ../generated_code/webshop
> npm install
> npm start
```

## Casos de Uso Comunes

### Generar un Frontend con React

```
GENERATE_CODE project_name="Dashboard" code_type="frontend" language="typescript" include_tests=true methodologies=["tdd"]
```

### Generar una API Backend con Express

```
GENERATE_CODE project_name="API" code_type="backend" language="javascript" include_tests=true methodologies=["tdd", "ci"]
```

### Generar una Extensión de Chrome

```
GENERATE_CODE project_name="Extension" code_type="extension" language="javascript" include_tests=true
```

## Ejemplo Completo

```
GENERATE_CODE project_name="WebShop"

> Verificando información del proyecto WebShop...
> Se encontraron especificaciones técnicas completas.
>
> ¿Dónde deseas que se genere el código?

../generated_code/webshop

> Las metodologías identificadas son: TDD
> ¿Deseas mantener estas metodologías o modificarlas?

Mantener

> ¿Deseas crear un repositorio GitHub para este código?

Sí

> ¿Cuál es el nombre del repositorio? (usuario/repo)

miusuario/webshop

> Configuración de generación de código:
> Proyecto: WebShop
> Tipo: Frontend (React)
> Lenguaje: TypeScript
> Testing: Jest + Testing Library
> Metodologías: TDD
> Flujo Git: GitHub Flow
> Salida: ../generated_code/webshop
> Repositorio: miusuario/webshop
>
> ¿Confirmas esta configuración?

Sí

> Iniciando generación de código...
> [... progreso de generación ...]
> Generación completada.
> Código generado en: ../generated_code/webshop
> Repositorio creado: https://github.com/miusuario/webshop
``` 