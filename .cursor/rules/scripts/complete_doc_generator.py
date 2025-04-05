#!/usr/bin/env python3
"""
PAELLADOC Complete Documentation Generator
------------------------------------------
This script implements the full GENERATE_DOC workflow:
1. Clones the repository if needed
2. Extracts code context
3. Forces the AI to read the context file
4. Displays the fixed 19-option menu

Usage:
    python complete_doc_generator.py repo_path language
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path

def ensure_directory_exists(directory):
    """Ensures the specified directory exists."""
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory

def run_generate_doc_script(repo_path, language, output_dir="docs/generated", 
                          context_file="code_context/extracted/repo_content.txt",
                          force_context=False, force_clone=False):
    """Run the repository extraction script."""
    script_path = os.path.join(os.path.dirname(__file__), "run_generate_doc.py")
    
    if not os.path.exists(script_path):
        print(f"Error: Script not found at {script_path}")
        return False
    
    # Prepare the command arguments
    cmd = [
        sys.executable,
        script_path,
        repo_path,
        language,
        "--output", output_dir,
        "--context-output-file", context_file
    ]
    
    if force_context:
        cmd.append("--force-context-regeneration")
    if force_clone:
        cmd.append("--force-clone")
    
    print(f"\nRunning context extraction using {script_path}...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        process = subprocess.run(cmd, check=True, text=True, capture_output=True)
        print(f"Output from run_generate_doc.py:")
        print(process.stdout)
        if process.stderr:
            print(f"Errors/Warnings:")
            print(process.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running generate_doc script: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def run_enforce_menu_script():
    """Run the menu enforcer script."""
    script_path = os.path.join(os.path.dirname(__file__), "enforce_fixed_menu.py")
    
    if not os.path.exists(script_path):
        print(f"Error: Menu enforcer script not found at {script_path}")
        return False
    
    print(f"\nRunning menu enforcer script...")
    try:
        process = subprocess.run(
            [sys.executable, script_path],
            check=True, text=True, capture_output=True
        )
        print(f"Output from enforce_fixed_menu.py:")
        print(process.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running menu enforcer script: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def verify_context_file(context_file):
    """Verify that the context file exists and has content."""
    if not os.path.exists(context_file):
        print(f"Error: Context file not found at {context_file}")
        return False
    
    file_size = os.path.getsize(context_file)
    print(f"Context file exists: {context_file}")
    print(f"Context file size: {file_size} bytes")
    
    if file_size == 0:
        print("Error: Context file is empty")
        return False
    
    # Read the first few lines for verification
    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            first_lines = ''.join([f.readline() for _ in range(5)])
        print(f"First few lines of context file:")
        print(first_lines)
        return True
    except Exception as e:
        print(f"Error reading context file: {e}")
        return False

def create_context_marker(repo_path, context_file):
    """Create a marker file to indicate the context has been prepared."""
    marker_dir = os.path.dirname(context_file)
    ensure_directory_exists(marker_dir)
    
    marker_file = os.path.join(marker_dir, ".context_ready")
    with open(marker_file, 'w', encoding='utf-8') as f:
        f.write(f"Repository: {repo_path}\n")
        f.write(f"Context file: {context_file}\n")
        f.write(f"Prepared at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"Created context marker file: {marker_file}")
    return True

def create_instructions_file(context_file):
    """Create a file with instructions for the AI to read the context."""
    instructions_file = os.path.join(os.path.dirname(context_file), "AI_INSTRUCTIONS.txt")
    
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write("=== CRITICAL INSTRUCTIONS FOR AI ===\n\n")
        f.write(f"1. READ the extracted code context at: {context_file}\n")
        f.write("2. DO NOT search the web for repository information\n")
        f.write("3. Give ONE brief paragraph about the repository based on the context\n")
        f.write("4. IMMEDIATELY show the fixed 19-option menu in Spanish\n")
        f.write("5. Wait for user selection\n\n")
        f.write("=== END CRITICAL INSTRUCTIONS ===\n")
    
    print(f"Created AI instructions file: {instructions_file}")
    return True

def main():
    """Main function to process arguments and run the scripts."""
    parser = argparse.ArgumentParser(description="Complete PAELLADOC documentation generator")
    parser.add_argument("repo_path", help="Path or URL to the repository")
    parser.add_argument("language", help="Output language for documentation (e.g., es, en)")
    parser.add_argument("--output", default="docs/generated", 
                        help="Output directory for generated documentation")
    parser.add_argument("--context-file", default="code_context/extracted/repo_content.txt",
                        help="Path to save the extracted repository context")
    parser.add_argument("--force-context", action="store_true",
                        help="Force regeneration of context file")
    parser.add_argument("--force-clone", action="store_true",
                        help="Force re-cloning of remote repo")
    
    args = parser.parse_args()
    
    print("\n===== PAELLADOC DOCUMENTATION GENERATOR =====")
    print(f"Repository: {args.repo_path}")
    print(f"Language: {args.language}")
    print(f"Output directory: {args.output}")
    print(f"Context file: {args.context_file}")
    print("=============================================\n")
    
    # Step 1: Run the generate_doc script to extract context
    print("\n[STEP 1] Extracting repository content...")
    if not run_generate_doc_script(
        args.repo_path, args.language, args.output, 
        args.context_file, args.force_context, args.force_clone
    ):
        print("Error: Failed to extract repository content. Exiting.")
        sys.exit(1)
    
    # Step 2: Verify the context file was created properly
    print("\n[STEP 2] Verifying context file...")
    if not verify_context_file(args.context_file):
        print("Error: Context file verification failed. Exiting.")
        sys.exit(1)
    
    # Step 3: Create marker and instruction files
    print("\n[STEP 3] Creating marker and instruction files...")
    create_context_marker(args.repo_path, args.context_file)
    create_instructions_file(args.context_file)
    
    # Step 4: Run the menu enforcer script
    print("\n[STEP 4] Enforcing menu presentation...")
    run_enforce_menu_script()
    
    print("\n===== DOCUMENTATION GENERATION READY =====")
    print("Repository content has been extracted.")
    print("AI should now:")
    print("1. Read the extracted context file")
    print("2. Present a brief paragraph about the repository")
    print("3. Show the fixed 19-option menu in Spanish")
    print("=============================================\n")
    
    # Create a prompt with the fixed menu
    spanish_menu = """
¿Qué te gustaría documentar? (Puedes seleccionar múltiples opciones indicando los números, por ejemplo: 1, 5, 9)

Documentación Técnica:
1.  Arquitectura Técnica
2.  Documentación de API
3.  Especificaciones de Componentes
4.  Esquema de Base de Datos
5.  Dependencias

Documentación de Producto (Requerida para Documentación de Negocio):
6.  Historias de Usuario
7.  Definición del Problema
8.  Propuesta de Valor

Documentación para Usuarios:
9.  Guía de Instalación
10. Guía de Uso

Documentación para Desarrolladores:
11. Instrucciones de Configuración
12. Guías de Contribución

Documentación de Negocio (Requiere Documentación de Producto):
13. Investigación de Mercado
14. Modelo de Negocio
15. Análisis Competitivo

Otras Opciones:
16. Toda la Documentación Técnica
17. Toda la Documentación de Producto
18. Todo
19. He Terminado
"""
    print("MENU TO DISPLAY:")
    print(spanish_menu)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 