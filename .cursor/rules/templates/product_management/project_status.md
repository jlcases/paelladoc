# Project Status Report: {{project_name}}

## Executive Summary
**Reporting Period:** {{start_date}} to {{end_date}}
**Overall Status:** {{overall_status}} {{#if status_icon}}{{status_icon}}{{/if}}
**Project Manager:** {{project_manager}}

{{executive_summary}}

## Project Timeline
**Start Date:** {{project_start_date}}
**End Date:** {{project_end_date}}
**Current Phase:** {{current_phase}}
**Days Remaining:** {{days_remaining}}
**Completion:** {{completion_percentage}}%

```
{{timeline_chart}}
```

## Recent Milestones
{{#each recent_milestones}}
- **{{name}}**: {{status}} - {{completion_date}}
{{/each}}

## Upcoming Milestones
{{#each upcoming_milestones}}
- **{{name}}**: Due {{due_date}} ({{days_away}} days away)
{{/each}}

## Sprint Status
{{#each sprint_status}}
### Sprint {{name}} ({{id}})
- **Status:** {{status}}
- **Progress:** {{progress}}%
- **Key Deliverables:** {{key_deliverables}}
- **End Date:** {{end_date}}
{{/each}}

## Team Velocity
```
{{velocity_chart}}
```

## Key Achievements
{{#each key_achievements}}
- {{this}}
{{/each}}

## Current Focus Areas
{{#each current_focus}}
- {{this}}
{{/each}}

## Blockers & Risks
{{#each blockers}}
### {{title}} (Impact: {{impact}})
{{description}}
- **Mitigation:** {{mitigation}}
- **Owner:** {{owner}}
- **Status:** {{status}}
{{/each}}

## Resource Allocation
```
{{resource_allocation_chart}}
```

## Budget Status
- **Total Budget:** {{currency}}{{total_budget}}
- **Spent to Date:** {{currency}}{{spent_to_date}} ({{budget_percentage}}%)
- **Projected Final:** {{currency}}{{projected_final}}
- **Variance:** {{currency}}{{budget_variance}} ({{budget_variance_percentage}}%)

## Quality Metrics
{{#each quality_metrics}}
- **{{name}}:** {{value}} {{#if trend}}({{trend}}){{/if}}
{{/each}}

## Customer/Stakeholder Updates
{{customer_stakeholder_updates}}

## Decisions Needed
{{#each decisions_needed}}
- **{{title}}** - {{description}}
  - **Options:** {{options}}
  - **Recommendation:** {{recommendation}}
  - **Due By:** {{due_date}}
{{/each}}

## Next Steps
{{#each next_steps}}
- {{this}}
{{/each}}

## Attachments
{{#each attachments}}
- [{{name}}]({{url}})
{{/each}}

---
**Report Prepared By:** {{prepared_by}}
**Date:** {{report_date}}
**Distribution:** {{distribution_list}} 