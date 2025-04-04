---
description: When user discusses interface design, contracts, adapter patterns, or interface testing, provide guidance based on PAELLADOC principles
globs: 
alwaysApply: false
---

# Interface Design and Management in PAELLADOC

This defines rules and guidelines for interface design, implementation, and verification.

## Interface Design Principles

1.  **Interface Segregation**: Prefer multiple small, focused interfaces.
2.  **Explicit Contracts**: Document preconditions, postconditions, errors, parameters, and return values clearly.
3.  **Consistency**: Maintain consistent naming and abstraction levels.

## Interface Documentation Requirements

- Purpose and context.
- Detailed method documentation (params, returns, exceptions, thread safety, performance).
- Contract specification (invariants, guarantees, side effects).

## Adapter Pattern Requirements

1.  Implement the entire target interface.
2.  Delegate to the adaptee; avoid reimplementing logic.
3.  Translate errors/exceptions to match the target interface contract.

## Interface Testing Requirements

1.  Create abstract contract test suites for interfaces.
2.  Write implementation-agnostic tests (test through the interface).
3.  Cover edge cases and error handling specified in the contract.

## Interface Evolution Guidelines

1.  Maintain backward compatibility (never remove methods, don't make breaking signature changes).
2.  Use versioning (e.g., `InterfaceV2`) or extension interfaces for major changes.
3.  Use a clear deprecation process for methods to be removed.

## Validation and Enforcement

- Static analysis (linting, doc coverage, type checking).
- Automated contract testing in CI.
- Code review checklists for interface design and implementation.

## Core Concepts

```json
{
  "name": "interfaces",
  "description": "Manages interface design principles and implementation patterns in PAELLADOC",
  "version": "1.0.0",
  "components": {
    "interface_contracts": {
      "enabled": true,
      "enforce_documentation": true,
      "verification_level": "strict"
    },
    "adapter_pattern": {
      "enabled": true,
      "enforce_delegation": true
    },
    "test_driven_interfaces": {
      "enabled": true,
      "require_test_first": true
    }
  }
}
```

## Template Documentation Example

```typescript
/**
 * DocumentationProvider interface for generating documentation
 * from various sources.
 * 
 * Thread-safety: Implementations must be thread-safe.
 * Performance: Methods should complete within reasonable time frames
 * relative to the size of the documentation source.
 */
interface DocumentationProvider {
  /**
   * Generates documentation from the provided source.
   * 
   * @param source - Source data containing documentation information.
   *                Must not be null or undefined.
   * @param options - Optional configuration for generation.
   * @returns DocumentationResult - Structured documentation data.
   *                               Will never return null.
   * @throws InvalidSourceError - If source cannot be parsed or is invalid.
   */
  generateDocumentation(source: Source, options?: GenerationOptions): DocumentationResult;
  
  /**
   * Checks if the provider can handle the given source.
   * Must be called before generateDocumentation for validation.
   * 
   * @param source - Source to check compatibility with.
   * @returns true if provider can generate documentation from this source.
   */
  canHandle(source: Source): boolean;
}
```

## Adapter Implementation Example

```typescript
// Target interface
interface AnalysisProvider {
  runAnalysis(data: AnalysisData): AnalysisResult;
  getSupportedTypes(): string[];
}

// Adaptee (existing implementation with different interface)
class LegacyAnalyzer {
  processData(rawData: any): any {
    // Implementation
  }
  
  getCapabilities(): { types: string[] } {
    // Implementation
  }
}

// Adapter implementation
class LegacyAnalyzerAdapter implements AnalysisProvider {
  private legacyAnalyzer: LegacyAnalyzer;
  
  constructor(legacyAnalyzer: LegacyAnalyzer) {
    this.legacyAnalyzer = legacyAnalyzer;
  }
  
  runAnalysis(data: AnalysisData): AnalysisResult {
    try {
      // Convert data format
      const legacyData = this.convertToLegacyFormat(data);
      
      // Delegate to adaptee
      const legacyResult = this.legacyAnalyzer.processData(legacyData);
      
      // Convert result
      return this.convertToAnalysisResult(legacyResult);
    } catch (error) {
      // Translate exceptions
      if (error instanceof LegacyDataError) {
        throw new AnalysisDataError("Invalid analysis data: " + error.message, error);
      }
      throw new AnalysisError("Analysis failed: " + error.message, error);
    }
  }
  
  getSupportedTypes(): string[] {
    const capabilities = this.legacyAnalyzer.getCapabilities();
    return capabilities.types;
  }
  
  private convertToLegacyFormat(data: AnalysisData): any {
    // Conversion logic
  }
  
  private convertToAnalysisResult(legacyResult: any): AnalysisResult {
    // Conversion logic
  }
}
```

## Interface Test Example

```typescript
describe('DocumentationProvider Interface Contract', () => {
  // Test with multiple implementations
  const implementations = [
    new MarkdownDocumentationProvider(),
    new JavadocDocumentationProvider(),
    new JsDocDocumentationProvider()
  ];
  
  implementations.forEach(provider => {
    describe(`Implementation: ${provider.constructor.name}`, () => {
      it('should return false for unsupported sources', () => {
        const unsupportedSource = { type: 'UNSUPPORTED', content: '' };
        expect(provider.canHandle(unsupportedSource)).toBe(false);
      });
      
      it('should successfully generate documentation from supported sources', () => {
        // Arrange
        const supportedSource = createSupportedSourceFor(provider);
        
        // Act
        const result = provider.generateDocumentation(supportedSource);
        
        // Assert
        expect(result).not.toBeNull();
        expect(result.sections.length).toBeGreaterThan(0);
        expect(result.metadata).toBeDefined();
      });
      
      it('should throw InvalidSourceError for invalid sources', () => {
        // Arrange
        const invalidSource = { type: 'INVALID', content: 'corrupted content' };
        
        // Act & Assert
        expect(() => {
          provider.generateDocumentation(invalidSource);
        }).toThrow(InvalidSourceError);
      });
    });
  });
});
```

## Implementation Requirements

All interface implementations in PAELLADOC must:

1. **Follow the Dependency Inversion Principle**
   - Depend on abstractions, not concrete implementations
   - Be injectable or configurable with different implementations
   - Support the use of mocks and stubs for testing

2. **Support Error Recovery**
   - Handle exceptional states according to the interface contract
   - Provide meaningful error messages
   - Preserve the system in a consistent state after errors

3. **Maintain Performance Characteristics**
   - Meet time and resource constraints specified in the interface
   - Scale appropriately with input size
   - Document performance characteristics if different from specification 