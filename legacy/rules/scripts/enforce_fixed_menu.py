#!/usr/bin/env python3
"""
PAELLADOC Fixed Menu Enforcer
-----------------------------
This script ensures that the AI chat presents the fixed 19-option menu
in the language selected by the user (Spanish or English)
after repository preparation.

It should be executed immediately after run_generate_doc.py completes.
"""

import sys
import os

FIXED_MENU_SPANISH = """
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

FIXED_MENU_ENGLISH = """
What would you like to document? (You can select multiple options by indicating the numbers, for example: 1, 5, 9)

Technical Documentation:
1.  Technical Architecture
2.  API Documentation
3.  Component Specifications
4.  Database Schema
5.  Dependencies

Product Documentation (Required for Business Documentation):
6.  User Stories
7.  Problem Definition
8.  Value Proposition

User Documentation:
9.  Installation Guide
10. Usage Guide

Developer Documentation:
11. Setup Instructions
12. Contribution Guidelines

Business Documentation (Requires Product Documentation):
13. Market Research
14. Business Model
15. Competitive Analysis

Other Options:
16. All Technical Documentation
17. All Product Documentation
18. Everything
19. I'm Done
"""

CRITICAL_INSTRUCTIONS = """
### CRITICAL AI INSTRUCTIONS ###
1. ALWAYS ASK FOR LANGUAGE CONFIRMATION FIRST
2. WAIT for explicit language confirmation from the user
3. DO NOT SEARCH THE WEB for repository information
4. Give ONE brief paragraph summarizing what the repository appears to be
5. IMMEDIATELY present the FIXED 19-option menu in the confirmed language (Spanish or English)
6. WAIT for user selection
7. DO NOT perform extensive analysis before showing the menu
8. DO NOT propose your own documentation structure
### END CRITICAL INSTRUCTIONS ###
"""

CODE_IS_KING_RULES = """
### CODE IS KING - CRITICAL RULES ###
1. ALL documentation MUST be based SOLELY on the extracted context file
2. The context file is the ONLY source of truth
3. DO NOT infer, guess, or create information not explicitly in the context file
4. If information for a requested section is not in the context file, state this explicitly
5. DO NOT use general knowledge about software, technologies, or frameworks
6. NEVER generate fictitious content when data is missing
7. STRICTLY adhere to "CODE IS KING" - context file is the only source of truth
### END CODE IS KING RULES ###
"""

CONTEXT_FILE_PATH = """
### ABSOLUTELY CRITICAL: USE THIS EXACT FILE PATH ###
THE ONLY SOURCE OF TRUTH IS:
/Users/jlcases/codigo/paelladoc/code_context/extracted/repo_content.txt

1. ALWAYS check this exact file path for EVERY piece of information
2. NEVER rely on memory without consulting the context file again
3. For EACH section of documentation, go back to this file
4. The file at this exact path contains all the information needed
5. DO NOT use any other sources of information
6. If the information isn't in this file, state that clearly
7. NEVER invent content or use general knowledge
### END CONTEXT FILE PATH RULES ###
"""

WORKFLOW_RULES = """
### MENU WORKFLOW AFTER DOCUMENTATION GENERATION ###
1. After generating documentation for a selected option, MARK it as COMPLETED in the menu with a ✓ symbol
2. IMMEDIATELY show the FULL menu AGAIN with completed items marked (e.g., "8. Value Proposition ✓" or "8. Propuesta de Valor ✓")
3. The updated menu must include ALL original options, both completed and remaining
4. This menu re-presentation MUST happen AFTER each documentation section is generated
5. Ask the user if they want to continue with another option from the menu
6. Maintain the EXACT same format as the original menu but add checkmarks to completed items
7. Example of marking a completed item: "8. Value Proposition ✓" or "8. Propuesta de Valor ✓"
### END MENU WORKFLOW RULES ###
"""

OUTPUT_PATH_INSTRUCTIONS = """
### OUTPUT PATH INSTRUCTIONS ###
1. SAVE ALL documentation files in /Users/jlcases/codigo/paelladoc/docs/generated/
2. For each documentation type, create a properly named markdown file:
   - Technical Architecture: architecture.md
   - API Documentation: api.md
   - Component Specifications: components.md
   - Database Schema: database.md
   - Dependencies: dependencies.md
   - User Stories: user_stories.md
   - Problem Definition: problem_definition.md
   - Value Proposition: value_proposition.md
   - Installation Guide: installation.md
   - Usage Guide: usage.md
   - Setup Instructions: setup.md
   - Contribution Guidelines: contribution.md
   - Market Research: market_research.md
   - Business Model: business_model.md
   - Competitive Analysis: competitive_analysis.md
3. Use templates from .cursor/rules/templates as a GUIDE for content structure, but ALWAYS save to docs/generated
4. VERIFY that each file is created in /Users/jlcases/codigo/paelladoc/docs/generated/
### END OUTPUT PATH INSTRUCTIONS ###
"""

TEMPLATE_USAGE_INSTRUCTIONS = """
### TEMPLATE USAGE INSTRUCTIONS ###
1. ALWAYS use the existing template files as GUIDES for your documentation structure
2. DO NOT save files to the template directories - SAVE to /Users/jlcases/codigo/paelladoc/docs/generated/
3. COPY the structure, section headings, and formatting from the templates
4. FILL IN the content under each section heading based ONLY on information from the context file
5. PRESERVE the overall organization and structure of the templates
6. FOLLOW the template's organization and structure precisely 
7. SAVE the filled-in documentation with appropriate filenames in docs/generated directory
8. When a user selects an option, USE the template as a guide, but SAVE to /Users/jlcases/codigo/paelladoc/docs/generated/
9. VERIFY that your generated content follows the template structure
10. SAVE MARKDOWN FILES in docs/generated, don't just display content in the conversation
### END TEMPLATE USAGE INSTRUCTIONS ###
"""

def main():
    """Print the fixed menu and critical instructions."""
    print("\n" + "=" * 80)
    print("PAELLADOC FIXED MENU ENFORCER")
    print("=" * 80)
    
    print("\nThe AI chat MUST use the following fixed menu in SPANISH:")
    print(FIXED_MENU_SPANISH)
    
    print("\nOR the following fixed menu in ENGLISH depending on user's language selection:")
    print(FIXED_MENU_ENGLISH)
    
    print("\nThe AI chat MUST follow these critical instructions:")
    print(CRITICAL_INSTRUCTIONS)
    
    print("\nThe AI chat MUST adhere to these CODE IS KING rules:")
    print(CODE_IS_KING_RULES)
    
    print("\nThe AI MUST use EXCLUSIVELY this specific context file path:")
    print(CONTEXT_FILE_PATH)
    
    print("\nThe AI MUST follow this workflow after documentation generation:")
    print(WORKFLOW_RULES)
    
    print("\nThe AI MUST use the correct output paths for each template type:")
    print(OUTPUT_PATH_INSTRUCTIONS)
    
    print("\nThe AI MUST follow these template usage instructions:")
    print(TEMPLATE_USAGE_INSTRUCTIONS)
    
    print("=" * 80)
    print("END OF FIXED MENU ENFORCER")
    print("=" * 80)
    
    # Create a marker file to indicate the menu has been enforced
    marker_file = os.path.join(os.path.dirname(__file__), ".menu_enforced")
    with open(marker_file, "w") as f:
        f.write("1")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 