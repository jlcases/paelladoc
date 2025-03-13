/**
 * MDC Generation Command Line Interface
 * This file provides a command-line interface for generating MDC files
 * from project documentation.
 */

const { generateMDC } = require('./mdc_generation');
const path = require('path');
const fs = require('fs');

/**
 * Main function to generate an MDC file from command line arguments
 */
function main() {
  // Get command line arguments
  const args = process.argv.slice(2);
  
  // Parse arguments
  const projectName = args[0];
  const outputPath = args[1] || `docs/${projectName}/`;
  
  if (!projectName) {
    console.error('Error: Project name is required');
    console.log('Usage: node generate_mdc.js <project_name> [output_path]');
    process.exit(1);
  }
  
  console.log(`Generating MDC for project: ${projectName}`);
  
  // Get development info from project documentation
  const developmentInfo = extractDevelopmentInfo(projectName);
  
  // Generate the MDC file
  const result = generateMDC({
    projectName,
    outputPath,
    filename: `${projectName}.mdc.example`,  // Use .example extension
    developmentInfo,
    mode: "orchestrator",
    referenceDoc: true,
    documentationRoot: `docs/${projectName}/`,
    structureType: "reference"
  });
  
  console.log(`MDC file generated successfully at: ${result.file_path}`);
  console.log(`Rule count: ${result.rule_count}`);
  console.log(`Pattern count: ${result.pattern_count}`);
  console.log(`Instruction count: ${result.instruction_count}`);
  
  // Create a copy in the project root directory if it doesn't exist there
  ensureProjectRootMDC(projectName, result.file_path);
}

/**
 * Ensures a copy of the MDC exists in the project root directory
 */
function ensureProjectRootMDC(projectName, sourcePath) {
  const projectRootPath = path.resolve(process.cwd());
  const targetPath = path.join(projectRootPath, `${projectName}.mdc.example`);
  
  // Don't copy if the source is already in the project root
  if (path.resolve(sourcePath) === path.resolve(targetPath)) {
    return;
  }
  
  // Copy the MDC file to project root
  fs.copyFileSync(sourcePath, targetPath);
  console.log(`MDC file also copied to project root: ${targetPath}`);
  console.log('Remember to rename it to ${projectName}.mdc when using in your development project.');
}

/**
 * Extracts development information from project documentation
 */
function extractDevelopmentInfo(projectName) {
  const projectDocsPath = path.join('docs', projectName);
  const info = {
    description: '',
    architecture: [],
    components: [],
    api: [],
    database: []
  };
  
  // Try to read project description from index file
  const indexPath = path.join(projectDocsPath, '00_index.md');
  if (fs.existsSync(indexPath)) {
    const content = fs.readFileSync(indexPath, 'utf8');
    // Extract description from first paragraphs
    const firstParagraphs = content.split('\n\n').slice(0, 3).join(' ');
    info.description = firstParagraphs.substring(0, 200) + (firstParagraphs.length > 200 ? '...' : '');
  }
  
  return info;
}

// Run the script if called directly
if (require.main === module) {
  main();
}

module.exports = {
  generateProjectMDC: main
}; 