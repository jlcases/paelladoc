# User Story: {{id}}

## Title
{{title}}

## Description
**As a** {{role}}
**I want to** {{action}}
**So that** {{benefit}}

## Acceptance Criteria
{{#each acceptance_criteria}}
- [ ] {{this}}
{{/each}}

## Additional Details
- **Priority:** {{priority}}
- **Story Points:** {{points}}
- **Sprint:** {{sprint}}
{{#if epic}}
- **Epic:** {{epic}}
{{/if}}
{{#if assignee}}
- **Assignee:** {{assignee}}
{{/if}}

## Dependencies
{{#if dependencies}}
{{#each dependencies}}
- {{this}}
{{/each}}
{{else}}
None
{{/if}}

## Technical Notes
{{#if technical_notes}}
{{technical_notes}}
{{else}}
None at this time.
{{/if}}

## UI/UX Considerations
{{#if ui_ux_considerations}}
{{ui_ux_considerations}}
{{else}}
None specified.
{{/if}}

## Testing Approach
{{#if testing_approach}}
{{testing_approach}}
{{else}}
Standard testing procedures apply.
{{/if}}

---
**Created:** {{created_date}}
**Last Updated:** {{updated_date}}
**Status:** {{status}} 