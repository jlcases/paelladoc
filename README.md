# 🧠 PAELLADOC: The AI-First Development Framework

![Version](https://img.shields.io/badge/version-0.3.1-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Philosophy](https://img.shields.io/badge/philosophy-AI--First-purple.svg)
![MCP](https://img.shields.io/badge/type-MCP-orange.svg)
![Updated](https://img.shields.io/badge/updated-2025--04--20-brightgreen.svg)
[![GitHub Stars](https://img.shields.io/github/stars/jlcases/paelladoc?style=social)](https://github.com/jlcases/paelladoc)
[![X Community](https://img.shields.io/badge/X%20Community-PAellaDOC-blue)](https://x.com/i/communities/1907494161458090406)

> **Version 0.3.3**: This release focuses on fixing dependency issues for PyPI packaging and improving configuration documentation for the Model Context Protocol (MCP).

> "In the AI era, context isn't supplementary to code—it's the primary creation."

PAELLADOC is an **AI-First Development framework** that implements the [5 Philosophical Principles of AI-First Development](https://paelladoc.com/blog/ai-first-development-principles/), transforming how we create software in the age of AI.

## 🎯 PAELLADOC and the Model Context Protocol (MCP)

PAELLADOC implements Anthropic's **Model Context Protocol (MCP)** ([see Anthropic's news](https://www.anthropic.com/news/model-context-protocol)). This protocol provides a structured way for Large Language Models (LLMs) to interact with external tools and context, enabling more sophisticated capabilities.

By implementing MCP, PAELLADOC allows LLMs to leverage its specific AI-First development tools and workflows directly through this standard. This approach facilitates functionalities similar to **Tool Use** or **Function Calling** seen in other platforms, but specifically utilizes the Anthropic MCP standard for interaction.

## 🎯 The AI-First Philosophy

Traditional development treats documentation as an afterthought. AI-First Development inverts this paradigm:
- Context becomes the primary artifact
- Code becomes its manifestation
- Knowledge evolves alongside systems
- Decisions preserve their philosophical context
- Human-AI collaboration is seamless

## 🧠 The Five Principles in Action

### 1. Context as Primary Creation
```python
# Traditional Way
write_code() -> document()

# PAELLADOC Way
create_context() -> manifest_as_code()
```
- Every artifact has a UUID for perfect traceability
- Context is versioned alongside code
- Knowledge graphs capture relationships
- Intent is preserved at every step

### 2. Intent-Driven Architecture
```mermaid
graph TD
    A[Business Intent] --> B[Context Creation]
    B --> C[Architecture Manifestation]
    C --> D[Code Generation]
    D --> E[Living Documentation]
```
- Architecture flows from intent, not implementation
- Every decision captures its philosophical context
- Systems adapt to evolving purpose

### 3. Knowledge as Living Entity
```bash
# Knowledge evolves with your system
paella continue my-project
```
- Project memory tracks evolution of understanding
- Documentation updates automatically with changes
- Context remains fresh and relevant
- Knowledge graphs show relationships

### 4. Human-AI Collaborative Consciousness
```python
# Not just code generation, but true collaboration
with paelladoc.context() as ctx:
    ctx.understand_intent()
    ctx.propose_solutions()
    ctx.implement_with_human()
```
- Natural language conversations
- Intent preservation
- Contextual awareness
- Seamless collaboration

### 5. Contextual Decision Architecture
```yaml
decision:
  id: uuid-123
  intent: "Why we chose this path"
  context: "What we knew at the time"
  alternatives: "What we considered"
  implications: "Future impact"
```
- Every decision preserves its context
- Future developers understand the "why"
- Changes respect historical context
- Intent remains clear

## 🚀 Installation & Integration

![Installation Demo](assets/paelladoc-demo.gif)

PAELLADOC is a Python application and should be installed in its own **dedicated Python virtual environment**. This keeps its dependencies separate and avoids conflicts. You'll need *one* PAELLADOC environment, regardless of how many different projects (Python, JS, Ruby, etc.) you plan to document.

*(Requires Python 3.12 or later)*

### 1. Create and Activate the Dedicated Environment

First, choose a permanent location for this environment. Your home directory is often a good choice.

```bash
# Navigate to where you want to store the environment (e.g., your home directory)
# cd ~  # Uncomment and run if you want it in your home directory

# Create the virtual environment (using python3.12 or your installed 3.12+ version)
# We'll name the folder '.paelladoc_venv' (starting with a dot makes it hidden)
python3.12 -m venv .paelladoc_venv

# Activate the environment 
# (The command depends on your shell. Use ONE of the following)

# For Bash/Zsh:
source .paelladoc_venv/bin/activate

# For Fish:
# source .paelladoc_venv/bin/activate.fish

# For Powershell (Windows):
# .\.paelladoc_venv\Scripts\activate.ps1 
```
*(You should see `(.paelladoc_venv)` at the beginning of your terminal prompt now)*

### 2. Install PAELLADOC in the Activated Environment

```bash
# Make sure your (.paelladoc_venv) prompt is visible before running pip
pip install paelladoc
```

### 3. Configure Database Path

PAELLADOC needs to know where to store its memory database (`memory.db`). There are two main ways to configure this:

**Option 1: Environment Variable (Less Reliable for LLM Integration)**

You can set the `PAELLADOC_DB_PATH` environment variable. This works well if you run PAELLADOC directly from your terminal.

```bash
# Example: Set the variable in your current terminal session
export PAELLADOC_DB_PATH="$HOME/.paelladoc/memory.db"

# Optional: Add the export line to your shell's startup file 
# (.bashrc, .zshrc, etc.) for it to persist across sessions.
```

*Important:* When PAELLADOC is run by an LLM tool (like Cursor via MCP), it might not inherit environment variables set this way. Therefore, this method is **less reliable** for LLM integration.

**Option 2: MCP Configuration (Recommended for LLM Integration)**

The most reliable way to ensure your LLM tool uses the correct database path is to configure it directly within the tool's MCP JSON file (`.cursor/mcp.json` for Cursor). This injects the variable directly into the server process launched by the LLM.

See the examples in the next section.

### 4. Configure Your LLM (MCP Setup)

Now, tell your LLM tool (like Cursor) how to find and run PAELLADOC.

**Key Information Needed:**

*   **Full Path to Python Executable:** Absolute path to `python` inside your `.paelladoc_venv`.

#### Cursor IDE Example

Edit your `.cursor/mcp.json` file. This is the **minimum required configuration**:

```json
{
  "mcpServers": {
    "Paelladoc": {
      "command": "/absolute/path/to/.paelladoc_venv/bin/python", 
      "args": [
        "-m",
        "paelladoc.ports.input.mcp_server_adapter",
        "--stdio"
      ],
      "disabled": false
    }
  },
  "mcp.timeout": 120000
}
```

**Important Notes:**

- The `command` path **must** be the absolute path to the Python executable created in Step 1 (e.g., `/Users/your_username/.paelladoc_venv/bin/python`). This is the only strictly required configuration.
- By default, PAELLADOC will use `~/.paelladoc/memory.db` for its database. If you need a custom location, you must add an `"env"` section inside the `"Paelladoc": { ... }` block, like this:
  ```