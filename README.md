# Claude Constructor

A workflow automation system that helps Claude Code implement features systematically in your codebase with built-in planning, validation, and review steps.

## What It Does

Claude Constructor provides a `/feature` command that guides Claude Code through a complete feature development workflow - from understanding requirements to creating a pull request. Instead of giving Claude Code open-ended instructions, this system ensures it follows a structured process that includes planning, getting your approval, implementing, testing, and self-review.

The workflow prevents common issues like Claude Code losing focus, making unplanned changes, or implementing features differently than intended.

## Quickstart

> **Important:** Claude Constructor will work with you to define requirements and create specifications, but the more detail you provide upfront, the better the results. Whether providing a prompt directly or using issue tracking, include clear requirements, acceptance criteria, and technical constraints when possible. The workflow includes approval gates where you can refine requirements before implementation begins.

### Installation Prerequisites

**Required:**

- Claude Code CLI installed and configured
- GitHub CLI (`gh`) authenticated

**Optional:**

- Linear MCP or Jira MCP configured (for issue tracking integration)

### Installation

1. **Navigate to your project:**

   ```bash
   cd /path/to/your/project
   claude
   ```

2. **Add the plugin marketplace:**

   ```console
   > /plugin marketplace add github Hurblat/claude-constructor
   ```

3. **Install the plugin:**

   ```console
   > /plugin install claude-constructor@hurblat-plugins
   ```

4. **Start using it:**

   ```console
   > /feature Add dark mode toggle to settings page
   ```

   That's it! No additional configuration needed. Claude Constructor will auto-detect your git branch and available issue tracking systems.

   You can also override settings with command arguments:

   ```console
   > /feature Add dark mode --provider=prompt --silent=true
   ```

### Local Development

To develop Claude Constructor locally:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Hurblat/claude-constructor.git
   cd claude-constructor
   ```

2. **Start Claude Code from the repository directory:**

   ```bash
   claude
   ```

3. **Add the local marketplace:**

   ```console
   > /plugin marketplace add ./
   ```

   This adds the current directory (the cloned repo) as a plugin marketplace.

4. **Install the plugin:**

   ```console
   > /plugin install claude-constructor@hurblat-plugins
   ```

Now any changes you make to the plugin files will be immediately available in Claude Code. You can test changes without reinstalling.

**Note:** If you make changes to `plugin.json` or `marketplace.json`, you may need to remove and reinstall the plugin:

```console
> /plugin uninstall claude-constructor@hurblat-plugins
> /plugin install claude-constructor@hurblat-plugins
```

**Recommended VS Code Extension:**

For a better development experience with markdown files, install the [markdownlint extension](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint):

- Provides real-time linting as you type
- Auto-fixes issues on save (configured in `.vscode/settings.json`)
- Quick fixes with `Ctrl+.` or light bulb icon
- Uses the project's `.markdownlint.json` configuration automatically

### Configuration (Optional)

Claude Constructor works out of the box with sensible defaults and auto-detects your setup. You can override settings using command arguments when calling `/feature`:

```console
> /feature ABC-123 --provider=prompt --silent=true
```

**Available arguments:**

- `--provider=<linear|jira|prompt>`: Override issue tracking system (auto-detected if not specified)
- `--silent=<true|false>`: Skip external API calls for testing (default: false)

To configure permissions in your project's `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "SlashCommand(/feature:*)",
      "SlashCommand(/create-state-management-file:*)",
      "SlashCommand(/requirements-sign-off:*)",
      "SlashCommand(/specification-sign-off:*)",
      "SlashCommand(/git-checkout:*)",
      "SlashCommand(/implement-increment:*)",
      "SlashCommand(/issue:*)",
      "SlashCommand(/write-end-to-end-tests:*)",
      "SlashCommand(/security-review:*)",
      "SlashCommand(/code-review:*)",
      "SlashCommand(/create-pull-request:*)",
      "SlashCommand(/review-pull-request:*)"
    ]
  }
}
```

### Tips for Success

- **Be specific**: Whether using a feature description (`/feature Add dark mode`) or issue key (`/feature ABC-123`), provide clear requirements
- **Use silent mode** for testing: Add `--silent=true` to skip write operations to issue tracker and GitHub (e.g., `/feature ABC-123 --silent=true`). Note: Issue details are still fetched.
- **Use prompt mode** for isolated testing: Add `--provider=prompt` to skip all external integrations (e.g., `/feature test-feature --provider=prompt`)
- **Monitor progress**: Claude Constructor will update you at each step and ask for approval at key points
- **Check the state file**: Find detailed progress in `state_management/{issue_key}.md` or `state_management/prompt-{number}.md`

## Core Workflow

The main orchestrator (`feature.md`) follows this sequence:

### Planning

1. **Read configuration files** - Load development guidelines, quality gates, and other documentation
2. **Create state management file** - Used to track workflow progress
3. **Read settings** - Get issue tracker and other settings
4. **Read issue/prompt** - Get feature details (from prompt or issue tracker)
5. **Define requirements** - Create detailed requirements specification covering business value, user journey, acceptance criteria, and technical constraints (using specialized agent)
6. **Validate requirements** - Quality assurance check to ensure requirements are complete, clear, and testable
7. **Get requirements sign-off** - Iterate on the requirements definition until it's ready *(Human Required)*
8. **Write specification** - Technical spec with parallelization plan (using specialized agent)
9. **Validate specification** - Technical validation to ensure implementation plan is actionable and properly parallelized
10. **Get specification sign-off** - Iterate on the specification until it's ready *(Human Required)*

### Implementation

11. **Check out new branch** - Create feature branch
12. **Implement increment** - Execute with parallel subagents if possible
13. **Write end-to-end tests** - Cover user behavior

### Review

14. **Perform code review** - Self-review, addressing findings automatically
15. **Create pull request** - Creating a pull request on GitHub, describing the work
16. **Review pull request** - Monitor and respond to feedback *(Human Required)*

### Team Setup

For team-wide adoption, add Claude Constructor configuration to your project's `.claude/settings.json`:

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
  },
  "permissions": {
    "allow": [
      "SlashCommand(/feature:*)",
      "SlashCommand(/create-state-management-file:*)",
      "SlashCommand(/requirements-sign-off:*)",
      "SlashCommand(/specification-sign-off:*)",
      "SlashCommand(/git-checkout:*)",
      "SlashCommand(/implement-increment:*)",
      "SlashCommand(/issue:*)",
      "SlashCommand(/write-end-to-end-tests:*)",
      "SlashCommand(/security-review:*)",
      "SlashCommand(/code-review:*)",
      "SlashCommand(/create-pull-request:*)",
      "SlashCommand(/review-pull-request:*)"
    ]
  }
}
```

Team members will automatically be prompted to install the plugin when they trust the repository folder.

Settings like issue tracking provider can be specified per-invocation using command arguments (e.g., `/feature ABC-123 --provider=linear`).

## Configuration

### Issue Tracking System Integration

The workflow supports multiple issue tracking systems through auto-detection and optional configuration.

#### Supported Providers

**Auto-Detection (Default)**
Claude Constructor automatically detects your issue tracking system:

- If Linear MCP is configured → uses Linear
- If Jira MCP is configured → uses Jira
- Otherwise → uses "prompt" mode (no external integration)

**Manual Override**
Override auto-detection using command arguments:

```console
> /feature ABC-123 --provider=prompt
```

**Provider Options:**

1. **Linear**
   - Requires Linear MCP integration configured
   - Uses `linear:get_issue`, `linear:update_issue`, `linear:create_comment`, `linear:list_issue_statuses`
   - Supports fuzzy matching for status names

2. **Jira**
   - Requires Jira MCP integration configured
   - Uses `jira:get_issue`, `jira:add_comment_to_issue`, `jira:get_transitions_for_issue`, `jira:transition_issue`
   - Supports fuzzy matching for status names

3. **Prompt Mode**
   - No external issue tracking system required
   - Use with: `/feature Your feature description here`
   - Creates local issue keys (prompt-1, prompt-2, etc.)
   - Perfect for local development and experimentation
   - Automatically skips issue tracker API calls and PR creation

#### Silent Mode

Silent mode prevents external **write operations** to issue trackers and GitHub, useful for testing and dry-runs with real issue tracking systems. Read operations (like fetching issue details) still execute normally.

Enable using command arguments:

```console
> /feature ABC-123 --silent=true
```

When silent mode is enabled:

- **Issue details**: Still fetched from issue tracker (read operation continues)
- **Issue comments**: Logged locally but not posted to issue tracker (write skipped)
- **Issue status updates**: Logged locally but not updated in the issue tracker (write skipped)
- **GitHub pull requests**: Code is committed and pushed, but PR creation is skipped (write skipped)
- **PR review comments**: Skipped entirely (write skipped)
- All other operations (git commits, code changes, tests) execute normally

**Note**: If you use `--provider=linear` or `--provider=jira`, the corresponding MCP tools must still be configured even in silent mode, since issue details are read from the tracker.

#### Issue Tracking System Requirements

The workflow expects issues to support these standard status transitions:

- **"In Progress"** - When implementation begins
- **"Code Review"** - When automated code review is done and pull request has been created

Your issue tracking system should have statuses that match or can be mapped to these workflow states.

#### Adding New Providers

To add support for additional issue tracking systems (GitHub Issues, etc.):

1. Update the issue command files (`get-issue.md`, `update-issue.md`, `create-comment.md` etc.)
2. Add provider-specific MCP command mappings
3. Submit a pull request!

### Other Customizations

This repository is a work in progress, and there are things you might want to change to fit your setup better:

- Using different status transitions within your issue tracking system
- Adding reference points for your specific way of doing things, e.g. adding documentation on your E2E test principles in `docs/` and then reference it in `commands/write-end-to-end-tests.md`
- Tweaking your technical guardrails (described in `CLAUDE.md`). I recommend using pre-commit hooks and/or Claude Code hooks and/or CI to make sure the technical guardrails are enforced. TDD is also a great instrument in my opinion.
- Adapting the git branch and commit guidelines to suit your preferences

## Key Features

### Extensive Planning

- Focus on creating a solid plan before starting any work
- Transparent description of Claude Code's understanding of the work to be done, and assumptions made

### Parallel Execution

- Specifications identify independent components (backend APIs, frontend components, database migrations)
- Agent IDs assigned for parallel work with dependency management

### State Management

- Persistent tracking across all workflow steps in `state_management/{issue_key}.md`
- TODO list maintenance and resumable workflows

### Issue Tracking Integration

- Issue status updates at each workflow stage
- Progress comments with implementation details

## Human-in-the-Loop Points

The workflow includes critical human approval gates:

### 1. Requirements Sign-off (Step 7)

- **Process**: Claude Constructor presents assumptions and detailed understanding of requirements after validation
- **Human Required**: Must approve definition of requirements

### 2. Specification Sign-off (Step 10)

- **Process**: Claude Constructor presents assumptions and detailed specification for review after validation
- **Human Required**: Must approve technical specification before implementation begins

### 3. Pull Request Review (Step 16)

- **Human Required**: Reviewing and approving pull request on GitHub
- **Process**: Human adds comments/feedback directly in GitHub PR interface as part of a Review
- **Workflow**: Claude Constructor monitors for new comments but must be asked to check for updates, and the Review needs to be submitted

### 4. Merging Pull Request (After Step 16)

- **Human Required**: Must merge the pull request manually

These gates ensure human oversight of decisions and final code quality before delivery.

I also recommend checking in on the work as it is happening, to gauge if anything was missed in the specification or otherwise not going according to plan.

## Prerequisites

### Technical Requirements

- Claude Code CLI installed and configured
- Issue tracking system MCP integration configured (optional - see Issue Tracking System Integration section)
- GitHub CLI (`gh`) authenticated
- Git repository
- Quality gate tools available

### Recommended Project Configuration Files

- `/CLAUDE.md` - General principles, quality gates, and development workflow
- `docs/git-commit.md` - Git commit guidelines (example available in `docs/git-commit.md` in Claude Constructor)

### Input Requirements

Claude Constructor will help you refine and validate requirements during the workflow, but providing clear input upfront leads to better results.

**Helpful details to include (when known):**

- Clear problem definition and business context
- Detailed feature requirements and acceptance criteria
- Proposed solution approach or architecture direction
- Sufficient domain context for implementation decisions
- Any relevant technical constraints or considerations

The workflow includes human approval gates where you can iterate on requirements and specifications before implementation begins. For issue tracking systems, well-groomed issues will streamline this process.

### Example: Well-Defined Input

**Good Example (Issue or Prompt):**

```text
Title: Add user preference for date format display

Description:
Currently, all dates in the application are displayed in US format (MM/DD/YYYY). International users have requested the ability to choose their preferred date format.

Requirements:
- Add a date format preference to user settings (options: US, ISO, European)
- Store preference in user profile database
- Apply format throughout the application (dashboard, reports, transaction history)
- Default to US format for existing users to maintain backward compatibility

Technical Notes:
- Use existing DateFormatter utility class
- Preference should persist across sessions
- Consider timezone handling for consistency

Acceptance Criteria:
- [ ] User can select date format in settings page
- [ ] Selected format applies immediately without page refresh
- [ ] Format persists after logout/login
- [ ] All date displays respect the preference
```

**Poor Example:**

```text
Make dates better for international users
```

The workflow will help refine vague requirements, but starting with detail saves iteration cycles and produces better results.

### Optional Configuration Files

- `docs/requirements.md` - Domain principles and business rules (can be referenced during implementation planning and code review)
- ...and any additional context

## File Structure

When you install Claude Constructor as a plugin, the workflow files are managed by Claude Code's plugin system. You don't need to copy any files - just install the plugin and optionally configure it in your project's `.claude/settings.json` (separate from the plugin).

### Plugin Structure

The plugin provides these components:

```text
.claude-plugin/
└── marketplace.json                          # Marketplace definition

plugins/
└── claude-constructor/                       # Plugin directory
    ├── .claude-plugin/
    │   └── plugin.json                       # Plugin manifest
    ├── agents/
    │   ├── requirements-definer.md           # Specialized agent for defining requirements
    │   ├── requirements-validator.md         # Quality assurance for requirements completeness
    │   ├── specification-writer.md           # Specialized agent for writing specifications
    │   └── specification-validator.md        # Technical validation of implementation plans
    ├── commands/
    │   ├── feature.md                        # Main orchestrator
    │   ├── create-state-management-file.md
    │   ├── read-settings.md
    │   ├── requirements-sign-off.md
    │   ├── specification-sign-off.md
    │   ├── git-checkout.md
    │   ├── implement-increment.md
    │   ├── write-end-to-end-tests.md
    │   ├── code-review.md
    │   ├── create-pull-request.md
    │   ├── review-pull-request.md
    │   └── issue/
    │       ├── get-issue.md                  # Issue tracking system: Get issue details
    │       ├── read-issue.md                 # Issue tracking system: Read issue details
    │       ├── update-issue.md               # Issue tracking system: Update issue status
    │       └── create-comment.md             # Issue tracking system: Add comments to issue
    └── docs/
        └── git-commit.md                     # Example git commit guidelines
```

### Generated files in your project

These files are automatically created in your project during the workflow:

```text
state_management/                             # Tracks workflow progress
└── {issue_key}.md

specifications/                               # Technical specifications
└── {issue_key}_specification_{timestamp}.md
```

### Recommended project files

Add these to your project for best results:

```text
/CLAUDE.md                                    # Project-specific development guidelines
docs/                                         # Project-specific documentation
└── git-commit.md                             # Your git commit conventions
```
