#!/bin/bash

# PAELLADOC Documentation PDF Generator
# This script converts all Markdown files in a specified directory to a single PDF with headers and footers

# Set terminal colors for better user experience
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print welcome message
echo -e "${BLUE}==================================================================${NC}"
echo -e "${BLUE}           PAELLADOC DOCUMENTATION PDF GENERATOR                  ${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo ""

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if pandoc is installed
if ! command_exists pandoc; then
    echo -e "${RED}Error: pandoc is not installed.${NC}"
    echo -e "Please run: ${YELLOW}.cursor/rules/scripts/install_dependencies.sh${NC}"
    exit 1
fi

# Check if required LaTeX dependencies are installed (required for PDF generation with headers/footers)
if ! command_exists pdflatex; then
    echo -e "${YELLOW}Warning: pdflatex is not installed.${NC}"
    echo -e "For better PDF generation, please run: ${YELLOW}.cursor/rules/scripts/install_dependencies.sh${NC}"
    echo -e "Continuing with basic conversion capabilities..."
    USE_BASIC_CONVERSION=true
else
    USE_BASIC_CONVERSION=false
fi

# Collect information about the document
echo -e "${GREEN}Please provide the following information:${NC}"
read -p "Company name: " COMPANY_NAME
read -p "Client name: " CLIENT_NAME
read -e -p "Confidentiality level [Public/Internal/Confidential/Strictly Confidential]: " CONFIDENTIALITY_LEVEL

# Set default if empty
if [ -z "$CONFIDENTIALITY_LEVEL" ]; then
    CONFIDENTIALITY_LEVEL="Confidential"
fi

# Validate confidentiality level
case "$CONFIDENTIALITY_LEVEL" in
    [Pp]ublic|[Ii]nternal|[Cc]onfidential|[Ss]trictly[[:space:]][Cc]onfidential)
        # Valid confidentiality level
        ;;
    *)
        echo -e "${YELLOW}Warning: Non-standard confidentiality level. Using as provided.${NC}"
        ;;
esac

# Get the directory with Markdown files
read -e -p "Path to documentation directory (relative to project root): " DOCS_DIR

# Set default if empty
if [ -z "$DOCS_DIR" ]; then
    DOCS_DIR="docs"
fi

# Remove trailing slash if present
DOCS_DIR=${DOCS_DIR%/}

# Check if directory exists
if [ ! -d "$DOCS_DIR" ]; then
    echo -e "${RED}Error: Directory '$DOCS_DIR' does not exist.${NC}"
    exit 1
fi

# Generate output filename
CURRENT_DATE=$(date +"%Y-%m-%d")
OUTPUT_FILENAME="${CLIENT_NAME// /_}_Documentation_${CURRENT_DATE}.pdf"
read -e -p "Output filename [$OUTPUT_FILENAME]: " CUSTOM_FILENAME

if [ ! -z "$CUSTOM_FILENAME" ]; then
    OUTPUT_FILENAME="$CUSTOM_FILENAME"
    # Add .pdf extension if not present
    if [[ ! "$OUTPUT_FILENAME" =~ \.pdf$ ]]; then
        OUTPUT_FILENAME="${OUTPUT_FILENAME}.pdf"
    fi
fi

echo -e "${BLUE}Generating PDF...${NC}"

# Create a temporary directory for processing
TMP_DIR=$(mktemp -d)
MERGED_MD="${TMP_DIR}/merged_document.md"

# Add title page content
cat > "${TMP_DIR}/title.md" <<EOF
---
title: "Documentation Package"
author: "${COMPANY_NAME}"
date: "${CURRENT_DATE}"
subtitle: "Prepared for ${CLIENT_NAME}"
---

# Documentation Package

**Prepared by:** ${COMPANY_NAME}  
**For:** ${CLIENT_NAME}  
**Date:** ${CURRENT_DATE}  
**Confidentiality:** ${CONFIDENTIALITY_LEVEL}

---

EOF

# Initialize merged file with title page
cat "${TMP_DIR}/title.md" > "$MERGED_MD"

# Find all markdown files and sort them alphabetically
echo -e "${BLUE}Finding Markdown files in $DOCS_DIR...${NC}"
# Skip files that start with an underscore or dot
MARKDOWN_FILES=$(find "$DOCS_DIR" -type f -name "*.md" -not -path "*/\.*" -not -name "_*" | sort)

FILE_COUNT=$(echo "$MARKDOWN_FILES" | wc -l | xargs)
if [ "$FILE_COUNT" -eq 0 ]; then
    echo -e "${RED}Error: No Markdown files found in '$DOCS_DIR'.${NC}"
    rm -rf "$TMP_DIR"
    exit 1
fi

echo -e "${GREEN}Found $FILE_COUNT Markdown files.${NC}"

# Create a table of contents file
echo -e "\n# Table of Contents\n" > "${TMP_DIR}/toc.md"
TOC_COUNT=1

# Process each markdown file
for file in $MARKDOWN_FILES; do
    filename=$(basename "$file")
    dirname=$(dirname "$file" | sed "s|^${DOCS_DIR}/||")
    title=$(head -n 20 "$file" | grep -E "^#\s+" | head -n 1 | sed 's/^#\s\+//')
    
    # Use filename as title if no title found in the file
    if [ -z "$title" ]; then
        title=$(basename "$file" .md | sed 's/_/ /g' | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')
    fi
    
    # Add to table of contents
    if [ "$dirname" = "$DOCS_DIR" ]; then
        echo "$TOC_COUNT. [$title](#$TOC_COUNT-${title// /-})" >> "${TMP_DIR}/toc.md"
    else
        echo "$TOC_COUNT. [$title ($dirname)](#$TOC_COUNT-${title// /-})" >> "${TMP_DIR}/toc.md"
    fi
    
    # Add section separator and title to the merged file
    echo -e "\n\n# $TOC_COUNT. $title\n" >> "$MERGED_MD"
    
    # Modify image paths to be relative to the directory containing the markdown file
    sed -E 's|\!\[(.*)\]\(([^http].*)\)|\![\1]('"$(dirname "$file")"'/\2)|g' "$file" >> "$MERGED_MD"
    
    # Add a page break
    echo -e "\n\\pagebreak\n" >> "$MERGED_MD"
    
    TOC_COUNT=$((TOC_COUNT + 1))
done

# Add table of contents after the title page
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS sed needs empty string after -i
    sed -i '' "/---/r ${TMP_DIR}/toc.md" "$MERGED_MD"
else
    # Linux sed works without empty string
    sed -i "/---/r ${TMP_DIR}/toc.md" "$MERGED_MD"
fi

# Create LaTeX header with custom header and footer
cat > "${TMP_DIR}/header.tex" <<EOF
\\usepackage{fancyhdr}
\\usepackage{lastpage}
\\usepackage{xcolor}

\\pagestyle{fancy}
\\fancyhf{}
\\renewcommand{\\headrulewidth}{0.4pt}
\\renewcommand{\\footrulewidth}{0.4pt}

\\fancyhead[L]{${COMPANY_NAME}}
\\fancyhead[R]{\\textbf{${CONFIDENTIALITY_LEVEL}}}
\\fancyfoot[L]{For: ${CLIENT_NAME}}
\\fancyfoot[C]{\\thepage\\ of \\pageref{LastPage}}
\\fancyfoot[R]{${CURRENT_DATE}}

\\definecolor{light-gray}{gray}{0.9}
EOF

# Generate PDF with pandoc
SUCCESS=false

if [ "$USE_BASIC_CONVERSION" = true ]; then
    # Try simple conversion without fancy headers
    echo "Attempting basic PDF conversion with pandoc..."
    pandoc "$MERGED_MD" -o "$OUTPUT_FILENAME" \
        --pdf-engine=pdflatex \
        --variable geometry:margin=1in \
        --variable fontsize=11pt \
        --toc
        
    if [ $? -eq 0 ] && [ -f "$OUTPUT_FILENAME" ]; then
        SUCCESS=true
    else
        echo -e "${YELLOW}Basic conversion failed. Trying alternate methods...${NC}"
        # Try using the Python fallback script
        if [ -f ".cursor/rules/scripts/simple_pdf_generator.py" ]; then
            echo "Attempting PDF generation with Python fallback script..."
            python3 .cursor/rules/scripts/simple_pdf_generator.py "$DOCS_DIR" "$OUTPUT_FILENAME" "$COMPANY_NAME" "$CLIENT_NAME" "$CONFIDENTIALITY_LEVEL"
            
            if [ $? -eq 0 ] && [ -f "$OUTPUT_FILENAME" ]; then
                SUCCESS=true
            fi
        fi
    fi
else
    # Try full conversion with headers and footers
    echo "Attempting full PDF conversion with LaTeX headers and footers..."
    pandoc "$MERGED_MD" -o "$OUTPUT_FILENAME" \
        --pdf-engine=pdflatex \
        --include-in-header="${TMP_DIR}/header.tex" \
        --variable geometry:margin=1in \
        --variable fontsize=11pt \
        --toc
        
    if [ $? -eq 0 ] && [ -f "$OUTPUT_FILENAME" ]; then
        SUCCESS=true
    else
        echo -e "${YELLOW}Full conversion failed. Trying basic conversion...${NC}"
        # Try basic conversion
        pandoc "$MERGED_MD" -o "$OUTPUT_FILENAME" \
            --pdf-engine=pdflatex \
            --variable geometry:margin=1in \
            --variable fontsize=11pt \
            --toc
            
        if [ $? -eq 0 ] && [ -f "$OUTPUT_FILENAME" ]; then
            SUCCESS=true
        else 
            echo -e "${YELLOW}Basic conversion failed. Trying alternate methods...${NC}"
            # Try using the Python fallback script
            if [ -f ".cursor/rules/scripts/simple_pdf_generator.py" ]; then
                echo "Attempting PDF generation with Python fallback script..."
                python3 .cursor/rules/scripts/simple_pdf_generator.py "$DOCS_DIR" "$OUTPUT_FILENAME" "$COMPANY_NAME" "$CLIENT_NAME" "$CONFIDENTIALITY_LEVEL"
                
                if [ $? -eq 0 ] && [ -f "$OUTPUT_FILENAME" ]; then
                    SUCCESS=true
                fi
            fi
        fi
    fi
fi

# Check if PDF was generated successfully
if [ "$SUCCESS" = true ] && [ -f "$OUTPUT_FILENAME" ]; then
    echo -e "${GREEN}Success! PDF generated as: ${NC}${YELLOW}$OUTPUT_FILENAME${NC}"
    # Get file size
    if [ -x "$(command -v stat)" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            FILE_SIZE=$(stat -f %z "$OUTPUT_FILENAME" | awk '{ suffix="KMGT"; for(i=0; $1>1024 && i < length(suffix); i++) $1/=1024; print int($1) substr(suffix, i, 1) "B"}')
        else
            # Linux
            FILE_SIZE=$(stat -c %s "$OUTPUT_FILENAME" | awk '{ suffix="KMGT"; for(i=0; $1>1024 && i < length(suffix); i++) $1/=1024; print int($1) substr(suffix, i, 1) "B"}')
        fi
        echo -e "File size: ${FILE_SIZE}"
    fi
    # Clean up temporary files
    rm -rf "$TMP_DIR"
    
    # Open file if on Mac
    if [[ "$OSTYPE" == "darwin"* ]]; then
        read -p "Would you like to open the PDF now? (y/n): " OPEN_PDF
        if [[ "$OPEN_PDF" =~ ^[Yy]$ ]]; then
            open "$OUTPUT_FILENAME"
        fi
    fi
else
    echo -e "${RED}Error: Failed to generate PDF using all available methods.${NC}"
    echo -e "${RED}Please run .cursor/rules/scripts/install_dependencies.sh to install all required dependencies.${NC}"
    # Clean up temporary files
    rm -rf "$TMP_DIR"
    exit 1
fi

exit 0 