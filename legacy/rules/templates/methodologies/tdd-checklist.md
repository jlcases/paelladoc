# Universal TDD Checklist

## Setup Phase

- [ ] Project initialized with appropriate build tools
- [ ] Testing framework installed and configured
- [ ] Code coverage tools set up
- [ ] Automatic test execution configured (watch mode)
- [ ] Directory structure created appropriately
- [ ] Verification test created and executed successfully
- [ ] Interface contracts defined before implementations
- [ ] Mock objects prepared for all external dependencies

## Development Cycle

### RED Phase
- [ ] Test written for new functionality
- [ ] Test executed and confirmed to fail for the expected reason
- [ ] Test is focused on a single responsibility
- [ ] Test uses the public interface, not implementation details
- [ ] Test validates behavior, not implementation
- [ ] Test explicitly validates interface contract compliance

### GREEN Phase
- [ ] Minimal code implemented to make the test pass
- [ ] No code beyond what's necessary for passing tests
- [ ] Tests executed and verified to pass
- [ ] Implementation follows the interface contract exactly
- [ ] Adapters properly connect incompatible interfaces when needed
- [ ] Class hierarchy and inheritance relationships respect Liskov Substitution Principle

### REFACTOR Phase
- [ ] Code improved while maintaining passing tests
- [ ] Duplication eliminated
- [ ] Names improved for clarity
- [ ] Complexity reduced where possible
- [ ] Tests still pass after all refactoring
- [ ] Interface contracts maintained throughout refactoring
- [ ] Adapters updated to maintain compatibility
- [ ] No implementation inheritance leaking through interfaces

## Interface Compliance Checks

- [ ] All implemented interfaces have full method coverage
- [ ] Method signatures match interface definitions exactly
- [ ] Return types and parameter types match interface specifications
- [ ] Error handling follows interface contract
- [ ] No additional behavior outside interface specification
- [ ] Adapters fully transform between interface types

## Adapter Pattern Verification

- [ ] Each adapter implements target interface completely
- [ ] Adapter correctly translates operations to adaptee
- [ ] Adapter handles all error cases from adaptee
- [ ] Adapter maintains type safety between interfaces
- [ ] No leaky abstractions in adapter implementation
- [ ] Tests verify adapter behavior through target interface

## Quality Gates

### Continuous Verification
- [ ] Tests executed after each significant change
- [ ] Watch mode used during active development
- [ ] Test coverage checked periodically
- [ ] Interface compliance verified during CI

### Pre-Commit Checks
- [ ] All tests pass
- [ ] Code coverage meets established threshold
- [ ] No incomplete or ignored tests without justification
- [ ] Documentation updated to reflect changes
- [ ] Interface contracts documented with examples
- [ ] Full implementation of all required interfaces verified

## Troubleshooting Guide

### Configuration Issues
- [ ] All dependencies correctly installed
- [ ] Framework configuration is correct
- [ ] Test file naming conventions followed
- [ ] Directory structure matches framework expectations

### Interface Implementation Issues
- [ ] Method signatures exactly match interface definition
- [ ] Return types compatible with interface specification
- [ ] Parameter types match interface requirements
- [ ] No missing methods from interface implementation
- [ ] Error handling follows interface contract

### Test Reliability Issues
- [ ] Tests are isolated from each other
- [ ] External dependencies are properly mocked
- [ ] No race conditions in asynchronous tests
- [ ] Test environment consistent between runs
- [ ] Mocks correctly simulate interface behavior

### CI/CD Integration
- [ ] Pipeline configured to run tests automatically
- [ ] Coverage threshold set for build approval
- [ ] Test reports generated and accessible
- [ ] Tests run successfully in CI environment
- [ ] Interface compliance checks automated

## Best Practices Verification

- [ ] Each test focuses on a single assertion or concept
- [ ] Tests are independent from one another
- [ ] Implementation follows the minimal requirements to pass tests
- [ ] Refactoring is performed after achieving passing tests
- [ ] Tests run quickly enough for frequent execution
- [ ] Test names clearly describe behavior being tested
- [ ] Interface contracts are tested explicitly
- [ ] Adapter pattern implementation follows best practices 