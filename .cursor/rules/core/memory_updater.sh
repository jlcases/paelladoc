#!/bin/bash

# memory_updater.sh - Actualización automática de archivos .memory.json para cualquier proyecto PAELLADOC
# Se instala como parte del sistema de hooks de Git
# Versión 2.0 con integración de IA para mantener contexto entre sesiones

# Determinar el directorio raíz del proyecto
PROJECT_ROOT=$(git rev-parse --show-toplevel)

# Buscar archivos .memory.json en el proyecto
find_memory_files() {
    find "$PROJECT_ROOT" -name ".memory.json" -type f
}

# Función para obtener la fecha actual en formato ISO
get_iso_date() {
    date -u '+%Y-%m-%dT%H:%M:%SZ'
}

# Obtener el nombre del proyecto desde el directorio
get_project_name() {
    basename "$PROJECT_ROOT"
}

# Guardar contexto de la conversación actual
update_ai_context() {
    local memory_file="$1"
    local current_date=$(get_iso_date)
    local ymd_date=$(date '+%Y-%m-%d')
    
    # Verificar dependencia de jq
    if ! command -v jq &> /dev/null; then
        echo "AVISO: jq no está instalado. No se puede actualizar el contexto de IA."
        return 1
    fi
    
    # Leer el archivo de memoria actual
    if [ ! -f "$memory_file" ]; then
        echo "ERROR: Archivo de memoria no encontrado: $memory_file"
        return 1
    fi
    
    # Actualizar la fecha de la última sesión
    jq --arg date "$current_date" '
    # Crear estructura ai_context si no existe
    if .ai_context == null then 
        .ai_context = {
            "last_session": $date,
            "conversation_summaries": [],
            "current_focus": "",
            "coding_preferences": {},
            "next_tasks": []
        } 
    else 
        .ai_context.last_session = $date
    end
    ' "$memory_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
    
    # Buscar archivos de Cursor para extraer contexto si existen
    cursor_context_file="$PROJECT_ROOT/.cursor/project_context.json"
    
    # También buscar en la carpeta de documentación del proyecto si existe
    project_name=$(basename "$PROJECT_ROOT")
    docs_context_file="$PROJECT_ROOT/docs/$project_name/project_context.json"
    
    if [ -f "$cursor_context_file" ]; then
        echo "Encontrado archivo de contexto de Cursor: $cursor_context_file"
        # Intentar integrar el contexto de Cursor
        jq -s '.[0].ai_context.cursor_data = .[1] | .[0]' "$memory_file" "$cursor_context_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
    elif [ -f "$docs_context_file" ]; then
        echo "Encontrado archivo de contexto del proyecto: $docs_context_file"
        # Intentar integrar el contexto del proyecto
        jq -s '.[0].ai_context.cursor_data = .[1] | .[0]' "$memory_file" "$docs_context_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
    fi
    
    echo "Contexto de IA actualizado en $memory_file"
    return 0
}

# Extraer información relevante de los mensajes de commit
extract_decisions_from_commits() {
    local memory_file="$1"
    local commit_msg="$2"
    local ymd_date=$(date '+%Y-%m-%d')
    
    # Verificar formato de mensaje que podría contener decisiones
    if echo "$commit_msg" | grep -q -E '(decision|decidido|implemented|refactor|DECISION|REFACTOR)'; then
        # Crear una entrada de decisión basada en el mensaje de commit
        decision=$(echo "$commit_msg" | sed -E 's/^(feat|fix|docs|style|refactor|perf|test|chore)(\([^)]+\))?:\s*//i')
        
        # Extraer motivo si está presente (después de "porque", "due to", etc.)
        rationale=""
        if echo "$commit_msg" | grep -q -E '(porque|debido a|due to|since|as|para)'; then
            rationale=$(echo "$commit_msg" | sed -E 's/^.*?(porque|debido a|due to|since|as|para)\s+//i')
        fi
        
        # Añadir decisión al archivo de memoria
        if [ -n "$decision" ]; then
            jq --arg date "$ymd_date" \
               --arg decision "$decision" \
               --arg rationale "$rationale" \
            '
            # Asegurar que existe key_decisions
            if .key_decisions == null then .key_decisions = [] else . end |
            # Añadir decisión
            .key_decisions += [{
                "date": $date,
                "decision": $decision,
                "rationale": $rationale,
                "ai_extracted": true,
                "source": "commit_message"
            }]
            ' "$memory_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
            
            echo "Decisión extraída del mensaje de commit: $decision"
        fi
    fi
}

# Analizar los archivos modificados para detectar patrones de deuda técnica
analyze_files_for_tech_debt() {
    local memory_file="$1"
    local modified_files="$2"
    local current_date=$(get_iso_date)
    local ymd_date=$(date '+%Y-%m-%d')
    
    # Solo proceder si tenemos jq
    if ! command -v jq &> /dev/null; then
        return 1
    fi
    
    # Patrones que podrían indicar deuda técnica
    # TODO, FIXME, HACK, WORKAROUND, XXX
    for file in $modified_files; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            # Analizar archivos de código
            if [[ $file == *.js || $file == *.ts || $file == *.jsx || $file == *.tsx || $file == *.py || $file == *.rb || $file == *.java || $file == *.c || $file == *.cpp || $file == *.h || $file == *.hpp || $file == *.cs ]]; then
                # Buscar comentarios de deuda técnica
                tech_debt=$(grep -n -E '(TODO|FIXME|HACK|WORKAROUND|XXX|tech[- ]?debt):?' "$PROJECT_ROOT/$file" | head -5)
                
                if [ -n "$tech_debt" ]; then
                    while IFS=: read -r line_num comment; do
                        # Eliminar prefijos comunes de comentarios
                        clean_comment=$(echo "$comment" | sed -E 's/^[[:space:]]*\/\/[[:space:]]*//;s/^[[:space:]]*#[[:space:]]*//;s/^[[:space:]]*\/\*[[:space:]]*//;s/^[[:space:]]*\*[[:space:]]*//')
                        
                        # Determinar prioridad basada en palabras clave
                        priority="medium"
                        if echo "$clean_comment" | grep -q -E '(urgent|critical|high|priority|blocker|ASAP)'; then
                            priority="high"
                        elif echo "$clean_comment" | grep -q -E '(eventually|someday|nice to have|low)'; then
                            priority="low"
                        fi
                        
                        # Añadir entrada de deuda técnica
                        jq --arg desc "[$file:$line_num] $clean_comment" \
                           --arg priority "$priority" \
                           --arg date "$current_date" \
                           --arg file "$file" \
                           --arg line "$line_num" \
                        '
                        # Asegurar que existe technical_debt
                        if .technical_debt == null then .technical_debt = [] else . end |
                        # Añadir deuda técnica
                        .technical_debt += [{
                            "description": $desc,
                            "priority": $priority,
                            "estimated_effort": "unknown",
                            "ai_identified": true,
                            "detected_at": $date,
                            "file": $file,
                            "line": $line
                        }]
                        ' "$memory_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
                        
                        echo "Deuda técnica detectada en $file:$line_num"
                    done <<< "$tech_debt"
                fi
            fi
        fi
    done
}

# Actualizar métricas de calidad desde archivos de cobertura
update_quality_metrics() {
    local memory_file="$1"
    local modified_files="$2"
    
    # Verificar si hay cambios en tests
    if echo "$modified_files" | grep -q "test\|spec"; then
        echo "Detectados cambios en tests, actualizando métricas..."
        
        # Buscar archivos de cobertura en ubicaciones comunes
        coverage_files=(
            "$PROJECT_ROOT/coverage/coverage-summary.json"
            "$PROJECT_ROOT/coverage/lcov-report/coverage-summary.json"
            "$PROJECT_ROOT/jest-coverage/coverage-summary.json"
        )
        
        for cov_file in "${coverage_files[@]}"; do
            if [ -f "$cov_file" ]; then
                if command -v jq &> /dev/null; then
                    # Extraer métricas detalladas de cobertura
                    LINES_PCT=$(jq -r '.total.lines.pct' "$cov_file" 2>/dev/null || echo "")
                    STATEMENTS_PCT=$(jq -r '.total.statements.pct' "$cov_file" 2>/dev/null || echo "")
                    FUNCTIONS_PCT=$(jq -r '.total.functions.pct' "$cov_file" 2>/dev/null || echo "")
                    BRANCHES_PCT=$(jq -r '.total.branches.pct' "$cov_file" 2>/dev/null || echo "")
                    
                    if [ -n "$LINES_PCT" ]; then
                        # Actualizar métricas de calidad
                        jq --argjson lines "$LINES_PCT" \
                           --argjson statements "$STATEMENTS_PCT" \
                           --argjson functions "$FUNCTIONS_PCT" \
                           --argjson branches "$BRANCHES_PCT" \
                        '
                        # Crear estructura de quality_metrics si no existe
                        if .quality_metrics == null then 
                            .quality_metrics = {}
                        else . end |
                        # Actualizar métricas
                        .quality_metrics.test_coverage = $lines |
                        .quality_metrics.coverage_details = {
                            "lines": $lines,
                            "statements": $statements,
                            "functions": $functions,
                            "branches": $branches,
                            "last_updated": "'$(get_iso_date)'"
                        }
                        ' "$memory_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
                        
                        echo "Métricas de cobertura actualizadas desde $cov_file"
                        break
                    fi
                else
                    echo "AVISO: jq no está instalado. No se pueden actualizar métricas detalladas."
                fi
            fi
        done
    fi
}

# Función para actualizar un archivo de memoria específico
update_memory_file() {
    local memory_file="$1"
    local rel_path="${memory_file#$PROJECT_ROOT/}"
    
    echo "Actualizando archivo de memoria: $rel_path"
    
    # Obtener datos necesarios
    ISO_DATE=$(get_iso_date)
    YMD_DATE=$(date '+%Y-%m-%d')
    PROJECT_NAME=$(get_project_name)
    MODIFIED_FILES=$(git diff --name-only --staged)
    COMMIT_MSG=$(git log -1 --pretty=%B 2>/dev/null || echo "WIP")
    COMMIT_TYPE=$(echo "$COMMIT_MSG" | grep -oE '^(feat|fix|docs|style|refactor|perf|test|chore)' || echo "update")
    
    # Verificar dependencia de jq
    if command -v jq &> /dev/null; then
        # Crear estructura de modificaciones
        local modules_json="[]"
        for file in $MODIFIED_FILES; do
            # Extraer tipo de archivo y módulo
            if [[ $file == *.ts || $file == *.js || $file == *.tsx || $file == *.jsx || $file == *.scss || $file == *.css || $file == *.html || $file == *.md ]]; then
                dir=$(dirname "$file")
                basename=$(basename "$file" .ts)
                basename=${basename%.js}
                basename=${basename%.tsx}
                basename=${basename%.jsx}
                basename=${basename%.scss}
                basename=${basename%.css}
                basename=${basename%.html}
                basename=${basename%.md}
                modules_json=$(echo "$modules_json" | jq --arg file "$file" --arg dir "$dir" --arg basename "$basename" '. += [{"file": $file, "dir": $dir, "module": $basename}]')
            fi
        done
        
        # Actualizar archivo .memory.json
        jq --arg date "$ISO_DATE" \
           --arg ymd "$YMD_DATE" \
           --arg commit_type "$COMMIT_TYPE" \
           --arg commit_msg "$COMMIT_MSG" \
           --arg project "$PROJECT_NAME" \
           --argjson modules "$modules_json" \
           '
           # Asegurar que existe project_name
           if .project_name == null then .project_name = $project else . end |
           
           # Actualizar fecha
           .last_updated = $date |
           
           # Crear o actualizar actividad git
           if (.git_activity | not) then .git_activity = [] else . end |
           .git_activity += [{
               "date": $ymd,
               "type": $commit_type,
               "message": $commit_msg,
               "files_count": ($modules | length),
               "files": $modules
           }] |
           
           # Limitar historial git a últimas 20 entradas
           .git_activity = (.git_activity | sort_by(.date) | reverse | .[0:20])
           ' \
           "$memory_file" > "$memory_file.tmp" && mv "$memory_file.tmp" "$memory_file"
        
        # Extraer decisiones del mensaje de commit
        extract_decisions_from_commits "$memory_file" "$COMMIT_MSG"
        
        # Analizar archivos para detectar deuda técnica
        analyze_files_for_tech_debt "$memory_file" "$MODIFIED_FILES"
        
        # Actualizar métricas
        update_quality_metrics "$memory_file" "$MODIFIED_FILES"
        
        # Actualizar contexto de IA
        update_ai_context "$memory_file"
        
        # Añadir el archivo actualizado al commit
        git add "$memory_file"
        
    else
        # Fallback básico sin jq
        echo "AVISO: jq no está instalado. Actualizando solo fecha en $rel_path"
        if [ -f "$memory_file" ]; then
            sed -i.bak "s/\"last_updated\":[[:space:]]*\"[^\"]*\"/\"last_updated\": \"$ISO_DATE\"/" "$memory_file" && rm -f "$memory_file.bak"
            git add "$memory_file"
        fi
    fi
}

# Función principal
main() {
    # Buscar todos los archivos de memoria
    memory_files=$(find_memory_files)
    
    if [ -z "$memory_files" ]; then
        echo "No se encontraron archivos .memory.json en el proyecto."
        return 0
    fi
    
    # Actualizar cada archivo de memoria
    for memory_file in $memory_files; do
        update_memory_file "$memory_file"
    done
    
    echo "Actualización de archivos de memoria completada."
}

# Ejecutar la función principal
main

exit 0 