/**
 * MDC Cleanup and Consolidation Script
 * This script consolidates multiple MDC files into a single orchestrator file
 * and moves functionality from individual MDC files into the main orchestrator.
 */

const fs = require('fs');
const path = require('path');

/**
 * Main function to consolidate MDC files
 */
function consolidateMDCFiles() {
  console.log('Starting MDC consolidation process...');
  
  const rulesDir = path.join('.cursor', 'rules');
  const mainMDCPath = path.join(rulesDir, 'paelladoc.mdc');
  const codeAnalysisPath = path.join(rulesDir, 'code_analysis.mdc');
  const workflowPath = path.join(rulesDir, 'documentation_workflow.mdc');
  
  // Read the main MDC file
  console.log('Reading main MDC file...');
  let mainMDCContent = '';
  if (fs.existsSync(mainMDCPath)) {
    mainMDCContent = fs.readFileSync(mainMDCPath, 'utf8');
  } else {
    console.error('Main MDC file not found!');
    process.exit(1);
  }
  
  // Read code analysis MDC if it exists
  console.log('Reading code analysis MDC...');
  let codeAnalysisContent = '';
  if (fs.existsSync(codeAnalysisPath)) {
    codeAnalysisContent = fs.readFileSync(codeAnalysisPath, 'utf8');
  }
  
  // Read workflow MDC if it exists
  console.log('Reading documentation workflow MDC...');
  let workflowContent = '';
  if (fs.existsSync(workflowPath)) {
    workflowContent = fs.readFileSync(workflowPath, 'utf8');
  }
  
  // Extract useful parts from code analysis and append to main MDC
  console.log('Consolidating MDC files...');
  let updatedMainMDC = mainMDCContent;
  
  // Check if main MDC already has code_analysis section
  if (!updatedMainMDC.includes('"code_analysis":') && codeAnalysisContent) {
    try {
      const codeAnalysisObj = JSON.parse(codeAnalysisContent);
      
      // Create a backup of the main MDC file
      fs.writeFileSync(`${mainMDCPath}.backup`, mainMDCContent, 'utf8');
      console.log(`Backup created at ${mainMDCPath}.backup`);
      
      // Find a good place to insert code analysis content (before the last command)
      const lastCommandIndex = updatedMainMDC.lastIndexOf('  ');
      if (lastCommandIndex !== -1) {
        const beforeLastCommand = updatedMainMDC.substring(0, lastCommandIndex);
        const afterLastCommand = updatedMainMDC.substring(lastCommandIndex);
        
        // Add code analysis as a new property
        updatedMainMDC = beforeLastCommand + 
          '  code_analysis: ' + JSON.stringify(codeAnalysisObj, null, 2) + '\n' + 
          afterLastCommand;
        
        console.log('Added code analysis content to main MDC');
      }
    } catch (e) {
      console.error('Error parsing code analysis MDC:', e.message);
    }
  } else {
    console.log('Code analysis section already exists in main MDC or no content available');
  }
  
  // Check if main MDC already has workflow section
  if (!updatedMainMDC.includes('"documentation_workflow":') && workflowContent) {
    try {
      const workflowObj = JSON.parse(workflowContent);
      
      // Find a good place to insert workflow content (before the last command)
      const lastCommandIndex = updatedMainMDC.lastIndexOf('  ');
      if (lastCommandIndex !== -1) {
        const beforeLastCommand = updatedMainMDC.substring(0, lastCommandIndex);
        const afterLastCommand = updatedMainMDC.substring(lastCommandIndex);
        
        // Add workflow as a new property
        updatedMainMDC = beforeLastCommand + 
          '  documentation_workflow: ' + JSON.stringify(workflowObj, null, 2) + '\n' + 
          afterLastCommand;
        
        console.log('Added workflow content to main MDC');
      }
    } catch (e) {
      console.error('Error parsing workflow MDC:', e.message);
    }
  } else {
    console.log('Workflow section already exists in main MDC or no content available');
  }
  
  // Save the updated main MDC file
  fs.writeFileSync(mainMDCPath, updatedMainMDC, 'utf8');
  console.log(`Updated main MDC file saved to ${mainMDCPath}`);
  
  // Create backup files for the ones we'll eventually remove
  if (fs.existsSync(codeAnalysisPath)) {
    fs.writeFileSync(`${codeAnalysisPath}.backup`, codeAnalysisContent, 'utf8');
    console.log(`Backup created at ${codeAnalysisPath}.backup`);
  }
  
  if (fs.existsSync(workflowPath)) {
    fs.writeFileSync(`${workflowPath}.backup`, workflowContent, 'utf8');
    console.log(`Backup created at ${workflowPath}.backup`);
  }
  
  console.log('MDC consolidation complete.');
  console.log('You can now review the updated main MDC file and, if satisfied, delete the other MDC files.');
  console.log('Backups have been created with .backup extension.');
}

// Run the script if called directly
if (require.main === module) {
  consolidateMDCFiles();
}

module.exports = {
  consolidateMDCFiles
}; 