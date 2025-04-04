# 🥘 PAELLADOC: The development exoskeleton

![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Cursor](https://img.shields.io/badge/cursor-0.47+-green.svg)
![Compatibility](https://img.shields.io/badge/compatibility-cursor%200.47+-orange.svg)
![Updated](https://img.shields.io/badge/updated-2025--03--23-brightgreen.svg)
[![GitHub Stars](https://img.shields.io/github/stars/jlcases/paelladoc?style=social)](https://github.com/jlcases/paelladoc)
[![GitHub Forks](https://img.shields.io/github/forks/jlcases/paelladoc?style=social)](https://github.com/jlcases/paelladoc/fork)
[![X Community](https://img.shields.io/badge/X%20Community-PAellaDOC-blue)](https://x.com/i/communities/1907494161458090406)

![image](https://github.com/user-attachments/assets/7abbd46b-1cbe-4e19-a5ec-e19c9a5ed791)


## 👥 Join the PAellaDOC Team

**I'm actively seeking contributors to help evolve PAellaDOC from concept to industry standard!**

Whether you're a:
- 🧠 Product manager with methodology insights
- 💻 Developer wanting to enhance the framework architecture
- 📝 Technical writer with documentation expertise
- 🎨 UX designer who can improve template systems
- 🛠️ DevOps engineer to streamline implementation workflows

**How to join:**
1. Join our X Community: [PAellaDOC Community](https://x.com/i/communities/1907494161458090406)
2. Star and fork the repository
3. Check the open issues or propose new improvements
4. Submit pull requests with your contributions

**Current priorities:**
- Template system expansion
- Rules architecture refinement
- New command implementations
- Real-world case studies and examples

No contribution is too small - from fixing typos to implementing major features, all help is appreciated and acknowledged!

As we build this together, we're creating the definitive standard for AI-assisted development documentation.

## 🎯 The Art of Documentation in the AI Era

Just as a master chef knows that the secret to a perfect paella lies in the quality of its ingredients and the order of preparation, PAELLADOC builds on a fundamental truth: **90% of success in AI programming depends on context**.

### 🧠 Why Context is Crucial?

- **AI is powerful, but needs direction**: Like an expert chef, it needs to know exactly what we want to achieve
- **Traditional documentation is scattered**: Like ingredients scattered in the kitchen
- **We waste time repeating context**: Like explaining the recipe over and over
- **Without proper context, we get generic answers**: Like a flavorless paella

### 🥘 The PAELLADOC Solution

Following the MECE principle (Mutually Exclusive, Collectively Exhaustive), we organize documentation with a modular architecture:

```
paelladoc/
├── .cursor/
│   └── rules/
│       ├── orchestrator/        # Central orchestrator definition
│       │   └── paelladoc.mdc    # Defines all commands and delegates to modules
│       ├── commands/            # Command definitions by category
│       │   ├── core/            # Core system commands (help, verification)
│       │   ├── memory/          # Project memory interaction commands
│       │   ├── code/            # Code analysis and generation commands
│       │   ├── styles/          # Coding style and Git workflow commands
│       │   ├── product/         # Product/Project management commands
│       │   └── templates/       # Documentation template management commands
│       ├── modules/             # Core functional implementations
│       │   ├── code_analysis/   # Logic for code analysis and doc generation
│       │   ├── memory_management/ # Logic for handling project memory
│       │   └── conversation/    # Logic for managing conversation flows
│       ├── scripts/             # Utility and executable scripts
│       ├── config/              # System-wide configuration files
│       └── docs/                # System documentation and guides
├── code_context/                # Processed repository content
│   ├── extracted/               # Repositories extracted as text
│   └── generated/               # Generated documentation
├── docs/                        # Generated documentation
└── .memory.json                 # Project memory store
```

### 🍳 Simple Usage

Just type one of our comprehensive commands:
```bash
PAELLA [project_name]           # Initialize new documentation
CONTINUE [project_name]         # Continue with existing documentation
GENERATE_CONTEXT repo_path=path # Extract repository context
GENERATE_DOC [options]          # Generate documentation from context
GENERATE_CODE [project_name]    # Generate code from documentation
STORY operation="create" [args] # Manage user stories
SPRINT operation="plan" [args]  # Plan and manage sprints
MEETING operation="create" [args] # Record meeting notes
```

### 🤖 Interactive Documentation Process

Like a well-trained chef, PAELLADOC will:
- Start by establishing clear communication in your preferred language
- Guide you through project documentation with relevant questions
- Research market trends and technical standards
- Generate comprehensive documentation
- Allow management of the entire product lifecycle

### 🌟 Key Features

1. **MECE Architecture**
   - **Orchestrator**: Central command hub with well-defined interfaces
   - **Commands**: Categorized by function (core, memory, code, styles, product, templates)
   - **Modules**: Implementation logic separated from command interfaces
   - **Centralized Configuration**: Clearly located configuration files
   - **Comprehensive Documentation**: Self-documenting system structure

2. **MECE System for Perfect Context**
   - Mutually Exclusive: Each piece of context has its place
   - Collectively Exhaustive: Nothing important is left out
   - Adaptable: Context level adjusts to the need

3. **End-to-End Product Development**
   - Documentation creation and maintenance
   - Product management with user stories and sprints
   - Meeting and decision tracking
   - Code generation from documentation
   - Repository creation and management

4. **Comprehensive Git Workflows**
   - GitHub Flow for simple projects
   - GitFlow for structured development
   - Trunk-Based Development for continuous delivery
   - Custom workflow options

5. **Programming Style Guidelines**
   - Frontend development with React
   - Backend development with Node.js
   - Chrome extension development
   - Test-Driven Development methodology

6. **Product Management Suite**
   - User story management
   - Sprint planning and reporting
   - Meeting notes with action items
   - Project status reporting
   - Task management and tracking

7. **Code Generation**
   - Generate code from documentation
   - Create repositories for generated code
   - Multiple language and framework support
   - Test generation and quality assurance
   
8. **Enhanced Conversation Workflows**
   - Structured conversation flows
   - Configurable interaction patterns
   - Intelligent context gathering
   - Dynamic question sequences

9. **Repository Analysis and Documentation**
   - Extract repository context with GENERATE_CONTEXT
   - Generate comprehensive documentation with GENERATE_DOC
   - Interactive documentation workflow
   - Multiple documentation templates

## 🚀 Getting Started

1. **Clone or Fork**: Clone the repository or fork it to your GitHub account
2. **Open with Cursor**: Open the project with Cursor 0.47 or higher
3. **Start Cooking**: Simply type `PAELLA` and follow the interactive conversation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# PAELLADOC - Intelligent Documentation System

PAELLADOC is a documentation system that uses AI to analyze code repositories and generate comprehensive technical documentation.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Access to terminal/command line
- Cursor 0.47+ (AI-powered IDE)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/paelladoc.git
   cd paelladoc
   ```

2. Create a virtual environment:
   ```bash
   # On macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   
   # On Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Using GENERATE_CONTEXT and GENERATE_DOC

The documentation generation process has two main steps:

1. **Extract repository context**:
   ```
   GENERATE_CONTEXT repo_path=/path/to/repository
   ```

2. **Generate documentation**:
   ```
   GENERATE_DOC repo_path=/path/to/repository
   ```

### Parameters for GENERATE_CONTEXT

- `repo_path`: Path to the repository you want to process (required)
- `output`: Path where to save the extracted content (optional)
- `line_numbers`: Whether to include line numbers (optional)
- `style`: Output format - plain or xml (optional)
- `ignore`: Additional patterns to ignore (optional)

### Parameters for GENERATE_DOC

- `repo_path`: Path to the repository you want to document (optional if context exists)
- `context_path`: Path to the context directory (optional)
- `output`: Path where to save the documentation (optional)
- `template`: Documentation template to use (optional)

### Examples

```
# Extract repository context
GENERATE_CONTEXT repo_path=~/projects/my-api

# Generate documentation
GENERATE_DOC repo_path=~/projects/my-api template=api-docs output=~/documentation/my-api
```

## Code Analysis Process

PAELLADOC uses a multi-step process to generate documentation:

1. **Content Extraction**: Extracts all source code from the repository
2. **Context Generation**: Converts code into an optimized text format
3. **Code Analysis**: Analyzes architecture patterns, APIs, and database schemas
4. **Interactive Documentation**: Creates comprehensive documentation with user input

## Directory Structure

```
paelladoc/
├── .cursor/rules/              # MECE-structured system rules
│   ├── orchestrator/           # Central command definitions
│   ├── commands/               # Categorized command implementations 
│   ├── modules/                # Core functional modules
│   ├── config/                 # System configuration
│   ├── scripts/                # Utility scripts
│   └── docs/                   # System documentation
├── code_context/               # Processed repository content
│   ├── extracted/              # Repositories extracted as text
│   └── generated/              # Generated documentation
├── docs/                       # Project documentation
└── README.md                   # This file
```

For more detailed information about the system architecture, see `.cursor/rules/docs/README.md`.
