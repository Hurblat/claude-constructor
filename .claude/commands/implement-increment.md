# Implement Increment Command

## Purpose

Implement the increment using the specification in the state management file.
$ARGUMENTS contains the path to the state management file.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Ensure that the specification was explicitly signed off by the user. If not, go back to the specification signoff step in the larger workflow.

2. Update issue status to "In Progress" - read .claude/commands/issue/update-issue.md and follow the instructions

Get the issue key from the state management file (path in $ARGUMENTS).

Format the arguments as:
```
Issue Key: [issue key from state management file]
New Status: In Progress
```

3. Add implementation comment - read .claude/commands/issue/create-comment.md and follow the instructions

Format the arguments as:
```
Issue Key: [issue key from state management file]
Comment Text: Claude Code implementation started for [name of specification file]
```

4. Understand the division of work and spawn subagents:
    - Read specification to identify agent_ids
    - For each agent_id: spawn a subagent using the Task tool, providing the agent_id and state management file path. For tasks that can be done in parallel, and where dependencies are fulfilled, spawn subagents in parallel.
    - Monitor subagent progress
    - Keep an updated list of TODOs in the state management file, including subagent status
    - When monitoring completes for all agent_ids, proceed to step 4

5. Report DONE and continue with the next workflow step

## This part of the workflow is done when

- [ ] All subagents report DONE
- [ ] Single behavior is fully implemented, both on the backend and the frontend
- [ ] All unit and integration tests pass
- [ ] All quality gates pass (see @CLAUDE.md for commands)
- [ ] No breaking changes introduced
- [ ] No test failures introduced in areas of the code unrelated to this increment
- [ ] Feature works in both development and build modes
- [ ] Business rules are enforced consistently
