#!/bin/bash

# Automatic setup script for Test-Driven Development (TDD)
# This script sets up everything needed to start TDD in various programming languages
# Author: PAELLADOC
# Version: 1.2

# Colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}      AUTOMATIC TDD SETUP          ${NC}"
echo -e "${BLUE}=====================================${NC}"

# Function to set up a Node.js/TypeScript project
setup_node() {
  echo -e "\n${BLUE}Setting up Node.js/TypeScript project...${NC}"
  
  # Check if we're in a Node project
  if [ ! -f package.json ]; then
    echo -e "${YELLOW}package.json not found. Do you want to initialize a new project? [y/n]${NC}"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
      echo -e "${GREEN}Initializing new project...${NC}"
      npm init -y
    else
      echo -e "${RED}Cannot continue without a Node project. Aborting.${NC}"
      return 1
    fi
  fi

  # Install basic dependencies
  echo -e "\n${BLUE}Installing development dependencies...${NC}"
  npm install --save-dev typescript ts-node

  # Install testing tools
  echo -e "\n${BLUE}Installing testing tools...${NC}"
  npm install --save-dev jest ts-jest @types/jest

  # Configure TypeScript if it doesn't exist
  if [ ! -f tsconfig.json ]; then
    echo -e "\n${BLUE}Configuring TypeScript...${NC}"
    npx tsc --init --target es2017 --module commonjs --esModuleInterop true --forceConsistentCasingInFileNames true --strict true --skipLibCheck true
  fi

  # Create Jest configuration
  echo -e "\n${BLUE}Creating Jest configuration...${NC}"
  cat > jest.config.js << 'EOL'
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/*.test.ts'],
  collectCoverage: true,
  coverageDirectory: 'coverage',
  collectCoverageFrom: ['src/**/*.ts', '!src/**/*.d.ts'],
};
EOL

  # Configure scripts in package.json
  echo -e "\n${BLUE}Configuring scripts in package.json...${NC}"
  npm pkg set "scripts.test=jest" "scripts.test:watch=jest --watch" "scripts.test:coverage=jest --coverage"

  # Create file structure
  echo -e "\n${BLUE}Creating directory structure...${NC}"
  mkdir -p src

  # Create initial test file
  echo -e "\n${BLUE}Creating initial test file...${NC}"
  cat > src/initial.test.ts << 'EOL'
describe('Initial configuration test', () => {
  it('should pass to verify that Jest is configured correctly', () => {
    expect(true).toBe(true);
  });
});
EOL

  # Run initial test
  echo -e "\n${BLUE}Running initial test to verify configuration...${NC}"
  npm test

  # Create example if requested
  create_node_example
}

# Function to create Node.js example
create_node_example() {
  echo -e "\n${BLUE}Do you want to create a function example with TDD? [y/n]${NC}"
  read -r create_example
  if [[ "$create_example" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo -e "${GREEN}Creating TDD example...${NC}"
    
    # Create test file
    cat > src/example.test.ts << 'EOL'
import { sum } from './example';

describe('Sum function', () => {
  it('should correctly add two positive numbers', () => {
    expect(sum(2, 3)).toBe(5);
  });
  
  it('should handle negative numbers', () => {
    expect(sum(-1, 1)).toBe(0);
    expect(sum(-1, -1)).toBe(-2);
  });
  
  it('should handle zero', () => {
    expect(sum(0, 5)).toBe(5);
    expect(sum(5, 0)).toBe(5);
    expect(sum(0, 0)).toBe(0);
  });
});
EOL

    # Create implementation file
    cat > src/example.ts << 'EOL'
/**
 * Adds two numbers and returns the result
 * @param a First number
 * @param b Second number
 * @returns The sum of a and b
 */
export function sum(a: number, b: number): number {
  return a + b;
}
EOL

    echo -e "${GREEN}Example created. Running example tests...${NC}"
    npm test
  fi
}

# Function to set up a Python project
setup_python() {
  echo -e "\n${BLUE}Setting up Python project...${NC}"

  # Check for python
  if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install it first.${NC}"
    return 1
  fi

  # Create virtual environment
  echo -e "\n${BLUE}Creating virtual environment...${NC}"
  python3 -m venv venv
  
  # Activate virtual environment
  if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    source venv/bin/activate
  elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
  else
    echo -e "${YELLOW}Could not automatically activate virtual environment.${NC}"
    echo -e "${YELLOW}Please activate it manually before continuing.${NC}"
  fi

  # Install testing tools
  echo -e "\n${BLUE}Installing testing tools...${NC}"
  pip install pytest pytest-cov

  # Create directory structure
  echo -e "\n${BLUE}Creating directory structure...${NC}"
  mkdir -p src tests

  # Create initial test file
  echo -e "\n${BLUE}Creating initial test file...${NC}"
  cat > tests/test_initial.py << 'EOL'
def test_initial_configuration():
    """Verify pytest is configured correctly."""
    assert True
EOL

  # Create pytest.ini
  echo -e "\n${BLUE}Creating pytest configuration...${NC}"
  cat > pytest.ini << 'EOL'
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
EOL

  # Run initial test
  echo -e "\n${BLUE}Running initial test to verify configuration...${NC}"
  python -m pytest tests/

  # Create example if requested
  create_python_example
}

# Function to create Python example
create_python_example() {
  echo -e "\n${BLUE}Do you want to create a function example with TDD? [y/n]${NC}"
  read -r create_example
  if [[ "$create_example" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo -e "${GREEN}Creating TDD example...${NC}"
    
    # Create test file
    cat > tests/test_calculator.py << 'EOL'
from src.calculator import sum_numbers

def test_sum_positive_numbers():
    """Test that the sum function can add positive numbers."""
    assert sum_numbers(2, 3) == 5

def test_sum_negative_numbers():
    """Test that the sum function can handle negative numbers."""
    assert sum_numbers(-1, 1) == 0
    assert sum_numbers(-1, -1) == -2

def test_sum_with_zero():
    """Test that the sum function works with zero."""
    assert sum_numbers(0, 5) == 5
    assert sum_numbers(5, 0) == 5
    assert sum_numbers(0, 0) == 0
EOL

    # Create module directory if it doesn't exist
    mkdir -p src

    # Create __init__.py to make it a proper package
    touch src/__init__.py

    # Create implementation file
    cat > src/calculator.py << 'EOL'
def sum_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b
EOL

    echo -e "${GREEN}Example created. Running example tests...${NC}"
    python -m pytest tests/
  fi
}

# Function to set up a Java project (Maven)
setup_java() {
  echo -e "\n${BLUE}Setting up Java project...${NC}"

  # Check for Java
  if ! command -v java &> /dev/null; then
    echo -e "${RED}Java is not installed. Please install it first.${NC}"
    return 1
  fi

  # Check for Maven
  if ! command -v mvn &> /dev/null; then
    echo -e "${RED}Maven is not installed. Please install it first.${NC}"
    return 1
  fi

  # Create Maven project
  echo -e "\n${BLUE}Creating Maven project...${NC}"
  mvn archetype:generate \
    -DgroupId=com.example \
    -DartifactId=tdd-project \
    -DarchetypeArtifactId=maven-archetype-quickstart \
    -DarchetypeVersion=1.4 \
    -DinteractiveMode=false

  # Change to project directory
  cd tdd-project

  # Update pom.xml to use JUnit 5
  echo -e "\n${BLUE}Updating POM to use JUnit 5...${NC}"
  sed -i.bak '/<dependencies>/,/<\/dependencies>/c\
  <dependencies>\
    <dependency>\
      <groupId>org.junit.jupiter</groupId>\
      <artifactId>junit-jupiter</artifactId>\
      <version>5.8.2</version>\
      <scope>test</scope>\
    </dependency>\
  </dependencies>\
  <build>\
    <plugins>\
      <plugin>\
        <groupId>org.apache.maven.plugins</groupId>\
        <artifactId>maven-surefire-plugin</artifactId>\
        <version>3.0.0-M5</version>\
      </plugin>\
      <plugin>\
        <groupId>org.apache.maven.plugins</groupId>\
        <artifactId>maven-compiler-plugin</artifactId>\
        <version>3.8.1</version>\
        <configuration>\
          <source>11</source>\
          <target>11</target>\
        </configuration>\
      </plugin>\
    </plugins>\
  </build>' pom.xml

  # Update App test to use JUnit 5
  echo -e "\n${BLUE}Updating initial test to use JUnit 5...${NC}"
  cat > src/test/java/com/example/AppTest.java << 'EOL'
package com.example;

import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

public class AppTest {
    @Test
    public void initialConfigurationTest() {
        assertTrue(true, "JUnit 5 is configured correctly");
    }
}
EOL

  # Run initial test
  echo -e "\n${BLUE}Running initial test to verify configuration...${NC}"
  mvn test

  # Create example if requested
  create_java_example
}

# Function to create Java example
create_java_example() {
  echo -e "\n${BLUE}Do you want to create a function example with TDD? [y/n]${NC}"
  read -r create_example
  if [[ "$create_example" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo -e "${GREEN}Creating TDD example...${NC}"
    
    # Create test file
    cat > src/test/java/com/example/CalculatorTest.java << 'EOL'
package com.example;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

public class CalculatorTest {
    @Test
    public void shouldAddPositiveNumbers() {
        Calculator calculator = new Calculator();
        assertEquals(5, calculator.sum(2, 3), "Should correctly add two positive numbers");
    }
    
    @Test
    public void shouldHandleNegativeNumbers() {
        Calculator calculator = new Calculator();
        assertEquals(0, calculator.sum(-1, 1), "Should handle negative with positive");
        assertEquals(-2, calculator.sum(-1, -1), "Should handle negative with negative");
    }
    
    @Test
    public void shouldHandleZero() {
        Calculator calculator = new Calculator();
        assertEquals(5, calculator.sum(5, 0), "Should handle zero as second param");
        assertEquals(5, calculator.sum(0, 5), "Should handle zero as first param");
        assertEquals(0, calculator.sum(0, 0), "Should handle zero for both params");
    }
}
EOL

    # Create implementation file
    cat > src/main/java/com/example/Calculator.java << 'EOL'
package com.example;

/**
 * Simple calculator class for TDD demonstration
 */
public class Calculator {
    /**
     * Adds two numbers and returns the result
     * 
     * @param a First number
     * @param b Second number
     * @return Sum of a and b
     */
    public int sum(int a, int b) {
        return a + b;
    }
}
EOL

    echo -e "${GREEN}Example created. Running example tests...${NC}"
    mvn test
  fi
}

# Function to set up a Ruby project
setup_ruby() {
  echo -e "\n${BLUE}Setting up Ruby project...${NC}"

  # Check for Ruby
  if ! command -v ruby &> /dev/null; then
    echo -e "${RED}Ruby is not installed. Please install it first.${NC}"
    return 1
  fi

  # Check for Bundler
  if ! command -v bundle &> /dev/null; then
    echo -e "${YELLOW}Bundler is not installed. Installing Bundler...${NC}"
    gem install bundler
    if [ $? -ne 0 ]; then
      echo -e "${RED}Failed to install Bundler. Please check your Ruby installation.${NC}"
      return 1
    fi
  fi

  # Create project directory if we're not already in a Ruby project
  if [ ! -f Gemfile ]; then
    echo -e "${YELLOW}Gemfile not found. Creating a new Ruby project...${NC}"
    
    # Create Gemfile
    cat > Gemfile << 'EOL'
source 'https://rubygems.org'

gem 'rspec', '~> 3.12'
gem 'simplecov', '~> 0.22.0', require: false
EOL
  fi

  # Install dependencies
  echo -e "\n${BLUE}Installing dependencies with Bundler...${NC}"
  bundle install

  # Initialize RSpec
  echo -e "\n${BLUE}Initializing RSpec...${NC}"
  mkdir -p spec
  bundle exec rspec --init

  # Update spec_helper.rb to add SimpleCov
  cat >> spec/spec_helper.rb << 'EOL'

# Enable code coverage with SimpleCov
require 'simplecov'
SimpleCov.start do
  add_filter '/spec/'
end
EOL

  # Create project structure
  echo -e "\n${BLUE}Creating project structure...${NC}"
  mkdir -p lib

  # Create initial test file
  echo -e "\n${BLUE}Creating initial test file...${NC}"
  cat > spec/initial_spec.rb << 'EOL'
require 'spec_helper'

describe 'Initial configuration' do
  it 'verifies that RSpec is configured correctly' do
    expect(true).to be true
  end
end
EOL

  # Run initial test
  echo -e "\n${BLUE}Running initial test to verify configuration...${NC}"
  bundle exec rspec spec/initial_spec.rb

  # Create example if requested
  create_ruby_example
}

# Function to create Ruby example
create_ruby_example() {
  echo -e "\n${BLUE}Do you want to create a function example with TDD? [y/n]${NC}"
  read -r create_example
  if [[ "$create_example" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo -e "${GREEN}Creating TDD example...${NC}"

    # Create test file
    cat > spec/calculator_spec.rb << 'EOL'
require 'spec_helper'
require_relative '../lib/calculator'

describe Calculator do
  describe '#sum' do
    let(:calculator) { Calculator.new }

    it 'correctly adds two positive numbers' do
      expect(calculator.sum(2, 3)).to eq(5)
    end

    it 'handles negative numbers' do
      expect(calculator.sum(-1, 1)).to eq(0)
      expect(calculator.sum(-1, -1)).to eq(-2)
    end

    it 'handles zero' do
      expect(calculator.sum(0, 5)).to eq(5)
      expect(calculator.sum(5, 0)).to eq(5)
      expect(calculator.sum(0, 0)).to eq(0)
    end
  end
end
EOL

    # Create implementation file
    cat > lib/calculator.rb << 'EOL'
# Calculator class for TDD demonstration
class Calculator
  # Adds two numbers and returns the result
  #
  # @param a [Numeric] First number
  # @param b [Numeric] Second number
  # @return [Numeric] Sum of a and b
  def sum(a, b)
    a + b
  end
end
EOL

    echo -e "${GREEN}Example created. Running example tests...${NC}"
    bundle exec rspec spec/calculator_spec.rb
  fi
}

# Select language
select_language() {
  echo -e "${PURPLE}Select the programming language for your TDD project:${NC}"
  echo -e "${YELLOW}1. Node.js/TypeScript${NC}"
  echo -e "${YELLOW}2. Python${NC}"
  echo -e "${YELLOW}3. Java${NC}"
  echo -e "${YELLOW}4. Ruby${NC}"
  read -r lang_choice

  case $lang_choice in
    1)
      setup_node
      ;;
    2)
      setup_python
      ;;
    3)
      setup_java
      ;;
    4)
      setup_ruby
      ;;
    *)
      echo -e "${RED}Invalid choice. Please select a valid option.${NC}"
      select_language
      ;;
  esac
}

# Main execution
select_language

# Success message
if [ $? -eq 0 ]; then
  echo -e "\n${GREEN}==================================================${NC}"
  echo -e "${GREEN}     TDD CONFIGURATION COMPLETED SUCCESSFULLY!     ${NC}"
  echo -e "${GREEN}==================================================${NC}"
  echo -e "\n${BLUE}Happy coding with TDD!${NC}"
else
  echo -e "\n${RED}==================================================${NC}"
  echo -e "${RED}ERROR: Configuration was not completed successfully${NC}"
  echo -e "${RED}==================================================${NC}"
  echo -e "\nPlease review the error messages above."
fi 