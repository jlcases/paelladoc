# Plantilla de Reglas del Proyecto

## Información General
- **Nombre del Proyecto**: [Nombre]
- **Fecha de Creación**: [Fecha]
- **Responsable**: [Nombre del responsable]
- **Versión**: [Número de versión]

## Propósito
Esta plantilla documenta las reglas y convenciones a seguir durante el desarrollo del proyecto. Sirve como referencia para el equipo de desarrollo para asegurar la consistencia, calidad y cumplimiento de estándares en todo el código y la documentación.

## Reglas de Testing (MECE)

### Estructura de Tests
- **Organización de Carpetas**:
  - `tests/domain/`: Tests de la capa de dominio (reglas de negocio)
    - `models/`: Tests de modelos de dominio
    - `services/`: Tests de servicios de dominio
    - `ports/`: Tests de contratos de interfaces
    - `repositories/`: Tests de interfaces de repositorios
    - `requests/`: Tests de modelos de solicitud
  - `tests/application/`: Tests de la capa de aplicación (orquestación)
  - `tests/infrastructure/`: Tests de la capa de infraestructura (integración externa)
  - `tests/interfaces/`: Tests de la capa de interfaces de usuario

### Convenciones de Nomenclatura
- **Archivos de Test**: `test_[nombre_del_modulo].py`
- **Clases de Test**: `Test[NombreClase]`
- **Métodos de Test**: `test_[funcionalidad_a_probar]_[condición]_[resultado_esperado]`

### Dependencias Permitidas
- **Tests de Dominio**:
  - Dependencias permitidas:
    - Pydantic v2 (para validación de modelos)
    - Typing (para hints de tipos)
    - Datetime (para lógica temporal)
    - Módulos de puertos de dominio
  - Enfoque: Reglas de negocio y validación

- **Tests de Aplicación**:
  - Pueden usar mocks tanto para dominio como para servicios externos
  - Enfoque: Coordinación entre dominio e infraestructura

- **Tests de Infraestructura**:
  - Integración real o mocks sofisticados
  - Enfoque: Interacciones con bases de datos y servicios externos

### Cobertura y Calidad
- **Cobertura Mínima**:
  - Capa de Dominio: [X%]
  - Capa de Aplicación: [X%]
  - Capa de Infraestructura: [X%]
  - Capa de Interfaces: [X%]

- **Validaciones de Calidad**:
  - Todos los tests deben ser independientes entre sí
  - No debe haber código de producción sin tests asociados
  - Evitar tests que dependan del orden de ejecución

## Reglas de Gestión de Tareas (MECE)

### Estructura de Tareas
- **Formato de ID**: [Prefijo]-[Número] (Ej: TASK-001)
- **Estados Permitidos**:
  - Pendiente
  - En Progreso
  - En Revisión
  - Completado
  - Bloqueado

### Priorización
- **Niveles de Prioridad**:
  - **Mandatory**: Debe completarse sin excepción
  - **Alta**: Crítica para el negocio/proyecto
  - **Media**: Importante pero no crítica
  - **Baja**: Puede posponerse si es necesario

### Asignación y Seguimiento
- **Reglas de Asignación**:
  - Cada tarea debe tener un responsable claro
  - No se debe trabajar en más de [X] tareas simultáneamente
  - Actualizar estado diariamente

- **Métricas de Seguimiento**:
  - Velocidad del equipo (story points por sprint)
  - Tasa de completitud (% de tareas completadas vs planificadas)
  - Lead time (tiempo desde creación hasta completado)

## Reglas de Comandos de Terminal (MECE)

### Convenciones Generales
- **Estructura de Comandos**: [Describa la estructura estándar para comandos]
- **Ubicación de Scripts**: [Directorio para scripts]
- **Documentación**: Todos los comandos deben tener ayuda accesible con `--help`

### Comandos Prohibidos
- **Lista de Comandos Prohibidos**:
  - [Comando 1]: [Razón]
  - [Comando 2]: [Razón]

### Comandos Recomendados
- **Gestión de Entorno**:
  - [Comando]: [Descripción y uso]
- **Build y Deploy**:
  - [Comando]: [Descripción y uso]
- **Testing**:
  - [Comando]: [Descripción y uso]

## Reglas de Protección de Pre-commit (MECE)

### Verificaciones Obligatorias
- **Linting**: Todos los archivos deben pasar las verificaciones de linter
- **Formatting**: Todos los archivos deben estar formateados según las convenciones
- **Tests**: [Conjunto de tests que deben pasar]
- **Tamaño de Commit**: [Reglas sobre el tamaño máximo de commits]

### Excepciones
- **Archivos Excluidos**: [Lista de archivos o patrones excluidos]
- **Condiciones de Bypass**: [Condiciones bajo las cuales se pueden omitir las verificaciones]

## Reglas de Lenguaje y Estilo (MECE)

### Convenciones Generales
- **Idioma**: [Idioma estándar para código, comentarios, documentación]
- **Indentación**: [Espacios/Tabs y cantidad]
- **Longitud Máxima de Línea**: [Número de caracteres]

### Por Lenguaje
- **Python**:
  - **Estilo**: [PEP 8, etc.]
  - **Docstrings**: [Formato: Google, NumPy, etc.]
  - **Imports**: [Orden y agrupación]

- **JavaScript/TypeScript**:
  - **Estilo**: [Airbnb, Standard, etc.]
  - **Formato de Documentación**: [JSDoc, etc.]
  - **Módulos**: [ES Modules vs CommonJS]

### Nomenclatura
- **Variables**: [Convención: camelCase, snake_case, etc.]
- **Funciones**: [Convención]
- **Clases**: [Convención]
- **Constantes**: [Convención]
- **Archivos**: [Convención]

## Reglas Operacionales (MECE)

### Entornos
- **Desarrollo**:
  - **URL**: [URL del entorno]
  - **Acceso**: [Cómo acceder]
  - **Limitaciones**: [Restricciones específicas]

- **Staging**:
  - **URL**: [URL del entorno]
  - **Acceso**: [Cómo acceder]
  - **Limitaciones**: [Restricciones específicas]

- **Producción**:
  - **URL**: [URL del entorno]
  - **Acceso**: [Cómo acceder]
  - **Limitaciones**: [Restricciones específicas]

### Despliegue
- **Frecuencia**: [Política de despliegue: continuo, programado, etc.]
- **Ventanas de Mantenimiento**: [Cuándo se pueden realizar despliegues]
- **Rollback**: [Procedimiento de rollback]

## Reglas de Commits (MECE)

### Granularidad
- **Tamaño Recomendado**: Commits pequeños y enfocados
- **Frecuencia**: Hacer commits frecuentes durante el desarrollo
- **Atomicidad**: Cada commit debe representar un cambio lógico único

### Mensajes de Commit
- **Formato**:
  ```
  [tipo]: [mensaje corto]
  
  [descripción detallada (opcional)]
  
  [referencias a issues (opcional)]
  ```

- **Tipos de Commits**:
  - `feat`: Nueva funcionalidad
  - `fix`: Corrección de errores
  - `docs`: Cambios en documentación
  - `style`: Cambios de formato (no funcionales)
  - `refactor`: Refactorización de código
  - `test`: Adición o corrección de tests
  - `chore`: Cambios en proceso de build, herramientas, etc.

- **Recomendaciones**:
  - Usar tiempo presente en mensajes
  - Primera línea máximo 50 caracteres
  - Cuerpo del mensaje máximo 72 caracteres por línea
  - Explicar el "qué" y "por qué" en vez del "cómo"

## Reglas de DeepThinker (MECE)

### Metodología
- **Proceso de Pensamiento**:
  - Descomponer problemas complejos en subproblemas manejables
  - Considerar múltiples perspectivas
  - Evaluar pros y contras de cada enfoque
  - Reflexionar sobre decisiones tomadas

### Fases
- **Análisis del Problema**:
  - Definir el problema claramente
  - Identificar restricciones y requisitos
  - Determinar criterios de éxito

- **Exploración de Soluciones**:
  - Generar múltiples enfoques
  - Investigar literatura y mejores prácticas
  - Considerar soluciones creativas

- **Evaluación y Decisión**:
  - Analizar ventajas y desventajas
  - Evaluar factibilidad y complejidad
  - Seleccionar enfoque óptimo

- **Implementación y Reflexión**:
  - Implementar solución elegida
  - Verificar resultados contra criterios
  - Documentar lecciones aprendidas

### Documentación
- **Formato**: [Detalles del formato de documentación]
- **Ubicación**: [Dónde se almacena la documentación]
- **Frecuencia de Actualización**: [Cuándo actualizar]

## Prioridades del Proyecto (MECE)

### Criterios de Priorización
- **Valor para el Usuario**: [Alta/Media/Baja] - [Descripción]
- **Complejidad Técnica**: [Alta/Media/Baja] - [Descripción]
- **Riesgo**: [Alto/Medio/Bajo] - [Descripción]
- **Dependencias**: [Alta/Media/Baja] - [Descripción]

### Directivas del Proyecto
- **Nombre del Proyecto**: [Nombre]
- **Enfoque AI-First**: [Sí/No] - [Implicaciones]
- **Formato de Timestamps**: [Formato estándar]

## Anexos
- **Herramientas Recomendadas**: [Lista de herramientas con enlaces]
- **Referencias**: [Enlaces a documentación externa relevante]
- **Ejemplos**: [Enlaces a ejemplos de buenas prácticas]

---

Esta plantilla sigue principios MECE al dividir las reglas del proyecto en categorías mutuamente excluyentes (testing, gestión de tareas, comandos, etc.) y colectivamente exhaustivas (cubriendo todos los aspectos necesarios para definir completamente las reglas del proyecto). 