# Test-Driven Development Rules

## Core Principles

1. **Test First Development**
   - Write tests before implementing code
   - Begin with the most important functionality
   - Tests should document expected behavior

2. **Interface-Driven Design**
   - Define interfaces before implementations
   - Test against interfaces, not concrete classes
   - Ensure proper contract documentation

3. **Red-Green-Refactor Cycle**
   - Red: Write failing tests first
   - Green: Implement minimal code to pass tests
   - Refactor: Improve design while maintaining passing tests

## Interface Implementation

### Critical Rules

1. **Complete Method Coverage**
   - All interface methods must be implemented
   - Method signatures must match exactly
   - Return types must be compatible
   
   ```typescript
   // CORRECT
   interface Analyzer {
     analyze(context: Context): AnalysisResult;
     getRecommendations(): Recommendation[];
   }
   
   class MetaAnalyzer implements Analyzer {
     analyze(context: Context): AnalysisResult {
       // Implementation
       return result;
     }
     
     getRecommendations(): Recommendation[] {
       // Implementation
       return recommendations;
     }
   }
   
   // INCORRECT
   class BrokenAnalyzer implements Analyzer {
     // Missing getRecommendations() method
     analyze(context: Context): AnalysisResult {
       return result;
     }
   }
   ```

2. **Parameter Type Compatibility**
   - Parameter types must match interface definition
   - No narrowing or broadening of types
   - No optional parameters if not in interface
   
   ```typescript
   // CORRECT
   interface DataProcessor {
     process(data: Record<string, any>): void;
   }
   
   class JsonProcessor implements DataProcessor {
     process(data: Record<string, any>): void {
       // Implementation
     }
   }
   
   // INCORRECT
   class XmlProcessor implements DataProcessor {
     process(data: string): void { // Wrong parameter type
       // Implementation
     }
   }
   ```

3. **Return Type Compliance**
   - Return types must be compatible with interface
   - No returning different types or structures
   - No throwing exceptions not specified in interface
   
   ```java
   // CORRECT
   interface ResultProvider {
     List<String> getResults() throws IOException;
   }
   
   class FileResultProvider implements ResultProvider {
     public List<String> getResults() throws IOException {
       // Implementation
       return results;
     }
   }
   
   // INCORRECT
   class DatabaseResultProvider implements ResultProvider {
     public String[] getResults() { // Wrong return type
       // Implementation
       return results;
     }
   }
   ```

## Adapter Pattern Rules

### Implementation

1. **Target Interface Compliance**
   - Adapters must implement the target interface fully
   - Adapter must maintain interface contract semantics
   - Type conversion must preserve semantic equivalence
   
   ```typescript
   // CORRECT
   interface Analyzer {
     analyze(context: Context): AnalysisResult;
   }
   
   class LegacyAnalyzerAdapter implements Analyzer {
     private legacyAnalyzer: LegacyAnalyzer;
     
     constructor(legacyAnalyzer: LegacyAnalyzer) {
       this.legacyAnalyzer = legacyAnalyzer;
     }
     
     analyze(context: Context): AnalysisResult {
       const legacyResult = this.legacyAnalyzer.runAnalysis(context.data);
       return this.convertToAnalysisResult(legacyResult);
     }
     
     private convertToAnalysisResult(legacyResult: LegacyResult): AnalysisResult {
       // Convert types
       return new AnalysisResult(/* ... */);
     }
   }
   ```

2. **Error Translation**
   - Adapter must translate error/exception types
   - Maintain semantic equivalence of errors
   - Preserve error context and information
   
   ```java
   // CORRECT
   public class DatabaseAdapter implements DataStorage {
     private LegacyDatabase legacyDb;
     
     public Data fetch(String id) throws NotFoundException {
       try {
         return legacyDb.retrieve(id);
       } catch (LegacyDbException e) {
         if (e.getCode() == 404) {
           throw new NotFoundException("Item not found: " + id, e);
         }
         throw new StorageException("Database error: " + e.getMessage(), e);
       }
     }
   }
   ```

3. **Delegation Over Reimplementation**
   - Adapters should delegate to adaptee
   - Avoid duplicating business logic
   - Focus on type conversion and interface alignment
   
   ```typescript
   // CORRECT
   class ReportGeneratorAdapter implements Reporter {
     constructor(private legacyGenerator: LegacyReportGenerator) {}
     
     generateReport(data: ReportData): Report {
       // Delegate core functionality
       const legacyReport = this.legacyGenerator.createReport(this.convertData(data));
       return this.convertReport(legacyReport);
     }
     
     // Only conversion logic in adapter
     private convertData(data: ReportData): LegacyData { /* ... */ }
     private convertReport(legacyReport: LegacyReport): Report { /* ... */ }
   }
   
   // INCORRECT
   class ReimplementingAdapter implements Reporter {
     // Reimplements business logic instead of delegating
     generateReport(data: ReportData): Report {
       // Completely new implementation
       // ...
     }
   }
   ```

## Testing Rules

### Interface Testing

1. **Contract Verification**
   - Test each interface method
   - Verify behavior against interface contract
   - Test edge cases specifically mentioned in contract
   
   ```javascript
   // CORRECT
   describe('Analyzer Interface Implementation', () => {
     it('should analyze context and return valid analysis result', () => {
       const analyzer = new MyAnalyzer();
       const context = createTestContext();
       const result = analyzer.analyze(context);
       
       // Verify result matches interface contract
       expect(result).toHaveProperty('id');
       expect(result).toHaveProperty('issues');
       expect(result).toHaveProperty('metrics');
     });
     
     it('should return recommendations based on analysis', () => {
       const analyzer = new MyAnalyzer();
       const recommendations = analyzer.getRecommendations();
       
       expect(Array.isArray(recommendations)).toBe(true);
       recommendations.forEach(rec => {
         expect(rec).toHaveProperty('id');
         expect(rec).toHaveProperty('description');
       });
     });
   });
   ```

2. **Testing Through Interfaces**
   - Test implementation through interface references
   - Avoid using implementation-specific methods in tests
   - Test polymorphic behavior with multiple implementations
   
   ```typescript
   // CORRECT
   test('analyzer processes input correctly', () => {
     // Reference through interface
     const analyzer: Analyzer = new ConcreteAnalyzer();
     // Test using only interface methods
     const result = analyzer.analyze(testContext);
     expect(result.score).toBeGreaterThan(0);
   });
   
   // INCORRECT
   test('analyzer processes input correctly', () => {
     // Direct reference to implementation
     const analyzer = new ConcreteAnalyzer();
     // Using implementation-specific method
     analyzer.internalMethod();
     const result = analyzer.analyze(testContext);
     expect(result.score).toBeGreaterThan(0);
   });
   ```

3. **Mock Behavior Verification**
   - Mock implementations should verify interface behavior
   - Test error handling in interfaces
   - Verify interface invariants
   
   ```java
   // CORRECT
   @Test
   public void shouldHandleErrorsAccordingToContract() {
     // Mock implementation of interface
     DataProvider mockProvider = mock(DataProvider.class);
     when(mockProvider.getData()).thenThrow(new DataException("Test error"));
     
     DataProcessor processor = new DataProcessor(mockProvider);
     
     // Verify behavior matches interface contract for errors
     assertThrows(ProcessingException.class, () -> {
       processor.process();
     });
   }
   ```

## Workflow Rules

1. **Test-First Approach**
   - Write test for new interface/method first
   - Implement interface after test is written
   - Verify test fails before implementation
   
   ```bash
   # Correct workflow
   git commit -m "Add tests for UserService interface"
   git commit -m "Implement UserService interface"
   
   # Incorrect workflow
   git commit -m "Implement UserService interface"
   git commit -m "Add tests for UserService"
   ```

2. **Interface Evolution**
   - Update tests when changing interfaces
   - Ensure all implementations are updated
   - Maintain backward compatibility when possible
   
   ```typescript
   // When extending an interface
   interface Analyzer {
     analyze(context: Context): AnalysisResult;
     // New method added
     getCategory(): string;
   }
   
   // Tests must be updated first
   test('analyzer provides category information', () => {
     const analyzer: Analyzer = new ConcreteAnalyzer();
     expect(analyzer.getCategory()).toBeDefined();
   });
   
   // Then update implementations
   class ConcreteAnalyzer implements Analyzer {
     // Existing methods...
     
     getCategory(): string {
       return "performance";
     }
   }
   ```

3. **Continuous Integration**
   - Run interface compliance tests in CI
   - Verify all implementations during PR review
   - Enforce style rules for interfaces
   
   ```yaml
   # CI configuration
   steps:
     - name: Run interface compliance tests
       run: npm run test:interfaces
     
     - name: Verify adapter implementations
       run: npm run test:adapters
   ```

## Best Practices

1. **Documentation**
   - Document interface contracts clearly
   - Include preconditions and postconditions
   - Document exceptions and error cases

2. **Consistency**
   - Use consistent naming across interfaces
   - Follow language-specific interface conventions
   - Maintain semantic consistency in adapter implementations

3. **Simplicity**
   - Keep interfaces focused and cohesive
   - Avoid large interfaces (prefer composition)
   - Follow Interface Segregation Principle 