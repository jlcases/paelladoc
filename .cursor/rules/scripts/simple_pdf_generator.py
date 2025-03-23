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
            print("Warning: Error using wkhtmltopdf. Trying with weasyprint...")
            try:
                # Convert markdown to HTML first
                html_content = markdown.markdown(open(temp_md.name).read())
                html_file = temp_md.name + ".html"
                with open(html_file, 'w') as f:
                    f.write(html_content)
                    
                # Try to use weasyprint if available
                try:
                    from weasyprint import HTML
                    HTML(html_file).write_pdf(output_file)
                    os.unlink(temp_md.name)
                    os.unlink(html_file)
                    return True
                except ImportError:
                    print("Warning: WeasyPrint not installed. Installing...")
                    subprocess.call([sys.executable, "-m", "pip", "install", "weasyprint"])
                    try:
                        from weasyprint import HTML
                        HTML(html_file).write_pdf(output_file)
                        os.unlink(temp_md.name)
                        os.unlink(html_file)
                        return True
                    except:
                        os.unlink(temp_md.name)
                        if os.path.exists(html_file):
                            os.unlink(html_file)
                        return False
            except:
                os.unlink(temp_md.name)
                return False

def main():
    # Corregido: debe aceptar 5 argumentos, pero el último es opcional
    if len(sys.argv) < 5:
        print(f"Error: Insufficient arguments. Got {len(sys.argv)-1}, expected 4-5.")
        print("Usage: python simple_pdf_generator.py <docs_dir> <output_file> <company> <client> [confidentiality]")
        return 1
    
    docs_dir = sys.argv[1]
    output_file = sys.argv[2]
    company = sys.argv[3]
    client = sys.argv[4]
    confidentiality = sys.argv[5] if len(sys.argv) > 5 else "Confidential"
    
    print(f"Parameters received:")
    print(f"  - Docs directory: {docs_dir}")
    print(f"  - Output file: {output_file}")
    print(f"  - Company: {company}")
    print(f"  - Client: {client}")
    print(f"  - Confidentiality: {confidentiality}")
    
    if not os.path.isdir(docs_dir):
        print(f"Error: Directory '{docs_dir}' does not exist.")
        return 1
    
    # Find markdown files
    md_files = find_markdown_files(docs_dir)
    if not md_files:
        print(f"Error: No markdown files found in '{docs_dir}'.")
        return 1
    
    print(f"Found {len(md_files)} markdown files.")
    
    # Try to create PDF with pandoc
    if create_pdf_with_pandoc(md_files, output_file, company, client, confidentiality):
        print(f"Success! PDF generated as: {output_file}")
        return 0
    else:
        print("Error: Failed to generate PDF.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
