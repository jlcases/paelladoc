#!/usr/bin/env python3
"""
PAELLADOC Documentation Generator
---------------------------------
This script integrates the repository analysis with the documentation generation process.
It runs the analyze_repo_context.py script first, and then presents the user with
appropriate documentation options based on the detected project type.

Usage:
    python run_generate_doc.py [context_file_path] [output_dir]
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path

def ensure_directory_exists(directory):
    """Ensures the specified directory exists."""
    os.makedirs(directory, exist_ok=True)
    return directory

def run_repo_analysis(context_file_path):
    """Runs the repository analysis script and returns the results."""
    # Path to the analyzer script
    analyzer_script = os.path.join(os.path.dirname(__file__), "analyze_repo_context.py")
    
    # Output path for analysis
    analysis_dir = ensure_directory_exists("code_context/analyzed")
    analysis_file = os.path.join(analysis_dir, "project_analysis.json")
    
    # Run the analyzer script
    try:
        subprocess.run([
            sys.executable, 
            analyzer_script, 
            context_file_path,
            analysis_file
        ], check=True)
        
        # Read the analysis results
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
        
        return analysis
    except Exception as e:
        print(f"Error running repository analysis: {str(e)}")
        sys.exit(1)

def generate_documentation_menu(analysis, output_dir):
    """Generates the documentation menu based on project analysis."""
    project_type = analysis.get("project_type", "unknown")
    frameworks = analysis.get("frameworks", [])
    languages = analysis.get("languages", [])
    
    # Start interactive documentation generation
    print("\n" + "=" * 60)
    print(f"PAELLADOC - Documentation Generation for {project_type.replace('_', ' ').title()}")
    print("=" * 60)
    
    print("\nProject Analysis Results:")
    print(f"- Project Type: {project_type.replace('_', ' ').title()}")
    print(f"- Languages: {', '.join(languages)}")
    print(f"- Frameworks: {', '.join(frameworks)}")
    print(f"- Dependencies: {len(analysis.get('dependencies', []))}")
    print(f"- Files: {analysis.get('file_count', 0)}")
    
    # Generate documentation options based on project type
    print("\nWhat documentation would you like to generate?")
    
    # Common options for all project types
    options = [
        "1. Technical Architecture",
        "2. Installation Guide",
        "3. Project Structure",
        "4. Development Guide",
        "5. Future Improvements"
    ]
    
    # Add project-specific options
    if project_type == "chrome_extension":
        options.extend([
            "6. Extension Components",
            "7. API Documentation",
            "8. User Guide"
        ])
    elif project_type == "frontend_webapp":
        options.extend([
            "6. UI Components",
            "7. State Management",
            "8. User Guide"
        ])
    elif project_type == "backend_api":
        options.extend([
            "6. API Endpoints",
            "7. Database Schema",
            "8. Authentication System"
        ])
    elif project_type == "mobile_app":
        options.extend([
            "6. Screen Components",
            "7. Navigation System",
            "8. Device Integration"
        ])
    elif project_type == "fullstack_app":
        options.extend([
            "6. Frontend Components",
            "7. Backend API",
            "8. Database Schema"
        ])
    
    # Add product documentation options
    options.extend([
        "9. Business Context",
        "10. User Stories",
        "11. Market Analysis",
        "12. Competitive Analysis",
        "13. Generate ALL Documentation",
        "14. Cancel"
    ])
    
    # Print options
    for option in options:
        print(option)
    
    # Get user selection
    while True:
        try:
            choice = input("\nEnter option number(s) separated by commas: ")
            
            # Check if user wants to cancel
            if choice.strip() == "14":
                print("Documentation generation cancelled.")
                return
            
            # Check if user wants all documentation
            if choice.strip() == "13":
                generate_all_documentation(project_type, frameworks, languages, output_dir)
                return
            
            # Parse user choices
            choices = [int(c.strip()) for c in choice.split(",") if c.strip().isdigit()]
            
            if not choices:
                print("Invalid selection. Please enter valid option numbers.")
                continue
            
            # Generate selected documentation
            generate_selected_documentation(choices, project_type, frameworks, languages, output_dir)
            break
            
        except ValueError:
            print("Invalid input. Please enter valid option numbers.")

def generate_selected_documentation(choices, project_type, frameworks, languages, output_dir):
    """Generates the selected documentation components."""
    # Map of option numbers to documentation types
    option_map = {
        1: "technical_architecture",
        2: "installation_guide",
        3: "project_structure",
        4: "development_guide",
        5: "future_improvements",
        6: "components",
        7: "api_documentation",
        8: "user_guide",
        9: "business_context",
        10: "user_stories",
        11: "market_analysis",
        12: "competitive_analysis"
    }
    
    # Map project-specific option 6-8 based on project type
    if project_type == "chrome_extension":
        option_map[6] = "extension_components"
        option_map[7] = "extension_api"
        option_map[8] = "extension_user_guide"
    elif project_type == "frontend_webapp":
        option_map[6] = "ui_components"
        option_map[7] = "state_management"
        option_map[8] = "webapp_user_guide"
    elif project_type == "backend_api":
        option_map[6] = "api_endpoints"
        option_map[7] = "database_schema"
        option_map[8] = "authentication_system"
    elif project_type == "mobile_app":
        option_map[6] = "screen_components"
        option_map[7] = "navigation_system"
        option_map[8] = "device_integration"
    elif project_type == "fullstack_app":
        option_map[6] = "frontend_components"
        option_map[7] = "backend_api"
        option_map[8] = "database_schema"
    
    # Generate each selected documentation
    for choice in choices:
        if choice in option_map:
            doc_type = option_map[choice]
            print(f"\nGenerating {doc_type.replace('_', ' ').title()} documentation...")
            
            # Generate specific documentation file
            file_name = f"{doc_type.upper()}.md"
            file_path = os.path.join(output_dir, file_name)
            
            generate_documentation_file(doc_type, project_type, frameworks, languages, file_path)
            
            print(f"✓ {doc_type.replace('_', ' ').title()} documentation saved to {file_path}")
    
    # Generate an index file if multiple docs were selected
    if len(choices) > 1:
        generate_index_file(choices, option_map, output_dir)

def generate_all_documentation(project_type, frameworks, languages, output_dir):
    """Generates all documentation components."""
    print("\nGenerating ALL documentation components. This may take a moment...")
    
    # Technical documentation
    tech_docs = ["technical_architecture", "installation_guide", "project_structure", 
                "development_guide", "future_improvements"]
    
    # Project-specific documentation
    if project_type == "chrome_extension":
        tech_docs.extend(["extension_components", "extension_api", "extension_user_guide"])
    elif project_type == "frontend_webapp":
        tech_docs.extend(["ui_components", "state_management", "webapp_user_guide"])
    elif project_type == "backend_api":
        tech_docs.extend(["api_endpoints", "database_schema", "authentication_system"])
    elif project_type == "mobile_app":
        tech_docs.extend(["screen_components", "navigation_system", "device_integration"])
    elif project_type == "fullstack_app":
        tech_docs.extend(["frontend_components", "backend_api", "database_schema"])
    
    # Product documentation
    product_docs = ["business_context", "user_stories", "market_analysis", "competitive_analysis"]
    
    # Generate all technical documentation
    for doc_type in tech_docs:
        print(f"Generating {doc_type.replace('_', ' ').title()}...")
        file_name = f"{doc_type.upper()}.md"
        file_path = os.path.join(output_dir, file_name)
        generate_documentation_file(doc_type, project_type, frameworks, languages, file_path)
    
    # Generate all product documentation
    for doc_type in product_docs:
        print(f"Generating {doc_type.replace('_', ' ').title()}...")
        file_name = f"{doc_type.upper()}.md"
        file_path = os.path.join(output_dir, file_name)
        generate_documentation_file(doc_type, project_type, frameworks, languages, file_path)
    
    # Generate README and index
    generate_readme_file(project_type, frameworks, languages, output_dir)
    generate_index_file(list(range(1, 13)), {}, output_dir)
    
    print("\n✓ All documentation generated successfully!")

def generate_documentation_file(doc_type, project_type, frameworks, languages, file_path):
    """Generates a specific documentation file."""
    # Create example content for each documentation type
    content = f"# {doc_type.replace('_', ' ').title()}\n\n"
    
    # Add specific content based on documentation type
    if doc_type == "technical_architecture":
        content += f"## Overview\n\nThis is a {project_type.replace('_', ' ')} project "
        content += f"built with {', '.join(languages)} "
        if frameworks:
            content += f"using {', '.join(frameworks)} "
        content += ".\n\n"
        
        content += "## Architecture\n\n"
        
        if project_type == "chrome_extension":
            content += "### Extension Components\n\n"
            content += "- **Background Script**: Manages extension state and browser events\n"
            content += "- **Content Scripts**: Interact with web page content\n"
            content += "- **Popup UI**: User interface for the extension\n"
            content += "- **Options Page**: Configuration settings\n\n"
        elif project_type == "frontend_webapp":
            content += "### Application Structure\n\n"
            content += "- **Components**: Reusable UI elements\n"
            content += "- **Pages/Views**: Top-level screen components\n"
            content += "- **State Management**: Data flow and state handling\n"
            content += "- **Services**: API integration and business logic\n\n"
        elif project_type in ["backend_api", "fullstack_app"]:
            content += "### API Structure\n\n"
            content += "- **Routes**: API endpoint definitions\n"
            content += "- **Controllers**: Request handling logic\n"
            content += "- **Models**: Data models and schemas\n"
            content += "- **Middleware**: Request/response processing\n\n"
    
    # Write content to file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_index_file(choices, option_map, output_dir):
    """Generates an index file for all documentation."""
    index_path = os.path.join(output_dir, "INDEX.md")
    
    content = "# Documentation Index\n\n"
    content += "## Table of Contents\n\n"
    
    # If option_map is empty (for "Generate ALL"), create a full index
    if not option_map:
        # Technical documentation
        content += "### Technical Documentation\n\n"
        content += "- [Technical Architecture](TECHNICAL_ARCHITECTURE.md)\n"
        content += "- [Installation Guide](INSTALLATION_GUIDE.md)\n"
        content += "- [Project Structure](PROJECT_STRUCTURE.md)\n"
        content += "- [Development Guide](DEVELOPMENT_GUIDE.md)\n"
        content += "- [Future Improvements](FUTURE_IMPROVEMENTS.md)\n\n"
        
        # Project-specific documentation might vary, so add a generic section
        content += "### Project-Specific Documentation\n\n"
        
        # Try to list files that might exist
        specific_docs = [
            "EXTENSION_COMPONENTS.md", "EXTENSION_API.md", "EXTENSION_USER_GUIDE.md",
            "UI_COMPONENTS.md", "STATE_MANAGEMENT.md", "WEBAPP_USER_GUIDE.md",
            "API_ENDPOINTS.md", "DATABASE_SCHEMA.md", "AUTHENTICATION_SYSTEM.md",
            "SCREEN_COMPONENTS.md", "NAVIGATION_SYSTEM.md", "DEVICE_INTEGRATION.md",
            "FRONTEND_COMPONENTS.md", "BACKEND_API.md"
        ]
        
        for doc in specific_docs:
            if os.path.exists(os.path.join(output_dir, doc)):
                content += f"- [{doc.replace('_', ' ').title().replace('.Md', '')}]({doc})\n"
        
        content += "\n### Product Documentation\n\n"
        content += "- [Business Context](BUSINESS_CONTEXT.md)\n"
        content += "- [User Stories](USER_STORIES.md)\n"
        content += "- [Market Analysis](MARKET_ANALYSIS.md)\n"
        content += "- [Competitive Analysis](COMPETITIVE_ANALYSIS.md)\n"
    else:
        # Add links based on selected options
        for choice in choices:
            if choice in option_map:
                doc_type = option_map[choice]
                file_name = f"{doc_type.upper()}.md"
                link_text = doc_type.replace('_', ' ').title()
                content += f"- [{link_text}]({file_name})\n"
    
    # Write index file
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Documentation index created at {index_path}")

def generate_readme_file(project_type, frameworks, languages, output_dir):
    """Generates a README.md file."""
    readme_path = os.path.join(output_dir, "README.md")
    
    content = f"# {project_type.replace('_', ' ').title()} Documentation\n\n"
    
    content += "## Project Overview\n\n"
    content += f"This is a {project_type.replace('_', ' ')} project "
    content += f"built with {', '.join(languages)} "
    if frameworks:
        content += f"using {', '.join(frameworks)} "
    content += ".\n\n"
    
    content += "## Documentation Contents\n\n"
    content += "This documentation package includes:\n\n"
    content += "- Technical architecture and design documentation\n"
    content += "- Installation and setup instructions\n"
    content += "- Usage guides and examples\n"
    content += "- API references and component specifications\n"
    content += "- Business context and requirements\n\n"
    
    content += "For a complete list of available documentation, see [Index](INDEX.md).\n"
    
    # Write README file
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ README created at {readme_path}")

def main():
    """Main function."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="PAELLADOC Documentation Generator")
    parser.add_argument('--context', default="code_context/extracted/repo_content.txt",
                      help="Path to the repository context file")
    parser.add_argument('--output', default="docs/generated",
                      help="Output directory for generated documentation")
    
    args = parser.parse_args()
    
    # Ensure context file exists
    if not os.path.exists(args.context):
        print(f"Error: Context file not found at {args.context}")
        sys.exit(1)
    
    # Ensure output directory exists
    output_dir = ensure_directory_exists(args.output)
    
    # Run repository analysis
    print(f"Analyzing repository context from {args.context}...")
    analysis = run_repo_analysis(args.context)
    
    # Present documentation options based on analysis
    generate_documentation_menu(analysis, output_dir)

if __name__ == "__main__":
    main() 