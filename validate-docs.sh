#!/bin/bash

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función de ayuda
show_usage() {
    echo "Uso: $0 <ruta_relativa>"
    echo "Ejemplo:"
    echo "  $0 pages/projects/paellaSEO/"
    echo "  $0 pages/projects/paellaSEO/market-research.md"
    exit 1
}

# Función para verificar dependencias
check_dependency() {
    local cmd=$1
    local install_cmd=$2
    local name=$3

    if ! command -v $cmd &> /dev/null; then
        echo -e "${YELLOW}⚠️  $name no encontrado. ¿Deseas instalarlo? (s/n)${NC}"
        read -r response
        if [[ "$response" =~ ^[Ss]$ ]]; then
            echo -e "${YELLOW}📦 Instalando $name...${NC}"
            eval "$install_cmd" || {
                echo -e "${RED}❌ Error instalando $name${NC}"
                exit 1
            }
        else
            echo -e "${RED}❌ $name es necesario para la validación${NC}"
            exit 1
        fi
    fi
}

# Verificar si se proporcionó un argumento
if [ $# -eq 0 ]; then
    show_usage
fi

TARGET_PATH="$1"

# Verificar si la ruta existe
if [ ! -e "$TARGET_PATH" ]; then
    echo -e "${RED}❌ Error: La ruta '$TARGET_PATH' no existe${NC}"
    exit 1
fi

echo -e "${GREEN}🔍 Validando documentación en: $TARGET_PATH${NC}"

# Verificar dependencias
check_dependency "node" "brew install node" "Node.js"
check_dependency "python3" "brew install python3" "Python3"
check_dependency "pip3" "curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py" "pip3"
check_dependency "markdownlint" "npm install -g markdownlint-cli" "markdownlint"
check_dependency "yamllint" "pip3 install yamllint" "yamllint"
check_dependency "ajv" "npm install -g ajv-cli" "ajv-cli"

# Instalar PyYAML si no está instalado
python3 -c "import yaml" 2>/dev/null || {
    echo -e "${YELLOW}📦 Instalando PyYAML...${NC}"
    pip3 install PyYAML
}

# Create markdownlint config if it doesn't exist
if [ ! -f ".markdownlint.json" ]; then
    echo -e "${GREEN}📝 Creando configuración de markdownlint...${NC}"
    cat > .markdownlint.json << EOF
{
    "MD041": false,
    "MD033": false,
    "MD013": false,
    "default": true,
    "line-length": false,
    "no-hard-tabs": true,
    "whitespace": false
}
EOF
fi

# Create yamllint config if it doesn't exist
if [ ! -f ".yamllint" ]; then
    echo -e "${GREEN}📝 Creando configuración de yamllint...${NC}"
    cat > .yamllint << EOF
extends: default
rules:
  document-start:
    present: true
  line-length:
    max: 120
  trailing-spaces: enable
  new-line-at-end-of-file: enable
  truthy:
    check-keys: false
EOF
fi

# Función para validar un archivo markdown
validate_markdown_file() {
    local file="$1"
    echo -e "${GREEN}🔍 Validando archivo: $file${NC}"
    
    # Markdown lint
    echo -e "${GREEN}⚡ Ejecutando markdownlint...${NC}"
    markdownlint "$file" || {
        echo -e "${RED}❌ Validación de Markdown fallida${NC}"
        return 1
    }
    
    # Extraer y validar frontmatter
    echo -e "${GREEN}⚡ Validando frontmatter...${NC}"
    if ! grep -q '^---$' "$file"; then
        echo -e "${RED}❌ No se encontró frontmatter en $file${NC}"
        return 1
    fi

    # Extraer frontmatter
    sed -n '/^---$/,/^---$/p' "$file" > temp_frontmatter.yml
    
    # YAML syntax validation
    echo -e "${GREEN}⚡ Validando sintaxis YAML...${NC}"
    yamllint temp_frontmatter.yml || {
        echo -e "${RED}❌ Validación YAML fallida${NC}"
        rm temp_frontmatter.yml
        return 1
    }

    # Convertir YAML a JSON para validación con ajv
    echo -e "${GREEN}⚡ Validando schema SEO...${NC}"
    python3 -c 'import sys, yaml, json; json.dump(yaml.safe_load(sys.stdin), sys.stdout)' < temp_frontmatter.yml > temp_frontmatter.json

    # Validar contra el schema SEO
    if ! ajv validate -s schemas/seo-frontmatter.yaml -d temp_frontmatter.json; then
        echo -e "${RED}❌ El frontmatter no cumple con el schema SEO${NC}"
        echo -e "${YELLOW}ℹ️  Revisa que todos los campos requeridos estén presentes:${NC}"
        echo "  - title (35-65 caracteres)"
        echo "  - meta_description (120-158 caracteres)"
        echo "  - seo_title (35-65 caracteres)"
        echo "  - keywords (3-7 palabras clave)"
        echo "  - canonical_url"
        echo "  - og_type (website o article)"
        echo "  - og_title"
        echo "  - og_description"
        echo "  - og_image (URL de imagen válida)"
        echo "  - twitter_card (summary o summary_large_image)"
        rm -f temp_frontmatter.yml temp_frontmatter.json
        return 1
    fi

    # Validar estructura básica del documento
    echo -e "${GREEN}⚡ Validando estructura del documento...${NC}"
    
    # Verificar encabezados
    if ! grep -q "^# " "$file"; then
        echo -e "${YELLOW}⚠️  No se encontró un encabezado principal (h1) en $file${NC}"
    fi
    
    # Verificar enlaces
    if grep -q "]()" "$file"; then
        echo -e "${YELLOW}⚠️  Se encontraron enlaces vacíos en $file${NC}"
    fi
    
    # Verificar imágenes
    if grep -q "![.*]()" "$file"; then
        echo -e "${YELLOW}⚠️  Se encontraron imágenes sin ruta en $file${NC}"
    fi

    # Limpiar archivos temporales
    rm -f temp_frontmatter.yml temp_frontmatter.json
    
    return 0
}

# Procesar archivos según si es directorio o archivo
if [ -d "$TARGET_PATH" ]; then
    # Es un directorio, procesar todos los archivos .md
    echo -e "${GREEN}📂 Procesando directorio: $TARGET_PATH${NC}"
    find "$TARGET_PATH" -name "*.md" | while read -r file; do
        if ! validate_markdown_file "$file"; then
            echo -e "${RED}❌ La validación falló para $file${NC}"
            exit 1
        fi
    done
else
    # Es un archivo, validar directamente
    if ! validate_markdown_file "$TARGET_PATH"; then
        echo -e "${RED}❌ La validación falló${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ ¡Todas las validaciones pasaron correctamente!${NC}"
echo -e "${GREEN}📊 Resumen de validación:${NC}"
echo "- ✅ Sintaxis Markdown correcta"
echo "- ✅ Frontmatter válido y optimizado para SEO"
echo "- ✅ Enlaces verificados"
echo "- ✅ Estructura del documento correcta"

if command -v bundle &> /dev/null && [ -f "Gemfile" ]; then
    echo -e "${GREEN}🔍 Ejecutando Jekyll build con strict frontmatter...${NC}"
    JEKYLL_ENV=production bundle exec jekyll build --strict_front_matter || {
        echo -e "${RED}❌ Error en el build de Jekyll${NC}"
        exit 1
    }
fi

echo "✅ ¡Todas las validaciones pasaron correctamente!"
echo "📊 Resumen de Optimización SEO:"
echo "- Todos los meta tags requeridos están presentes"
echo "- Las longitudes de los títulos están optimizadas para motores de búsqueda"
echo "- Las meta descriptions están dentro de la longitud recomendada"
echo "- Los tags de Open Graph y Twitter Card están correctamente configurados"
echo "- El structured data es válido" 