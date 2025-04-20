# MCP Server Tests

This directory contains tests for the Paelladoc MCP server following hexagonal architecture principles. Tests are organized into three main categories:

## Test Structure

```
tests/
├── unit/            # Unit tests for individual components
│   └── test_tools.py  # Tests for MCP tools in isolation
├── integration/     # Integration tests for component interactions
│   └── test_server.py # Tests for server STDIO communication
└── e2e/             # End-to-end tests simulating real-world usage
    └── test_cursor_simulation.py # Simulates Cursor interaction
```

## Test Categories

1. **Unit Tests** (`unit/`)
   - Test individual functions/components in isolation
   - Don't require a running server
   - Fast to execute
   - Example: Testing the `ping()` function directly

2. **Integration Tests** (`integration/`)
   - Test interactions between components
   - Verify STDIO communication with the server
   - Example: Starting the server and sending/receiving messages

3. **End-to-End Tests** (`e2e/`)
   - Simulate real-world usage scenarios
   - Test the system as a whole
   - Example: Simulating how Cursor would interact with the server

## Running Tests

### Run All Tests

```bash
python -m unittest discover mcp_server/tests
```

### Run Tests by Category

```bash
# Unit tests only
python -m unittest discover mcp_server/tests/unit

# Integration tests only
python -m unittest discover mcp_server/tests/integration

# End-to-end tests only
python -m unittest discover mcp_server/tests/e2e
```

### Run a Specific Test File

```bash
python -m unittest mcp_server/tests/unit/test_tools.py
```

### Run a Specific Test Case

```bash
python -m unittest mcp_server.tests.unit.test_tools.TestToolsPing
```

### Run a Specific Test Method

```bash
python -m unittest mcp_server.tests.unit.test_tools.TestToolsPing.test_ping_returns_dict
```

## TDD Process

These tests follow the Test-Driven Development (TDD) approach:

1. **RED**: Write failing tests first
2. **GREEN**: Implement the minimal code to make tests pass
3. **REFACTOR**: Improve the code while keeping tests passing

## Adding New Tests

When adding new MCP tools:

1. Create unit tests for the tool's functionality
2. Add integration tests for the tool's STDIO communication
3. Update E2E tests to verify Cursor interaction with the tool 