# Qoder Action - GitHub Integration Reference

Qoder Action brings Qoder CLI into GitHub workflows for intelligent code collaboration in PRs and Issues.

## Key Features

- **Intelligent PR Auto-Review**: Every PR gets automated code review (defects, security, test coverage)
- **@qoder On-Demand Response**: Mention `@qoder` in comments for code explanations, suggestions, or fixes
- **Deep Project Understanding**: Respects project coding standards via AGENTS.md
- **Secure**: Code runs on GitHub Runner

## Quick Setup

Run `/setup-github` in qodercli for guided setup.

## Manual Setup

### Step 1: Install GitHub App & Get Token

1. Visit Qoder Integrations
2. Link Qoder account with GitHub account
3. Install **qoderai** GitHub App to target repository
4. Generate Qoder Personal Access Token at `https://qoder.com/account/integrations`

### Step 2: Add Secret to Repository

In repo **Settings > Secrets and variables > Actions**, add `QODER_PERSONAL_ACCESS_TOKEN`.

### Step 3: Add Workflow

Choose a workflow from Qoder Action examples and copy to `.github/workflows/`:

| Workflow | Description |
|---|---|
| **Code Review** | Auto-analyze PR code quality, test coverage, security |
| **Assistant** | `@qoder` interactive conversation in Issues and PRs |

### Step 4: Use

- **Code Review**: Create a PR, wait for Qoder feedback
- **Assistant**: Comment `@qoder explain this code` or `@qoder fix this issue`

## Customize Output Language

```yaml
- name: Run Qoder Code Review
  uses: QoderAI/qoder-action@v0
  with:
    qoder_personal_access_token: ${{ secrets.QODER_PERSONAL_ACCESS_TOKEN }}
    prompt: |
      /review-pr
      REPO:${{ github.repository }} PR_NUMBER:${{ github.event.pull_request.number }}
      OUTPUT_LANGUAGE: Chinese
```

## Define Review Rules via AGENTS.md

Create `Agents.md` in repo root:

```markdown
# Code Review Standards

## Focus Areas
- All database queries must use parameterized queries
- API endpoints must have permission verification
- Sensitive data (passwords, tokens) must not be hardcoded or logged
- All external input must be validated and sanitized

## Ignore
- Test file code duplication
- Auto-generated file code style
- Mock data complexity warnings

## Team Conventions
- Use async/await over Promise.then()
- Component names: PascalCase
- Utility functions: camelCase
- Constants: UPPER_SNAKE_CASE
```

## Skip Review for Large PRs

```yaml
steps:
  - name: Check PR Size
    id: check_size
    run: |
      LINES_CHANGED=$(jq .pull_request.additions < $GITHUB_EVENT_PATH)
      if [ "$LINES_CHANGED" -gt 500 ]; then
        echo "skip=true" >> $GITHUB_OUTPUT
      else
        echo "skip=false" >> $GITHUB_OUTPUT
      fi

  - uses: QoderAI/qoder-action@v0
    if: steps.check_size.outputs.skip == 'false'
    with:
      qoder_personal_access_token: ${{ secrets.QODER_PERSONAL_ACCESS_TOKEN }}
```

## Resources

- GitHub Repository: https://github.com/QoderAI/qoder-action
- Issue Reporting: https://github.com/QoderAI/qoder-action/issues
