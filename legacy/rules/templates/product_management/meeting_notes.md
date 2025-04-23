# Meeting Notes: {{meeting_title}}

## Meeting Details
**Date:** {{meeting_date}}
**Time:** {{start_time}} - {{end_time}}
**Location:** {{location}}
**Meeting Type:** {{meeting_type}}

## Attendees
### Present
{{#each attendees_present}}
- {{this}}
{{/each}}

### Absent
{{#each attendees_absent}}
- {{this}}
{{/each}}

## Agenda
{{#each agenda_items}}
1. **{{title}}** - {{#if duration}}({{duration}} min){{/if}}
{{/each}}

## Discussion Notes
{{#each discussion_items}}
### {{title}}
{{content}}

{{/each}}

## Key Decisions
{{#each decisions}}
- **Decision:** {{description}}
  - **Context:** {{context}}
  - **Rationale:** {{rationale}}
  - **Impact:** {{impact}}
{{/each}}

## Action Items
{{#each action_items}}
- [ ] **{{description}}**
  - **Assignee:** {{assignee}}
  - **Due Date:** {{due_date}}
  - **Priority:** {{priority}}
{{/each}}

## Blocked Items / Issues
{{#each blocked_items}}
- **{{title}}** - {{description}}
  - **Blocker:** {{blocker}}
  - **Next Steps:** {{next_steps}}
{{/each}}

## Sprint Status Update
{{#if sprint_status}}
- **Sprint:** {{sprint_name}} ({{sprint_id}})
- **Completed Points:** {{completed_points}}/{{total_points}}
- **On Track:** {{on_track}}
- **Blockers:** {{blockers}}
{{/if}}

## Project Risks
{{#each risks}}
- **{{title}}** ({{severity}}) - {{description}}
  - **Mitigation:** {{mitigation}}
{{/each}}

## Next Meeting
**Date:** {{next_meeting_date}}
**Time:** {{next_meeting_time}}
**Agenda Items:**
{{#each next_meeting_agenda}}
- {{this}}
{{/each}}

## Additional Notes
{{additional_notes}}

---
**Minutes Taken By:** {{minutes_taker}}
**Minutes Approved By:** {{minutes_approver}}
**Distribution List:** {{distribution_list}} 