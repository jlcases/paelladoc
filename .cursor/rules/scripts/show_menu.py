#!/usr/bin/env python3
"""
PAELLADOC Menu Display
---------------------
This script simply displays the fixed 19-option menu in Spanish
that the AI MUST show after repository extraction.
"""

import sys
import os
import argparse

SPANISH_MENU = """
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

FIXED_INSTRUCTIONS = """
=== CRITICAL INSTRUCTIONS FOR AI ===

1. ALWAYS ASK FOR LANGUAGE CONFIRMATION FIRST
2. WAIT for explicit language confirmation from the user
3. ONLY THEN read the extracted context file (not search the web)
4. The AI MUST give ONE brief paragraph about the repository based on context
5. The AI MUST IMMEDIATELY show the fixed 19-option menu in Spanish shown above
6. The AI MUST wait for user selection before proceeding
7. The AI MUST NOT perform extensive analysis before showing the menu
8. The AI MUST NOT propose its own documentation structure

=== END CRITICAL INSTRUCTIONS ===
"""

CODE_IS_KING_RULES = """
=== CODE IS KING - CRITICAL RULES ===

1. ALL documentation MUST be based SOLELY on the extracted context file
2. The context file is the ONLY source of truth
3. DO NOT infer, guess, or create information not explicitly in the context file
4. If information for a requested section is not in the context file, state this explicitly
5. DO NOT use general knowledge about software, technologies, or frameworks
6. NEVER generate fictitious content when data is missing
7. STRICTLY adhere to "CODE IS KING" - context file is the only source of truth

=== END CODE IS KING RULES ===
"""

CONTEXT_FILE_RULES = """
=== ABSOLUTELY CRITICAL: USE THIS EXACT FILE ===

THE ONLY SOURCE OF TRUTH IS:
/Users/jlcases/codigo/paelladoc/code_context/extracted/repo_content.txt

1. ALWAYS check this exact file path for EVERY piece of information
2. NEVER rely on memory without consulting the context file again
3. For EACH section of documentation, go back to this file
4. The file at this exact path contains all the information needed
5. DO NOT use any other sources of information
6. If the information isn't in this file, state that clearly
7. NEVER invent content or use general knowledge

=== END CONTEXT FILE RULES ===
"""

MENU_WORKFLOW_RULES = """
=== MENU WORKFLOW AFTER DOCUMENTATION ===

1. After generating documentation for a selected option, MARK it as COMPLETED in the menu with a ✓ symbol
2. IMMEDIATELY show the FULL menu AGAIN with completed items marked (e.g., "8. Propuesta de Valor ✓")
3. The menu must include ALL original options, both completed and remaining
4. This menu re-presentation MUST happen AFTER each documentation section is generated
5. Ask the user if they want to continue with another option from the menu
6. Maintain the EXACT same format as the original menu but add checkmarks to completed items
7. Example of how to mark a completed item: "8. Propuesta de Valor ✓"

=== END MENU WORKFLOW RULES ===
"""

def main():
    """Display the fixed menu with instructions."""
    parser = argparse.ArgumentParser(description="PAELLADOC Menu Display")
    parser.add_argument("--context-file", default="code_context/extracted/repo_content.txt",
                      help="Path to the extracted context file (for reference)")
    
    args = parser.parse_args()
    
    # Check if context file exists
    context_exists = os.path.exists(args.context_file)
    
    print("\n" + "=" * 80)
    print("PAELLADOC FIXED MENU DISPLAY")
    print("=" * 80)
    
    if context_exists:
        print(f"\nContext file exists at: {args.context_file}")
        print(f"File size: {os.path.getsize(args.context_file)} bytes")
    else:
        print(f"\nWarning: Context file not found at {args.context_file}")
        print("The AI should still show the menu but may have limited repository information.")
    
    print("\nThe AI MUST display this EXACT menu in Spanish:")
    print("-" * 80)
    print(SPANISH_MENU)
    print("-" * 80)
    
    print(FIXED_INSTRUCTIONS)
    
    print("\nThe AI MUST adhere to these CODE IS KING rules:")
    print(CODE_IS_KING_RULES)
    
    print("\nThe AI MUST use EXCLUSIVELY this specific context file:")
    print(CONTEXT_FILE_RULES)
    
    print("\nThe AI MUST follow this workflow after generating documentation:")
    print(MENU_WORKFLOW_RULES)
    
    print("=" * 80)
    print("END OF FIXED MENU DISPLAY")
    print("=" * 80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 