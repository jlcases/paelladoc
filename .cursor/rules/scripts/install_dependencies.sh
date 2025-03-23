#!/bin/bash

# Colors for better output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}==================================================================${NC}"
echo -e "${BLUE}      PAELLADOC PDF GENERATOR DEPENDENCY INSTALLER                ${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${YELLOW}This script is optimized for macOS. Some commands may differ on other systems.${NC}"
fi

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python 3 is installed
if ! command_exists python3; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

# Create virtual environment using built-in venv module
echo -e "${GREEN}Step 1: Setting up Python virtual environment${NC}"
VENV_DIR=".cursor/rules/scripts/venv"

# Create virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    
    if [ ! -d "$VENV_DIR" ]; then
        echo -e "${RED}Failed to create virtual environment. Continuing without it...${NC}"
        USE_VENV=false
    else
        USE_VENV=true
    fi
else
    USE_VENV=true
fi

# Activate virtual environment if it exists
if [ "$USE_VENV" = true ]; then
    echo "Activating virtual environment..."
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
    else
        echo -e "${RED}Activation script not found. Continuing without virtual environment...${NC}"
        USE_VENV=false
    fi
fi

# Install Python dependencies
echo -e "${GREEN}Step 2: Installing Python dependencies${NC}"
if [ "$USE_VENV" = true ]; then
    pip install --upgrade pip
    pip install -r .cursor/rules/scripts/requirements.txt
else
    pip3 install -r .cursor/rules/scripts/requirements.txt
fi

# Check and install Pandoc
echo -e "${GREEN}Step 3: Checking Pandoc installation${NC}"
if ! command_exists pandoc; then
    echo "Pandoc not found. Installing via Homebrew..."
    if ! command_exists brew; then
        echo -e "${RED}Homebrew not found. Please install Homebrew first or install Pandoc manually.${NC}"
        echo -e "Visit https://pandoc.org/installing.html for manual installation instructions."
    else
        brew install pandoc
    fi
else
    echo "Pandoc is already installed."
fi

# Check and install LaTeX
echo -e "${GREEN}Step 4: Checking LaTeX installation${NC}"
if ! command_exists pdflatex; then
    echo "LaTeX not found. Installing BasicTeX (smaller than full MacTeX)..."
    if ! command_exists brew; then
        echo -e "${RED}Homebrew not found. Please install Homebrew first or install LaTeX manually.${NC}"
        echo -e "Visit https://tug.org/mactex/morepackages.html for BasicTeX installation instructions."
    else
        echo -e "${YELLOW}BasicTeX (300MB) will be installed. This is a smaller alternative to MacTeX (4GB+).${NC}"
        echo -e "${YELLOW}If you need more LaTeX packages, you might want to install the full MacTeX instead:${NC}"
        echo -e "${YELLOW}brew install --cask mactex${NC}"
        
        read -p "Proceed with BasicTeX installation? (y/n): " INSTALL_BASICTEX
        if [[ "$INSTALL_BASICTEX" =~ ^[Yy]$ ]]; then
            brew install --cask basictex
            
            # Add BasicTeX to PATH
            echo "Updating PATH to include TeX binaries..."
            if [[ ":$PATH:" != *":/Library/TeX/texbin:"* ]]; then
                echo 'export PATH="$PATH:/Library/TeX/texbin"' >> ~/.zshrc
                export PATH="$PATH:/Library/TeX/texbin"
            fi
            
            # Waiting for TeX installation to complete
            echo "Waiting for TeX installation to finish..."
            sleep 5
            
            # Install additional LaTeX packages needed for the PDF generation
            echo "Installing additional LaTeX packages..."
            if command_exists tlmgr; then
                sudo tlmgr update --self
                sudo tlmgr install lastpage fancyhdr xcolor
            else
                echo -e "${YELLOW}Warning: tlmgr not found. You may need to install these packages manually:${NC}"
                echo -e "- lastpage"
                echo -e "- fancyhdr"
                echo -e "- xcolor"
            fi
        else
            echo -e "${YELLOW}Skipping LaTeX installation. PDF generation will use basic conversion mode.${NC}"
        fi
    fi
else
    echo "LaTeX is already installed."
    
    # Check if necessary packages are installed and install them if needed
    if command_exists tlmgr; then
        echo "Checking for required LaTeX packages..."
        for pkg in lastpage fancyhdr xcolor; do
            if ! kpsewhich ${pkg}.sty >/dev/null 2>&1; then
                echo "Package ${pkg} not found. Installing..."
                sudo tlmgr update --self
                sudo tlmgr install ${pkg}
            fi
        done
    else
        echo -e "${YELLOW}Warning: tlmgr not found. Cannot check for required LaTeX packages.${NC}"
        echo -e "You may need to install these packages manually if they're missing:"
        echo -e "- lastpage"
        echo -e "- fancyhdr"
        echo -e "- xcolor"
    fi
fi

# Create a simple Python script to generate PDF without full dependencies
echo -e "${GREEN}Step 5: Creating fallback PDF generator${NC}"
cat > .cursor/rules/scripts/simple_pdf_generator.py <<EOF
#!/usr/bin/env python3
"""
Simple PDF generator for PAELLADOC that doesn't rely on LaTeX.
Uses WeasyPrint or Markdown2PDF as a fallback.
"""
import os
import sys
import subprocess
import tempfile
import shutil
from datetime import datetime

try:
    import markdown
    has_markdown = True
except ImportError:
    has_markdown = False
    print("Warning: markdown package not installed. Installing...")
    subprocess.call([sys.executable, "-m", "pip", "install", "markdown"])
    import markdown

def find_markdown_files(directory):
    """Find all markdown files in a directory recursively."""
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') and not file.startswith('_') and not file.startswith('.'):
                md_files.append(os.path.join(root, file))
    return sorted(md_files)

def create_pdf_with_pandoc(md_files, output_file, company, client, confidentiality):
    """Attempt to create a PDF using pandoc."""
    if not shutil.which('pandoc'):
        print("Error: pandoc not found. Cannot generate PDF.")
        return False
    
    # Create a temporary markdown file
    with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False) as temp_md:
        # Add title page
        temp_md.write(f"""---
title: "Documentation Package"
author: "{company}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
subtitle: "Prepared for {client}"
---

# Documentation Package

**Prepared by:** {company}  
**For:** {client}  
**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Confidentiality:** {confidentiality}

---

""")
        
        # Add table of contents
        temp_md.write("\n# Table of Contents\n\n")
        
        # Process each markdown file
        for i, file_path in enumerate(md_files, 1):
            with open(file_path, 'r') as md_file:
                content = md_file.read()
            
            # Extract title from content or use filename
            title = file_path.split('/')[-1].replace('.md', '').replace('_', ' ').title()
            first_line = content.split('\n', 1)[0] if content else ''
            if first_line.startswith('# '):
                title = first_line[2:].strip()
            
            # Add to table of contents
            temp_md.write(f"{i}. [{title}](#section-{i})\n")
        
        temp_md.write("\n---\n\n")
        
        # Add content of each file
        for i, file_path in enumerate(md_files, 1):
            with open(file_path, 'r') as md_file:
                content = md_file.read()
            
            # Extract title from content or use filename
            title = file_path.split('/')[-1].replace('.md', '').replace('_', ' ').title()
            first_line = content.split('\n', 1)[0] if content else ''
            if first_line.startswith('# '):
                title = first_line[2:].strip()
                content = content.split('\n', 1)[1] if '\n' in content else ''
            
            # Add section with title
            temp_md.write(f"\n# {i}. {title}<a id='section-{i}'></a>\n\n")
            temp_md.write(content)
            temp_md.write("\n\n---\n\n")
    
    # Try to convert to PDF
    try:
        subprocess.run(['pandoc', temp_md.name, '-o', output_file, '--pdf-engine=pdflatex'], 
                      check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.unlink(temp_md.name)
        return True
    except subprocess.CalledProcessError:
        print("Warning: Error using pandoc with pdflatex. Trying with wkhtmltopdf...")
        try:
            subprocess.run(['pandoc', temp_md.name, '-o', output_file, '--pdf-engine=wkhtmltopdf'], 
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.unlink(temp_md.name)
            return True
        except subprocess.CalledProcessError:
            os.unlink(temp_md.name)
            return False

def main():
    if len(sys.argv) != 5:
        print("Usage: python simple_pdf_generator.py <docs_dir> <output_file> <company> <client> <confidentiality>")
        return
    
    docs_dir = sys.argv[1]
    output_file = sys.argv[2]
    company = sys.argv[3]
    client = sys.argv[4]
    confidentiality = sys.argv[5] if len(sys.argv) > 5 else "Confidential"
    
    if not os.path.isdir(docs_dir):
        print(f"Error: Directory '{docs_dir}' does not exist.")
        return
    
    # Find markdown files
    md_files = find_markdown_files(docs_dir)
    if not md_files:
        print(f"Error: No markdown files found in '{docs_dir}'.")
        return
    
    print(f"Found {len(md_files)} markdown files.")
    
    # Try to create PDF with pandoc
    if create_pdf_with_pandoc(md_files, output_file, company, client, confidentiality):
        print(f"Success! PDF generated as: {output_file}")
    else:
        print("Error: Failed to generate PDF.")

if __name__ == "__main__":
    main()
EOF

chmod +x .cursor/rules/scripts/simple_pdf_generator.py

# Final message
echo -e "${GREEN}==================================================================${NC}"
echo -e "${GREEN}Installation complete!${NC}"
echo -e "You can now run: ${YELLOW}.cursor/rules/scripts/generate_docs_pdf.sh${NC}"
echo -e "${GREEN}==================================================================${NC}"

# Clean up
if [ "$USE_VENV" = true ]; then
    deactivate || true
fi

exit 0 