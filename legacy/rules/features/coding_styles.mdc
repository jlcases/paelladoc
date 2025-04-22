---
description: When user asks about coding styles, standards, or uses the CODING_STYLE command, manage the application and customization of style guides
globs: 
alwaysApply: false
---

# Coding Styles

## Commands

### CODING_STYLE
Manages programming style guides for the project

#### Arguments:
- `operation` (string, required): Style operation to perform. Options: "apply", "customize", "list", "show"
- `style_name` (string, required): Name of the style. Options: "frontend", "backend", "chrome_extension", "tdd", "github_workflow"
- `project_name` (string, required): Name of the project to apply style to
- `customizations` (string): Path to customization file or inline JSON customizations

## Available Coding Styles

PAELLADOC provides several coding style templates that can be applied to projects:

### Frontend Technologies
- **React**: Modern functional components, hooks, and state management
- **Vue**: Component structure, Composition API, and Vue best practices
- **Angular**: Module organization, services, and Angular patterns

### Backend Technologies
- **Node.js**: Express structure, middleware patterns, and API design
- **Python**: Flask/Django patterns, project organization
- **Java**: Spring Boot structure and patterns

### Extension Development
- **Chrome Extension**: Background scripts, content scripts, and manifest structure
- **Firefox Extension**: Add-on structure and WebExtensions API
- **VS Code Extension**: Extension structure and activation patterns

## Methodology Templates

### Test-Driven Development (TDD)
- Test-first approach
- Red-Green-Refactor cycle
- Test organization and structure

### Clean Architecture
- Layer separation
- Dependency inversion
- Use case driven design

## Style Application Process

When applying a coding style, PAELLADOC:

1. **Analyzes** the project structure
2. **Maps** the style guide to the project
3. **Generates** linting rules and configuration files
4. **Creates** documentation about the style
5. **Integrates** with the project's build process

## Style Customization

Styles can be customized by:

```json
{
  "rules": {
    "indentation": 2,
    "quotes": "single",
    "component_type": "functional",
    "state_management": "redux"
  },
  "extensions": {
    "linting": true,
    "formatter": "prettier",
    "testing_framework": "jest"
  }
}
```

## Style Enforcement

Styles can be enforced through:

- **Linting Rules**: ESLint, Pylint, Checkstyle
- **Formatters**: Prettier, Black, Google Java Format
- **Pre-commit Hooks**: Husky, pre-commit
- **CI Integration**: GitHub Actions, Jenkins 

/**
 * Manages programming style guides and coding standards in PAELLADOC
 */
{
    "name": "coding_styles",
    "description": "Programming style guides and coding standards for PAELLADOC",
    "version": "1.5.0",
    "patterns": ["**/*.{js,ts,jsx,tsx,py,java,go,rb,cs,php}"],
    "style_categories": {
        "interface_implementation": {
            "description": "Rules for implementing interfaces correctly",
            "rules": [
                {
                    "id": "interface-method-signature",
                    "description": "Method signatures must exactly match the interface definition",
                    "severity": "critical",
                    "applies_to": ["all"],
                    "verification": "static_analysis",
                    "example": {
                        "correct": "public String getName(int id) { return \"Test\"; }",
                        "incorrect": "public String getName(long id) { return \"Test\"; }"
                    }
                },
                {
                    "id": "complete-interface-implementation",
                    "description": "Classes must implement all methods defined in the interface",
                    "severity": "critical",
                    "applies_to": ["all"],
                    "verification": "static_analysis",
                    "example": {
                        "correct": "class MyAnalyzer implements Analyzer { analyze() {...}, getRecommendations() {...} }",
                        "incorrect": "class MyAnalyzer implements Analyzer { analyze() {...} }"
                    }
                },
                {
                    "id": "interface-return-types",
                    "description": "Return types must be compatible with interface specifications",
                    "severity": "critical",
                    "applies_to": ["all"],
                    "verification": "static_analysis",
                    "example": {
                        "correct": "public List<String> getItems() { return new ArrayList<>(); }",
                        "incorrect": "public String[] getItems() { return new String[0]; }"
                    }
                },
                {
                    "id": "interface-parameter-types",
                    "description": "Parameter types must match interface specifications exactly",
                    "severity": "critical",
                    "applies_to": ["all"],
                    "verification": "static_analysis",
                    "example": {
                        "correct": "public void process(Context context) { ... }",
                        "incorrect": "public void process(String contextData) { ... }"
                    }
                },
                {
                    "id": "interface-error-handling",
                    "description": "Error handling must follow interface contract",
                    "severity": "high",
                    "applies_to": ["all"],
                    "verification": "code_review",
                    "example": {
                        "correct": "public Data fetch() throws NotFoundException { ... }",
                        "incorrect": "public Data fetch() { ... }"
                    }
                }
            ]
        },
        "adapter_pattern": {
            "description": "Rules for implementing the Adapter pattern correctly",
            "rules": [
                {
                    "id": "adapter-target-interface",
                    "description": "Adapters must implement the target interface completely",
                    "severity": "critical",
                    "applies_to": ["all"],
                    "verification": "static_analysis",
                    "example": {
                        "correct": "class MetaAnalyzerAdapter implements Analyzer { ... }",
                        "incorrect": "class MetaAnalyzerAdapter { ... }"
                    }
                },
                {
                    "id": "adapter-delegation",
                    "description": "Adapters should delegate to adaptee rather than reimplementing functionality",
                    "severity": "high",
                    "applies_to": ["all"],
                    "verification": "code_review",
                    "example": {
                        "correct": "public Result analyze() { return adaptee.performAnalysis(); }",
                        "incorrect": "public Result analyze() { /* reimplement analysis logic */ }"
                    }
                },
                {
                    "id": "adapter-encapsulation",
                    "description": "Adapters should encapsulate the adaptee and not expose it directly",
                    "severity": "medium",
                    "applies_to": ["all"],
                    "verification": "code_review",
                    "example": {
                        "correct": "private final LegacyAnalyzer adaptee;",
                        "incorrect": "public final LegacyAnalyzer adaptee;"
                    }
                },
                {
                    "id": "adapter-error-translation",
                    "description": "Adapters must translate adaptee errors to match target interface",
                    "severity": "high",
                    "applies_to": ["all"],
                    "verification": "testing",
                    "example": {
                        "correct": "try { adaptee.method(); } catch (OldException e) { throw new TargetException(e); }",
                        "incorrect": "adaptee.method(); // Allows OldException to propagate"
                    }
                },
                {
                    "id": "adapter-type-conversion",
                    "description": "Adapters must properly convert between adaptee and target types",
                    "severity": "critical",
                    "applies_to": ["all"],
                    "verification": "testing",
                    "example": {
                        "correct": "return new TargetResult(adaptee.getResultData());",
                        "incorrect": "return adaptee.getResultData();"
                    }
                }
            ]
        },
        "test_driven_development": {
            "description": "Rules for applying TDD correctly",
            "rules": [
                {
                    "id": "test-interface-contract",
                    "description": "Tests must verify interface contract compliance",
                    "severity": "high",
                    "applies_to": ["test"],
                    "verification": "code_review",
                    "example": {
                        "correct": "test('should return valid result according to Analyzer interface', () => { ... })",
                        "incorrect": "test('should analyze correctly', () => { ... })"
                    }
                },
                {
                    "id": "test-adapter-through-interface",
                    "description": "Adapter tests should use the target interface, not implementation details",
                    "severity": "high",
                    "applies_to": ["test"],
                    "verification": "code_review",
                    "example": {
                        "correct": "Analyzer analyzer = new LegacyAnalyzerAdapter(legacySystem); analyzer.analyze();",
                        "incorrect": "LegacyAnalyzerAdapter adapter = new LegacyAnalyzerAdapter(legacySystem); adapter.adapteeMethod();"
                    }
                },
                {
                    "id": "test-first-implementation",
                    "description": "Tests must be written before implementation code",
                    "severity": "high",
                    "applies_to": ["workflow"],
                    "verification": "git_history",
                    "example": {
                        "correct": "commit 1: Add tests for MetaAnalyzer, commit 2: Implement MetaAnalyzer",
                        "incorrect": "commit 1: Implement MetaAnalyzer, commit 2: Add tests for MetaAnalyzer"
                    }
                },
                {
                    "id": "mock-dependencies",
                    "description": "Tests should mock external dependencies to isolate unit tests",
                    "severity": "medium",
                    "applies_to": ["test"],
                    "verification": "code_review",
                    "example": {
                        "correct": "DependencyService mockService = mock(DependencyService.class);",
                        "incorrect": "DependencyService realService = new DependencyService();"
                    }
                }
            ]
        }
    },
    "enforcement": {
        "static_analysis": {
            "tools": ["eslint", "tslint", "pylint", "checkstyle", "golint"],
            "custom_rules": true,
            "ci_integration": true
        },
        "code_review": {
            "automated_checks": true,
            "peer_review_checklist": true,
            "pr_templates": true
        },
        "testing": {
            "enforce_test_first": true,
            "coverage_thresholds": {
                "statements": 85,
                "branches": 80,
                "functions": 90,
                "lines": 85,
                "interface_methods": 100
            }
        }
    }
} 