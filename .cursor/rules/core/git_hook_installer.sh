#!/bin/bash

# git_hook_installer.sh - Instalador de hooks de Git para proyectos PAELLADOC
# Este script instala los hooks necesarios para el funcionamiento del sistema de memoria
# Versión 2.0 con soporte para integración de IA

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

# Determinar directorio raíz del proyecto
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$PROJECT_ROOT" ]; then
    log_error "No se encontró un repositorio Git. Ejecute este script desde un repositorio Git."
    exit 1
fi

# Ruta al directorio de hooks de Git
GIT_HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
if [ ! -d "$GIT_HOOKS_DIR" ]; then
    log_error "No se encontró el directorio de hooks de Git en $GIT_HOOKS_DIR"
    exit 1
fi

# Ruta al directorio de scripts en PAELLADOC
PAELLADOC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
MEMORY_UPDATER="$PAELLADOC_DIR/core/memory_updater.sh"

if [ ! -f "$MEMORY_UPDATER" ]; then
    log_error "No se encontró el script memory_updater.sh en $MEMORY_UPDATER"
    exit 1
fi

# Ruta para el directorio de Cursor
CURSOR_DIR="$PROJECT_ROOT/.cursor"

# Instalar o actualizar el hook pre-commit
install_pre_commit_hook() {
    local pre_commit_hook="$GIT_HOOKS_DIR/pre-commit"
    local temp_hook="$pre_commit_hook.temp"
    
    # Crear hook llamando al script memory_updater.sh
    cat > "$temp_hook" << EOF
#!/bin/bash

# Pre-commit hook para proyectos PAELLADOC
# Instalado automáticamente por git_hook_installer.sh

# Ejecución del actualizador de memoria
MEMORY_UPDATER="$MEMORY_UPDATER"
if [ -f "\$MEMORY_UPDATER" ]; then
    bash "\$MEMORY_UPDATER"
else
    echo "ERROR: No se encontró el script memory_updater.sh en \$MEMORY_UPDATER"
    exit 1
fi

# Continuar con el flujo normal de pre-commit hooks
EOF

    # Si ya existe un hook pre-commit, añadir su contenido al nuevo
    if [ -f "$pre_commit_hook" ]; then
        log_info "Actualizando hook pre-commit existente..."
        echo -e "\n# Hook pre-commit original\n" >> "$temp_hook"
        cat "$pre_commit_hook" | grep -v "memory_updater.sh" >> "$temp_hook"
    else
        log_info "Creando nuevo hook pre-commit..."
    fi
    
    # Hacer ejecutable e instalar
    chmod +x "$temp_hook"
    mv "$temp_hook" "$pre_commit_hook"
    
    log_info "Hook pre-commit instalado correctamente en $pre_commit_hook"
}

# Instalar estructura para contexto de IA
setup_cursor_ai_context() {
    # Obtener nombre del proyecto
    project_name=$(basename "$PROJECT_ROOT")
    
    # Crear directorio de documentación del proyecto si no existe
    PROJECT_DOCS_DIR="$PROJECT_ROOT/docs/$project_name"
    if [ ! -d "$PROJECT_DOCS_DIR" ]; then
        mkdir -p "$PROJECT_DOCS_DIR"
        log_info "Creado directorio para documentación en $PROJECT_DOCS_DIR"
    fi
    
    # Crear directorio de Cursor si no existe
    if [ ! -d "$CURSOR_DIR" ]; then
        mkdir -p "$CURSOR_DIR"
        log_info "Creado directorio para Cursor en $CURSOR_DIR"
    fi
    
    # Definir ubicaciones para el archivo de contexto
    local cursor_context_file="$CURSOR_DIR/project_context.json"
    local project_context_file="$PROJECT_DOCS_DIR/project_context.json"
    
    # Decidir qué ubicación usar para el contexto
    # Priorizar el directorio del proyecto específico
    local context_file="$project_context_file"
    local context_path_for_gitignore=".cursor/project_context.json docs/$project_name/project_context.json"
    
    # Crear archivo de contexto inicial si no existe
    if [ ! -f "$context_file" ]; then
        cat > "$context_file" << EOF
{
  "project_name": "$project_name",
  "initialized_at": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "last_updated": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "conversation_summaries": [],
  "key_insights": [],
  "current_focus": "",
  "development_context": {
    "methodology": "",
    "current_phase": "",
    "active_tasks": []
  }
}
EOF
        log_info "Creado archivo de contexto de IA en $context_file"
        
        # Si existe en otra ubicación, migrar los datos
        if [ -f "$cursor_context_file" ] && [ "$context_file" != "$cursor_context_file" ]; then
            log_info "Encontrado contexto existente en $cursor_context_file, migrando datos..."
            if command -v jq &> /dev/null; then
                # Combinar datos de ambos contextos
                jq -s '.[0] * .[1]' "$context_file" "$cursor_context_file" > "$context_file.tmp" && mv "$context_file.tmp" "$context_file"
                log_info "Datos de contexto migrados exitosamente"
            else
                log_warn "No se pudo migrar datos del contexto (jq no está instalado)"
                cp "$cursor_context_file" "$context_file"
            fi
        fi
        
        # Añadir archivos de contexto a .gitignore si no están ya
        if [ -f "$PROJECT_ROOT/.gitignore" ]; then
            context_files_ignored=true
            for path in $context_path_for_gitignore; do
                if ! grep -q "^$path" "$PROJECT_ROOT/.gitignore"; then
                    context_files_ignored=false
                    break
                fi
            done
            
            if [ "$context_files_ignored" = false ]; then
                echo -e "\n# Archivos de contexto de IA\n$context_path_for_gitignore" >> "$PROJECT_ROOT/.gitignore"
                log_info "Añadidos archivos de contexto a .gitignore"
            fi
        else
            echo -e "# Archivos de contexto de IA\n$context_path_for_gitignore" > "$PROJECT_ROOT/.gitignore"
            log_info "Creado .gitignore con exclusión de archivos de contexto"
        fi
    else
        log_info "El archivo de contexto de IA ya existe en $context_file"
    fi
}

# Verificar requisitos
check_requirements() {
    # Verificar jq (recomendado pero no obligatorio)
    if ! command -v jq &> /dev/null; then
        log_warn "jq no está instalado. Se recomienda para una funcionalidad completa."
        log_warn "Instale jq con: brew install jq (macOS) o apt-get install jq (Linux)"
    else
        log_info "jq está instalado correctamente."
    fi
    
    # Verificar archivos de memoria
    memory_files=$(find "$PROJECT_ROOT" -name ".memory.json" -type f)
    if [ -z "$memory_files" ]; then
        log_warn "No se encontraron archivos .memory.json en el proyecto."
        
        # Preguntar si desea crear un archivo de memoria
        read -p "¿Desea crear un archivo .memory.json en docs/PROYECTO/.memory.json? (s/n): " create_memory
        if [[ "$create_memory" =~ ^[Ss]$ ]]; then
            # Obtener nombre del proyecto
            project_name=$(basename "$PROJECT_ROOT")
            
            # Crear directorio si no existe
            mkdir -p "$PROJECT_ROOT/docs/$project_name"
            
            # Crear memoria inicial con soporte para integración de IA
            cat > "$PROJECT_ROOT/docs/$project_name/.memory.json" << EOF
{
  "project_name": "$project_name",
  "project_type": "",
  "language": "",
  "created_at": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "last_updated": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "methodology": "",
  "git_workflow": "",
  "progress": {
    "current_phase": "initialization",
    "completed_percentage": 0,
    "completed_stories": [],
    "in_progress_stories": [],
    "pending_stories": []
  },
  "code_structure": {
    "source_directory": "",
    "test_directory": "",
    "main_modules": []
  },
  "git_activity": [],
  "key_decisions": [],
  "technical_debt": [],
  "quality_metrics": {
    "test_coverage": 0,
    "code_duplication": 0
  },
  "ai_context": {
    "last_session": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
    "conversation_summaries": [],
    "current_focus": "",
    "coding_preferences": {},
    "next_tasks": []
  },
  "dependencies": {
    "production": [],
    "development": []
  },
  "next_steps": []
}
EOF
            log_info "Archivo .memory.json creado en docs/$project_name/.memory.json"
        fi
    else
        log_info "Se encontraron $(echo "$memory_files" | wc -l | tr -d ' ') archivos .memory.json:"
        echo "$memory_files" | sed 's|'"$PROJECT_ROOT"'/||g' | sed 's|^|  - |g'
        
        # Verificar si tienen soporte para IA
        for memory_file in $memory_files; do
            if command -v jq &> /dev/null; then
                if ! jq -e '.ai_context' "$memory_file" > /dev/null 2>&1; then
                    log_warn "El archivo $memory_file no tiene soporte para IA. Se actualizará automáticamente."
                    jq '. + {"ai_context": {"last_session": "'$(date -u '+%Y-%m-%dT%H:%M:%SZ')'", "conversation_summaries": [], "current_focus": "", "coding_preferences": {}, "next_tasks": []}}' "$memory_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
                    log_info "Actualizado $memory_file con soporte para IA"
                fi
            fi
        done
    fi
}

# Función principal
main() {
    log_info "Instalando hooks de Git y sistema de IA para proyecto PAELLADOC..."
    
    # Verificar requisitos
    check_requirements
    
    # Instalar hook pre-commit
    install_pre_commit_hook
    
    # Configurar estructura para IA
    setup_cursor_ai_context
    
    log_info "Instalación completada. El sistema de IA y memoria se actualizará automáticamente con cada commit."
    log_info "Para activar la integración completa de IA en Cursor, utilice el comando CONTEXT en sus chats."
}

# Ejecutar la función principal
main

exit 0 