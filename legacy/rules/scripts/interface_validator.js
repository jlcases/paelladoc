#!/usr/bin/env node

/**
 * Interface Validator for PAELLADOC
 * 
 * This script validates TypeScript interface implementations to ensure they
 * correctly implement all required methods with proper signatures and return types.
 * 
 * Usage:
 *   node interface_validator.js <path-to-project> [--strict] [--verbose]
 */

const fs = require('fs');
const path = require('path');
const ts = require('typescript');
const glob = require('glob');
const chalk = require('chalk');

// Command line arguments
const args = process.argv.slice(2);
const projectPath = args[0] || '.';
const isStrict = args.includes('--strict');
const isVerbose = args.includes('--verbose');

// Configuration
const config = {
  requireExactReturnTypes: isStrict,
  requireExactParameterTypes: isStrict,
  requireCompleteDocumentation: isStrict,
  checkAdapterPattern: true,
  validateErrorHandling: true
};

// Results tracking
const results = {
  totalInterfaces: 0,
  totalImplementations: 0,
  validImplementations: 0,
  invalidImplementations: 0,
  errors: []
};

/**
 * Main validation function
 */
async function validateInterfaces() {
  console.log(chalk.blue('PAELLADOC Interface Validator'));
  console.log(chalk.blue('=============================='));
  console.log(`Scanning project at: ${chalk.yellow(projectPath)}`);
  console.log(`Mode: ${isStrict ? chalk.red('Strict') : chalk.green('Standard')}`);
  
  // Find all TypeScript files
  const files = glob.sync(`${projectPath}/**/*.ts`, {
    ignore: ['**/node_modules/**', '**/dist/**', '**/build/**']
  });
  
  if (files.length === 0) {
    console.error(chalk.red('No TypeScript files found in the specified path'));
    process.exit(1);
  }
  
  console.log(`Found ${chalk.yellow(files.length)} TypeScript files`);
  
  // Create TypeScript program
  const program = ts.createProgram(files, {
    target: ts.ScriptTarget.ES2020,
    module: ts.ModuleKind.CommonJS,
    strict: true
  });
  
  const checker = program.getTypeChecker();
  
  // Process each file
  for (const sourceFile of program.getSourceFiles()) {
    if (sourceFile.fileName.includes('node_modules') || 
        !sourceFile.fileName.endsWith('.ts')) {
      continue;
    }
    
    if (isVerbose) {
      console.log(`Checking ${chalk.cyan(path.relative(projectPath, sourceFile.fileName))}`);
    }
    
    processSourceFile(sourceFile, checker);
  }
  
  // Report results
  reportResults();
}

/**
 * Process a single TypeScript source file
 */
function processSourceFile(sourceFile, checker) {
  ts.forEachChild(sourceFile, node => {
    // Find interfaces
    if (ts.isInterfaceDeclaration(node)) {
      results.totalInterfaces++;
      const interfaceName = node.name.text;
      const interfaceSymbol = checker.getSymbolAtLocation(node.name);
      
      if (isVerbose) {
        console.log(`  Found interface: ${chalk.cyan(interfaceName)}`);
      }
      
      // Store interface methods for later comparison
      const interfaceMethods = getInterfaceMethods(node, checker);
      
      // Find implementations of this interface
      findImplementations(sourceFile, interfaceName, interfaceMethods, checker);
    }
    
    // Find classes directly
    if (ts.isClassDeclaration(node)) {
      validateClass(node, checker, sourceFile);
    }
  });
}

/**
 * Get all methods defined in an interface
 */
function getInterfaceMethods(interfaceNode, checker) {
  const methods = {};
  
  interfaceNode.members.forEach(member => {
    if (ts.isMethodSignature(member) && member.name) {
      const methodName = member.name.getText();
      const signature = checker.getSignatureFromDeclaration(member);
      
      if (!signature) return;
      
      const returnType = signature.getReturnType();
      const returnTypeString = checker.typeToString(returnType);
      
      const parameters = [];
      member.parameters.forEach(param => {
        const paramName = param.name.getText();
        const paramType = param.type 
          ? checker.typeToString(checker.getTypeFromTypeNode(param.type))
          : 'any';
        const isOptional = !!param.questionToken;
        
        parameters.push({
          name: paramName,
          type: paramType,
          isOptional
        });
      });
      
      // Check for method documentation
      const docs = getDocumentation(member);
      
      methods[methodName] = {
        name: methodName,
        returnType: returnTypeString,
        parameters,
        documentation: docs
      };
    }
  });
  
  return methods;
}

/**
 * Extract documentation from a node
 */
function getDocumentation(node) {
  const jsDoc = ts.getJSDocCommentsAndTags(node);
  if (jsDoc && jsDoc.length > 0) {
    return jsDoc[0].getText();
  }
  return '';
}

/**
 * Find classes that implement a specific interface
 */
function findImplementations(sourceFile, interfaceName, interfaceMethods, checker) {
  // Process the source file to find classes implementing the interface
  ts.forEachChild(sourceFile, node => {
    if (ts.isClassDeclaration(node) && node.heritageClauses) {
      for (const clause of node.heritageClauses) {
        if (clause.token === ts.SyntaxKind.ImplementsKeyword) {
          for (const type of clause.types) {
            // Check if this class implements our interface
            if (type.expression.getText() === interfaceName) {
              results.totalImplementations++;
              const className = node.name ? node.name.text : 'AnonymousClass';
              
              if (isVerbose) {
                console.log(`    Found implementation: ${chalk.green(className)}`);
              }
              
              validateImplementation(node, className, interfaceName, interfaceMethods, checker, sourceFile);
            }
          }
        }
      }
    }
  });
}

/**
 * Validate a class for adapter pattern usage
 */
function validateClass(classNode, checker, sourceFile) {
  if (!classNode.name || !config.checkAdapterPattern) return;
  
  const className = classNode.name.text;
  
  // Check if class name suggests it's an adapter
  if (className.includes('Adapter')) {
    if (isVerbose) {
      console.log(`  Checking adapter: ${chalk.magenta(className)}`);
    }
    
    // Look for private fields that could be adaptees
    let hasAdapteeField = false;
    let delegationCount = 0;
    let methodCount = 0;
    
    // Check for private fields
    classNode.members.forEach(member => {
      if (ts.isPropertyDeclaration(member) && 
          member.modifiers && 
          member.modifiers.some(m => m.kind === ts.SyntaxKind.PrivateKeyword)) {
        hasAdapteeField = true;
      }
      
      // Count methods for delegation analysis
      if (ts.isMethodDeclaration(member) && member.name) {
        methodCount++;
        
        // Check method body for delegation pattern
        if (member.body) {
          const methodText = member.body.getText();
          if (methodText.includes('this.') && 
              (methodText.includes('return this.') || methodText.includes('await this.'))) {
            delegationCount++;
          }
        }
      }
    });
    
    // Validate adapter implementation
    if (!hasAdapteeField) {
      results.errors.push({
        type: 'adapter',
        class: className,
        file: sourceFile.fileName,
        message: 'Adapter class does not have a private adaptee field'
      });
    }
    
    // Check for delegation
    if (methodCount > 0 && delegationCount / methodCount < 0.5) {
      results.errors.push({
        type: 'adapter',
        class: className,
        file: sourceFile.fileName,
        message: `Adapter only delegates ${delegationCount} of ${methodCount} methods, suggesting reimplementation instead of delegation`
      });
    }
  }
}

/**
 * Validate that a class correctly implements an interface
 */
function validateImplementation(classNode, className, interfaceName, interfaceMethods, checker, sourceFile) {
  const errors = [];
  const implementedMethods = {};
  
  // Find methods in the class
  classNode.members.forEach(member => {
    if (ts.isMethodDeclaration(member) && member.name) {
      const methodName = member.name.getText();
      implementedMethods[methodName] = true;
      
      // Check if this method is required by the interface
      if (interfaceMethods[methodName]) {
        const interfaceMethod = interfaceMethods[methodName];
        const signature = checker.getSignatureFromDeclaration(member);
        
        if (!signature) return;
        
        // Check return type
        const returnType = signature.getReturnType();
        const returnTypeString = checker.typeToString(returnType);
        
        if (config.requireExactReturnTypes) {
          if (returnTypeString !== interfaceMethod.returnType) {
            errors.push(`Method '${methodName}' has return type '${returnTypeString}' but interface requires '${interfaceMethod.returnType}'`);
          }
        } else {
          // Less strict check: just ensure it's compatible
          const isCompatible = isTypeCompatible(returnTypeString, interfaceMethod.returnType);
          if (!isCompatible) {
            errors.push(`Method '${methodName}' has incompatible return type '${returnTypeString}', interface requires '${interfaceMethod.returnType}'`);
          }
        }
        
        // Check parameters
        if (member.parameters.length !== interfaceMethod.parameters.length) {
          const requiredCount = interfaceMethod.parameters.filter(p => !p.isOptional).length;
          
          if (member.parameters.length < requiredCount) {
            errors.push(`Method '${methodName}' has ${member.parameters.length} parameters but interface requires at least ${requiredCount}`);
          }
        }
        
        // Check each parameter type
        member.parameters.forEach((param, index) => {
          if (index < interfaceMethod.parameters.length) {
            const paramName = param.name.getText();
            const interfaceParam = interfaceMethod.parameters[index];
            
            if (param.type) {
              const paramType = checker.typeToString(checker.getTypeFromTypeNode(param.type));
              
              if (config.requireExactParameterTypes) {
                if (paramType !== interfaceParam.type && !interfaceParam.isOptional) {
                  errors.push(`Parameter '${paramName}' has type '${paramType}' but interface requires '${interfaceParam.type}'`);
                }
              } else {
                // Less strict check
                const isCompatible = isTypeCompatible(interfaceParam.type, paramType);
                if (!isCompatible && !interfaceParam.isOptional) {
                  errors.push(`Parameter '${paramName}' has incompatible type '${paramType}', interface requires '${interfaceParam.type}'`);
                }
              }
            }
          }
        });
        
        // Check documentation if strict mode
        if (config.requireCompleteDocumentation) {
          const docs = getDocumentation(member);
          if (!docs && interfaceMethod.documentation) {
            errors.push(`Method '${methodName}' is missing documentation`);
          }
        }
        
        // Check error handling for methods that might throw
        if (config.validateErrorHandling && member.body) {
          const methodText = member.body.getText();
          if (interfaceMethod.documentation && 
              interfaceMethod.documentation.includes('@throws') && 
              !methodText.includes('try') && 
              !methodText.includes('throw')) {
            errors.push(`Method '${methodName}' is missing error handling (try/catch or throw)`);
          }
        }
      }
    }
  });
  
  // Check if all interface methods are implemented
  for (const methodName in interfaceMethods) {
    if (!implementedMethods[methodName]) {
      errors.push(`Missing method '${methodName}' required by interface '${interfaceName}'`);
    }
  }
  
  // Record results
  if (errors.length > 0) {
    results.invalidImplementations++;
    results.errors.push({
      type: 'implementation',
      class: className,
      interface: interfaceName,
      file: sourceFile.fileName,
      errors
    });
  } else {
    results.validImplementations++;
  }
}

/**
 * Simple type compatibility check
 */
function isTypeCompatible(required, provided) {
  // Exact match
  if (required === provided) return true;
  
  // Any is compatible with everything
  if (required === 'any' || provided === 'any') return true;
  
  // Void is only compatible with void and any
  if (required === 'void') return provided === 'void' || provided === 'any';
  
  // Handle promise types
  if (required.startsWith('Promise<') && provided.startsWith('Promise<')) {
    const requiredInner = required.substring(8, required.length - 1);
    const providedInner = provided.substring(8, provided.length - 1);
    return isTypeCompatible(requiredInner, providedInner);
  }
  
  // Handle array types
  if (required.endsWith('[]') && provided.endsWith('[]')) {
    const requiredItem = required.substring(0, required.length - 2);
    const providedItem = provided.substring(0, provided.length - 2);
    return isTypeCompatible(requiredItem, providedItem);
  }
  
  // Number is compatible with specific numeric types
  if (required === 'number') {
    return ['number', 'bigint', 'any'].includes(provided);
  }
  
  // String compatibility
  if (required === 'string') {
    return ['string', 'any'].includes(provided);
  }
  
  // Boolean compatibility
  if (required === 'boolean') {
    return ['boolean', 'any'].includes(provided);
  }
  
  // Object is compatible with any non-primitive type
  if (required === 'object') {
    return ['object', 'any', '{}'].includes(provided) || 
           (!['string', 'number', 'boolean', 'void', 'undefined', 'null'].includes(provided));
  }
  
  // Generic fallback for complex types - this is a simplification
  return false;
}

/**
 * Report validation results
 */
function reportResults() {
  console.log('\n');
  console.log(chalk.blue('Validation Results'));
  console.log(chalk.blue('=================='));
  console.log(`Interfaces found: ${chalk.yellow(results.totalInterfaces)}`);
  console.log(`Implementations found: ${chalk.yellow(results.totalImplementations)}`);
  console.log(`Valid implementations: ${chalk.green(results.validImplementations)}`);
  console.log(`Invalid implementations: ${chalk.red(results.invalidImplementations)}`);
  
  if (results.errors.length > 0) {
    console.log('\n');
    console.log(chalk.red('Errors'));
    console.log(chalk.red('======'));
    
    results.errors.forEach(error => {
      if (error.type === 'implementation') {
        console.log(`\n${chalk.red('✗')} Class ${chalk.yellow(error.class)} incorrectly implements ${chalk.cyan(error.interface)}`);
        console.log(`  ${chalk.dim(path.relative(projectPath, error.file))}`);
        
        error.errors.forEach(err => {
          console.log(`  • ${err}`);
        });
      } else if (error.type === 'adapter') {
        console.log(`\n${chalk.red('✗')} Adapter ${chalk.yellow(error.class)} has issues:`);
        console.log(`  ${chalk.dim(path.relative(projectPath, error.file))}`);
        console.log(`  • ${error.message}`);
      }
    });
    
    process.exit(1);
  } else {
    console.log('\n');
    console.log(chalk.green('All interface implementations are valid! ✓'));
  }
}

// Run the validation
validateInterfaces().catch(err => {
  console.error(chalk.red('Error running validation:'), err);
  process.exit(1);
}); 