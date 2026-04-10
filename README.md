# CyberTicket: Automated IT Support Desk

## Environment Motivation
CyberTicket simulates a real-world IT Support Desk environment where an AI agent must handle incoming support tickets effectively. The agent is responsible for prioritizing urgency, escalating major issues, and categorizing common requests to reduce operational burden while maintaining acceptable system load.

## Action Definition
- **TicketAction**:
  - `ticket_id`: the identification of the ticket
  - `action_type`: one of `[categorize, escalate, close]`
  - `value`: context-specific value (category name, user to assign, or close reason)

## Observation Definition
- **TicketObs**:
  - `active_tickets`: list of current open tickets.
  - `system_load`: a float between 0.0 and 1.0 representing computational/human load.
  - `last_action_status`: text summary or error from the previous action.

## Reproducible Baseline Scores
- **GPT-4 (Easy)**: Score: ~0.60
- **GPT-4 (Medium)**: Score: ~1.00
- **GPT-4 (Hard)**: Score: ~0.80

*(Tested with standard prompting techniques.)*
