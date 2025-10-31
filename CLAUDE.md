## Repository Purpose

Claude Constructor is a workflow automation plugin for Claude Code that guides feature development through structured planning, validation, implementation, and review steps. This repository contains the plugin's orchestration commands and specialized agents.

## Architecture

### Plugin Structure

```text
.claude-plugin/
└── marketplace.json          # Marketplace definition, points to plugins/

plugins/claude-constructor/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/                # Slash commands (orchestration)
│   ├── feature.md           # Main orchestrator for /feature workflow
│   ├── issue/               # Issue tracking integration commands
│   └── *.md                 # Individual workflow step commands
├── agents/                  # Specialized agents (subagents)
│   ├── code-reviewer.md
│   ├── increment-implementer.md
│   ├── requirements-definer.md
│   ├── requirements-validator.md
│   ├── specification-validator.md
│   └── specification-writer.md
└── docs/
    └── git-commit.md        # Example git commit guidelines
```

### Key Concepts

**Commands vs Agents:**

- **Commands** (`commands/*.md`): Slash commands that orchestrate workflow steps. The main user-facing command is `/feature`. Other commands are called internally by the orchestrator.
- **Agents** (`agents/*.md`): Specialized subagents for complex tasks (requirements definition, specification writing, validation). Called by commands using the Task tool with `subagent_type`.

**State Management:**

- Workflow progress tracked in `state_management/{issue_key}.md` files (created in projects that use the plugin)
- Each workflow step updates the state file with its outputs
- Enables resumable workflows and cross-step communication

**Specifications:**

- Created in `specifications/{issue_key}_specification_{timestamp}.md` (in target projects)
- Contains Requirements Definition and Implementation Plan sections
- Used throughout implementation and review phases

**Code Reviews:**

- Review history tracked in `code_reviews/{issue_key}.md` files (created in target projects)
- Each review iteration appends findings, verdict, and quality gate results
- Implementation team reads latest review when addressing feedback

### Workflow Orchestration

The `/feature` command (in `commands/feature.md`) orchestrates a sequential workflow:

1. **Planning phase**: Read config → Create state file → Read settings → Read issue → Define requirements → Validate requirements → Requirements sign-off → Write specification → Validate specification → Specification sign-off
2. **Implementation phase**: Checkout branch → Implement → Security review → Write E2E tests
3. **Review phase**: Code review → Create PR → Review PR

Each step is a separate command. The orchestrator blocks until user sign-off at the **requirements sign-off** and **specification sign-off** steps.

### Issue Tracking Integration

Commands in `commands/issue/` support multiple providers:

- **Linear**: Uses MCP tools (`linear:get_issue`, `linear:update_issue`, etc.)
- **Jira**: Uses MCP tools (`jira:get_issue`, `jira:transition_issue`, etc.)
- **Prompt mode**: No external system, generates local issue keys (`prompt-1`, `prompt-2`)

Provider is auto-detected by checking for MCP tool availability.

### Agent Execution Pattern

Specialized agents (in `agents/`) follow this pattern:

1. **Parse input**: Extract state management file path and optional user feedback
2. **Read state**: Load current workflow context
3. **Determine mode**: Creation vs revision based on existing content
4. **Gather context**: Explore codebase briefly to understand existing patterns
5. **Execute task**: Define requirements, write spec, or validate
6. **Update state**: Write outputs to specification file and update state management

## Settings

Settings are passed as optional arguments to `/feature` and stored in the state management file:

- `--provider=<linear|jira|prompt>`: Override issue tracking provider (auto-detected if not specified)
- `--silent=<true|false>`: Skip external API calls for testing (default: false)

Example: `/feature ABC-123 --provider=prompt --silent=true`

Settings are auto-detected on first use and stored in the state management file as the single source of truth.

## Markdown Development

Markdown files use strict linting via markdownlint:

- Configuration: `.markdownlint.json` disables MD013 (line length), MD029 (ordered list prefix), MD033 (HTML), MD041 (first line heading)
- VS Code auto-formats on save if markdownlint extension is installed (see `.vscode/settings.json`)
- All command and agent files are markdown with YAML frontmatter

## Important Patterns

### Workflow Integration

Commands are called sequentially by the orchestrator. Each command:

- Must complete all steps without skipping
- Should update the state management file with its outputs
- Should fail gracefully and log errors without blocking workflow

## Testing Workflow Changes

When modifying workflow commands or agents:

1. Use `--silent=true` argument to skip external API calls (e.g., `/feature ABC-123 --silent=true`)
2. Test with `/feature prompt-test-description` to avoid needing real issues
3. Check `state_management/`, `specifications/`, and `code_reviews/` outputs in target project
4. Verify all workflow steps complete in sequence without hanging or skipping steps
