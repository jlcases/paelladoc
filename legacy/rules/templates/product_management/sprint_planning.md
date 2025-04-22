# Sprint Planning: {{sprint_name}} ({{sprint_id}})

## Overview
**Start Date:** {{start_date}}
**End Date:** {{end_date}}
**Duration:** {{duration}} days
**Capacity:** {{capacity}} points

## Sprint Goal
{{sprint_goal}}

## Team Members
{{#each team_members}}
- **{{name}}** - Availability: {{availability}}%
{{/each}}

## Selected User Stories
{{#each user_stories}}
### {{id}}: {{title}} ({{points}} points)
**Priority:** {{priority}}

{{description}}

**Acceptance Criteria:**
{{#each acceptance_criteria}}
- [ ] {{this}}
{{/each}}

**Tasks:**
{{#each tasks}}
- [ ] {{title}} ({{estimate}}h) {{#if assignee}}@{{assignee}}{{/if}}
{{/each}}

---
{{/each}}

## Sprint Metrics
- **Total Stories:** {{total_stories}}
- **Total Points:** {{total_points}}
- **Previous Sprint Velocity:** {{previous_velocity}}
- **Confidence Level:** {{confidence_level}}

## Risks and Dependencies
{{#each risks}}
- **{{title}}** - {{description}} (Mitigation: {{mitigation}})
{{/each}}

## Definition of Done
{{#each definition_of_done}}
- [ ] {{this}}
{{/each}}

## Action Items
{{#each action_items}}
- [ ] {{description}} ({{assignee}}, Due: {{due_date}})
{{/each}}

## Notes
{{notes}}

---
**Meeting Date:** {{meeting_date}}
**Facilitator:** {{facilitator}}
**Attendees:** {{attendees}} 