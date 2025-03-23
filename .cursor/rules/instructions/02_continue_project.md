# Instrucciones: Continuar un Proyecto Existente

Este documento explica cómo continuar trabajando en un proyecto de documentación existente utilizando PAELLADOC.

## Requisitos Previos

- Un proyecto iniciado previamente con el comando `PAELLA`
- La estructura de documentación en `docs/[nombre-proyecto]/`

## Paso 1: Utilizar el Comando CONTINUE

El comando principal para continuar un proyecto es `CONTINUE`. Debes especificar el nombre del proyecto:

```
CONTINUE project_name="MiProyecto"
```

Este comando:
- Carga el estado actual del proyecto desde el sistema de memoria
- Recupera toda la información previamente recopilada
- Permite retomar el trabajo desde donde lo dejaste

## Paso 2: Revisar el Estado Actual

PAELLADOC te mostrará:

1. Un resumen del proyecto (nombre, tipo, descripción)
2. El estado actual de la documentación
3. Las secciones completadas y pendientes

Por ejemplo:
```
> Proyecto: WebShop (frontend)
> Descripción: Una tienda en línea para vender productos artesanales
> Estado: 3 secciones completadas, 2 secciones pendientes
```

## Paso 3: Seleccionar el Área de Trabajo

Se te presentarán opciones para continuar:

1. **Completar secciones pendientes**: Trabajar en secciones incompletas
2. **Actualizar secciones existentes**: Modificar documentación ya creada
3. **Añadir nueva documentación**: Crear secciones adicionales
4. **Gestionar memoria del proyecto**: Registrar decisiones, problemas o logros

## Paso 4: Completar Secciones Pendientes

Si eliges completar secciones pendientes:

1. Se mostrará la lista de secciones incompletas
2. Selecciona la sección que quieres completar
3. PAELLADOC iniciará un flujo de conversación para recopilar la información necesaria

Por ejemplo:
```
> Secciones pendientes:
> 1. Arquitectura técnica
> 2. Estrategia de pruebas
> ¿Qué sección deseas completar?

1

> Vamos a completar la documentación de arquitectura técnica...
```

## Paso 5: Actualizar Secciones Existentes

Si eliges actualizar secciones existentes:

1. Se mostrará la lista de secciones ya documentadas
2. Selecciona la sección que deseas modificar
3. PAELLADOC mostrará la información actual y te guiará para actualizarla

## Paso 6: Añadir Nueva Documentación

Si eliges añadir nueva documentación:

1. Se mostrarán las plantillas disponibles
2. Selecciona el tipo de documentación que deseas añadir
3. PAELLADOC te guiará para crear la nueva sección

## Paso 7: Gestionar Memoria del Proyecto

Para registrar elementos en la memoria del proyecto:

1. **Logros**: `ACHIEVEMENT description="Logro importante" category="development" impact_level="high"`
2. **Problemas**: `ISSUE description="Problema crítico" severity="high" area="technical"`
3. **Decisiones**: `DECISION description="Cambio de arquitectura" impact=["architecture"] rationale="Mejorar escalabilidad"`

## Paso 8: Guardar Cambios

Al finalizar, confirma los cambios:

1. PAELLADOC actualizará los archivos de documentación
2. Se actualizará el sistema de memoria del proyecto
3. Se generarán o actualizarán las reglas Cursor si están habilitadas

## Casos de Uso Comunes

### Actualizar Detalles Técnicos

```
CONTINUE project_name="WebShop"
> Selecciona: Actualizar secciones existentes
> Selecciona: Especificaciones técnicas
```

### Añadir Nueva Funcionalidad

```
CONTINUE project_name="WebShop"
> Selecciona: Añadir nueva documentación
> Selecciona: Especificación de componente
```

### Registrar Una Decisión Importante

```
DECISION description="Migrar de MySQL a PostgreSQL" impact=["architecture", "development"] rationale="Mejor soporte para datos JSON y mayor escalabilidad"
```

## Ejemplo Completo

```
CONTINUE project_name="WebShop"

> Proyecto: WebShop (frontend)
> Descripción: Una tienda en línea para vender productos artesanales
> Estado: 3 secciones completadas, 2 secciones pendientes
>
> ¿Qué deseas hacer?
> 1. Completar secciones pendientes
> 2. Actualizar secciones existentes
> 3. Añadir nueva documentación
> 4. Gestionar memoria del proyecto

1

> Secciones pendientes:
> 1. Arquitectura técnica
> 2. Estrategia de pruebas
> ¿Qué sección deseas completar?

1

> Vamos a completar la documentación de arquitectura técnica...
> [... continúa el flujo de conversación ...]

> Documentación de arquitectura técnica completada.
> Archivo actualizado: docs/WebShop/architecture/technical_architecture.md
``` 