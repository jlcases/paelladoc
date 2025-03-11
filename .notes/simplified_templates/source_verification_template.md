# Plantilla de Verificación de Fuentes

## Propósito
Esta plantilla proporciona una estructura estandarizada para verificar y documentar las fuentes de información utilizadas en la documentación del proyecto, siguiendo el principio MECE (Mutuamente Excluyente, Colectivamente Exhaustivo).

## Estructura

### Metadatos
```
---
título: [Título del Documento]
fecha: [YYYY-MM-DD]
autor: [Autor o Equipo]
estado: [Borrador/En Revisión/Finalizado]
versión: [X.Y]
fecha_última_verificación_fuentes: [YYYY-MM-DD]
---
```

### Sección de Referencias
Al final de cada documento que contenga datos estadísticos, cifras de mercado o afirmaciones basadas en fuentes externas, incluir una sección de Referencias con el siguiente formato:

```
## Referencias

### [Categoría 1 - ej. Tamaño y Crecimiento del Mercado]
1. [Autor/Organización]. (Año). [Título del documento/informe]. Recuperado de [URL]
   - [Dato clave 1 extraído de esta fuente]
   - [Dato clave 2 extraído de esta fuente]
   - [Dato clave 3 extraído de esta fuente]

### [Categoría 2 - ej. Estadísticas de Usuarios]
1. [Autor/Organización]. (Año). [Título del documento/informe]. Recuperado de [URL]
   - [Dato clave 1 extraído de esta fuente]
   - [Dato clave 2 extraído de esta fuente]

### Fecha de última verificación de fuentes: [YYYY-MM-DD]
```

## Criterios de Verificación (MECE)

### Actualidad
- **Antigüedad máxima**: 1-2 años para datos de mercado y estadísticas
- **Fecha de publicación**: Claramente identificada
- **Versión o edición**: Especificada cuando sea relevante

### Credibilidad
- **Tipo de fuente**: Priorizar fuentes primarias sobre secundarias
- **Autoridad**: Organizaciones reconocidas, investigadores respetados, publicaciones con revisión por pares
- **Metodología**: Transparente y sólida cuando se trate de estudios o encuestas

### Relevancia
- **Pertinencia temática**: Directamente relacionada con el tema tratado
- **Alcance geográfico**: Apropiado para el contexto del proyecto
- **Segmento de mercado**: Específico para la industria o tecnología relevante

### Consistencia
- **Triangulación**: Datos contrastados entre múltiples fuentes cuando sea posible
- **Coherencia interna**: Sin contradicciones entre diferentes partes del documento
- **Coherencia externa**: Alineación con otras fuentes confiables

## Proceso de Verificación

1. **Identificación de afirmaciones clave**: Marcar todas las afirmaciones que requieren respaldo con fuentes
2. **Búsqueda de fuentes primarias**: Localizar la fuente original de cada dato o estadística
3. **Evaluación según criterios**: Aplicar los criterios de verificación a cada fuente
4. **Documentación**: Registrar las fuentes verificadas en la sección de Referencias
5. **Revisión cruzada**: Verificar que todas las afirmaciones clave tengan su correspondiente referencia
6. **Actualización de metadatos**: Incluir la fecha de verificación en los metadatos del documento

## Notas al Pie

Para cifras específicas dentro del texto, utilizar el formato de notas al pie:

```
Según estudios recientes, el 78% de los desarrolladores reporta problemas de calidad con código generado por IA[1].

[1] Stack Overflow. (2024). 2024 Stack Overflow Developer Survey.
```

## Documento Centralizado de Referencias

Mantener actualizado el documento centralizado de referencias (`docs/[tipo]/[nombre]/referencias.md`) con todas las fuentes utilizadas en el proyecto, organizadas por categorías.

## Próxima Revisión

Programar la próxima revisión de fuentes para 3-6 meses después de la fecha de verificación actual.

---

Esta plantilla sigue principios MECE al organizar los criterios de verificación en categorías mutuamente excluyentes y colectivamente exhaustivas, cubriendo todos los aspectos relevantes para garantizar la calidad y fiabilidad de las fuentes utilizadas. 