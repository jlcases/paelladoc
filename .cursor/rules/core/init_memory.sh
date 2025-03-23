#!/bin/bash

# init_memory.sh - Inicializador de memoria para proyectos externos
# Este script crea archivo de memoria y contexto sin instalar hooks de Git
# Útil para proyectos que están en directorios externos a PAELLADOC

# Colores para mensajes
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# Función para mensajes
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Obtener la ruta del directorio de PAELLADOC
PAELLADOC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../../.." && pwd )"
log_info "Directorio de PAELLADOC: $PAELLADOC_DIR"

# Obtener la ruta del directorio objetivo (proyecto de código)
if [ -z "$1" ]; then
    # Si no se proporciona un argumento, usar el directorio actual
    PROJECT_PATH="$(pwd)"
else
    # Usar el directorio proporcionado, convirtiendo a ruta absoluta
    PROJECT_PATH="$(cd "$1" 2>/dev/null && pwd || echo "$1")"
    if [ ! -d "$PROJECT_PATH" ]; then
        log_error "El directorio del proyecto '$1' no existe o no es accesible."
        exit 1
    fi
fi

log_info "Proyecto de código en: $PROJECT_PATH"

# Obtener nombre del proyecto desde el directorio
project_name=$(basename "$PROJECT_PATH")
log_info "Nombre del proyecto: $project_name"

# Directorio de documentación en PAELLADOC (no en el repositorio de código)
DOCS_DIR="$PAELLADOC_DIR/docs/$project_name"
if [ ! -d "$DOCS_DIR" ]; then
    mkdir -p "$DOCS_DIR"
    log_info "Creado directorio para documentación en $DOCS_DIR"
else
    log_info "El directorio para documentación ya existe en $DOCS_DIR"
fi

# Obtener fecha actual en formato ISO 8601
CURRENT_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TODAY=$(date +"%Y-%m-%d")

# Crear archivo de memoria
MEMORY_FILE="$DOCS_DIR/.memory.json"
if [ ! -f "$MEMORY_FILE" ]; then
    # Usar la plantilla de memoria y reemplazar las variables
    TEMPLATE_FILE="$(dirname "$0")/plantilla_memoria.json"
    if [ ! -f "$TEMPLATE_FILE" ]; then
        log_error "No se encuentra el archivo de plantilla de memoria en $TEMPLATE_FILE"
        exit 1
    fi
    
    # Reemplazar variables en la plantilla
    sed -e "s/NOMBRE_PROYECTO/$project_name/g" \
        -e "s|RUTA_PROYECTO|$PROJECT_PATH|g" \
        -e "s/FECHA_ACTUAL/$CURRENT_DATE/g" \
        -e "s/FECHA_HOY/$TODAY/g" \
        "$TEMPLATE_FILE" > "$MEMORY_FILE"
        
    log_info "Archivo .memory.json creado en $MEMORY_FILE usando plantilla"
else
    log_info "El archivo .memory.json ya existe en $MEMORY_FILE"
    
    # Verificar si tiene soporte para AI y ruta del proyecto
    if command -v jq &> /dev/null; then
        if ! jq -e '.ai_context' "$MEMORY_FILE" > /dev/null 2>&1; then
            log_warn "El archivo de memoria no tiene soporte para IA. Se actualizará automáticamente."
            jq '. + {"ai_context": {"last_session": "'$CURRENT_DATE'", "conversation_summaries": [], "current_focus": "", "coding_preferences": {}, "next_tasks": []}}' "$MEMORY_FILE" > "$MEMORY_FILE.tmp" && mv "$MEMORY_FILE.tmp" "$MEMORY_FILE"
            log_info "Actualizado $MEMORY_FILE con soporte para IA"
        fi
        
        # Actualizar la ruta del proyecto si ha cambiado
        current_path=$(jq -r '.project_path // ""' "$MEMORY_FILE")
        if [ "$current_path" != "$PROJECT_PATH" ]; then
            log_info "Actualizando ruta del proyecto en archivo de memoria"
            jq --arg path "$PROJECT_PATH" '.project_path = $path' "$MEMORY_FILE" > "$MEMORY_FILE.tmp" && mv "$MEMORY_FILE.tmp" "$MEMORY_FILE"
        fi
    else
        log_warn "jq no está instalado. No se puede verificar soporte para IA."
    fi
fi

# Crear archivo de contexto
CONTEXT_FILE="$DOCS_DIR/project_context.json"
if [ ! -f "$CONTEXT_FILE" ]; then
    # Usar la plantilla de contexto y reemplazar las variables
    TEMPLATE_FILE="$(dirname "$0")/plantilla_contexto.json"
    if [ ! -f "$TEMPLATE_FILE" ]; then
        log_error "No se encuentra el archivo de plantilla de contexto en $TEMPLATE_FILE"
        exit 1
    fi
    
    # Reemplazar variables en la plantilla
    sed -e "s/NOMBRE_PROYECTO/$project_name/g" \
        -e "s|RUTA_PROYECTO|$PROJECT_PATH|g" \
        -e "s/FECHA_ACTUAL/$CURRENT_DATE/g" \
        -e "s/FECHA_HOY/$TODAY/g" \
        "$TEMPLATE_FILE" > "$CONTEXT_FILE"
        
    log_info "Archivo de contexto de IA creado en $CONTEXT_FILE usando plantilla"
else
    log_info "El archivo de contexto de IA ya existe en $CONTEXT_FILE"
    
    # Actualizar la ruta del proyecto si ha cambiado
    if command -v jq &> /dev/null; then
        current_path=$(jq -r '.project_path // ""' "$CONTEXT_FILE")
        if [ "$current_path" != "$PROJECT_PATH" ]; then
            log_info "Actualizando ruta del proyecto en archivo de contexto"
            jq --arg path "$PROJECT_PATH" '.project_path = $path' "$CONTEXT_FILE" > "$CONTEXT_FILE.tmp" && mv "$CONTEXT_FILE.tmp" "$CONTEXT_FILE"
        fi
    fi
fi

# Limpiar archivos antiguos en el proyecto de código si existen
PROJECT_DOCS_DIR="$PROJECT_PATH/docs/$project_name"
if [ -d "$PROJECT_DOCS_DIR" ]; then
    log_warn "Se encontraron archivos de memoria en el repositorio de código."
    read -p "¿Desea eliminarlos? (s/n): " clean_old_files
    if [[ "$clean_old_files" =~ ^[Ss]$ ]]; then
        if [ -f "$PROJECT_DOCS_DIR/.memory.json" ]; then
            rm "$PROJECT_DOCS_DIR/.memory.json"
            log_info "Eliminado archivo .memory.json del repositorio de código"
        fi
        if [ -f "$PROJECT_DOCS_DIR/project_context.json" ]; then
            rm "$PROJECT_DOCS_DIR/project_context.json"
            log_info "Eliminado archivo project_context.json del repositorio de código"
        fi
        # Si el directorio queda vacío, eliminarlo también
        if [ -z "$(ls -A "$PROJECT_DOCS_DIR")" ]; then
            rmdir "$PROJECT_DOCS_DIR"
            log_info "Eliminado directorio vacío en el repositorio de código"
        fi
    fi
fi

# Sugerir siguiente paso para instalación de hooks
log_info "Memoria inicializada correctamente en $DOCS_DIR"
log_info ""
log_info "Para habilitar la actualización automática de memoria con cada commit, ejecute:"
log_info "bash $(dirname "$0")/git_hook_installer.sh $PROJECT_PATH"
log_info ""
log_info "O use manualmente los comandos CONTEXT, ACHIEVEMENT, ISSUE y DECISION de PAELLADOC"

exit 0 