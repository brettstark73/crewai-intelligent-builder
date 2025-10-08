# Claude Code GitHub Integration Setup

This repository is configured to use Claude Code via GitHub Issues integration. When you @mention `@claude` in any issue, a GitHub Actions workflow will run Claude Code to address your request.

## Setup Steps

### 1. Add Anthropic API Key to Repository Secrets

You need to add your Anthropic API key as a repository secret:

```bash
# Using GitHub CLI
gh secret set ANTHROPIC_API_KEY

# Or manually:
# 1. Go to https://github.com/brettstark73/crewai-intelligent-builder/settings/secrets/actions
# 2. Click "New repository secret"
# 3. Name: ANTHROPIC_API_KEY
# 4. Value: Your Anthropic API key from https://console.anthropic.com/
# 5. Click "Add secret"
```

### 2. Commit and Push the Workflow

The workflow file has been created at `.github/workflows/claude-code.yml`. Commit and push it:

```bash
git add .github/
git commit -m "Add Claude Code GitHub integration workflow"
git push origin master
```

## How to Use

1. **Create a GitHub Issue** describing the task you want Claude to work on
2. **Mention @claude** in the issue body or in a comment
3. **Wait for the workflow** to run (you'll see it in the Actions tab)
4. **Review the PR** that Claude creates with the changes

### Example Issue

```
@claude Please add error handling to the intelligent_crew_runner.py file
to catch and log exceptions when loading environment variables.
```

## What Happens

1. The workflow triggers when you mention @claude
2. Claude Code analyzes the task and your codebase
3. Claude makes the necessary changes
4. A pull request is automatically created
5. A comment is added to the issue with the status

## Features

- ✅ Works from GitHub mobile app (perfect for on-the-go tasks)
- ✅ Automatically creates pull requests
- ✅ Provides status updates in issue comments
- ✅ Respects your repository's coding standards
- ✅ Creates proper git commits with attribution

## Workflow Permissions

The workflow has the following permissions:
- `contents: write` - To create branches and commits
- `issues: write` - To comment on issues
- `pull-requests: write` - To create pull requests

## Troubleshooting

If the workflow doesn't run:
1. Check that ANTHROPIC_API_KEY is set in repository secrets
2. Verify the workflow file is in `.github/workflows/claude-code.yml`
3. Make sure you're mentioning `@claude` in the issue
4. Check the Actions tab for error logs

## Security Notes

- The ANTHROPIC_API_KEY is stored securely in GitHub Secrets
- The workflow only runs when explicitly triggered by @claude mentions
- All changes are made via pull requests for review before merging
