---
model: claude-sonnet-4-20250514
---

# Implement Increment Command

## Purpose

Implement the increment for the issue described in $ARGUMENTS, using the specification linked in $ARGUMENTS.
This command is called by an orchestrating command, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Update issue status to "In Progress" - run the .claude/commands/ticket-update-issue.md command, passing the issue key and new status as arguments to it

Get the issue key from the state management file in $ARGUMENTS.

Format the arguments as:
```
Ticket Number: [issue key from state management file]
New Status: In Progress
```

2. Add implementation comment - run the .claude/commands/ticket-create-comment.md command, passing the issue key and comment as arguments to it

Format the arguments as:
```
Ticket Number: [issue key from state management file]
Comment Text: Claude Code implementation started for {name of specification file linked in $ARGUMENTS}
```

3. Understand the division of work and spawn sub-agents:
   a. Read specification to identify agent_ids
   b. For each agent_id: spawn a sub-agent using the Task tool, with agent_id and $ARGUMENTS as arguments to it. For tasks that can be done in parallel, and where dependencies are fulfilled, spawn sub-agents in parallel.
   c. Monitor sub-agent progress
   d. Keep an updated list of TODOs in $ARGUMENTS, including sub-agent status
   e. When monitoring completes for all agent_ids, proceed to step 4

4. Report DONE to the orchestrating command

## This part of the workflow is done when

- [ ] All sub-agents report DONE
- [ ] Single behavior is fully implemented, both on the backend and the frontend
- [ ] All unit and integration tests pass
- [ ] All quality gates pass (see `/CLAUDE.md` for commands)
- [ ] No breaking changes introduced
- [ ] No test failures introduced in areas of the code unrelated to this increment
- [ ] Feature works in both development and build modes
- [ ] Business rules are enforced consistently
