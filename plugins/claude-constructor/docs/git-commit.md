# Git Commit Guidelines

## Git Workflow

### Add Standards

Never do `git add .`. Always add individual files, and only the files related to the current implementation you are working on.

### Commit Standards

Use conventional commits format consistently:

```bash
# Feature commits
feat: {issue key} add validation to user creation

# Bug fixes
fix: {issue key} correct validation in entity creation

# Refactoring
refactor: {issue key} extract validation logic

# Tests
test: {issue key} add edge cases for entity calculation

# Documentation
docs: {issue key} update API documentation for new endpoints
docs: {issue key} add terminology reference
```
