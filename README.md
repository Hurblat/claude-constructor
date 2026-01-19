# Claude Constructor

A workflow automation plugin for Claude Code that guides feature development through structured planning, validation, and review—with human approval gates at every critical decision point.

## Why Use This?

| Problem | Solution |
|---------|----------|
| Claude loses focus mid-implementation | Structured workflow with state tracking prevents drift |
| Unplanned changes and scope creep | Requirements and spec sign-off gates before coding begins |
| Implementation differs from intent | Detailed specifications with parallel execution plans |
| No visibility into Claude's assumptions | Transparent requirements definition you approve |
| Code ships without review | Built-in code review and security audit before PR |

## Quick Start

```bash
# 1. Add the marketplace
/plugin marketplace add https://github.com/Hurblat/claude-constructor

# 2. Install the plugin
/plugin install claude-constructor@hurblat-plugins

# 3. Start your first feature
/feature Add dark mode toggle to settings page
```

That's it. Claude Constructor will guide you through planning → approval → implementation → review → PR.

## The Workflow

```text
┌─────────────────────────────────────────────────────────────────────┐
│                           PLANNING                                  │
├─────────────────────────────────────────────────────────────────────┤
│  /feature "description"                                             │
│       ↓                                                             │
│  Requirements Definition  →  Audit  →  ✋ YOUR SIGN-OFF             │
│       ↓                                                             │
│  Specification Writing    →  Audit  →  ✋ YOUR SIGN-OFF             │
├─────────────────────────────────────────────────────────────────────┤
│                        IMPLEMENTATION                               │
├─────────────────────────────────────────────────────────────────────┤
│  Git checkout  →  Parallel implementation  →  Security review       │
│       ↓                                                             │
│  E2E tests  →  Code review  →  Create PR                            │
├─────────────────────────────────────────────────────────────────────┤
│                           REVIEW                                    │
├─────────────────────────────────────────────────────────────────────┤
│  ✋ YOU REVIEW PR  →  Address feedback  →  ✋ YOU MERGE              │
└─────────────────────────────────────────────────────────────────────┘
```

**Human checkpoints (✋):** You approve requirements, specifications, and the final PR. Nothing ships without your sign-off.

## Commands

| Command | Description |
|---------|-------------|
| `/feature <description or issue-key>` | Main orchestrator—runs the full workflow |
| `/feature ABC-123` | Start from a Linear/Jira issue |
| `/feature ABC-123 --silent=true` | Skip external API calls (testing mode) |

### Internal Commands (called by orchestrator)

| Command | Phase |
|---------|-------|
| `/create-state-management-file` | Setup |
| `/read-settings` | Setup |
| `/requirements-sign-off` | Planning |
| `/specification-sign-off` | Planning |
| `/git-checkout` | Implementation |
| `/implement-increment` | Implementation |
| `/write-end-to-end-tests` | Implementation |
| `/create-pull-request` | Review |
| `/review-pull-request` | Review |

## Agents

Specialized subagents handle complex tasks:

| Agent | Purpose |
|-------|---------|
| `requirements-definer` | Extracts and structures requirements from issue/prompt |
| `requirements-definer-auditor` | Validates requirements are complete and testable |
| `specification-writer` | Creates implementation spec with parallel execution plan |
| `specification-writer-auditor` | Validates spec is actionable and properly scoped |
| `increment-implementer` | Executes implementation tasks (can run in parallel) |
| `increment-implementer-auditor` | Verifies implementation quality and scope adherence |
| `code-reviewer` | Reviews code against specification requirements |
| `security-reviewer` | Security-focused code analysis |

## Issue Tracking Integration

Claude Constructor auto-detects your issue tracking system via MCP tools:

| Provider | Detection | Usage |
|----------|-----------|-------|
| **Linear** | `linear:*` MCP tools present | `/feature ABC-123` |
| **Jira** | `jira:*` MCP tools present | `/feature PROJ-456` |
| **Prompt** | No MCP tools / explicit | `/feature Add dark mode` |

Override detection with `--provider=<linear|jira|prompt>`.

### Configuration (Optional)

Create `.claude/settings.claude-constructor.local.json`:

```json
{
  "issue-tracking-provider": "linear",
  "default-branch": "main",
  "silent-mode": false
}
```

## Generated Files

Claude Constructor creates these files in your target project:

```text
state_management/
└── {issue_key}.md              # Workflow progress and context

specifications/
└── {issue_key}_spec_{ts}.md    # Requirements + implementation plan

code_reviews/
└── {issue_key}.md              # Review history across iterations
```

## Team Setup

Add to your project's `.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "claude-constructor@hurblat-plugins": true
  },
  "extraKnownMarketplaces": {
    "hurblat-plugins": {
      "source": {
        "source": "github",
        "repo": "Hurblat/claude-constructor"
      }
    }
  }
}
```

## Local Development

For contributing or customizing:

```bash
git clone https://github.com/Hurblat/claude-constructor.git
cd claude-constructor

# Add as local marketplace
/plugin marketplace add ./

# Install from local
/plugin install claude-constructor@hurblat-plugins

# Test with silent mode
/feature prompt-test --silent=true
```

Changes to command/agent files are immediately available. Changes to `plugin.json` require reinstall.

## Prerequisites

- **Required:** Claude Code CLI, GitHub CLI (`gh`) authenticated, Git
- **Optional:** Linear MCP or Jira MCP (for issue tracking integration)

## Tips

- **Be specific:** Clear requirements upfront = better results
- **Use silent mode:** `--silent=true` skips external APIs for testing
- **Check state files:** `state_management/{issue_key}.md` shows detailed progress
- **Stay engaged:** Monitor implementation and provide feedback at checkpoints

## Plugin Structure

```text
plugins/claude-constructor/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── commands/                 # Slash commands (orchestration)
│   ├── feature.md            # Main workflow orchestrator
│   └── issue/                # Issue tracking integration
├── agents/                   # Specialized subagents
└── docs/
    └── git-commit.md         # Git commit guidelines
```

## License

MIT
