---
name: implement-increment
description: Orchestrate implementation of feature increment
argument-hint: [issue-key] [state-management-file-path]
model: claude-3-5-sonnet-latest
---

# Implement Increment Command

## Purpose

Implement the increment using the specification in the state management file.
$1 contains the issue key, $2 contains the path to the state management file.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Ensure that the specification was explicitly signed off by the user. If not, go back to the specification signoff step in the larger workflow.

2. Update issue status to "In Progress":
   - Use the SlashCommand tool to execute `/update-issue $1 "In Progress"`

3. Add implementation comment:
   - Read the state management file ($2) to get the specification file name
   - Use the SlashCommand tool to execute `/create-comment $1 "Claude Code implementation started for [specification-file-name]"`

4. Understand the division of work and implement tasks:
    - Read specification to identify agent_ids
    - For each agent_id: Use the Task tool to spawn a subagent with prompt: "Implement tasks for agent_id [agent_id] in specification at $2. Only implement tasks assigned to [agent_id]. Follow all guidelines in @CLAUDE.md." For tasks that can be done in parallel where dependencies are fulfilled, spawn subagents in parallel.
    - Monitor subagent progress
    - Keep an updated list of TODOs in the state management file, including subagent status
    - When all agent_ids are complete, implementation is finished

## This part of the workflow is done when

- [ ] All subagents are complete
- [ ] Single behavior is fully implemented, both on the backend and the frontend
- [ ] All unit and integration tests pass
- [ ] All quality gates pass (see @CLAUDE.md for commands)
- [ ] No breaking changes introduced
- [ ] No test failures introduced in areas of the code unrelated to this increment
- [ ] Feature works in both development and build modes
- [ ] Business rules are enforced consistently
