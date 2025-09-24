---
name: implement-sub-increment
description: Implement assigned tasks from specification
argument-hint: [state-management-file-path] [agent-id]
model: claude-3-5-sonnet-latest
---

# Implement Sub-Increment Command

## Purpose

Implement the sub-increment for the issue described in $ARGUMENTS, using the specification linked in $ARGUMENTS.
Your agent_id can be found in $ARGUMENTS.
You must only do the work that has your agent_id associated with it. 
This command is called by an orchestrating command, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Implement the sub-increment, in accordance with @CLAUDE.md

2. Keep an updated list of TODOs and update status

3. The increment is done when all tasks assigned to you are done

4. Report DONE to the orchestrating command
