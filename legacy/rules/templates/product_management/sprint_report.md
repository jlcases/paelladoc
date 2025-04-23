# Sprint Report: {{sprint_name}} ({{sprint_id}})

## Overview
**Duration:** {{start_date}} to {{end_date}}
**Sprint Goal:** {{sprint_goal}}
**Team:** {{team_name}}

## Summary Metrics
- **Planned Story Points:** {{planned_points}}
- **Completed Story Points:** {{completed_points}}
- **Completion Rate:** {{completion_percentage}}%
- **Added Scope:** {{added_scope}} points
- **Velocity:** {{velocity}} points

## Burndown Chart
```
{{burndown_chart}}
```

## Completed User Stories
{{#each completed_stories}}
- **{{id}}:** {{title}} ({{points}} points)
  - **Description:** {{description}}
  - **Acceptance Criteria Met:** {{#each acceptance_criteria}}{{#if @index}}, {{/if}}{{this}}{{/each}}
{{/each}}

## Incomplete User Stories
{{#each incomplete_stories}}
- **{{id}}:** {{title}} ({{points}} points)
  - **Status:** {{status}}
  - **Reason:** {{reason_incomplete}}
  - **Plan:** {{plan_for_next_sprint}}
{{/each}}

## Key Achievements
{{#each achievements}}
- {{this}}
{{/each}}

## Technical Debt and Quality
{{#each technical_debt_items}}
- **{{title}}** - {{description}}
  - **Impact:** {{impact}}
  - **Proposed Solution:** {{solution}}
{{/each}}

## Bugs Found/Fixed
### Found
{{#each bugs_found}}
- **{{id}}:** {{title}} (Priority: {{priority}})
{{/each}}

### Fixed
{{#each bugs_fixed}}
- **{{id}}:** {{title}}
{{/each}}

## Team Health
- **Workload Balance:** {{workload_balance}}
- **Team Morale:** {{team_morale}}
- **Collaboration Level:** {{collaboration_level}}

## Retrospective Summary
### What Went Well
{{#each went_well}}
- {{this}}
{{/each}}

### What Could Be Improved
{{#each to_improve}}
- {{this}}
{{/each}}

### Action Items for Next Sprint
{{#each action_items}}
- [ ] {{description}} ({{assignee}})
{{/each}}

## Next Sprint Preview
- **Projected Velocity:** {{projected_velocity}}
- **Recommended Focus Areas:** {{recommended_focus}}
- **Capacity Adjustments:** {{capacity_adjustments}}

## Attachments
{{#each attachments}}
- [{{name}}]({{url}})
{{/each}}

---
**Report Prepared By:** {{prepared_by}}
**Date:** {{report_date}} 