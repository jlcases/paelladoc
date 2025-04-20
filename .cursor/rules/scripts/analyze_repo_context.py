#!/usr/bin/env python3
"""
PAELLADOC Repository Context Analyzer
-------------------------------------
This script analyzes a repository context file (created by extract_repo_content.py)
and extracts project type, technologies, frameworks, and other key information.
It outputs a JSON file with the analysis results that PAELLADOC can use for
documentation generation.

Usage:
    python analyze_repo_context.py [context_file_path] [output_json_path]

    If no paths are provided, it uses:
    - context_file_path: code_context/extracted/repo_content.txt
    - output_json_path: code_context/analyzed/project_analysis.json
"""

import os
import re
import json
import sys
from collections import Counter

# Project types and their detection patterns
PROJECT_TYPES = {
    "chrome_extension": {
        "files": ["manifest.json"],
        "content_patterns": [
            r"\"manifest_version\":\s*[23]",
            r"content_scripts",
            r"background",
            r"browser_action|page_action|action",
            r"chrome\.extension|chrome\.runtime|chrome\.tabs"
        ],
        "directories": ["popup", "content_scripts", "background"]
    },
    "frontend_webapp": {
        "files": ["package.json", "index.html", "webpack.config.js", "vite.config.js"],
        "content_patterns": [
            r"\"react\":|\"vue\":|\"angular\":|\"svelte\":",
            r"\"dependencies\":|\"devDependencies\":",
            r"<html",
            r"<div\s+id=\"root\"|<div\s+id=\"app\"",
            r"ReactDOM\.render|createApp|new Vue|bootstrapApplication"
        ],
        "directories": ["src", "public", "components", "pages", "views"]
    },
    "backend_api": {
        "files": ["package.json", "server.js", "app.js", "requirements.txt", "Gemfile"],
        "content_patterns": [
            r"express\(\)|new Express\(\)|fastify\(\)|new Koa\(\)|Flask\(__name__\)|Django|rails",
            r"app\.listen\(\d+\)|app\.use\(|@app\.route|router\.",
            r"mongodb|mongoose|sequelize|prisma|typeorm|ActiveRecord|SQLAlchemy"
        ],
        "directories": ["routes", "controllers", "models", "api", "middleware"]
    },
    "mobile_app": {
        "files": ["App.js", "app.json", "AndroidManifest.xml", "AppDelegate.swift", "MainActivity.java"],
        "content_patterns": [
            r"react-native|expo|flutter|SwiftUI|UIKit|androidx|android\.os|android\.app",
            r"componentDidMount|useEffect|runApp\(|AppRegistry|UIViewController"
        ],
        "directories": ["android", "ios", "screens", "lib/screens"]
    },
    "fullstack_app": {
        "files": ["package.json", "server.js", "index.html", "webpack.config.js"],
        "content_patterns": [
            r"\"dependencies\":|\"devDependencies\":",
            r"express\(\)|new Express\(\)|fastify\(\)|new Koa\(\)|Flask\(__name__\)|Django|rails",
            r"\"react\":|\"vue\":|\"angular\":|\"svelte\":",
            r"<html",
            r"mongodb|mongoose|sequelize|prisma|typeorm"
        ],
        "directories": ["client", "server", "frontend", "backend", "src/client", "src/server"]
    },
    "library_package": {
        "files": ["package.json", "setup.py", "Cargo.toml", "pom.xml", "build.gradle"],
        "content_patterns": [
            r"\"main\":",
            r"module\.exports|export default|export const|export function",
            r"setuptools\.setup|pip install|cargo build|mvn package",
            r"\"license\":|\"version\":",
            r"\"files\":|\"scripts\":|\"build\":|\"test\":"
        ],
        "directories": ["lib", "dist", "src", "test", "examples"]
    }
}

# Framework detection patterns
FRAMEWORKS = {
    "React": r"react|react-dom|jsx|createRoot|useState|useEffect|React\.Component",
    "Vue": r"vue|createApp|Vue\.|v-if|v-for|v-model|v-on|v-bind|Vue\.component",
    "Angular": r"angular|@Component|@NgModule|@Injectable|templateUrl",
    "Svelte": r"svelte|onMount|onDestroy|createEventDispatcher",
    "Express": r"express\(\)|app\.use\(|app\.get\(|app\.post\(|app\.listen\(",
    "NestJS": r"@Module|@Controller|@Injectable|@Get\(|@Post\(",
    "Django": r"django|urls\.py|views\.py|models\.py|settings\.py",
    "Flask": r"Flask\(__name__\)|@app\.route|flask\.request|flask\.jsonify",
    "React Native": r"react-native|AppRegistry|StyleSheet\.create|useWindowDimensions",
    "Flutter": r"flutter|StatelessWidget|StatefulWidget|BuildContext|MaterialApp",
    "jQuery": r"jQuery|\$\(|\$\.|\.ready\(",
    "Bootstrap": r"bootstrap|navbar-|container-fluid|row-|col-|btn-",
    "Tailwind": r"tailwindcss|bg-|text-|flex|grid-|p-[0-9]|m-[0-9]"
}

# Language detection patterns
LANGUAGES = {
    "JavaScript": r"\.js$|function\s+\w+\s*\(|const\s+\w+\s*=|let\s+\w+\s*=|var\s+\w+\s*=",
    "TypeScript": r"\.ts$|\.tsx$|interface\s+\w+|type\s+\w+|<\w+>|as\s+\w+",
    "Python": r"\.py$|def\s+\w+\s*\(|import\s+\w+|from\s+\w+\s+import",
    "HTML": r"\.html$|<!DOCTYPE html>|<html|<body|<div|<span|<p>",
    "CSS": r"\.css$|\.scss$|\.less$|\.sass$|\{[\s\n]*[\w\-]+:|\@media|\@import",
    "Java": r"\.java$|public\s+class|private\s+\w+|protected\s+\w+|@Override",
    "Ruby": r"\.rb$|def\s+\w+|require\s+['\"]|class\s+\w+\s+<",
    "Swift": r"\.swift$|func\s+\w+|var\s+\w+:|let\s+\w+:|import\s+\w+|class\s+\w+:",
    "Kotlin": r"\.kt$|fun\s+\w+|val\s+\w+|var\s+\w+|data\s+class",
    "Go": r"\.go$|func\s+\w+|package\s+\w+|import\s+\(|type\s+\w+\s+struct",
    "PHP": r"\.php$|<\?php|\$\w+\s*=|function\s+\w+\s*\(|\->\w+"
}

def read_repo_context(file_path):
    """Reads the repository context file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def extract_file_structure(content):
    """Extracts file structure from repo content."""
    files = []
    directories = []
    
    # Extract the repository structure section
    repo_structure_pattern = r"Repository Structure\n.*?\n(.*?)(?:Repository Files|===|$)"
    repo_structure_match = re.search(repo_structure_pattern, content, re.DOTALL)
    
    if repo_structure_match:
        structure_text = repo_structure_match.group(1)
        
        # Process each line in the structure
        for line in structure_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Count leading spaces to determine nesting level
            indent_level = len(line) - len(line.lstrip())
            path = line.strip()
            
            # If line ends with /, it's a directory
            if path.endswith('/'):
                directories.append(path)
            else:
                files.append(path)
    
    # Extract files from "File:" markers in the content
    file_pattern = r"File:\s+(.*?)\n"
    file_matches = re.findall(file_pattern, content)
    files.extend(file_matches)
    
    return {"files": files, "directories": directories}

def detect_project_type(content, file_structure):
    """Detects the project type based on content patterns and file structure."""
    scores = {project_type: 0 for project_type in PROJECT_TYPES}
    
    # Check files
    for project_type, patterns in PROJECT_TYPES.items():
        for file_pattern in patterns["files"]:
            for file in file_structure["files"]:
                if file.endswith(file_pattern):
                    scores[project_type] += 2
        
        # Check directories
        for dir_pattern in patterns["directories"]:
            for directory in file_structure["directories"]:
                if dir_pattern in directory:
                    scores[project_type] += 1
        
        # Check content patterns
        for pattern in patterns["content_patterns"]:
            if re.search(pattern, content, re.IGNORECASE):
                scores[project_type] += 2
    
    # Get the project type with the highest score
    max_score = max(scores.values())
    if max_score == 0:
        return "unknown"
    
    # If there's a tie, prefer more specific project types
    top_types = [pt for pt, score in scores.items() if score == max_score]
    if len(top_types) > 1:
        priority_order = ["chrome_extension", "mobile_app", "backend_api", "frontend_webapp", "library_package", "fullstack_app"]
        for pt in priority_order:
            if pt in top_types:
                return pt
    
    return max(scores, key=scores.get)

def detect_frameworks(content):
    """Detects frameworks used in the project."""
    frameworks = []
    for framework, pattern in FRAMEWORKS.items():
        if re.search(pattern, content, re.IGNORECASE):
            frameworks.append(framework)
    return frameworks

def detect_languages(content, file_structure):
    """Detects programming languages used in the project."""
    languages = []
    
    # Count file extensions
    extensions = []
    for file in file_structure["files"]:
        ext = os.path.splitext(file)[1].lower()
        if ext:
            extensions.append(ext)
    
    extension_counter = Counter(extensions)
    
    # Check language patterns
    for language, pattern in LANGUAGES.items():
        if re.search(pattern, content, re.IGNORECASE):
            languages.append(language)
    
    # Add languages based on file extensions
    if extension_counter.get('.js', 0) > 0 and 'JavaScript' not in languages:
        languages.append('JavaScript')
    if extension_counter.get('.ts', 0) > 0 and 'TypeScript' not in languages:
        languages.append('TypeScript')
    if extension_counter.get('.py', 0) > 0 and 'Python' not in languages:
        languages.append('Python')
    if extension_counter.get('.html', 0) > 0 and 'HTML' not in languages:
        languages.append('HTML')
    if extension_counter.get('.css', 0) > 0 and 'CSS' not in languages:
        languages.append('CSS')
    
    return languages

def extract_dependencies(content):
    """Extracts dependencies from package.json or similar files."""
    dependencies = []
    
    # Look for package.json content
    package_json_pattern = r"File: package\.json.*?\n(.*?)(?:={10,}|$)"
    package_json_match = re.search(package_json_pattern, content, re.DOTALL)
    
    if package_json_match:
        package_json_content = package_json_match.group(1)
        
        # Extract dependencies and devDependencies
        dep_pattern = r"\"dependencies\":\s*\{(.*?)\}"
        dev_dep_pattern = r"\"devDependencies\":\s*\{(.*?)\}"
        
        for pattern in [dep_pattern, dev_dep_pattern]:
            match = re.search(pattern, package_json_content, re.DOTALL)
            if match:
                deps_text = match.group(1)
                # Extract individual dependencies
                deps = re.findall(r"\"([@\w\-\/\.]+)\":\s*\"", deps_text)
                dependencies.extend(deps)
    
    return dependencies

def analyze_repository(context_file_path, output_json_path):
    """Main function to analyze the repository context."""
    # Read repository context
    content = read_repo_context(context_file_path)
    
    # Extract file structure
    file_structure = extract_file_structure(content)
    
    # Detect project type
    project_type = detect_project_type(content, file_structure)
    
    # Detect frameworks
    frameworks = detect_frameworks(content)
    
    # Detect languages
    languages = detect_languages(content, file_structure)
    
    # Extract dependencies
    dependencies = extract_dependencies(content)
    
    # Create analysis result
    analysis = {
        "project_type": project_type,
        "frameworks": frameworks,
        "languages": languages,
        "dependencies": dependencies,
        "file_count": len(file_structure["files"]),
        "directory_count": len(file_structure["directories"])
    }
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    
    # Write analysis to JSON file
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2)
    
    return analysis

def print_analysis_summary(analysis):
    """Prints a summary of the analysis."""
    print("Repository Analysis Complete")
    print("==========================")
    print(f"Project Type: {analysis['project_type']}")
    print(f"Languages: {', '.join(analysis['languages'])}")
    print(f"Frameworks: {', '.join(analysis['frameworks'])}")
    print(f"Dependencies: {len(analysis['dependencies'])}")
    print(f"Files: {analysis['file_count']}")
    print(f"Directories: {analysis['directory_count']}")
    print("==========================")
    print(f"Full analysis saved to: {output_json_path}")

if __name__ == "__main__":
    # Get file paths from command line arguments or use defaults
    if len(sys.argv) > 1:
        context_file_path = sys.argv[1]
    else:
        context_file_path = "code_context/extracted/repo_content.txt"
    
    if len(sys.argv) > 2:
        output_json_path = sys.argv[2]
    else:
        output_json_path = "code_context/analyzed/project_analysis.json"
    
    # Make sure the paths are absolute
    context_file_path = os.path.abspath(context_file_path)
    output_json_path = os.path.abspath(output_json_path)
    
    # Run analysis
    try:
        analysis = analyze_repository(context_file_path, output_json_path)
        print_analysis_summary(analysis)
    except Exception as e:
        print(f"Error analyzing repository: {str(e)}")
        sys.exit(1) 