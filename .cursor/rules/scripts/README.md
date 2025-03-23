# PAELLADOC Scripts

This directory contains all scripts used for managing and generating PAELLADOC documentation and configurations.

## Script Overview

### generate_mdc.js
**Purpose**: Generates MDC (Mutually Exclusive, Collectively Exhaustive) documentation files from templates.
**Usage**: `node generate_mdc.js [project_name] [output_path]`
**Dependencies**: Requires Node.js and access to template files.

### mdc_cleanup.js
**Purpose**: Cleans up and validates MDC files, removing redundancies and ensuring consistent formatting.
**Usage**: `node mdc_cleanup.js [file_path]`
**Dependencies**: Requires Node.js.

### mdc_generation.js
**Purpose**: Core generation logic for MDC files. Usually called by generate_mdc.js.
**Usage**: Not typically called directly. Used as a module by other scripts.
**Dependencies**: Requires Node.js.

## Workflow

The typical workflow for using these scripts is:

1. Initialize a project with PAELLA command
2. Generate MDC files with `generate_mdc.js`
3. Clean up and validate the MDC files with `mdc_cleanup.js`
4. Review and commit the generated files

## Integration with PAELLADOC

These scripts are integrated with the PAELLADOC system and are called automatically when using the PAELLA or CONTINUE commands with the `generate_rules` parameter set to true.

## Development

When modifying these scripts, ensure that:
1. All scripts maintain backward compatibility
2. Error handling is robust
3. Any new dependencies are documented
4. Scripts follow Node.js best practices

# PAELLADOC PDF Generator

Esta herramienta permite generar un PDF a partir de todos los archivos Markdown de una carpeta de documentación, incluyendo cabeceras y pies de página personalizados con información de la empresa, cliente y nivel de confidencialidad.

## Requisitos

Para utilizar el generador de PDF, necesitas:

1. **Python 3** con las siguientes dependencias:
   - pandoc
   - pypandoc
   - markdown
   - pyyaml

2. **Pandoc** (convertidor de documentos universal)

3. **LaTeX** (para generar PDFs con formato completo)
   - Se recomienda BasicTeX (más ligero, ~300MB) o MacTeX (completo, ~4GB)
   - Paquetes LaTeX necesarios: lastpage, fancyhdr, xcolor

## Instalación

El script incluye un instalador de dependencias para facilitar la configuración:

```bash
./install_dependencies.sh
```

Este instalador:
- Crea un entorno virtual de Python
- Instala los paquetes Python requeridos
- Intenta instalar Pandoc a través de Homebrew (si está disponible)
- Ofrece instalar BasicTeX (versión ligera de LaTeX)

## Uso

Para generar un PDF de documentación:

```bash
./generate_docs_pdf.sh
```

El script te solicitará:

1. **Nombre de la empresa**: Aparecerá en la cabecera y portada
2. **Nombre del cliente**: Aparecerá en el pie de página y portada
3. **Nivel de confidencialidad**: [Public/Internal/Confidential/Strictly Confidential]
4. **Ruta de la carpeta de documentación**: Relativa a la raíz del proyecto (por defecto: 'docs')
5. **Nombre del archivo de salida**: (por defecto: [Nombre_Cliente]_Documentation_[Fecha].pdf)

## Características

- Portada personalizada con información de la empresa y cliente
- Índice de contenidos generado automáticamente
- Cabeceras y pies de página profesionales con información relevante
- Detección automática del título de cada documento Markdown
- Gestión adecuada de rutas de imágenes
- Modo de conversión básico si LaTeX no está disponible
- Saltos de página entre documentos
- Numeración de páginas con formato "X de Y"

## Notas

- Si LaTeX no está instalado, el PDF se generará en modo básico sin cabeceras/pies de página personalizados
- La numeración de documentos en el PDF sigue el orden alfabético de los archivos
- Se omiten archivos Markdown que comienzan con "_" o "."

## Solución de problemas

Si encuentra problemas al generar el PDF:

1. **Pandoc o LaTeX no encontrado**:
   - Ejecute `./install_dependencies.sh` para instalar las dependencias necesarias

2. **Error en la generación del PDF**:
   - Verifique que los archivos Markdown no contengan sintaxis incorrecta
   - Asegúrese de que las rutas de las imágenes sean relativas al archivo Markdown

3. **Problemas con caracteres especiales**:
   - Asegúrese de que sus archivos Markdown utilicen codificación UTF-8

4. **Personalización adicional**:
   - Puede modificar las plantillas LaTeX en el script para personalizar aún más el formato 