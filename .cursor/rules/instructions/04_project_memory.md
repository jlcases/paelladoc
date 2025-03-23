# Instrucciones: Utilizar el Sistema de Memoria del Proyecto

Este documento explica cómo utilizar el sistema de memoria de PAELLADOC para registrar y consultar la evolución de un proyecto.

## ¿Qué es el Sistema de Memoria?

El sistema de memoria de PAELLADOC es un registro estructurado que almacena:
- Logros importantes (ACHIEVEMENTS)
- Problemas encontrados (ISSUES)
- Decisiones técnicas (DECISIONS)

Esta memoria facilita:
- El seguimiento de la evolución del proyecto
- La documentación de decisiones clave
- La transferencia de conocimiento
- La justificación de cambios arquitectónicos

## Registrar Elementos en la Memoria

### Registrar un Logro

Utiliza el comando `ACHIEVEMENT`:

```
ACHIEVEMENT description="Implementación exitosa de autenticación OAuth" category="security" impact_level="high"
```

Parámetros:
- `description`: Descripción detallada del logro (obligatorio)
- `category`: Categoría del logro (obligatorio)
  - Opciones: architecture, development, documentation, testing, security, performance, product, design, research
- `impact_level`: Nivel de impacto (opcional, predeterminado: "medium")
  - Opciones: high, medium, low

### Registrar un Problema

Utiliza el comando `ISSUE`:

```
ISSUE description="Vulnerabilidad de inyección SQL en formulario de búsqueda" severity="critical" area="security"
```

Parámetros:
- `description`: Descripción detallada del problema (obligatorio)
- `severity`: Nivel de severidad (obligatorio)
  - Opciones: critical, high, medium, low
- `area`: Área afectada (obligatorio)
  - Opciones: product, technical, process, security, performance

### Registrar una Decisión Técnica

Utiliza el comando `DECISION`:

```
DECISION description="Cambiar de MySQL a PostgreSQL para el almacenamiento de datos" impact=["architecture", "development"] rationale="Mejor soporte para datos JSON y mayor escalabilidad"
```

Parámetros:
- `description`: Descripción de la decisión (obligatorio)
- `impact`: Áreas impactadas (obligatorio, array)
  - Opciones: architecture, development, documentation, testing, security, performance, product, design, process
- `rationale`: Justificación de la decisión (obligatorio)

## Consultar la Memoria del Proyecto

Utiliza el comando `MEMORY` para visualizar el registro:

```
MEMORY filter="all" format="detailed"
```

Parámetros:
- `filter`: Filtrar por categoría (opcional, predeterminado: "all")
  - Opciones: all, achievements, issues, decisions, product, technical
- `format`: Formato de salida (opcional, predeterminado: "detailed")
  - Opciones: detailed, summary, timeline

### Ejemplos de Filtrado

Mostrar solo decisiones:
```
MEMORY filter="decisions"
```

Mostrar solo problemas técnicos:
```
MEMORY filter="issues" format="summary"
```

Ver la línea de tiempo completa:
```
MEMORY filter="all" format="timeline"
```

## Casos de Uso Comunes

### Cambio Arquitectónico

Cuando realizas un cambio arquitectónico importante:

1. Documenta la decisión:
```
DECISION description="Migrar de arquitectura monolítica a microservicios" impact=["architecture", "development", "operations"] rationale="Mejorar la escalabilidad y permitir despliegues independientes de componentes"
```

2. Registra los logros durante la implementación:
```
ACHIEVEMENT description="Primer microservicio desplegado (Autenticación)" category="architecture" impact_level="high"
```

3. Documenta los problemas encontrados:
```
ISSUE description="Latencia incrementada en las comunicaciones entre servicios" severity="medium" area="performance"
```

### Trazabilidad de Seguridad

Para documentar mejoras de seguridad:

1. Registra el problema:
```
ISSUE description="Tokens JWT sin tiempo de expiración" severity="high" area="security"
```

2. Registra la decisión:
```
DECISION description="Implementar tokens JWT con expiración y rotación" impact=["security", "development"] rationale="Mitigar riesgos de tokens comprometidos"
```

3. Registra el logro:
```
ACHIEVEMENT description="Sistema de autenticación mejorado con tokens seguros" category="security" impact_level="high"
```

### Cambios en la Estrategia de Pruebas

Para documentar cambios en las pruebas:

1. Registra la decisión:
```
DECISION description="Adoptar Testing Library en lugar de Enzyme" impact=["testing", "development"] rationale="Mejores prácticas para pruebas centradas en el usuario"
```

2. Registra los logros:
```
ACHIEVEMENT description="100% de pruebas migradas a Testing Library" category="testing" impact_level="medium"
```

## Ejemplo Completo

```
# Registrar una decisión importante
DECISION description="Migrar la base de datos a un servicio gestionado en la nube" impact=["architecture", "operations", "security"] rationale="Reducir la carga de mantenimiento y mejorar la disponibilidad"

> Decisión registrada en la memoria del proyecto.

# Registrar un logro después de implementar la decisión
ACHIEVEMENT description="Migración completa a base de datos gestionada en Azure" category="operations" impact_level="high"

> Logro registrado en la memoria del proyecto.

# Ver la memoria completa
MEMORY

> === MEMORIA DEL PROYECTO WEBSHOP ===
> 
> DECISIONES:
> [2023-07-15] Migrar la base de datos a un servicio gestionado en la nube
>   Impacto: architecture, operations, security
>   Justificación: Reducir la carga de mantenimiento y mejorar la disponibilidad
>
> LOGROS:
> [2023-08-01] Migración completa a base de datos gestionada en Azure
>   Categoría: operations
>   Impacto: alto
>
> PROBLEMAS:
> No hay problemas registrados. 