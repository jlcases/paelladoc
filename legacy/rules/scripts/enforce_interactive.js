/**
 * INTERACTIVE MODE ENFORCER
 * 
 * This script ensures that the GENERATE_DOC command runs in interactive mode,
 * presenting users with a menu and waiting for their selection.
 */

const INTERACTIVE_MENU = `
Based on my analysis of the repository content, I can help you generate various types of documentation.
What would you like to document? Here are your options:

**Technical Documentation:**
1. Technical Architecture
2. API Documentation
3. Component Specifications
4. Database Schema
5. Dependencies

**Product Documentation (Required for Business Documentation):**
6. User Stories
7. Problem Definition
8. Value Proposition

**User Documentation:**
9. Installation Guide
10. Usage Guide

**Developer Documentation:**
11. Setup Instructions
12. Contribution Guidelines

**Business Documentation (Requires Product Documentation):**
13. Market Research
14. Business Model
15. Competitive Analysis

**Other Options:**
16. All Technical Documentation
17. All Product Documentation
18. Everything
19. I'm Done

Please indicate which documentation you'd like to generate (you can select multiple options).
Note: Business Documentation options will only be available after generating Product Documentation.
`;

// Export the interactive menu for use by the AI
module.exports = {
  INTERACTIVE_MENU,
  
  // Enforce interactive mode for GENERATE_DOC
  enforceInteractiveMode: function(command) {
    if (command === 'GENERATE_DOC') {
      console.log('INTERACTIVE MODE ENFORCED');
      return {
        interactive: true,
        requireSelection: true,
        preventAutoGeneration: true,
        menu: INTERACTIVE_MENU,
        validationRules: {
          'Market Research': ['Problem Definition', 'Value Proposition', 'User Stories'],
          'Business Model': ['Problem Definition', 'Value Proposition', 'User Stories'],
          'Competitive Analysis': ['Problem Definition', 'Value Proposition']
        }
      };
    }
    return null;
  },
  
  // Verify that the AI is following the interactive flow
  verifyInteractiveFlow: function(step, hasUserSelection) {
    if (step === 'documentation_generation' && !hasUserSelection) {
      throw new Error('INTERACTIVE MODE VIOLATION: Cannot generate documentation without user selection');
    }
    return true;
  }
}; 