# Contributing to PAELLADOC

Thank you for your interest in contributing to PAELLADOC! This document provides guidelines and important information for contributors.

## License Information

PAELLADOC is licensed under the MIT License with Commons Clause. Before contributing, please understand what this means:

### ✅ You CAN:
- Use PAELLADOC in your projects (personal, commercial, academic)
- Modify the code and documentation
- Distribute copies of your modified version
- Create and sell products BUILT USING PAELLADOC
- Contribute improvements back to PAELLADOC

### ❌ You CANNOT:
- Sell PAELLADOC itself
- Offer PAELLADOC as a hosted/SaaS service
- Create competing products based on PAELLADOC

## How to Contribute

1. **Fork the Repository**
   - Fork the PAELLADOC repository to your GitHub account
   - Clone your fork locally

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow our coding standards
   - Keep commits atomic and well-described
   - Add tests if applicable
   - Update documentation as needed

4. **Test Your Changes**
   - Ensure all tests pass
   - Test your changes thoroughly
   - Verify documentation accuracy

5. **Submit a Pull Request**
   - Push your changes to your fork
   - Create a Pull Request from your branch
   - Describe your changes in detail
   - Reference any related issues

## Development Guidelines

### Test-Driven Development (TDD)

We follow strict TDD practices in this project. Each feature or bug fix MUST follow the RED-GREEN-REFACTOR cycle:

1. **RED Phase** 🔴
   - Write a failing test first
   - Commit with prefix `test(red):` 
   - Example: `test(red): add test for MCP server plugin registration`

2. **GREEN Phase** 💚
   - Implement minimal code to make the test pass
   - Commit with prefix `feat(green):` 
   - Example: `feat(green): implement plugin registration`

3. **REFACTOR Phase** 🔄
   - Clean up and optimize the code
   - Ensure tests remain green
   - Commit with prefix `refactor:` 
   - Example: `refactor: improve plugin registration efficiency`

Each PR should show this TDD cycle in the commit history. PRs without proper TDD commits will need revision.

### Code Style
- Use clear, descriptive variable and function names
- Follow existing code formatting
- Comment complex logic
- Keep functions focused and concise

### Documentation
- Update relevant documentation
- Add JSDoc comments for new functions
- Include examples for new features
- Keep README.md up to date

### Testing
- Write tests for new features
- Update existing tests as needed
- Ensure all tests pass before submitting

## Pull Request Process

1. **Before Submitting**
   - Rebase your branch on latest main
   - Resolve any conflicts
   - Run all tests
   - Update documentation

2. **PR Description**
   - Clearly describe the changes
   - Explain the motivation
   - List any breaking changes
   - Include relevant issue numbers

3. **Review Process**
   - Address review comments promptly
   - Keep discussions focused
   - Be open to feedback
   - Make requested changes

## Community Guidelines

- Be respectful and inclusive
- Help others when possible
- Keep discussions constructive
- Follow our Code of Conduct

## Questions or Problems?

- Check existing issues first
- Open a new issue if needed
- Join our discussions
- Ask in our community channels

## Legal Notes

By contributing to PAELLADOC, you agree that your contributions will be licensed under its MIT License with Commons Clause. You also certify that:

- You have the right to submit the code
- Your contribution is your original work
- You understand and agree to our licensing terms

## Additional Resources

- [Documentation](https://paelladoc.com/docs)
- [Issue Tracker](https://github.com/jlcases/paelladoc/issues)
- [Discussion Forum](https://github.com/jlcases/paelladoc/discussions)

Thank you for contributing to PAELLADOC! 🚀 